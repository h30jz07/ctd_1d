#IMPORTS
from random import choice, sample
from time import sleep
from colorama import Fore
import json

#GLOBAL VARIABLES
FOODS_FILE = "food.csv"
USER_DATA = "user.json"
LOCAL_FOODS = """burger,non-spicy,western
banmian,spicy,non,asian,chinese
chicken rice,non-spicy,chinese"""

MENU = Fore.LIGHTYELLOW_EX + """ 
========================
What can we get you today, {}?
------------------------
1. I'm thinking about trying something new
2. I would like to pick from my favourites
3. I'm craving...
4. Recommend me anything
5. View my food history
0. EXIT
========================
""" + Fore.WHITE

class User:
    def __init__(self, name, history={1:[], 2:[], 3:[]}):
        self.name = name
        self.history = history

    def __str__(self):
        placeholder = "nothing yet"
        rating_1 = ", ".join(self.history[1]) if self.history[1] else placeholder
        rating_2 = ", ".join(self.history[2]) if self.history[2] else placeholder
        rating_3 = ", ".join(self.history[3]) if self.history[3] else placeholder
        string = Fore.WHITE + """
Profile
=======
{}

Ratings
=======
meh: {}
not bad: {}
it's bussin: {}
""".format(self.name, rating_1, rating_2, rating_3)
        return string
        
    def get_favourites(self):
        if self.history[3] != []:
            favourite = self.history[3]
        elif self.history[2] != []:
            favourite = self.history[2]
        else:
            favourite = []
        return favourite 

    def get_new(self, ls):
        new = []
        for item in ls:
            if item not in self.history.values():
                new.append(item)
        return new
    
    def set_history(self, rating, food):
        self.history[rating].append(food)

    def to_dict(self):
        return {"name": self.name, "history": self.history}

#FUNCTIONS
def display_banner():
    print(Fore.LIGHTYELLOW_EX + r"""

 __          ___           _     _                     _  ___  
 \ \        / / |         | |   | |                   | ||__ \ 
  \ \  /\  / /| |__   __ _| |_  | |_ ___     ___  __ _| |_  ) |
   \ \/  \/ / | '_ \ / _` | __| | __/ _ \   / _ \/ _` | __|/ / 
    \  /\  /  | | | | (_| | |_  | || (_) | |  __/ (_| | |_|_|  
     \/  \/   |_| |_|\__,_|\__|  \__\___/   \___|\__,_|\__(_)  
                                                               
                                                               
""")

def display_menu(username): #display menu and ask for input
    return input(MENU.format(username))

def add_to_dict(lines): #sort foods into a dictionary with tags as keys
    dictionary = {}
    for line in lines.splitlines():
        items = line.split(',')
        for i in range(1, len(items)):
            if items[i] in dictionary:
                dictionary[items[i]].append(items[0])
            else:
                dictionary[items[i]] = [items[0]]
    return dictionary

def read_database():    #read excel sheet and return in list format
    try: #try to open food database
        f = open(FOODS_FILE)
        lines = f.read()
        f.close()
    
    except FileNotFoundError: #if no food database, use local small one
        lines = LOCAL_FOODS

    finally:
        return add_to_dict(lines)
    
def try_new(food_dict, user):  #select from list of all foods - less those that have been tried
    food_ls = set(sum(food_dict.values(), []))
    new_food = user.get_new(food_ls)
    return choice(new_food)

def from_favourites(user):  #Select from list of tried and well rated foods
    favourites = user.get_favourites()
    if favourites:
        return choice(favourites)
    else:
        return None

def filter_by(food_dict): #given a list of "tags" - spicy, thai, noodles, western, etc. choose from foods with those tags
    running = True
    while running:
        tag = input(Fore.WHITE + "So, what cuisine are you craving today? ")
        match tag:
            case "more":
                [print(Fore.YELLOW + x) for x in food_dict]

            case anything:
                try:
                    filtered = food_dict[anything]
                    running = False
                except KeyError:
                   tags = sample(sorted(food_dict), 3)

                   print(Fore.RED + "Sorry, we do not have {}. How about {}, {}, or {}".format(anything, tags[0], tags[1], tags[2]))

    
    return choice(filtered)

def eat_anything(food_dict): #choose from all foods, less dietary requirements
    all_food = sum(food_dict.values(), [])
    return choice(all_food)

def init_user():
    try:
        with open(USER_DATA) as f:
            data = json.load(f)
            d = data["history"]
            history = {1: d["1"], 2: d["2"], 3: d["3"]}
            return User(data["name"], history)

    except (FileNotFoundError, IndexError):
        return User(input(Fore.WHITE + "Welcome new user! Please enter your name: "))

def update_user(user):
    try:
        with open(USER_DATA, "w") as f:
            f.write(json.dumps(user.to_dict()))
    except KeyError:
        user = User(user.name)

def rate_food():
    rate_loop = True
    rating = input(Fore.WHITE + "Was the food to your liking? Please rate it from 1-3 stars!: ")
    while rate_loop:
        match rating:
            case "1":
                rating = 1
                rate_loop = False
                break
            case "2":
                rating = 2
                rate_loop = False
                break
            case "3":
                rating = 3
                rate_loop = False
                break
            case _:
                Fore.RESET
                rating = input("Enter a number from 1 - 3!: ")
                continue
    sleep(0.5)
    return rating

def main():
    running = True
    display_banner()
    user = init_user()
    food_dict = read_database()
    while running:
        choice = display_menu(user.name)
        match choice:
            case "0":
                print(Fore.LIGHTYELLOW_EX + "Exiting. Enjoy your meal!")
                running = False
                sleep(1)
                break
            case "1":
                print(Fore.YELLOW + "Hmm, if you want to try something new,")
                food = try_new(food_dict, user)
            case "2":
                print(Fore.YELLOW + "Ok, let me pick something from your favourites,")
                food = from_favourites(user)
                if food is None:
                    print(Fore.RED + "I don't know what you like yet :( Choose a different option")
                    continue
            case "3":
                print(Fore.YELLOW + "Enter 'more' for options or you can enter the type of food directly.")
                food = filter_by(food_dict)
            case "4":
                print(Fore.YELLOW + "Anything")
                food = eat_anything(food_dict)

            case "5":
                print(Fore.LIGHTGREEN_EX + "Loading your profile")
                print(user)
                sleep(1)
                continue

            case _:
                print(Fore.RED + "Choice", choice, "is not available, please enter a valid choice.")
                sleep(0.5)
                continue

        print(Fore.LIGHTGREEN_EX + "You should try {}.".format(food))
        sleep(1)
        user.set_history(rate_food(), food)

    update_user(user)

if __name__ == "__main__":
    main()
