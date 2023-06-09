"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, abort
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planet, Fav_Planet, Fav_People
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():
    users = User.query.all()
    result = []
    for user in users: result.append({
    'id': user.id,
    'email': user.email
    })
    return jsonify(result)

@app.route('/user', methods=['POST'])
def create_new_user():
    new = User(
        email= request.json['email'],
        password = request.json['password'],
        is_active= request.json['is_active'],
    )
    db.session.add(new)
    db.session.commit()
    return jsonify(new.serialize()), 200


@app.route('/people', methods=['POST'])
def create_new_people():
    new = People(
        name_people = request.json['name_people'],
        age= request.json['age'],
        born_date= request.json['born_date'],
    )
    db.session.add(new)
    db.session.commit()
    return jsonify(new.serialize()), 200

@app.route('/planet', methods=['POST'])
def create_new_planet():
    new = Planet(
        name_people = request.json['name_people'],
        age= request.json['age'],
        born_date= request.json['born_date'],
    )
    db.session.add(new)
    db.session.commit()
    return jsonify(new.serialize()), 200

@app.route('/user/<string:user_id>', methods=['PUT'])
def edit_user(user_id):
    editUser = User.query.get(user_id)
    if editUser is None:
        abort(404)
    editUser.email = request.json['email']
    db.session.commit()

    return (jsonify(editUser.serialize()))

    
@app.route('/people', methods=['GET'])
def handle_people():
    peoples = People.query.all()    
    result = list(map(lambda user:user.serialize(),peoples))
    return jsonify(result)

@app.route('/people/<string:people_id>', methods=['GET'])
def get_people(people_id):
    peopl = People.query.get(people_id)
    if peopl is None:
        abort(404)
    return jsonify(peopl.serialize())

@app.route('/planet', methods=['GET'])
def handle_planet():
    planets = Planet.query.all()
    result = []
    for plant in planets: result.append({
    'planet_id': plant.planet_id,
    'name_planet': plant.name_planet,
    'population': plant.population,
    'climate': plant.climate,
    })
    return jsonify(result)


@app.route('/planet/<string:planet_id>', methods=['GET'])
def get_planet(planet_id):
    plant = Planet.query.get(planet_id)
    if plant is None:
        abort(404)
    return jsonify(plant.serialize())

#Post

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def post_fav_planet(planet_id):
    fav = planet_id
    favorite = Fav_Planet(
        user_id = request.json["user_id"],
        planet_id= fav
    ) 
    db.session.add(favorite)
    db.session.commit()
    
    return jsonify(favorite.serialize()), 200



@app.route('/favorite/people/<int:characeteres_id>', methods=['POST'])
def post_fav_people(characeteres_id):
    fav = characeteres_id
    favorite = Fav_People(
        user_id = request.json["user_id"],
        characeteres_id= fav
    ) 
    db.session.add(favorite)
    db.session.commit()

    return jsonify(favorite.serialize()), 200

#delete

@app.route('/user/favorites/<int:user_id>/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(user_id, planet_id):
    favorite = Fav_Planet.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if favorite is None:
        return jsonify({'error': 'Favorite planet not found for the user'}), 404

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({'message': 'Favorite planet deleted successfully'})

@app.route('/user/favorites/<int:user_id>/people/<int:characeteres_id>', methods=['DELETE'])
def delete_favorite_people(user_id, characeteres_id):
    favorite = Fav_People.query.filter_by(user_id=user_id, characeteres_id=characeteres_id).first()
    if favorite is None:
        return jsonify({'error': 'Favorite planet not found for the user'}), 404

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({'message': 'Favorite planet deleted successfully'})

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
