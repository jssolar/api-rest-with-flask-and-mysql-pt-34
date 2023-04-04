import os
from datetime import datetime
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager, get_jwt_identity, jwt_required, create_access_token
from models import db, User, Profile, Message, Role
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['JWT_SECRET_KEY'] = 'secret-key'

db.init_app(app)
Migrate(app, db) # db init, db migrate, db upgrade, db downgrade
jwt = JWTManager(app)
CORS(app)

@app.route('/')
def main():
    return jsonify({
        "message": "API REST WITH FLASK AND MYSQL"
    }), 200


@app.route('/login', methods=['POST'])
def login():

    username = request.json.get('username')
    password = request.json.get('password')

    if not username:
        return jsonify({ "msg": "Username is required"}), 422

    if not password:
        return jsonify({ "msg": "Password is required"}), 422

    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({ "msg": "Username/Password are incorrects"}), 401

    if not check_password_hash(user.password, password):
        return jsonify({ "msg": "Username/Password are incorrects"}), 401

    # Token con vencimiento 
    # expires = datetime.timedelta(days=3)
    # access_token = create_access_token(identity=user.id, expires_delta=expires)
    
    # Token sin vencimiento
    access_token = create_access_token(identity=user.id)

    data = {
        "access_token": access_token,
        "user": user.serialize_with_profile()
    }

    return jsonify(data), 200


@app.route('/users', methods=['GET', 'POST'])
@jwt_required() # que todas estas rutas o endpoints son privadas
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

        # Datos de la tabla roles
        roles = request.json.get('roles')

        
                

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

        if len(roles) > 0:
            for roles_id in roles:
                role = Role.query.get(roles_id)
                user.roles.append(role)

        # usando el relationship para crear el usuario con su perfil
        user.profile = profile
        user.save()

        return jsonify(user.serialize_with_profile()), 201


@app.route('/messages', methods=['GET', 'POST'])
@app.route('/messages/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def messages(id = None):
    print(datetime.now())
    current_user = get_jwt_identity()

    if request.method == 'GET':
        if id is not None:
            message = Message.query.filter_by(id=id, users_from_id=current_user).first()
            if not message:
                return jsonify({ "msg": "Message not found"}), 404

            return jsonify(message.serialize()), 200
        else:
            messages = Message.query.filter_by(users_from_id=current_user)
            messages = list(map(lambda msg: msg.serialize(), messages))

            return jsonify(messages), 200


    if request.method == 'POST':
        message = request.json.get('message')
        users_from_id = request.json.get('users_from_id')
        users_to_id = request.json.get('users_to_id')

        msg = Message()
        msg.message = message
        msg.users_from_id = users_from_id
        msg.users_to_id = users_to_id

        msg.save()

        return jsonify(msg.serialize()), 201


    if request.method == 'PUT':
        pass

    if request.method == 'DELETE':
        pass

if __name__ == '__main__':
    app.run()
