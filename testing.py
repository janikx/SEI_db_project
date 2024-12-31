
import mysql.connector
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="pokemon_app_db"
)
mycursor = mydb.cursor()



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
#     ('Bulbasaur', 60, 'grass/poison', 'base'),
#     ('Ivysaur', 90, 'grass/poison', 'stage 1'),
#     ('Venusaur', 250, 'grass/poison', 'stage 2'),
#     ('Charmander', 60, 'fire', 'base'),
#     ('Charmeleon', 90, 'fire', 'stage 1'),
#     ('Charizard', 220, 'fire/flying', 'stage 2'),
#     ('Squirtle', 60, 'water', 'base'),
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
def InsertPokemon():
  p_name = (input("Name > ")).capitalize()
  p_hp = int(input("Base HP > "))
  p_type = (input("Type > ")).lower()
  p_evolution = (input("Evolution stage > ")).lower()
  insert_query = """
  INSERT INTO pokemon (name, base_hp, type, evolution)
  VALUES (%s, %s, %s, %s)
  """
  insert_values = (p_name, p_hp, p_type, p_evolution)
  mycursor.execute(insert_query, insert_values)
  mydb.commit()
  print(f"Pokemon '{p_name}' succesfully added to pokedex.")

### READ
def ShowPokemon(filter: str):
  mycursor.execute("SELECT * FROM Pokemon " + f"{filter}")
  all_pokemons = mycursor.fetchall()
  print(all_pokemons)

def FilterPokemon():
  filter_base = int(input("How do you want to filter Pokemon? (1-8) > "))
  # Name A-Z
  if filter_base == 1:
    ShowPokemon("ORDER BY name ASC")
  # Name Z-A
  elif filter_base == 2:
    ShowPokemon("ORDER BY name DESC")
  # Letter in name
  elif filter_base == 3:
    must_have_str = input("What does the name contain? > ")
    ShowPokemon(f"WHERE name LIKE '%{must_have_str.lower()}%'")
  # HP asc
  elif filter_base == 4:
    ShowPokemon("ORDER BY base_hp ASC")
  # HP desc
  elif filter_base == 5:
    ShowPokemon("ORDER BY base_hp DESC")
  # Paticular type
  elif filter_base == 6:
    pokemon_type = input("What type? > ")
    ShowPokemon(f"WHERE type LIKE '%{pokemon_type.lower()}%'")
  # Evolution stage
  elif filter_base == 7:
    pokemon_stage = input("What evolution stage? > ")
    ShowPokemon(f"WHERE evolution LIKE '%{pokemon_stage.lower()}%'")
  # Type asc
  elif filter_base == 8:
    ShowPokemon("ORDER BY type ASC")

### UPDATE
def EditPokemon():
    pokemon = int(input("ID of the pokemon you want to edit > "))
    pokemon_property = input("Which property do you want to edit > ")
    change_property = input("Edit the property > ")
    query = f"UPDATE Pokemon SET {pokemon_property}=%s WHERE id=%s"
    try:
        mycursor.execute(query, (change_property, pokemon))
        mydb.commit()
        print(f"Successfully edited the {pokemon_property} of pokemon with ID {pokemon}.")
    except Exception as e:
        print("An error occurred:", e)

### DELETE
def DeletePokemon():
  del_pokemon = input("Name or ID of the pokemon you want to delete > ")
  if del_pokemon.isdigit() == True:
    del_pokemon = int(del_pokemon)
    mycursor.execute(f"DELETE FROM Pokemon WHERE id={del_pokemon}")
    mydb.commit()
    print(f"Pokemon with ID {del_pokemon} succesfully deleted from pokedex.")
  else:
    mycursor.execute(f"DELETE FROM Pokemon WHERE name = '{del_pokemon}'")
    mydb.commit()
    all_pokemons = mycursor.fetchall()
    for pokemon in all_pokemons:
      print(pokemon)
    print(f"Pokemon '{del_pokemon}' succesfully deleted from pokedex.")
    


"""
CHECKER
"""

ShowPokemon("")
