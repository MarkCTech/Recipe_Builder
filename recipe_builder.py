from pathlib import Path
import sqlite3


def main():
    ingredient = input("Enter Ingredient to add to recipe: ")

    database(ingredient)


def database(ingredient):
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
    make_table(cur)

    if not check_database(cur, ingredient):
        add_database(cur, ingredient)

    # Commit the changes and close
    con.commit()
    con.close()


def check_path(path_obj):
    return str(path_obj.exists())


def connect(path_obj):
    sqlite3.connect(str(path_obj))


def make_table(cur):
    cur.execute(
        '''CREATE TABLE IF NOT EXISTS ingredients (Ingredient,Grams,Calories,Protein,Carbs,Satfat,Unsat,Fibre)''')


def check_database(cur, ingredient):
    try:
        cur.execute("select * from ingredients where ingredient=:name", {"name": {ingredient}})
        result = cur.fetchall()
        return result
    finally:
        return False


def add_database(cur, ingredient):
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


if __name__ == '__main__':
    main()
