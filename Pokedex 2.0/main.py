
from flask import Flask, render_template, request, redirect
from flask_scss import Scss

import mysql.connector
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="pokemon_app_db"
)
mycursor = mydb.cursor()

app = Flask(__name__)
Scss(app)



"""
CREATE DB
"""
    # mycursor.execute("CREATE DATABASE pokemon_app_db")
    # mydb.database = "pokemon_app_db"

    # create_table_query = """
    # CREATE TABLE Pokemon (
    #     id INT AUTO_INCREMENT UNIQUE NOT NULL PRIMARY KEY,
    #     name VARCHAR(255) NOT NULL,
    #     base_hp INT NOT NULL,
    #     type VARCHAR(50),
    #     evolution VARCHAR(50)
    # );
    # """
    # mycursor.execute(create_table_query)
    #
    # pokemon_data = [
    #     ('Bulbasaur', 60, 'grass/poison', 'basic'),
    #     ('Ivysaur', 90, 'grass/poison', 'stage 1'),
    #     ('Venusaur', 250, 'grass/poison', 'stage 2'),
    #     ('Charmander', 60, 'fire', 'basic'),
    #     ('Charmeleon', 90, 'fire', 'stage 1'),
    #     ('Charizard', 220, 'fire/flying', 'stage 2'),
    #     ('Squirtle', 60, 'water', 'basic'),
    #     ('Wartortle', 90, 'water', 'stage 1'),
    #     ('Blastoise', 230, 'water', 'stage 2'),
    # ]
    # insert_query = """
    # INSERT INTO pokemon (name, base_hp, type, evolution)
    # VALUES (%s, %s, %s, %s)
    # """
    # mycursor.executemany(insert_query, pokemon_data)
    # mydb.commit()



"""
APP FUNCTIONS
"""
## CREATE
def insert_pokemon(p_name, p_type, p_hp, p_evolution):
  p_name = p_name.capitalize()
  p_hp = int(p_hp)
  p_type = p_type.lower()
  p_evolution = p_evolution.lower()
  insert_query = """
  INSERT INTO Pokemon (name, base_hp, type, evolution)
  VALUES (%s, %s, %s, %s)
  """
  insert_values = (p_name, p_hp, p_type, p_evolution)
  mycursor.execute(insert_query, insert_values)
  mydb.commit()
  print(f"Pokemon '{p_name}' succesfully added to pokedex.")

### READ
def show_pokemon(filter: str):
  mycursor.execute("SELECT * FROM Pokemon " + f"{filter}")
  all_pokemons = mycursor.fetchall()
  return all_pokemons

def filter_pokemon():
  filter_base = int(input("How do you want to filter Pokemon? (1-8) > "))
  # Name A-Z
  if filter_base == 1:
    show_pokemon("ORDER BY name ASC")
  # Name Z-A
  elif filter_base == 2:
    show_pokemon("ORDER BY name DESC")
  # Letter in name
  elif filter_base == 3:
    must_have_str = input("What does the name contain? > ")
    show_pokemon(f"WHERE name LIKE '%{must_have_str.lower()}%'")
  # HP asc
  elif filter_base == 4:
    show_pokemon("ORDER BY base_hp ASC")
  # HP desc
  elif filter_base == 5:
    show_pokemon("ORDER BY base_hp DESC")
  # Paticular type
  elif filter_base == 6:
    pokemon_type = input("What type? > ")
    show_pokemon(f"WHERE type LIKE '%{pokemon_type.lower()}%'")
  # Evolution stage
  elif filter_base == 7:
    pokemon_stage = input("What evolution stage? > ")
    show_pokemon(f"WHERE evolution LIKE '%{pokemon_stage.lower()}%'")
  # Type asc
  elif filter_base == 8:
    show_pokemon("ORDER BY type ASC")



"""
MAIN PAGE
"""
@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        p_name = request.form["Name"]
        p_type = request.form["Type"]
        p_hp = int(request.form["base_hp"])
        p_evolution = request.form["Evolution"]
        if p_hp > 0:
            insert_pokemon(p_name, p_type, p_hp, p_evolution)
        return redirect("/")
    else:
        pokemons = show_pokemon("")
        return render_template("index.html", pokemons=pokemons)



"""
SECONDARY PAGE
"""
### DELETE
@app.route("/delete/<int:pokemon_id>")
def delete_pokemon(pokemon_id):
    try:
        mycursor.execute("DELETE FROM Pokemon WHERE id = %s", (pokemon_id,))
        mydb.commit()
        print(f"Pokemon with ID {pokemon_id} successfully deleted.")
        return redirect("/")
    except Exception as e:
        print(f"Error deleting Pokemon: {str(e)}")
        return f"Error: {str(e)}"


  
### UPDATE
@app.route("/edit/<int:pokemon_id>",methods=["POST","GET"])
def edit_pokemon(pokemon_id):
    mycursor.execute("SELECT * FROM Pokemon WHERE id = %s", (pokemon_id,))
    pokemon = mycursor.fetchone()
    if not pokemon:
        return f"Pokemon with ID {pokemon_id} not found.", 404

    if request.method == "POST":
      p_id = request.form.get("ID")
      p_name = request.form.get("Name", "").capitalize()
      p_hp = request.form.get("base_hp")
      p_type = request.form.get("Type", "").lower()
      p_evolution = request.form.get("Evolution", "").lower()
      update_fields = {}
      if p_id and p_id.isdigit() and int(p_id) != pokemon_id and int(p_id) > 0:
          update_fields["id"] = int(p_id)
      if p_name:
          update_fields["name"] = p_name
      if p_hp and p_hp.isdigit():
          update_fields["base_hp"] = int(p_hp)
      if p_type:
          update_fields["type"] = p_type
      if p_evolution:
          update_fields["evolution"] = p_evolution
      
      for key, value in update_fields.items():
        if value:
            query = (f"UPDATE Pokemon SET {key}=%s WHERE id=%s")
            mycursor.execute(query, (value, pokemon_id))
      mydb.commit()
      if "id" in update_fields:
            return redirect(f"/edit/{update_fields['id']}")
      return render_template("edit.html", pokemon=pokemon)
    else:
        return render_template("edit.html", pokemon=pokemon)



"""
CHECKER
"""
if __name__ in "__main__":
  app.run(debug=True)
