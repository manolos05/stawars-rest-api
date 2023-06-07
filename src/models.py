from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    fav= db.relationship("Fav_Planet", lazy=True)
    fav1= db.relationship("Fav_People", lazy=True)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Planet(db.Model):
    __tablename__ = 'planets'
    planet_id = db.Column(db.Integer, primary_key=True)
    name_planet = db.Column(db.String(120), unique=True, nullable=False)
    population = db.Column(db.String(80), unique=False, nullable=False)
    climate = db.Column(db.String(80), unique=False, nullable=False)
    fav= db.relationship("Fav_Planet", lazy=True)

    def __repr__(self):
        return '<Planet %r>' % self.planets

    def serialize(self):
        return {
            "name_planet": self.name_planet,
            "population": self.population,
            "climate": self.climate,
        }

class People(db.Model):
    __tablename__ = 'peoples'
    characeteres_id = db.Column(db.Integer, primary_key=True)
    name_people = db.Column(db.String(120), unique=True, nullable=False)
    age = db.Column(db.String(80), unique=False, nullable=False)
    born_date = db.Column(db.String(80), unique=False, nullable=False)


    def __repr__(self):
        return '<People %r>' % self.peoples

    def serialize(self):
        return {
            'name_people': self.name_people,
            'age': self.age,
            'born_date': self.born_date,
        }

class Fav_Planet(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), primary_key=True)
    planet_id =db.Column(db.Integer, db.ForeignKey(Planet.planet_id), primary_key=True)
    
    def __repr__(self):
        return '<Fav_Planet %r>' % self.user_id


    def serialize(self):
        return {
            "user_id": self.user_id,
            "planet_id": self.planet_id,
        }

class Fav_People(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), primary_key=True)
    characeteres_id =db.Column(db.Integer, db.ForeignKey(People.characeteres_id), primary_key=True)
    
    def __repr__(self):
        return '<Fav_People %r>' % self.user_id


    def serialize(self):
        return {
            "user_id": self.user_id,
            "characeteres_id": self.characeteres_id,
        }

