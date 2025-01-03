
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

username = "Janik4833"
password = "pokemondbpassword"



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

def order_pokemon(order_base: str):
    if order_base == "NameAsc":   # Name A-Z
        return "name ASC"
    elif order_base == "NameDesc":   # Name Z-A
        return "name DESC"
    elif order_base == "HPAsc":   # HP asc
        return "base_hp ASC"
    elif order_base == "HPDesc":   # HP desc
        return "base_hp DESC"
    elif order_base == "TypeAsc":   # Type A-Z
        return "type ASC"
    elif order_base == "TypeDesc":   # Type Z-A
        return "type DESC"
    elif order_base == "EvolutionStage":   # Evolution
        return "evolution ASC"  # Correct column name
    else:
        return "id ASC"



"""
MAIN PAGE
"""
@app.route("/", methods=["POST","GET"])
def index():
    if request.method == "POST":
        p_name = request.form["Name"]
        p_type = request.form["Type"]
        p_secondary_type = request.form["Second Type"]
        p_hp = int(request.form["HP"])
        p_evolution = request.form["Evolution"]
        if p_secondary_type != "":
            p_type = p_type + "/" + p_secondary_type
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
      order = order_pokemon(order_base)
      pokemons = show_pokemon(order, filters)
      pokemons_count = len(pokemons)
      return render_template("index.html", pokemons=pokemons, pokemons_count=pokemons_count, order_base=order_base, **filters)
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
@app.route("/edit/<int:pokemon_id>", methods=["POST", "GET"])
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
        update_fields = []
        update_values = []
        if p_id and p_id.isdigit() and int(p_id) != pokemon_id and int(p_id) > 0:
            update_fields.append("id")
            update_values.append(int(p_id))
        if p_name:
            update_fields.append("name")
            update_values.append(p_name)
        if p_hp and p_hp.isdigit():
            update_fields.append("base_hp")
            update_values.append(int(p_hp))
        if p_type:
            update_fields.append("type")
            update_values.append(p_type)
        if p_evolution:
            update_fields.append("evolution")
            update_values.append(p_evolution)
        if update_fields:
            set_clause = ", ".join([f"{field}=%s" for field in update_fields])
            query = f"UPDATE Pokemon SET {set_clause} WHERE id=%s"
            update_values.append(pokemon_id)
            mycursor.execute(query, tuple(update_values))
            mydb.commit()
        if "id" in update_fields:
            return redirect(f"/edit/{update_values[0]}")
        return redirect(f"/edit/{pokemon_id}")
    return render_template("edit.html", pokemon=pokemon)




"""
CHECKER
"""
if __name__ in "__main__":
  app.run(debug=True)
