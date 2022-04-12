from .. import db

class Product(db.Model):
    __tablename__ = 'product'

    product_id = db.Column(db.String(100),  primary_key=True, unique=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=True)
    price = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "<Product '{}'>".format(self.name)
