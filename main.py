#IMPORTS
from csv import writer, QUOTE_NONE
from random import randrange


#GLOBAL VARIABLES
FOODS_FILE = "food.csv"
USER_DATA = "user.csv"
LOCAL_FOODS = "burger,,non-spicy,western\nbanmian,spicy,non-spicy,asian,chinese"

MENU = """ 
========================
I love food!!!
------------------------
1. Try something new!
2. Pick from my favourites
3. I'm craving...
4. ANYTHING
0. QUIT
========================
"""

class User:
    def __init__(self, name, history={1:[], 2:[], 3:[]}):
        self.name = name
        self.history = history
        
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
            if item not in self.tried.values():
                new.append(item)
        return new

#FUNCTIONS
def display_menu(): #display menu and ask for input
    return input(MENU)

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
    new_food = []
    for food in set(food_dict.values()):
        if food not in user.history.values():
            new_food.add(food)
    random_int = randrange(len(new_food))
    return new_food[random_int]

def from_favourites(user):  #Select from list of tried and well rated foods
    return user.get_favourites()

def filter_by(food_dict, tag): #given a list of "tags" - spicy, thai, noodles, western, etc. choose from foods with those tags
    running = True
    while running:
        tag = input("What are you craving today? (Enter 'more' for options)")
        match tag:
            case "more":
                [print(x) for x in food_dict.headers()]

            case anything:
                try:
                    filtered = food_dict[anything]
                    running = False
                except KeyError:
                   print("We do not have that.")

    return filtered

def eat_anything(food_dict): #choose from all foods, less dietary requirements
    all_food = set(food_dict.values())
    random_int = randrange(len(all_food))
    return all_food[random_int]

def init_user():
    try:
        with open("user.csv") as f:
            user_data = f.read().splitlines()
            food_dict = {}
            for i in range(1,len(user_data)):
                food_dict[i] = user_data[i]
            return User(user_data[0], food_dict)

    except FileNotFoundError:
        return User(input("Welcome new user! Please enter your name: "))

def update_user(user):
    try:
        with open("user.csv", "w", newline="") as f:
            wr = writer(f, quoting=QUOTE_NONE, escapechar="\\")
            f.write(user.name+"\n")
            wr.writerow(user.history[1])
            wr.writerow(user.history[2])
            wr.writerow(user.history[3])
    except KeyError:
        user = User(user.name)

def main():
    running = True
    while running:
        user = init_user()
        food_dict = read_database()
        choice = display_menu()
        match choice:
            case "0":
                "Exiting. Enjoy your meal!"
                running = False
                continue
            case "1":
                print("Try something new")
                food = try_new(food_dict, user)

            case "2":
                print("Pick from my favourites")
                from_favourites(user)

            case "3":
                print("Filter by choice of cuisine")
                filter_by(food_dict)

            case "4":
                print("Anything")
                eat_anything(food_dict)

            case _:
                print("No such option: ", choice)
                continue

        print("You should eat {}".format(food))
            

    update_user(user)
    return

if __name__ == "__main__":
    main()
