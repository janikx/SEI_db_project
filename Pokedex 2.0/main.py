
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

### READ
def show_pokemon(order: str, filters={}):
    conditions = []
    parameters = []

    # Add type filters
    if "filter_type" in filters and filters["filter_type"]:
      type_conditions = " OR ".join(["type LIKE %s"] * len(filters["filter_type"]))
      conditions.append(f"({type_conditions})")
      parameters.extend([f"%{t}%" for t in filters["filter_type"]])


    # Add stage filters
    if "filter_stage" in filters and filters["filter_stage"]:
      type_conditions = " OR ".join(["evolution LIKE %s"] * len(filters["filter_stage"]))
      conditions.append(f"({type_conditions})")
      parameters.extend([f"%{t}%" for t in filters["filter_stage"]])

    # Add HP filter
    if "filter_hp" in filters and filters["filter_hp"]:
        conditions.append("base_hp >= %s")
        parameters.append(filters["filter_hp"])

    # Add name filter
    if "filter_name" in filters and filters["filter_name"]:
        conditions.append("name LIKE %s")
        parameters.append(f"%{filters['filter_name']}%")

    filter_query = "WHERE " + " AND ".join(conditions) if conditions else ""
    query = f"SELECT * FROM Pokemon {filter_query} ORDER BY {order}"
    mycursor.execute(query, parameters)
    return mycursor.fetchall()

def order_pokemon(order_base:str):
  if order_base == "NameAsc":   # Name A-Z
      return show_pokemon("name ASC")
  elif order_base == "NameDesc":   # Name Z-A
      return show_pokemon("name DESC")
  elif order_base == "HPAsc":   # HP asc
      return show_pokemon("base_hp ASC")
  elif order_base == "HPDesc":   # HP desc
      return show_pokemon("base_hp DESC")
  elif order_base == "TypeAsc":   # Type A-Z
      return show_pokemon("type ASC")
  elif order_base == "TypeDesc":   # Type Z-A
      return show_pokemon("type DESC")
  elif order_base == "EvolutionStage":   # Evolution
      return show_pokemon("evolution ASC")
  else:
      return show_pokemon("id ASC")


"""
MAIN PAGE
"""
@app.route("/", methods=["POST","GET","FILTER"])
def index():
    if request.method == "POST":
        p_name = request.form["Name"]
        p_type = request.form["Type"]
        p_hp = int(request.form["base_hp"])
        p_evolution = request.form["Evolution"]
        insert_pokemon(p_name, p_type, p_hp, p_evolution)
        return redirect("/")
    if request.method == "GET":
      filters = {
            "filter_type": request.args.getlist("filter_type"),
            "filter_stage": request.args.getlist("filter_stage"),
            "filter_hp": request.args.get("filter_hp", type=int),
            "filter_name": request.args.get("filter_name", ""),
        }
      order_base = request.args.get("order", "ID")
      pokemons = show_pokemon(order_base, filters)
      return render_template("index.html", pokemons=pokemons, order_base=order_base, **filters)
    else:
        pokemons = order_pokemon("")
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
