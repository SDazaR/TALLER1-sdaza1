from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from typing import List
import json
from db.db import db
from models.dog import Dog
from models.dog_sitter import DogSitter
from models.user import User
from flask_login import LoginManager, login_user, login_required
import os

app = Flask(__name__, template_folder="views")

secret_key = os.urandom(24)
app.config["SECRET_KEY"] = secret_key

login_manager = LoginManager(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)

with app.app_context():
    db.create_all()

user_db = [
    User(1, "pperez", "123", True),
    User(2, "lperez", "234", False),
    User(3, "bperez", "345", False)
]

@login_manager.user_loader
def load_user(user_id):
    for user in user_db:
        if user.id == int(user_id):
            return user
    return None

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        username = request.form["username"]
        password = request.form["password"]

        for user in user_db:
            if user.username == username and user.password == password:
                login_user(user)
                print(user)
                if user.is_admin:
                    return redirect(url_for("view_dogs"))
                else:
                    return redirect(url_for("get_home"))
        return redirect(url_for("invalid"))
@app.route("/home")
def get_home():
    return render_template("home.html")

@app.route("/invalid")
def invalid():
    return render_template("invalid.html")

@app.route("/add_sample_data")
def add_sample_data():
    db.session.query(Dog).delete()
    db.session.query(DogSitter).delete()

    dog_sitter1 = DogSitter(name="John Doe", phone="123-456-7890")
    dog_sitter2 = DogSitter(name="Jane Smith", phone="098-765-4321")

    dog1 = Dog(name="Lassie", breed="Golden Retriever", age=3, weight=30.5, dog_sitter=dog_sitter1)
    dog2 = Dog(name="Bella", breed="Labrador", age=4, weight=25.0, dog_sitter=dog_sitter1)
    dog3 = Dog(name="Lassie", breed="German Shepherd", age=5, weight=1.0, dog_sitter=dog_sitter2)

    db.session.add_all([dog_sitter1, dog_sitter2, dog1, dog2, dog3])
    db.session.commit()

    return "Sample data added successfully!"

@app.route("/count_lassie")
def count_lassie():
    lassie_count = db.session.query(Dog).filter(Dog.name == "Lassie").count()
    return f"There are {lassie_count} dogs named Lassie."

@app.route("/view_dogs")
def view_dogs():
    dogs = db.session.query(Dog)
    dogs_data = [
        {
            "id": dog.id,
            "name": dog.name,
            "breed": dog.breed,
            "age": dog.age,
            "weight": dog.weight,
            "id_dog_sitter": dog.id_dog_sitter
        }
        for dog in dogs
    ]
    return render_template("all_dogs.html", dogs=dogs_data)


@app.route("/assign_small_dogs_to_mario")
def assign_small_dogs_to_mario():
    mario = db.session.query(DogSitter).filter(DogSitter.name == "Mario").first()
    if not mario:
        mario = DogSitter(name="Mario", phone="000-000-0000")
        db.session.add(mario)
        db.session.commit()

    small_dogs = db.session.query(Dog).filter(Dog.weight < 3).all()
    for dog in small_dogs:
        dog.dog_sitter = mario

    db.session.commit()
    return f"Assigned {len(small_dogs)} small dogs to Mario."



if __name__ =='__main__':
    app.run(debug=True)

    