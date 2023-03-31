from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    is_active = db.Column(db.Boolean(), default=True)
    profile = db.relationship('Profile', uselist=False, backref="user") # [<Profile 1>] => <Profile 1>

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