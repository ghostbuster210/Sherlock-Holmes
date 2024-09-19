import os
import sys
import random
import gradio as gr
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import AIMessage, HumanMessage
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain_core.runnables import RunnableLambda
from langchain_core.messages import AIMessage, AIMessageChunk, HumanMessage, HumanMessageChunk
from game_info import *
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.environ["API_KEY"]

# Constants for the UI and game settings
CHATBOT_HEIGHT = 500
IMAGE_HEIGHT = 500
IMAGE_WIDTH = 500
LINES_PER_BOX = 12
SUSPECTS_PER_PAGE = 8

# Initialize the mystery game
game = cMystery()

# Initialize the LLM
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=1.0, max_tokens=1024, timeout=None, max_retries=2, api_key=API_KEY)

def output_parser(ai_message: AIMessage) -> str:
    """
    Parse the AI message and save the conversation recap.
    
    Args:
        ai_message (AIMessage): The AI message to be parsed.
        
    Returns:
        str: The content of the AI message.
    """
    global game
    current_suspect = game.get_current_suspect()
    game.add_note_to_recap(ai_message.content, current_suspect)
    return ai_message.content

def predict(message, history):
    """
    Feed the chat message to the LLM and generate a response.
    
    Args:
        message (str): The user's input message.
        history (list): The history of the conversation.
        
    Returns:
        str: The AI's response to the user's message.
    """
    global game
    global llm

    current_suspect = game.get_current_suspect()

    if current_suspect is None:
        return "Please select a suspect."

    AI_Instructions = (
        f"You are a suspect in an art theft. "
        f"Your name is {game.get_suspect_proper_name(current_suspect)} "
        f"and your background is {game.get_suspect_background(current_suspect)}. "
        f"Your motive for stealing the painting is {game.get_suspect_motive(current_suspect)}. "
        f"If you stole the painting do not admit it. "
        f"Base all conversations on the following JSON text: {game.create_interview(current_suspect)}"
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", f"{AI_Instructions}"),
        ("human", f"{message}"),
    ])

    history_langchain_format = []
    history_langchain_format.append(AIMessage(content=AI_Instructions))
    history_langchain_format.append(HumanMessage(content=message))

    gpt_response = llm(history_langchain_format)
    output_parser(gpt_response)
    response = gpt_response.content
    return response

def get_recap():
    """
    Generate a recap of the game's hints and interview notes.
    
    Returns:
        gr.Textbox: A Gradio textbox containing the recap.
    """
    global game

    recap = "💡 Hints 💡 \n\n" + game.get_hints_recap() + "\n"
    recap += "🕵 Suspect Interview Notes 🕵 \n\n" + game.get_crime_recap()

    return gr.Textbox(lines=LINES_PER_BOX, label="Recap of the Mystery", value=recap)

def question_suspect(image, name):
    """
    Set the current suspect and display their profile.
    
    Args:
        image: The image of the suspect.
        name (str): The name of the suspect.
        
    Returns:
        gr.Textbox: A Gradio textbox with the suspect's profile.
    """
    global game

    game.set_current_suspect(name)
    current_suspect = game.get_current_suspect()

    return gr.Textbox(lines=LINES_PER_BOX,
                      label="About the Suspect",
                      value=game.get_suspect_profile(current_suspect))

def get_hint():
    """
    Generate a hint about the mystery.
    
    Returns:
        gr.Textbox: A Gradio textbox containing the hint.
    """
    global game

    return gr.Textbox(lines=LINES_PER_BOX,
                      label="Hint About the Mystery",
                      value=game.give_hint())

def new_crime():
    """
    Reset the game for a new mystery.
    
    Returns:
        list: A list of Gradio components representing the new game state.
    """
    global game

    game = cMystery()
    game.print_game()

    return [
        gr.Image(value=game.get_stolen_painting(), height=IMAGE_HEIGHT, width=IMAGE_WIDTH, label=game.get_stolen_painting_name(), interactive=False),
        gr.Textbox(lines=LINES_PER_BOX, label="A Crime has been Committed", value=game.get_crime_text()),
        gr.Image(value="Question_Mark.jpg", height=IMAGE_HEIGHT, width=IMAGE_WIDTH, label="Suspect", interactive=False),
        gr.Textbox(lines=LINES_PER_BOX, label="About the Suspect", value=""),
    ]

def arrest():
    """
    Attempt to arrest the current suspect and provide the results.
    
    Returns:
        gr.Textbox: A Gradio textbox displaying the results of the arrest attempt.
    """
    global game

    current_suspect = game.get_current_suspect()
    guilty_suspect = game.get_guilty_suspect_name()

    if current_suspect is None:
        arrest_results = "Please select a suspect on the right to arrest."
    elif current_suspect == guilty_suspect:
        arrest_results = (
            "👍👍 Congratulations 👍👍 \n\n"
            f"You caught {guilty_suspect} and recovered the painting.\n\n"
            f"{guilty_suspect} confessed why: \n\n'"
            f"{game.get_suspect_motive(guilty_suspect)}' and said 'I would have gotten away with it too if it weren't for you meddling detectives'"
        )
    else:
        arrest_results = (
            "❌❌❌ You Failed Detective ❌❌❌\n\n"
            f"{guilty_suspect} stole the painting and snuck away while you were arresting the wrong person"
        )

    return gr.Textbox(lines=LINES_PER_BOX,
                      label="Results of Your Arrest",
                      value=arrest_results)

# Main Code - Draw Gradio UI
game.print_game()

with gr.Blocks() as demo:
    image_manor = gr.Image(value="assets/mystery_manor.jpg")

    with gr.Row():
        with gr.Column():
            painting = gr.Image(value=game.get_stolen_painting(), height=IMAGE_HEIGHT, width=IMAGE_WIDTH, label=game.get_stolen_painting_name(), interactive=False)
            crime_desc = gr.Textbox(lines=LINES_PER_BOX, label="A Crime has been Committed", value=game.get_crime_text())
            with gr.Row():
                btn_new_crime = gr.Button("⚡ New Crime ⚡")
                btn_recap = gr.Button("💡 Recap 💡")

        with gr.Column():
            suspect_image = gr.Image(value="assets/Question_Mark.jpg", height=IMAGE_HEIGHT, width=IMAGE_WIDTH, label="Suspect", interactive=False)
            suspect_desc = gr.Textbox(lines=LINES_PER_BOX, label="About the Suspect", value="")
            with gr.Row():
                btn_arrest = gr.Button("👮 Arrest 👮")
                btn_hint = gr.Button("🕵 Clue 🕵")

        with gr.Column():
            suspect_list = gr.Examples(
                examples=game.get_suspect_images(),
                inputs=[suspect_image, suspect_desc],
                outputs=[suspect_desc],
                examples_per_page=SUSPECTS_PER_PAGE,
                fn=question_suspect,
                run_on_click=True,
                label="Suspect List",
                cache_examples=False
            )

        with gr.Column():
            QnA = gr.ChatInterface(
                fn=predict,
                examples=game.get_sample_questions(),
                title="❓ Question the Suspect ❓",
                fill_height=False,
                retry_btn=None,
                undo_btn=None,
                cache_examples=False
            )

    btn_new_crime.click(new_crime, inputs=None, outputs=[painting, crime_desc, suspect_image, suspect_desc])
    btn_recap.click(get_recap, inputs=None, outputs=[crime_desc])
    btn_arrest.click(arrest, inputs=None, outputs=[suspect_desc])
    btn_hint.click(get_hint, inputs=None, outputs=[suspect_desc])

if __name__ == "__main__":
    demo.launch()
