#IMPORTS
# To do, 
#1. Global variable of food options (use SUTD canteen for reference)


#GLOBAL VARIABLES
FOODS_FILE = "food.csv"
LOCAL_FOODS = "burger,,non-spicy,western\nbanmian,spicy,non-spicy,asian,chinese"
USER_DATA = "user.csv"

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


""" #PROLLY CAN DELETE
class Food:
    def __init__(self, name, tags):
        self.name = name
        self.tags = tags """

class User:
    def __init__(self, name):
        self.name = name
        self.tried = {1:[], 2:[], 3:[]}
        
    def get_favourites(self):
        return self.tried[3]

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
    
def try_new():  #select from list of all foods - less those that have been tried
    return

def from_favourites():  #Select from list of tried and well rated foods
    return

def filter_by():
    #given a list of "tags" - spicy, thai, noodles, western, etc. choose from 
    #foods with those tags
    return

def eat_anything(): #choose from all foods, less dietary requirements
    return

def main():
    running = True
    while running:
        choice = display_menu()
        match choice:
            case "0":
                "Exiting. Enjoy your meal!"
                running = False

            case "1":
                print("Try something new")
                try_new()

            case "2":
                print("Pick from my favourites")
                from_favourites()

            case "3":
                print("Filter by choice of cuisine")
                filter_by()

            case "4":
                print("Anything")
                eat_anything()

            case _:
                print("No such option: ", choice)
                continue

    return

if __name__ == "__main__":
    main()
