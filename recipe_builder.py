from pathlib import Path
import sqlite3


def main():
    recipe = input("Enter recipe name to search for: ")
    recipe_database(recipe)


# def recipe(ingredient):
#     recipe = []
#     ingr_row = ingredient
#     recipe += ingr_row
#     recipe_database(recipe)


def recipe_database(recipe):
    path = (Path.cwd() / "database")
    path_obj = path / 'recipes.db'
    conn = ''

    try:
        conn = sqlite3.connect(str(path_obj))
    except ValueError:
        print("Database 'recipes.db' does not exist")
        if not check_path(path_obj):
            conn = sqlite3.connect(str(path_obj))

    curr = conn.cursor()
    make_recipe_table(curr)
    add_recipe(curr, recipe)

    # Commit the changes and close
    conn.commit()
    conn.close()


def make_recipe_table(cur):
    cur.execute(
        '''CREATE TABLE IF NOT EXISTS recipes (Recipe,Servings)''')


def check_rec_database(cur, recipe):
    try:
        cur.execute("select * from recipes where Recipe=:name", {"name": {recipe}})
        result = cur.fetchall()
        return result
    finally:
        return False


def add_recipe(cur, recipe):
    if not check_rec_database(cur, recipe):
        print("\nRecipe not found, please add it yourself!")
        recipe = [recipe]

        while True:
            ingredient = input("\nEnter Ingredient to add to recipe: ")
            ingr_database(ingredient)
            recipe.append(ingredient)
            x = input("Add another ingredient? (Y/N): ")

            if x[0].lower() == 'y':
                continue

            elif x[0].lower() == 'n':
                break

            else:
                print("Try again.")
                continue

        add_rec_database(cur, recipe)


def add_rec_database(cur, recipe):
    rec_name = recipe[0]
    rec_serv = input("Servings: ")

    # Insert a row of data
    cur.execute(
        "INSERT INTO recipes (Recipe,Servings) VALUES (?,?)",
        (rec_name, rec_serv))


def check_recipe_database(cur, recipe):
    try:
        cur.execute("select * from recipes where recipe=:name", {"name": {recipe}})
        result = cur.fetchall()
        return result
    finally:
        return False


def ingr_database(ingredient):
    path = (Path.cwd() / "database")
    path_obj = path / 'ingredients.db'
    con = ''

    try:
        con = sqlite3.connect(str(path_obj))
    except ValueError:
        print("Database 'ingredients.db' does not exist")
        if not check_path(path_obj):
            con = sqlite3.connect(str(path_obj))

    cur = con.cursor()
    make_ingr_table(cur)
    add_ingredient(cur, ingredient)

    # Commit the changes and close
    con.commit()
    con.close()


def make_ingr_table(cur):
    cur.execute(
        '''CREATE TABLE IF NOT EXISTS ingredients (Ingredient,Grams,Calories,Protein,Carbs,Satfat,Unsat,Fibre)''')


def add_ingredient(cur, ingredient):
    if not check_ingr_database(cur, ingredient):
        add_ingr_database(cur, ingredient)


def check_ingr_database(cur, ingredient):
    try:
        cur.execute("select * from ingredients where ingredient=:name", {"name": {ingredient}})
        result = cur.fetchall()
        return result
    finally:
        return False


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
