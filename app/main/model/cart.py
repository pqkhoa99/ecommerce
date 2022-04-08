from .. import db

class Cart(db.Model):
    __tablename__ = 'cart'

    cart_id = db.Column(db.String(100), primary_key=True)
    user_id = db.Column(db.String(100), db.ForeignKey('user.public_id'))
    quantity = db.Column(db.Integer, default = 0)
    cart_items = db.relationship('CartItem', backref='cart', lazy='dynamic')
    subtotal_ex_tax = db.Column(db.Float, default=0)
    tax_total = db.Column(db.Float, default=0)
    total = db.Column(db.Float, default=0)

    def __repr__(self):
        return "<Cart '{}'>".format(self.cart_id)
