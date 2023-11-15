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

read_database()
