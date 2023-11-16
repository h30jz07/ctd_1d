#IMPORTS
from csv import writer, QUOTE_NONE
from random import randrange


#GLOBAL VARIABLES
FOODS_FILE = "food.csv"
USER_DATA = "user.csv"
LOCAL_FOODS = "burger,,non-spicy,western\nbanmian,spicy,non-spicy,asian,chinese"

MENU = """ 
========================
What can we get you today, sir/madam?
------------------------
1. I'm thinking about trying something new.
2. I would like to pick from my favorites.
3. I'm craving...
4. Recommend me anything.
0. EXIT
========================
"""

class User:
    def __init__(self, name, history={1:[], 2:[], 3:[]}):
        self.name = name
        self.history = history
        
    def get_favorites(self):
        if self.history[3] != []:
            favorite = self.history[3]
        elif self.history[2] != []:
            favorite = self.history[2]
        else:
            favorite = []
        return favorite 

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
    new_food = set()
    for food_ls in list(food_dict.values()):
        for food in food_ls:
            if food not in user.history.values():
                new_food.add(food)
    random_int = randrange(len(new_food))
    return list(new_food)[random_int]

def from_favorites(user):  #Select from list of tried and well rated foods
    return user.get_favorites()

def filter_by(food_dict): #given a list of "tags" - spicy, thai, noodles, western, etc. choose from foods with those tags
    running = True
    while running:
        tag = input("So, what are you craving today?")
        match tag:
            case "more":
                [print(x) for x in food_dict]

            case anything:
                try:
                    filtered = food_dict[anything]
                    running = False
                except KeyError:
                   print("Sorry, we do not have {}.".format(anything))

    return filtered

def eat_anything(food_dict): #choose from all foods, less dietary requirements
    all_food = list(food_dict.values())
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
                print("Hmm, if you want to try something new,")
                food = try_new(food_dict, user)

            case "2":
                print("Ok, let me pick something from your favorites,")
                food = from_favorites(user)

            case "3":
                print("Enter 'more' for options or you can enter the type of food directly.")
                food = filter_by(food_dict)

            case "4":
                print("Anything")
                food = eat_anything(food_dict)

            case _:
                print("Choice", choice, "is not available, please enter a valid choice.")
                continue

        print("You should try {}.".format(food))
            

    update_user(user)
    return

if __name__ == "__main__":
    main()
