# imports
from flask import Flask, render_template, request, redirect
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy



"""
APP BASE
"""
app = Flask(__name__)
Scss(app)

# db creation
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///pokemon_db.db"
pokemon_db = SQLAlchemy(app)

# Model for one row
class Pokemon(pokemon_db.Model):
  p_name = pokemon_db.Column(pokemon_db.String(100))
  p_id = pokemon_db.Column(pokemon_db.Integer, primary_key=True)
  p_type = pokemon_db.Column(pokemon_db.String(50))
  p_hp = pokemon_db.Column(pokemon_db.Integer)
  p_evolution = pokemon_db.Column(pokemon_db.String(50))

  def __repr__(self) -> str:
    return f"Pokemon #{self.p_id}"



"""
MAIN PAGE
"""
@app.route("/",methods=["POST","GET"])
def index():
  # add pokemon
  if request.method == "POST":
    pokemon_name = request.form["Name"]
    pokemon_type = request.form["Type"]
    pokemon_hp = int(request.form["Base HP"])
    pokemon_ev = request.form["Evolution stage"]
    new_pokemon = Pokemon(p_name=pokemon_name, p_type=pokemon_type, p_hp=pokemon_hp, p_evolution=pokemon_ev)
    try:
      pokemon_db.session.add(new_pokemon)
      pokemon_db.session.commit()
      return redirect("/")
    except Exception as e:
      print(f"ERROR:{e}")
      return f""
  # see all pokemons
  else:
    pokemons = Pokemon.query.order_by(Pokemon.p_id).all()
    return render_template("index.html", pokemons=pokemons)



"""
SECONDARY PAGE
"""
# delete pokemon
@app.route("/delete/<int:id>")
def delete(id:int):
  del_pokemon = Pokemon.query.get_or_404(id)
  try:
    pokemon_db.session.delete(del_pokemon)
    pokemon_db.session.commit()
    return redirect("/")
  except Exception as e:
      print(f"ERROR:{e}")
      return f""
  
# update pokemon
@app.route("/edit/<int:id>",methods=["POST","GET"])
def edit(id:int):
  pokemon = Pokemon.query.get_or_404(id)
  if request.method == "POST":
    pokemon.p_name = request.form["Name"]
    try:
      pokemon_db.session.commit()
      return redirect("/")
    except Exception as e:
      print(f"ERROR:{e}")
      return f""
  else:
    return render_template("edit.html", pokemon=pokemon)



"""
START this shit
"""
if __name__ in "__main__":
  with app.app_context():
    pokemon_db.create_all()
  app.run(debug=True)
