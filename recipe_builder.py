from datetime import datetime
import sqlite3
from pathlib import Path


class AddData:
    def __init__(self, name, calories, ingr_list):
        self.name = name
        self.calories = calories
        self.ingr_list = ingr_list

    def add_deets(self, *args):
        print("Add SQL values to database")


class AddRecipe(AddData):
    def add_deets(self, name, calories, ingr_list):
        # Connect to database, insert a row of data into recipe table and close
        con = set_con()
        cur = con.cursor()
        values = (name, calories, ingr_list)
        cur.execute(
            "REPLACE INTO recipes VALUES (?,?,?)",
            values)
        end_con(con)


class AddIngr(AddData):
    def __init__(self, name, calgrams, macros):
        super().__init__(name, calgrams, macros)
        self.calgrams = calgrams
        self.macros = macros

    def add_deets(self, name, calgrams, macros):
        calories = calgrams[0]
        grams = calgrams[1]
        # Connect to database, insert a row of data into ingredient table and close
        con = set_con()
        cur = con.cursor()
        values = (name, calories, grams, macros[1], macros[1], macros[2], macros[3], macros[4])
        cur.execute(
            "REPLACE INTO ingredients VALUES (?,?,?,?,?,?,?,?)",
            values)
        end_con(con)


class AddLog(AddData):
    def add_deets(self, recipe_name, date_time, ingredients):
        # Connect to database, insert a row of data into daily log and close
        con = set_con()
        cur = con.cursor()
        values = (recipe_name, date_time, ingredients)
        cur.execute(
            "INSERT INTO log VALUES (?,?,?)",
            values)
        end_con(con)


class Searcher:
    def __init__(self, name):
        self.name = name

    def search(self, name):
        print("Returns database query")


class SearchRec(Searcher):
    def search(self, name):
        # Connect to database, searches the name of a row of data and close
        con = set_con()
        cur = con.cursor()
        try:
            cur.execute("select * from recipes where Recipe=:name", {"name": name})
            return cur.fetchall()
        except ValueError:
            return [None]
        finally:
            end_con(con)


class SearchIngr(Searcher):
    def search(self, name):
        # Connect to database, searches the name of a row of data and close
        con = set_con()
        cur = con.cursor()
        try:
            cur.execute("select * from ingredients where Ingredient=:name", {"name": name})
            return cur.fetchall()
        except ValueError:
            return [None]
        finally:
            end_con(con)


def ask_another(name):
    # Asks to add more recipes or ingredients
    x = input(f"Add another {name}? (Y/N): ")
    if x == '':
        print("Try again")
    elif x[0].lower() == 'y':
        return True
    elif x[0].lower() == 'n':
        return False
    else:
        print("Try again.")


def add_ingr():
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
    # Sets cursor to handle SQL, and ensures tables are built
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS recipes (Recipe,Calories,Ingredients)''')
    cur. execute('''CREATE UNIQUE INDEX IF NOT EXISTS idx_recipe ON recipes(Recipe);''')
    cur.execute('''CREATE TABLE IF NOT EXISTS ingredients (Ingredient,Grams,Calories,Protein,Carbs,Satfat,Unsat,
    Fibre)''')
    cur. execute('''CREATE UNIQUE INDEX IF NOT EXISTS idx_ingredient ON ingredients(Ingredient);''')
    cur.execute('''CREATE TABLE IF NOT EXISTS log (Name, DateTime, Ingredients)''')
    # Commit the changes and close
    con.commit()
    con.close()


def choose(res_list):
    # Presents User with list of search results from recipe or ingredient query
    # And asks them to pick one, or enter 0 for none
    print(f"\nAre any of these what you're looking for? \n\n{res_list}")
    length = len(res_list)
    while True:
        try:
            x = int(input("\nEnter item number, or 0 for no: "))
            if type(x) is int:
                if x > length:
                    print(f'Choice must be below {length}')
                elif x == 0:
                    return False
                else:
                    return x - 1
                break
        except ValueError:
            print('Must be integer, Try Again!')


def make_recipe(name, servings, ingredient_list):
    # Adds recipe to database
    rec_name = str(name)
    servings = str(servings)
    ingr_list = str(ingredient_list)
    recipe = AddRecipe(rec_name, servings, ingr_list)
    recipe.add_deets(rec_name, servings, ingr_list)
    return recipe


def ingr_db_logic():
    # Search for ingredient, User choose which or none
    ingr_name = input("Enter Ingredient to add to recipe: ")
    srch_ingr = SearchIngr(ingr_name)
    srch_ingr_res = srch_ingr.search(ingr_name)
    choice = choose(srch_ingr_res)

    if type(choice) is int:
        # If choice is valid index, ingredient is added to ingredient list
        ingredient = srch_ingr_res[choice]
        print("\nIngredient found!")
        print(ingredient)
        grams = str(input("How many grams for this serving? "))
        name = ingredient[0]
        name.join(grams)
        calories = str(input("How many calories for this serving? "))
        print(f"\nEntering {grams} grams, or {calories} calories of {name} to ingredient database \n")
        ingredient = AddIngr(ingredient[0], ingredient[1], ingredient[2])
        return ingredient

    if not choice and type(choice) is not int:
        # If ingredient not in database, User adds macros
        calories = int(input("How many calories for this serving: "))
        macros = add_ingr()
        grams = int(input("\nHow many grams for this serving?  "))
        calgrams = (calories, grams)

        # Adds ingredient to database
        ingredient = AddIngr(ingr_name, calgrams, macros)
        ingredient.add_deets(ingr_name, calgrams, macros)
        grams = ingredient.calgrams
        calories = grams[0]
        grams = grams[1]
        print(f"\nEntering {grams} grams, or {calories} calories of {ingredient.name} "
              f"into ingredient database ")
        return ingredient


def rec_db_logic():
    ingredient_list = []

    # Search for recipe in database
    rec_name = input("\nEnter recipe name to search for: ")
    srch_rec = SearchRec(rec_name)
    srch_rec_res = srch_rec.search(rec_name)

    # User chooses which recipe from search results, or none. Assigns int or False to choice
    choice = choose(srch_rec_res)

    # If recipe in database, recipe log is saved
    if type(choice) is int:
        # needs add to log
        recipe = srch_rec_res[choice]
        print("\nRecipe found!")
        print(recipe)
        recipe = AddRecipe(recipe[0], recipe[1], recipe[2])
        return recipe

    # If recipe not in database, User adds the details
    elif not choice:
        print("\nRecipe not found, please add it yourself!")

        # Controls state of play
        calories = 0
        ingr_play = True
        while ingr_play:
            # Calls ingr_db_logic, searches db to insert or return ingredient
            ingredient = ingr_db_logic()
            ingredient_list.append(ingredient.name)
            calgrams = ingredient.calories
            calories += int(calgrams[0])

            # Asks if user is finished adding to ingredient list
            ingr_play = ask_another("ingredient")

        recipe = make_recipe(rec_name, calories, ingredient_list)
        return recipe


def main():
    set_db()
    play_check = True
    while play_check:
        # Returns, or creates and returns a recipe
        recipe = rec_db_logic()

        # Add recipe to log
        date_time = datetime.now()
        print(f"\nRecipe name is: {recipe.name}\n"
              f"Calories in this recipe are: {recipe.calories}\n"
              f"Ingredients are: {recipe.ingr_list}\n")
        addlog = AddLog(recipe.name, date_time, recipe.ingr_list)
        addlog.add_deets(recipe.name, date_time, recipe.ingr_list)

        # Asks if finished
        play_check = ask_another("recipe")


if __name__ == '__main__':
    main()
