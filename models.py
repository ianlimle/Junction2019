from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Product(db.Model):

    __tablename__ = 'skincare'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.String(500), unique=True, nullable=False)
    category_id = db.Column(db.Integer)
    product_id = db.Column(db.String(100), nullable=False)
    picture = db.Column(db.String(500), unique=True)
    url = db.Column(db.String(500), unique=True)
    price = db.Column(db.Integer)
    currency_id = db.Column(db.Integer)
    condition = db.Column(db.String(100), nullable=True)
    severity = db.Column(db.String(10), nullable=True)


    @classmethod
    def find_by_severity(cls, severity):
        return cls.query.filter_by().all()

    def serialize(self):
        return dict(
            id = self.id,
            name = self.description,
            price = self.price,
            picture = self.picture,
            ingredients = "Beetroot, Carrot, Hummus"
        )

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()