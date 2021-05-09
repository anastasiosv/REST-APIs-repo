from db import db


class AddressModel(db.Model):
    __tablename__ = 'Address'

    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(80))
    street = db.Column(db.String(80))
    postalCode = db.Column(db.String(80))
    Country = db.Column(db.String(80))
    County = db.Column(db.String(80))

    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    user = db.relationship('User')


    def __init__(self, city, street,postalCode, Country, County, user_id):
        self.city = city
        self.street = street
        self.postalCode = postalCode
        self.Country = Country
        self.County = County
        self.user_id = user_id


    def json(self):
        return {
            'id': self.id,
            'city': self.city,
            'street': self.street,
            'postal_code': self.postalCode,
            'Country': self.Country,
            'County': self.County,
            'user_id': self.user_id,
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_street(cls, street):
        return cls.query.filter_by(street=street).first()

    @classmethod
    def find_by_city(cls, city):
        return cls.query.filter_by(street=city).first()

    @classmethod
    def find_by_county(cls, county):
        return cls.query.filter_by(street=county).first()


    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
