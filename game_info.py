import sys, random
import networkx as nx


class cMystery():
    def __init__(
        self,
        NUMBER_OF_SUSPECTS = 14, 
        NUMBER_OF_TIMESLOTS = 12,
        NUMBER_OF_ROOMS = 10,
        NUMBER_OF_PAINTINGS = 13,
        HOURS_TO_SHIFT = 9,
        CRIME_OCCURS = 6,
        CRIME_WINDOW = 4,
    ):
        
        print("Initializing Mystery Game Object")

        self.suspects = {
        "Agnus the Art Gallery Owner":{"name": "Agnus Gerhard","background":"owns local art gallery", "motive": "I sold all of the poodle art to the manor and only I know the true value of each painting", "did I steal the painting": "No", "timeline":[],
                                       "profile": "Agnus Gerhard studied Art History at the University of Vienna which was her passion.  After her internship at the MoMA in New York, Agnus was finally able to realize her dream and opened The Gallery of Eclectics Poodle Art.\n\nMOTIVE: She sold all of the poodle art to the manor and knows the high value of each painting."} ,
        "Ben the Butler"             :{"name": "Benjamin Atwood",  "background": "butler for the manor","motive": "I have expensive tastes that cannot be funded with my pittance of a salary", "did I steal the painting": "No", "timeline":[],
                                       "profile": "Benjamin Atwood has always been drawn to elegance and sophistication, fascinated with works of fine literature, art, and culture. Recognizing Ben's sharp mind and quick learning abilities, he soon ascended to the position of the manor's lead butler.\n\nMOTIVE: Ben's expensive tastes cannot be funded with his modest butler's salary."} ,
        "Bernice the Bartender"      :{"name": "Bernice Lo",  "background": "bartender for the manor","motive": "I am angry that you keep falsely accusing me of stealing from the manor so why not make it real", "did I steal the painting": "No", "timeline":[] ,
                                       "profile": "Bernice is more than just a bartender. She is a storehouse of stories, secrets, and emotions.  Her compassionate listening and signature cocktails managed to give solace to many and catch the attention of the Head of the Manor.\n\nMOTIVE: Bernice has been angry ever since she was falsely accused of stealing a case of expensive wine."} ,
        "Buddy the Business Partner" :{"name": "Buddy Bannister",  "background": "business partner of the owner of the manor","motive": "Well I have been known to dabble in business deals others won't touch", "did I steal the painting": "No", "timeline":[] ,
                                       "profile": "Hard-working Buddy Bannister always knows how to strike a deal. Good with numbers and an absolute shark at negotiating, he quickly climbed the business ladder to become a successful business partner.\n\nMOTIVE: Buddy is a man of secrets and questionable legal involvements with rumors of bribery, blackmail, even corporate espionage."} ,
        "Chef Chuck"                 :{"name": "Charles Toussaint but people call me Chuck",  "background": "chef for the manor","motive": "You may have heard on the street that I have some gambling debts.  I'll pay them off you know", "did I steal the painting": "No", "timeline":[] ,
                                       "profile": "Charles 'Chuck' Toussaint was born and raised in New Orleans.  He is a cooking prodigy trained at an esteemed culinary school in Paris then returning home as an accomplished young chef and local celebrity.\n\nMOTIVE: The Chef is in a deep pot of trouble thanks to unpaid gambling debts."} ,
        "Daughter-In-Law Daphne"     :{"name": "Daphne Dartmouth",  "background": "philanthopist and wife of son Samuel","motive": "I have no motive - how can I steal a painting that is rightfully mine", "did I steal the painting": "No", "timeline":[] ,
                                       "profile": "Daphne met future husband Sam when they both lived in NYC.  She was immediately attracted to the prospect of marrying into a wealthy family and saw Sam as an attractive ticket.\n\nMOTIVE: Daphne is always after the Bigger Better Thing including valuable paintings that will eventually be hers."} ,
        "Frank the Brother"          :{"name": "Franklin Edward Morris",  "background": "brother of manor owner and not currently employed", "motive": "Well I have no money and no job", "did I steal the painting": "No", "timeline":[] ,
                                       "profile": "Franklin Edward Morris, the youngest of three siblings including older sister Sarah, grew up in the city of New Chester.  Frank was spoiled by money and largely struggled to achieve any meaningful accomplishments academically or in his career.\n\nMOTIVE: Frank holds a deep level of jealousy and will act out accordingly."} , 
        "Gary the Gardener"          :{"name": "Gary Eves",  "background": "manor gardener","motive": "Once a thief always I thief I guess", "did I steal the painting": "No", "timeline":[] ,
                                       "profile": "Gary grew up in a small town foster home and found himself in trouble with the law.  In a life changing moment he became a dedicated gardener, taking up the mission to regenerate the green life of the city and eventually catching the attention of the manor.\n\nMOTIVE: Gary has a past rap sheet for burglary of luxury goods. Has he truly reformed?"} , 
        "Larry the Lawyer"           :{"name": "Lawrence Morington III",  "background": "lawyer for the manor owner","motive": "Think of this as a down payment on my fees for my last legal settlement", "did I steal the painting": "No", "timeline":[] ,
                                       "profile": "Lawrence Morington was born into a prestigious family known for its lineage of top-tier lawyers.  Larry became a lawyer but his his passion for law and scheming blended into a deadly combo.  With his intelligence he started to twist laws and bend cases to his will.\n\nMOTIVE: Larry thinks he deserved a bigger cut of that last legal settlement so why not take it?"} ,  
        "Madam Marmalade"            :{"name": "Gillian Marmalade",  "background": "","motive": "The proceeds from that painting could fund the retirement package the owners promised me", "did I steal the painting": "No", "timeline":[] ,
                                       "profile": "Gillian Marmalade she found herself in the opulent manor as a housekeeper. With her diligent manner and uncanny knack for problem-solving, she quickly moved up the ranks eventually becoming the House Manager.\n\nMOTIVE: The manor is pushing her to retire and the proceeds from a painting would serve her nicely."} ,
        "Nick the Nephew"            :{"name": "Nick Wallace",  "background": "investment banker and nephew of the manor's owner","motive": "Consider it a loan and I'll pay it back with a huge profit", "did I steal the painting": "No", "timeline":[] ,
                                       "profile": "Nick Wallace, the ambitious nephew, is a top-notch graduate of a prestigious Ivy League business school.  He is extremely eager to access the family fortune and invest it.\n\nMOTIVE: There is no money in dog art.  Nick will generate better returns from this unofficial loan."} ,
        "Rebel the Niece"            :{"name": "Rachel Wallace niece of the manor's owner and Nick's sister",  "background": "currently a student","motive": "Just boredom and to show everyone I am smarter than they think", "did I steal the painting": "No", "timeline":[] ,
                                       "profile": "A childhood prodigy, Rachel 'Rebel' Wallace found at an early age she could hack into any electronic or mechanical system, which is a skill set she developed due to her parents' constant absence.  Early successes fueled her rebellious streak only made her more determined to break more rules and gain forbidden knowledge.\n\nMOTIVE: To relieve the daily boredom of living in the manor."} ,
        "Samuel the Son"             :{"name": "Sam Morris",  "background": "philanderer - I mean philanthopist and son of the manor's owner","motive": "My wife Daphne is very expensive and has threatened divorce", "did I steal the painting": "No", "timeline":[] ,
                                       "profile": "Sam Morris, also known as “Silent Sam,” led a life that was quite unlike his other siblings.  His dabbling in philanthropy led him to rub elbows with the rich and elite of NYC including Daphne who he later married.\n\nMOTIVE: Daphne is a really expensive wife to keep happy."} ,
        "Sarah the Sister"           :{"name": "Sarah Evelyn Morris",  "background": "local judge and sister of manor's owner","motive": "Poodle art is a waste of the family's money", "did I steal the painting": "No", "timeline":[] ,      
                                       "profile": "Sarah Evelyn Morris always stood out among her siblings due to her serious and analytical demeanor even at a young age.  After acing the bar and practicing as a lawyer for the prosecution she quickly rose to become one of the youngest appointed judge in the county.\n\nMOTIVE: Thinks that wasting family money on poodle art is a already a crime so no one can charge her thanks to double jeapardy."} ,
        }
        self.times = ["Breakfast Time","Early Morning","Mid Morning","Noon","Early Afternoon","Tea Time","Late Afternoon","Cocktail Hour","Dinner Time","After Dinner","Evening","Late Evening","Suspect Questioning"]
        self.rooms = [
            {"name": "Dining Area", "activities": ["having a meal", "finishing up", "walking through"]},
            {"name": "Foyer", "activities": ["waiting for a guest", "taking a phone call"]},
            {"name": "Outdoor Pool Deck", "activities": ["swimming in the pool", "lounging on a deck chair", "having a drink"]},
            {"name": "Main Hall", "activities": ["looking at the art", "passing through", "having a drink","lounging on a deck chair"]},
            {"name": "Home Theater", "activities": ["watching a movie", "waiting for the movie to start", "lounging"]},
            {"name": "Library", "activities": ["looking at the art", "reading a book", "checking out a map of the area"]},
            {"name": "Mezzanine", "activities": ["looking at the art", "reading a book", "Exercising"]},
            {"name": "Art Gallery", "activities": ["looking at the art", "sat down and admired the paintings", "exploring"]},
            {"name": "Living Room", "activities": ["looking at the art", "talking with the other guests", "talking with the staff"]},
            {"name": "Grand Ballroom", "activities": ["getting questioned by the police", "don't know why we were summoned", "you summoned me to come here"]}
        ]

        self.paintings = [
            {"name": "Pop Art Poodles", "image": "assets/victims/1.jpg"},
            {"name": "Poodle with a Pearl Earring", "image": "assets/victims/2.jpg"},
            {"name": "Portrait of a Poodle", "image": "assets/victims/3.jpg"},
            {"name": "Starry Poodle", "image": "assets/victims/4.jpg"},
            {"name": "Mona Lisa with Poodle", "image": "assets/victims/5.jpg"},
            {"name": "Queen Elizabeth with Poodle", "image": "assets/victims/6.jpg"},
            {"name": "American Poodle", "image": "assets/victims/7.jpg"},
            {"name": "Whistler's Poodle", "image": "assets/victims/8.jpg"},
            {"name": "Night Poodles", "image": "assets/victims/9.jpg"},
            {"name": "Portrait of a Poodle", "image": "assets/victims/10.jpg"},
            {"name": "The Birth of Poodles", "image": "assets/victims/11.jpg"},
            {"name": "A Park Full of Parisian Poodles", "image": "assets/victims/12.jpg"},
        ]

        self.sample_questions = [                                  # Suggested questions for the QnA Chat interface
            "Where were you at the time of the crime?",          
            "Where were you when the power went out?",
            "Who was with you at the time of the crime?"
        ]
        self.NUMBER_OF_SUSPECTS = NUMBER_OF_SUSPECTS                             
        self.NUMBER_OF_TIMESLOTS = NUMBER_OF_TIMESLOTS
        self.NUMBER_OF_ROOMS = NUMBER_OF_ROOMS
        self.NUMBER_OF_PAINTINGS = NUMBER_OF_PAINTINGS
        self.HOURS_TO_SHIFT = HOURS_TO_SHIFT
        self.CRIME_OCCURS = CRIME_OCCURS
        self.CRIME_WINDOW = CRIME_WINDOW
        self.timeline = {}                                                           # Timeline for the crime scene
        self.current_suspect = None                                           # Name of current suspect
        self.guilty_suspect_idx = None                                           # Index of guilty suspect
        self.guilty_suspect = None                                           # Name of guilty suspect
        self.prime_suspects = None                                           # List of potential suspects (as indices)
        self.have_alibi = None                                           # List of suspects with alibis (as indices)
        self.the_usual_suspects = None                                           # Names of potential suspects
        self.power_cut_time_idx = None                                           # Index to time when power was cut (occurs just before crime)
        self.power_cut_room_idx = None                                           # Index to room where power was cut (occurs just before crime)
        self.crime_occurs_time_idx = None                                           # Index to time when crime occurred 
        self.crime_occurs_room_idx = None                                           # Index to room where crime occurred 
        self.power_cut_time_name = None                                           # Time when power was cut (occurs just before crime)
        self.power_cut_room_name = None                                           # Room where power was cut (occurs just before crime)
        self.crime_occurs_time_name = None                                           # Time when crime occurred 
        self.crime_occurs_room_name = None                                           # Room where crime occurred 
        self.stolen_painting = None                                           # Reference to the stolen painting
        self.stolen_painting_img = None 
        self.stolen_painting_name = None 
        self.crime_description = ""                                             # Text describing the crime
        self.crime_recap = ""                                             # Text summarizing the responses from suspects and clues
        self.hints_given = 0                                              # Number of hints given during the gaming session
        self.hints_recap = []                                             # Recap of hints given during the gaming session
 
        # Creates a new game by default when an object is created
        self.new_game()

        return

    # Game Functions - Information Retrieval
    def get_current_suspect(self):
        print("Current suspect is: ",self.current_suspect)
        return self.current_suspect

    def set_current_suspect(self, name):
        self.current_suspect = name
        print("Setting current suspect to: ", self.current_suspect)
        return

    def get_suspect(self, name):
        return self.suspects.get(name)

    def get_suspect_idx(self, name):
        suspects    = [suspect for suspect in self.suspects.keys()]
        suspect_idx = suspects.index(name)    
        return suspect_idx

    def get_suspect_name(self, suspect_idx):
        suspects    = [suspect for suspect in self.suspects.keys()]
        return suspects[suspect_idx]

    def get_guilty_suspect_name(self):
        return self.guilty_suspect

    def get_suspect_profile(self, name):
        selected = self.suspects.get(name)
        return selected["profile"]

    def get_suspect_proper_name(self, name):
        selected = self.suspects.get(name)
        return selected["name"]

    def get_suspect_background(self, name):
        selected = self.suspects.get(name)
        return selected["background"]

    def get_suspect_motive(self, name):
        selected = self.suspects.get(name)
        return selected["motive"]

    def get_suspect_images(self):
        suspect_images = [["assets/suspects/" + suspect + ".jpg", suspect]  for suspect in self.suspects.keys()]
        return suspect_images

    def get_room_names(self):
        return [room["name"] for room in self.rooms]

    def get_room_name(self, room_idx):
        rooms = [room["name"] for room in self.rooms]
        return rooms[room_idx]

    def get_room_activities(self):
        return [room["activities"] for room in self.rooms]

    def get_random_room_activity(self, room):
        selected = self.rooms[room]
        return random.choice(selected["activities"])

    def get_random_painting(self):
        return random.choice(self.paintings)

    def get_stolen_painting(self):
        return self.stolen_painting_img

    def get_stolen_painting_name(self):
        return self.stolen_painting_name

    def get_power_off_room_idx(self):
        guilty_timeline = self.get_timeline_for_person(self.guilty_suspect_idx, self.timeline)     
        return guilty_timeline[self.power_cut_time_idx]

    def get_power_off_room_name(self):
        guilty_timeline = self.get_timeline_for_person(self.guilty_suspect_idx, self.timeline)     
        return self.rooms[guilty_timeline[self.power_cut_time_idx]]["name"]

    def get_crime_occurs_room_idx(self):
        guilty_timeline = self.get_timeline_for_person(self.guilty_suspect_idx, self.timeline)     
        return guilty_timeline[self.crime_occurs_time_idx]
        
    def get_crime_occurs_room_name(self):
        guilty_timeline = self.get_timeline_for_person(self.guilty_suspect_idx, self.timeline)     
        return self.rooms[guilty_timeline[self.crime_occurs_time_idx]]["name"]

    def round_up_the_usual_suspects(self):
        return ", ".join([self.get_suspect_name(suspect_idx) for suspect_idx in self.prime_suspects])

    def have_alibis(self):
        all_suspects = [x for x, suspect in enumerate(self.suspects)]
        have_alibis  = list(set(all_suspects).difference(set(self.prime_suspects)))
        return have_alibis

    def names_of_suspects_with_alibis(self):
        return ", ".join([self.get_suspect_name(suspect_idx) for suspect_idx in self.have_alibis()])

    def get_crime_text(self):     
        return f"Mystery Manor was showing its world-renowned collection of its finest poodle-themed art at a gala." + \
               f"\nA painting called ||{self.stolen_painting_name}|| was stolen from the ||{self.crime_occurs_room_name}||.  " + \
               f"Power to the security system was cut off in the ||{self.power_cut_room_name}|| just before the crime.  " + \
               f"Your job is to question the suspects and arrest the thief.  Good luck detective !!" + \
               f"\n ⬥ Select a suspect on the right" + \
               f"\n ⬥ Ask questions in the chat" + \
               f"\n ⬥ Get a hint (if you need it) with the 'Clue' button" + \
               f"\n ⬥ Hit 'Arrest' while questioning the suspect to convict"

    def give_hint(self):
        hints = [
            f"Your suspect was in the {self.power_cut_room_name} during the power outage and the {self.crime_occurs_room_name} when the theft occurred",
            f"These suspects have valid alibis for the theft:\n{self.names_of_suspects_with_alibis()}",
            f"At the time of theft, these people were alone:\n{self.round_up_the_usual_suspects()}",
        ]
        if self.hints_given < len(hints):
            hint = hints[self.hints_given]
            self.hints_given += 1
            self.hints_recap += " ⬥ " + hint +"\n"
        else:
            hint = "Sorry no more hints are available"
        
        return hint

    def get_hints_recap(self):
        return "".join(self.hints_recap)

    def add_note_to_recap(self, note, current_suspect):
        if current_suspect is not None:
            self.crime_recap +=  current_suspect + " said the following delineated in square brackets\n"
        self.crime_recap += "[" + note + "]\n\n"
        return note

    def get_crime_recap(self):      
        return self.crime_recap

    def get_sample_questions(self):      
        return self.sample_questions
        
    # Game Functions - Generate a New Game
    def get_people_in_room(self, room, suspects_positions):                   # List people in a room
        return [person for person, position in suspects_positions.items() if position == room]

    def get_timeline_for_person(self, suspect_idx, timeline):
        return [suspects_locations[suspect_idx] for timeline, suspects_locations in timeline.items()]                

    def generate_new_game(self):

       # Local variables used to record the crime 
       timeline = {}     # Log of all suspects and their movements over the day
       prime_suspects = []     # All potential criminals

       # Create a fully connected graph of ROOMS with rooms equal to NUMBER_OF_ROOMS 
       G = nx.Graph()
       G.add_nodes_from(range(self.NUMBER_OF_ROOMS))   

       for i in range(self.NUMBER_OF_ROOMS-1):
          for j in range(self.NUMBER_OF_ROOMS-1):
             G.add_edge(i, j)

       # Everyone starts in the DINING ROOM
       suspects_positions = {i: 0 for i in range(self.NUMBER_OF_SUSPECTS)}        
       timeline[0] = suspects_positions.copy()

       # Helper function that moves people to adjacent rooms
       def move_people(suspects_positions, G):
        
           for person, current_position in suspects_positions.items():
               neighbors = list(nx.neighbors(G, current_position))               # Get adjacent neighbouring rooms
               suspects_positions[person] = random.choice(neighbors)             # Move person to a random room

           return suspects_positions

       # Simulate movement of suspects over NUMBER_OF_TIMESLOTS steps
       for time_slot in range(1, self.NUMBER_OF_TIMESLOTS):
           suspects_positions = move_people(suspects_positions, G)
           timeline[time_slot] = suspects_positions.copy()

       # All suspects end up in the GRAND BALLROOM 
       suspects_positions = {i: (self.NUMBER_OF_ROOMS-1) for i in range(self.NUMBER_OF_SUSPECTS)}
       timeline[self.NUMBER_OF_TIMESLOTS] = suspects_positions.copy()

       # Create a thief by checking the paths of all suspects
       # The thief is someone alone in a room during the crime window
       # defined as the time between CRIME_OCCURS plus CRIME_WINDOW
       # the power off room is where the thief was one step before
       for idx, time_slot in enumerate(timeline):     # Walk through whole day  

          # if we are within the crime window, see who is alone in a room
          if idx in range(self.CRIME_OCCURS,self.CRIME_OCCURS+self.CRIME_WINDOW):

             people_in_room = [self.get_people_in_room(room, timeline[time_slot]) for room in range(self.NUMBER_OF_ROOMS)]
             counts_in_room = [len(x) for x in people_in_room]
             prime_suspects = []

             for room_idx, count in enumerate(counts_in_room):
                if count == 1:
                   prime_suspects.append(people_in_room[room_idx][0])

             if len(prime_suspects) >= 1:
                 return random.choice(prime_suspects), idx, prime_suspects, timeline

       # We did not generate a proper crime, return None for the suspect and None for the crime time
       return None, None, prime_suspects, timeline

    def new_game(self):
        guilty_suspect_idx = None

        while (guilty_suspect_idx is None):
            guilty_suspect_idx, crime_occurs_time, prime_suspects, timeline = self.generate_new_game()

        self.current_suspect = None                                           # No suspect selected             
        self.guilty_suspect_idx = guilty_suspect_idx                             # Index of guilty suspect
        self.guilty_suspect = self.get_suspect_name(guilty_suspect_idx)      # Name of guilty suspect
        self.timeline = timeline                                       # Timeline for the crime scene 
        self.prime_suspects = prime_suspects                                 # List of potential suspects (as indices)
        self.have_alibi = self.have_alibis()                             # List of suspects with alibis (as indices)
        self.the_usual_suspects = self.round_up_the_usual_suspects()             # List of names of potential suspects
        self.power_cut_time_idx = crime_occurs_time - 1                          # Index to time when power was cut (occurs just before crime)
        self.crime_occurs_time_idx = crime_occurs_time                              # Index to time when crime occurred 
        self.power_cut_room_idx = self.get_power_off_room_idx()                  # Index to room where power was cut (occurs just before crime)
        self.crime_occurs_room_idx = self.get_crime_occurs_room_idx()               # Index to room where crime occurred
        self.times[self.power_cut_time_idx] = "Power Outage"  
        self.times[self.crime_occurs_time_idx] = "Time of Theft"
        self.power_cut_time_name = self.times[self.power_cut_time_idx]            # Time when power was cut (occurs just before crime)
        self.power_cut_room_name = self.get_power_off_room_name()                 # Room where power was cut (occurs just before crime)
        self.crime_occurs_time_name = self.times[self.crime_occurs_time_idx]         # Time when crime occurred 
        self.crime_occurs_room_name = self.get_crime_occurs_room_name()              # Room where crime occurred 
        self.stolen_painting = self.get_random_painting()                     # Reference to the stolen painting
        self.stolen_painting_img = self.stolen_painting["image"]
        self.stolen_painting_name = self.stolen_painting["name"]
        self.crime_description = self.get_crime_text()                          # Description of the crime
        self.crime_recap = ""                                             # A summary of hints and notes from suspects
        self.hints_given = 0                                              # Count of hints given
        self.hints_recap = []                                             # Recap of hints given during the gaming session

    def print_game(self):
        print("Crime timeline: \n", self.timeline, "\n")
        print("Name of current suspect: ", self.current_suspect)
        print("Index of guilty suspect: ", self.guilty_suspect_idx)
        print("Name of guilty suspect: ", self.guilty_suspect)
        print("Prime Suspects: ", self.prime_suspects)
        print("The usual suspects: ", self.the_usual_suspects)
        print("Have alibis: ", self.names_of_suspects_with_alibis())
        print("Time when power was cut: ", self.power_cut_time_name)    
        print("Room where power was cut: ", self.power_cut_room_name)    
        print("Time when crime occurred: ", self.crime_occurs_time_name)
        print("Room where crime occurred: ", self.crime_occurs_room_name)
        print("stolen_painting_img: ", self.stolen_painting_img)   
        print("stolen_painting_name: ", self.stolen_painting_name)   
        print("Crime Description: \n", self.crime_description)
        print("Hints Given: ", self.hints_given)

    # Game Function - Generate Script for Suspect
    def create_interview(self, suspect_name):
        suspect_idx = self.get_suspect_idx(suspect_name)                         
        whereabouts = self.get_timeline_for_person(suspect_idx, self.timeline)
        witnesses = [self.get_people_in_room(room, self.timeline[idx]) for idx, room in enumerate(whereabouts)]

        alibi = {
            "name": self.get_suspect_proper_name(suspect_name),
            "key suspect": suspect_idx in self.prime_suspects,
            "have alibi for time of theft": suspect_idx in self.have_alibi,
            "guilty": suspect_idx == self.guilty_suspect_idx,
            "stole painting": suspect_idx == self.guilty_suspect_idx,
        }

        timeline = []

        for idx, room in enumerate(whereabouts):
            if len(witnesses[idx]) == self.NUMBER_OF_SUSPECTS:
                witnesses_text = "Everyone"
            elif len(witnesses[idx]) == 1:
                witnesses_text = "No one. I was alone"
            else:
                witnesses_text = [self.get_suspect_name(witness) for witness in witnesses[idx] if witness != suspect_idx]

            timeline_dict = {
                "time": self.times[idx],
                "location": self.get_room_name(room),
                "activity": self.get_random_room_activity(room),
                "witnesses": witnesses_text,
            }
            
            timeline.append(timeline_dict)

        alibi["timeline"] = timeline        
        
        return str(alibi)

# Game Destructor
def __del__(self):
    print("Game Destructor Called")
    return
