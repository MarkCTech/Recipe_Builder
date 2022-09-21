from datetime import datetime
import sqlite3
from pathlib import Path


class AddData:
    def __init__(self, name):
        self.name = name

    def add_deets(self, *args):
        print("Add SQL values to database")

    def search(self, name):
        # Connect to database, searches/returns the name of a row of data and closes connection
        print("Returns database query")

    def populate(self, search_result):
        print("Populates attributes with SQL search results")


class Recipe(AddData):
    def __init__(self, name):
        super().__init__(name)
        self.grams = 0
        self.calories = 0
        self.macros = [0, 0, 0, 0, 0]
        self.ingr_list = []

    def add_deets(self, name, grams, calories, macros, ingr_list):
        # Connect to database, insert a row of data into recipe table and close
        con = set_con()
        cur = con.cursor()
        values = (name, grams, calories, macros, ingr_list)
        cur.execute(
            "REPLACE INTO recipes VALUES (?,?,?,?,?)",
            values)
        end_con(con)

    def search(self, name):
        con = set_con()
        cur = con.cursor()
        try:
            cur.execute("select * from recipes where Recipe=:name", {"name": name})
            return cur.fetchall()
        except ValueError:
            return [None]
        finally:
            end_con(con)

    def populate(self, search_results):
        self.grams = search_results[0][1]
        self.calories = search_results[0][2]
        self.macros = search_results[0][3]
        self.ingr_list = search_results[0][4]


class Ingredient(AddData):
    def __init__(self, name):
        super().__init__(name)
        self.grams = 0
        self.calories = 0
        self.macros = [0, 0, 0, 0, 0]

    def add_deets(self, name, grams, calories, macros):
        # Connect to database, insert a row of data into ingredient table and close
        con = set_con()
        cur = con.cursor()
        values = (name, grams, calories, macros[0], macros[1], macros[2], macros[3], macros[4])
        cur.execute(
            "REPLACE INTO ingredients VALUES (?,?,?,?,?,?,?,?)",
            values)
        end_con(con)

    def search(self, name):
        con = set_con()
        cur = con.cursor()
        try:
            cur.execute("select * from ingredients where Ingredient=:name", {"name": name})
            return cur.fetchall()
        except ValueError:
            return [None]
        finally:
            end_con(con)

    def populate(self, search):
        self.grams = str(search[1])
        self.calories = str(search[2])
        self.macros = search[3:]


class AddLog(AddData):
    def add_deets(self, recipe_name, date_time, calories, ingredients):
        # Connect to database, insert a row of data into daily log and close
        con = set_con()
        cur = con.cursor()
        values = (recipe_name, date_time, calories, ingredients)
        cur.execute(
            "INSERT INTO log VALUES (?,?,?,?)",
            values)
        end_con(con)


def ask_another(name):
    # Asks to add more recipes or ingredients
    x = input(f"\nAdd another {name}? (Y/N): ")
    if x == '':
        print("Try again")
    elif x[0].lower() == 'y':
        return True
    elif x[0].lower() == 'n':
        return False
    else:
        print("Try again.")


def add_macros():
    # Adds values and returns a tuple of ingredient macros
    pro = input("Protein per Serving: ")
    carbs = input("Carbs per serving: ")
    satfat = input("Saturated Fat per Serving: ")
    unsat = input("Unsaturated Fat per Serving: ")
    fibre = input("Fibre per Serving: ")

    macro_tup = (pro, carbs, satfat, unsat, fibre)
    return macro_tup


def set_con():
    # Connects to SQL database
    path = (Path.cwd() / "database")
    path_obj = path / 'recipes.db'
    con = sqlite3.connect(str(path_obj))
    return con


def end_con(con):
    # Commit the changes and close
    con.commit()
    con.close()


def set_db():
    # Connects to SQL database
    path = (Path.cwd() / "database")
    path_obj = path / 'recipes.db'
    con = sqlite3.connect(str(path_obj))
    # Sets cursor to handle SQL, and ensures tables are built, with unique ingredients and recipes
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS recipes (Recipe,Grams,Calories,Macros,Ingredients)''')
    cur. execute('''CREATE UNIQUE INDEX IF NOT EXISTS idx_recipe ON recipes(Recipe);''')
    cur.execute('''CREATE TABLE IF NOT EXISTS ingredients (Ingredient,Grams,Calories,Protein,Carbs,Satfat,Unsat,
    Fibre)''')
    cur. execute('''CREATE UNIQUE INDEX IF NOT EXISTS idx_ingredient ON ingredients(Ingredient);''')
    cur.execute('''CREATE TABLE IF NOT EXISTS log (Name,DateTime,Calories,Ingredients)''')
    # Commit the changes and close
    con.commit()
    con.close()


def display_ingr_list(name, macros, ingr_list):
    m = rmv_paren(str(macros))
    # Display the ingredient list in the log
    print(f"\n               {name}\n--------------------------------------------")
    print("| Protein | Carbs | Satfat | Unsat | Fibre |")
    print("| " + m[0] + "    | " + m[1] + "  | " + m[2] +
          "    | " + m[3] + "   | " + m[4] + "  |")
    print("--------------------------------------------")
    print("\n           Ingredients")
    print("---------------------------------")
    print("| Ingredient | Grams | Calories |")
    print(' ------------------------------')
    ingrs = rmv_paren(str(ingr_list))
    for i in ingrs:
        print("| " + str(i[0]) + "    | " + str(i[1]) + "    | " + str(i[2]) + "    |")
        print("---------------------------------")


def rmv_paren(mystr):
    stack = ""
    heap = []
    returnable = []
    noinclude = ["(", ")", ",", "'", "[", "]", " "]
    close = [")", ",", "]"]
    for i in mystr:
        append_play = True
        while append_play:
            if i not in noinclude:
                stack += i
            if i in close:
                if len(stack) > 0:
                    heap.append(stack)
                if i == ")" or i == mystr[-1]:
                    if len(heap) > 0:
                        returnable.append(heap)
                    heap = []
                stack = ""
            break

    if len(returnable) > 1:
        return returnable
    elif len(returnable) == 1:
        return returnable[0]
    else:
        return "Error, cannot parse string"


def choose(res_list):
    # Presents User with search results from recipe or ingredient query
    print(f"\nAre these the details you're looking for? \n\n{res_list}")
    while True:
        try:
            x = str(input("\nEnter Yes or No: "))
            if type(x) is str:
                if x[0].lower() == 'n':
                    return 0
                elif x[0].lower() == 'y':
                    return 1
                else:
                    print("Must be y or n")
                    continue
        except ValueError:
            print('Must be integer, Try Again!')


def convert_serving(ingredient):
    # Asks serving size for this instance and adjusts ingredient object
    print(f"\nUsual serving is {ingredient.grams} grams, for {ingredient.calories} calories of {ingredient.name}")
    instance_grams = int(input("How many grams for your serving this time? "))
    percentage = instance_grams / int(ingredient.grams)
    instance_cals = int(ingredient.calories) * percentage
    instance_macros = [int(i) * percentage for i in ingredient.macros]

    ingredient.grams = instance_grams
    ingredient.calories = instance_cals
    ingredient.macros = instance_macros


def ingr_db_logic():
    # Search for ingredient in database
    ingr_name = input("Enter Ingredient to add to recipe: ")
    ingredient = Ingredient(ingr_name)
    search = ingredient.search(ingr_name)
    choice = choose(search)  # User chooses if premade ingredient is present and correct

    # User chooses an ingredient or makes it, enters grams per STANDARD serving / THIS serving
    try:
        if choice:
            # If choice is True, premade ingredient is added to ingredient list

            print(f"\nIngredient found!")
            print(f'{ingredient.name}')
            ingredient.populate(search[0])

        if not choice:
            # If ingredient not in database
            ingredient.grams = str(input(f"How many grams is the standard serving for {ingr_name}? "))
            ingredient.calories = str(input(f"How many calories for {ingredient.grams} grams of {ingr_name}? "))
            ingredient.macros = add_macros()

            # Adds Ingredient to database
            ingredient.add_deets(ingr_name, ingredient.grams, ingredient.calories, ingredient.macros)

            # Displays object
            print(f"\n{ingredient.grams} grams or {ingredient.calories} calories of {ingredient.name}")

    finally:
        convert_serving(ingredient)
        return ingredient


def rec_db_logic():
    # Search for recipe in database
    rec_name = input("\nEnter recipe name to search for: ")
    recipe = Recipe(rec_name)
    search = recipe.search(rec_name)
    # User chooses if premade recipe is present and correct
    choice = choose(search)

    # If recipe in database, recipe is resaved with the same details
    if choice:
        recipe.populate(search)
        print("\nRecipe found!")

    # If recipe not in database, User adds the details
    elif not choice:
        print("\nRecipe not found, please add it yourself!")
        # Adds ingredients to Recipe
        ingr_play = True
        while ingr_play:
            # Searches database to insert and/or return ingredient
            ingredient = ingr_db_logic()
            # Adds ingredient data to Recipe object
            recipe.grams += ingredient.grams
            recipe.calories += ingredient.calories
            recipe.macros = [a + b for a, b in zip(recipe.macros, ingredient.macros)]
            recipe.ingr_list.append((ingredient.name, ingredient.grams, ingredient.calories, ingredient.macros))
            print(f"\nEntering into recipe:\n\n"
                  f"{ingredient.grams} grams of {ingredient.name}\n"
                  f"{ingredient.calories} calories \n")
            print(f"\nRecipe so far is {recipe.calories} calories")

            # Asks if user is finished adding to ingredient list
            ingr_play = ask_another("ingredient")

        recipe.add_deets(str(rec_name), str(recipe.grams), str(recipe.calories),
                         str(recipe.macros), str(recipe.ingr_list))
    return recipe


def main():
    set_db()
    play_check = True
    while play_check:
        # Returns, or creates and returns a recipe
        recipe = rec_db_logic()

        # Add recipe to log
        date_time = datetime.now()
        display_ingr_list(recipe.name, recipe.macros, recipe.ingr_list)
        addlog = AddLog(recipe.name)
        addlog.add_deets(str(recipe.name), str(date_time), str(recipe.calories), str(recipe.ingr_list))

        # Asks if finished
        play_check = ask_another("recipe")


if __name__ == '__main__':
    main()
