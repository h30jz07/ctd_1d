import csv

LOCAL_FOODS = "chicken rice,spicy,non-spicy,asian,chinese\nbanmian,spicy,non-spicy,asian"

def read_database():    #read excel sheet and return in list format
    try:
        f = open("food.csv")
        lines = f.read()
        f.close()

    except FileNotFoundError:
        lines = LOCAL_FOODS
    finally:
        foods = {}
        for line in lines.splitlines():
            items = line.split(',')
            for i in range(1, len(items)):
                if items[i] in foods:
                    foods[items[i]].append(items[0])
                else:
                    foods[items[i]] = [items[0]]
        for food in foods:
            print(food, foods[food])

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
    with open("user.csv", "w", newline="") as f:
        wr = csv.writer(f, quoting=csv.QUOTE_NONE)
        f.write(user.name+"\n")
        wr.writerow(user.history[1])
        wr.writerow(user.history[2])
        wr.writerow(user.history[3])
        f.close()

""" user = User("chengyi", {1: ["good"], 2: ["better"], 3: ["best", "nigag"]})
update_user(user)
user = init_user()
print(user.name)
print(user.history) """

f = open("art.csv")
file = f.read()
print(file)
