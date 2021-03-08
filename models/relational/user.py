from db import db


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    age = db.Column(db.String(80))
    height = db.Column(db.String(80))
    weight = db.Column(db.String(80))
    status = db.Column(db.String(80))
    favSport = db.Column(db.String(80))
    isAthlete = db.Column(db.Boolean)

    def __init__(self, username, password,age, height, weight, status, favSport, isAthlete):
        self.username = username
        self.password = password
        self.age = age
        self.height = height
        self.weight = weight
        self.status = status
        self.favSport = favSport
        self.isAthlete = isAthlete

    def json(self):
        return {
            'id': self.id,
            'username': self.username,
            'age': self.age,
            'height': self.height,
            'weight': self.weight,
            'status': self.status,
            'favSport': self.favSport,
            'isAthlete': self.isAthlete,
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
