import sqlite3
from pathlib import Path


class AddData:
    def __init__(self, name, ingr_list, macros):
        self.name = name
        self.ingr_list = ingr_list
        self.macros = macros

    def add_deets(self, *args):
        print("Add SQL values to database")


class AddRecipe(AddData):
    def add_deets(self, name, servings, ingr_list):
        # Connect to database, insert a row of data into recipe table and close
        con = set_con()
        cur = con.cursor()
        values = (name, servings, ingr_list)
        cur.execute(
            "INSERT INTO recipes VALUES (?,?,?)",
            values)
        end_con(con)


class AddIngr(AddData):
    def add_deets(self, ingr_name, servings, macros):
        # Connect to database, insert a row of data into ingredient table and close
        con = set_con()
        cur = con.cursor()

        values = (ingr_name, servings, macros[0], macros[1], macros[2], macros[3], macros[4], macros[5])

        cur.execute(
            "INSERT INTO ingredients VALUES (?,?,?,?,?,?,?,?)",
            values)
        end_con(con)


class AddLog(AddData):
    def add_deets(self, log_name, *args):
        # Connect to database, insert a row of data into daily log and close
        con = set_con()
        cur = con.cursor()
        cur.execute(
            "INSERT INTO log VALUES (?,?,?)",
            (args[0], args[1], args[2]))
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
    cals = input("Calories per Serving: ")
    pro = input("Protein per Serving: ")
    carbs = input("Carbs per serving: ")
    satfat = input("Saturated Fat per Serving: ")
    unsat = input("Unsaturated Fat per Serving: ")
    fibre = input("Fibre per Serving: ")

    macro_tup = (cals, pro, carbs, satfat, unsat, fibre)
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
    cur.execute('''CREATE TABLE IF NOT EXISTS recipes (Recipe,Servings,Ingredients)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS ingredients (Ingredient,Grams,Calories,Protein,Carbs,Satfat,Unsat,
    Fibre)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS log (Day, Time, Recipe, Calories)''')
    # Commit the changes and close
    con.commit()
    con.close()


def choose(res_list):
    # Presents User with list of search results from recipe or ingredient query
    # And asks them to pick one, or enter 0 for none
    print(f"\nAre any of these what you're looking for? {res_list}")
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


def ingr_func(ingr_name):
    # Controls state of play
    rec_ingr = []
    ingr_play = True
    while ingr_play:

        # Search for ingredient, User choose which or none
        srch_ingr = SearchIngr(ingr_name)
        srch_ingr_res = srch_ingr.search(ingr_name)
        choice = choose(srch_ingr_res)
        print(choice)
        print(bool(choice))

        if type(choice) is int:
            # If choice is valid index, ingredient is added to recipe ingredients rec_ingr
            result = srch_ingr_res[choice]
            print("\nIngredient found!")
            print(result)
            rec_ingr.append(ingr_name)

        if not choice and choice != 0:
            # If ingredient not in database, User adds macros
            grams = input("Serving in Grams: ")
            macros = add_ingr()

            # Adds ingredient to database
            ingredient = AddIngr(ingr_name, grams, macros)
            ingredient.add_deets(ingr_name, grams, macros)

            # Adds ingredient to recipe ingredient list
            rec_ingr.append(ingr_name)

        # Asks if user is finished adding ingredients rec_ingr
        ingr_play = ask_another("ingredient")
    return rec_ingr


def main():
    set_db()
    play_check = True
    while play_check:
        # Search for recipe in database, User choose which or none
        rec_name = input("\nEnter recipe name to search for: ")
        srch_rec = SearchRec(rec_name)
        srch_rec_res = srch_rec.search(rec_name)
        choice = choose(srch_rec_res)

        rec_ingr = []

        # If recipe in database, recipe log is saved
        if choice is int:
            # needs add to log
            recipe = srch_rec_res[choice]
            print("\nRecipe found!")
            print(recipe)

        elif not choice:
            # If recipe not in database, User adds the details
            print("\nRecipe not found, please add it yourself!")
            ingr_name = input("Enter Ingredient to add to recipe: ")
            rec_ingr.append(ingr_func(ingr_name)[0])

        # Adds recipe to database
        servings = str(input(f"How many servings of {rec_name}? "))
        str_rec_ingr = str(rec_ingr)
        print(type(str_rec_ingr), str_rec_ingr)
        recipe = AddRecipe(rec_name, servings, str_rec_ingr)
        recipe.add_deets(rec_name, servings, str_rec_ingr)

        # Asks if finished
        play_check = ask_another("recipe")


if __name__ == '__main__':
    main()
