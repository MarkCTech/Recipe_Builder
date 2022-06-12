import sqlite3
from pathlib import Path


class AddData:
    def __init__(self, name, ingr_list, macros):
        self.name = name
        self.ingr_list = ingr_list
        self.macros = macros

    def add_deets(self, name, servings, ingr):
        print("Add SQL values to database")


class AddRecipe(AddData):
    def add_deets(self, name: str, servings: str, rec_ingr: str):
        con = set_con()
        cur = con.cursor()
        # Insert a row of data
        cur.execute(
            "INSERT INTO recipes VALUES (?,?,?)",
            (name, servings, rec_ingr))
        end_con(con)


class AddIngr(AddData):
    def add_deets(self, ingredient: str, grams: str, macro: tuple):
        con = set_con()
        cur = con.cursor()
        # Insert a row of data
        cur.execute(
            "INSERT INTO ingredients VALUES (?,?,?,?,?,?,?,?)",
            (ingredient, grams, macro[0], macro[1], macro[2], macro[3], macro[4], macro[5]))
        end_con(con)


class Searcher:
    def __init__(self, name):
        self.name = name

    def search(self, name):
        pass


class SearchRec(Searcher):
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


class SearchIngr(Searcher):
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
    # Commit the changes and close
    con.commit()
    con.close()


def choose(res_list):
    print(f"\nAre any of these what you're looking for? {res_list}")
    length = len(res_list)
    while True:
        try:
            x = int(input("\nEnter item number, or 0 for no: "))
        except ValueError:
            print('Must be integer, Try Again!')
        else:
            if x > length:
                print(f'Choice must be below {length}')
            elif x == 0:
                x = False
                return x
            else:
                return x
        break


def main():
    set_db()
    play_check = True
    while play_check:
        rec_name = input("\nEnter recipe name to search for: ")
        rec_ingr = []

        srch_rec = SearchRec(rec_name)
        srch_rec_res = srch_rec.search(rec_name)
        choice = choose(srch_rec_res)

        if choice is int:
            result = srch_rec_res[choice]
            print("\nRecipe found!")
            print(result)

        if not choice:
            print("\nRecipe not found, please add it yourself!")

            ingr_check = True
            while ingr_check:
                ingr_name = input("\nEnter Ingredient to add to recipe: ")

                srch_ingr = SearchIngr(ingr_name)
                srch_ingr_res = srch_ingr.search(ingr_name)
                choice = choose(srch_ingr_res)

                if choice is int:
                    result = srch_rec_res[choice]
                    print("\nIngredient found!")
                    print(result)
                    rec_ingr.append(result)
                if not choice:
                    grams = input("Serving in Grams: ")
                    macros = add_ingr()
                    ingredient = AddIngr(ingr_name, grams, macros)
                    ingredient.add_deets(ingr_name, grams, macros)
                ingr_check = ask_another("ingredient")

        servings = str(input(f"How many servings of {rec_name}? "))
        recipe = AddRecipe(rec_name, servings, str(rec_ingr))
        recipe.add_deets(rec_name, servings, str(rec_ingr))
        play_check = ask_another("recipe")


if __name__ == '__main__':
    main()
