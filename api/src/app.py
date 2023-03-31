import os
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from models import db, User, Profile
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')

db.init_app(app)
Migrate(app, db) # db init, db migrate, db upgrade, db downgrade
CORS(app)

@app.route('/')
def main():
    return jsonify({
        "message": "API REST WITH FLASK AND MYSQL"
    }), 200


@app.route('/users', methods=['GET', 'POST'])
def obtener_crear_users():
    if request.method == 'GET':
        users = User.query.all()
        users = list(map(lambda user: user.serialize_with_profile(), users))
        return jsonify(users)

    if request.method == 'POST':
        # Datos de la tabla "users"
        username = request.json.get('username')
        password = request.json.get('password')
        is_active = request.json.get('is_active', True)
        ## Datos de la tabla "profiles"
        biography = request.json.get('biography', "")
        github = request.json.get('github', "")
        linkedin = request.json.get('linkedin', "")
        instagram = request.json.get('instagram', "")

        """ 
        user = User()
        user.username = username
        user.password = generate_password_hash(password)
        user.is_active = is_active
        user.save()

        profile = Profile()
        profile.biography = biography
        profile.github = github
        profile.linkedin = linkedin
        profile.instagram = instagram
        profile.users_id = user.id
        profile.save() 
        """

        user = User()
        user.username = username
        user.password = generate_password_hash(password)
        user.is_active = is_active

        profile = Profile()
        profile.biography = biography
        profile.github = github
        profile.linkedin = linkedin
        profile.instagram = instagram

        # usando el relationship para crear el usuario con su perfil
        user.profile = profile
        user.save()

        return jsonify(user.serialize_with_profile()), 201


if __name__ == '__main__':
    app.run()
