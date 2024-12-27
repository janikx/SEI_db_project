"""
BASIC IMPORT
"""
import mysql.connector
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password=""
)
mycursor = mydb.cursor()



"""
CREATE DATABASE
"""
mycursor.execute("CREATE DATABASE pokemon_app_db")
mydb.database = "pokemon_app_db"

create_table_query = """
CREATE TABLE Pokemon (
    pokemon_id INT UNIQUE NOT NULL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    base_hp INT NOT NULL,
    base_atk INT NOT NULL,
    type VARCHAR(20),
    evolution VARCHAR(50)
);
"""
mycursor.execute(create_table_query)



"""
CREATE TABLE AND INSERT DATA
"""
pokemon_data = [
    (1, 'Bulbasaur', 45, 49, 'Grass/Poison', 'Base'),
    (2, 'Ivysaur', 60, 62, 'Grass/Poison', 'Stage 1'),
    (3, 'Venusaur', 80, 82, 'Grass/Poison', 'Stage 2'),
    (4, 'Charmander', 39, 52, 'Fire', 'Base'),
    (5, 'Charmeleon', 58, 64, 'Fire', 'Stage 1'),
    (6, 'Charizard', 78, 84, 'Fire/Flying', 'Stage 2'),
    (7, 'Squirtle', 44, 48, 'Water', 'Base'),
    (8, 'Wartortle', 59, 63, 'Water', 'Stage 1'),
    (9, 'Blastoise', 79, 83, 'Water', 'Stage 2'),
    (10, 'Pikachu', 35, 55, 'Electric', 'Base'),
    (11, 'Raichu', 60, 90, 'Electric', 'Stage 1')
]
insert_query = """
INSERT INTO pokemon (pokemon_id, name, base_hp, base_atk, type, evolution)
VALUES (%s, %s, %s, %s, %s, %s)
"""
mycursor.executemany(insert_query, pokemon_data)
mydb.commit()



"""
APP FUNCTIONS
"""
### CREATE
def InsertPokemon():
  p_id = mycursor.lastrowid + 1
  p_name = input("Name: ")
  p_hp = int(input("Base HP: "))
  p_atk = int(input("Base ATK: "))
  p_type = input("Type: ")
  p_evolution = input("Evolution stage: ")
  insert_query = """
  INSERT INTO pokemon (p_id, p_name, p_hp, p_atk, p_type, p_evolution)
  VALUES (%s, %s, %s, %s, %s, %s)
  """
  mycursor.execute(insert_query)
  mydb.commit()

### READ
def FilterPokemon():
  filter_base = input("How do you want to filter Pokemon? > ") # bude sa dat vybrat podla coho filtrovat
  filter_options = ["Name A-Z", "Name Z-A", "Letter in name", "HP", "ATK", "Type", "Evolution stage"]

### UPDATE
def EditPokemon():
  pass

### DELETE
def DeletePokemon():
  pass



"""
CHECKER
"""
mycursor.execute("SHOW TABLES")
print("Tables in 'pokemon_app_db':")
for table in mycursor:
    print(table)

mycursor.execute("SELECT * FROM pokemon")
print("Inserted Pokémon:")
for row in mycursor:
    print(row)
