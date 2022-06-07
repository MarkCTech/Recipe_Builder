from pathlib import Path
import sqlite3


def main():
    recipe = input("Enter recipe name to search for: ")
    recipe_database(recipe)


def recipe_database(recipe):
    # Create or connect to database
    path = (Path.cwd() / "database")
    path_obj = path / 'recipes.db'
    con = sqlite3.connect(str(path_obj))
    cur = con.cursor()
    make_recipe_table(cur)
    make_ingr_table(cur)

    add_recipe(cur, recipe)

    # Commit the changes and close
    con.commit()
    con.close()


def make_recipe_table(cur):
    cur.execute(
        '''CREATE TABLE IF NOT EXISTS recipes (Recipe,Servings,Ingredients)''')


def add_recipe(cur, recipe):
    check = check_rec_database(cur, recipe)
    if not check:
        print("\nRecipe not found, please add it yourself!")
        rec_ingr = []
        while True:
            ingredient = input("\nEnter Ingredient to add to recipe: ")
            add_ingredient(cur, ingredient)
            rec_ingr.append(ingredient)

            if ask_another_ingr():
                continue
            if not ask_another_ingr():
                break

        add_rec_database(cur, recipe, rec_ingr)

    elif check[0] == recipe:
        print("Recipe found!")


def ask_another_ingr():
    global playing
    while True:
        x = input("Add another ingredient? (Y/N): ")
        if x == '':
            print("Try again")
        elif x[0].lower() == 'y':
            return True
        elif x[0].lower() == 'n':
            return False
        else:
            print("Try again.")
            continue



def check_rec_database(cur, recipe):
    cur.execute("select * from recipes where Recipe=:name", {"name": recipe})
    return cur.fetchall()


def add_rec_database(cur, name, rec_ingr):
    rec_name = str(name)
    rec_serv = input("Servings: ")
    rec_ingr = str(rec_ingr)

    # Insert a row of data

    cur.execute(
        "INSERT INTO recipes (Recipe,Servings,Ingredients) VALUES (?,?,?)",
        (rec_name, rec_serv, rec_ingr))


def make_ingr_table(cur):
    cur.execute(
        '''CREATE TABLE IF NOT EXISTS ingredients (Ingredient,Grams,Calories,Protein,Carbs,Satfat,Unsat,Fibre)''')


def add_ingredient(cur, ingredient):
    check = check_ingr_database(cur, ingredient)
    print(check)
    if not check:
        add_ingr_database(cur, ingredient)
    elif check[0] == ingredient:
        print("Ingredient found!")


def check_ingr_database(cur, ingredient):
    cur.execute("select * from ingredients where Ingredient=:name", {"name": ingredient})
    return cur.fetchall()


def add_ingr_database(cur, ingredient):
    ingr_name = ingredient
    ingr_grams = input("Serving in Grams: ")
    ingr_cals = input("Calories per Serving: ")
    ingr_pro = input("Protein per Serving: ")
    ingr_carbs = input("Carbs per serving: ")
    ingr_satfat = input("Saturated Fat per Serving: ")
    ingr_unsat = input("Unsaturated Fat per Serving: ")
    ingr_fibre = input("Fibre per Serving: ")

    # Insert a row of data
    cur.execute(
        "INSERT INTO ingredients (Ingredient,Grams,Calories,Protein,Carbs,Satfat,Unsat,Fibre) VALUES (?,?,?,?,?,?,?,?)",
        (ingr_name, ingr_grams, ingr_cals, ingr_pro, ingr_carbs, ingr_satfat, ingr_unsat, ingr_fibre))


def check_path(path_obj):
    return str(path_obj.exists())


def connect(path_obj):
    sqlite3.connect(str(path_obj))


if __name__ == '__main__':
    main()
