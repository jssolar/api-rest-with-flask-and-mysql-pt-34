from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

roles_users = db.Table(
    'roles_users',
    db.Column('roles_id', db.Integer, db.ForeignKey('roles.id'), nullable=False, primary_key=True),
    db.Column('users_id', db.Integer, db.ForeignKey('users.id'), nullable=False, primary_key=True)
)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    is_active = db.Column(db.Boolean(), default=True)
    profile = db.relationship('Profile', uselist=False, backref="user") # [<Profile 1>] => <Profile 1>
    msg_from = db.relationship('Message', foreign_keys="[Message.users_from_id]", backref="user_from")
    msg_to = db.relationship('Message', foreign_keys="[Message.users_to_id]", backref="user_to")
    roles = db.relationship('Role', secondary=roles_users)


    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "is_active": self.is_active
        }

    def serialize_with_profile(self):
        return {
            "id": self.id,
            "username": self.username,
            "is_active": self.is_active,
            "profile": self.profile.serialize()
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    users = db.relationship('User', secondary=roles_users)
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Profile(db.Model):
    __tablename__ = 'profiles'
    id = db.Column(db.Integer, primary_key=True)
    biography = db.Column(db.Text(), default="")
    github = db.Column(db.String(100), default="")
    linkedin = db.Column(db.String(100), default="")
    instagram = db.Column(db.String(100), default="")
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)

    def serialize(self):
        return {
            "id": self.id,
            "biography": self.biography,
            "github": self.github
        }

    def serialize_with_user(self):
        return {
            "id": self.id,
            "biography": self.username,
            "github": self.is_active,
            "username": self.user.serialize(),
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text(), nullable=False)
    users_from_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    users_to_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.DateTime(), default=db.func.now())

    def serialize(self):
        return {
            "id": self.id,
            "message": self.message,
            "users_from_id": self.users_from_id,
            "users_to_id": self.users_to_id,
            "date": self.date,
            "user_from": self.user_from.serialize(),
            "user_to": self.user_to.serialize(),
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
