from .. import db

class Order(db.Model):
    __tablename__ = 'order'

    order_id = db.Column(db.String(100), primary_key=True)
    user_id = db.Column(db.String(100), db.ForeignKey('user.public_id'))
    quantity = db.Column(db.Integer, default = 0)
    order_items = db.relationship('OrderItem', backref='order', lazy='dynamic')
    subtotal_ex_tax = db.Column(db.Float, default=0)
    tax_total = db.Column(db.Float, default=0)
    total = db.Column(db.Float, default=0)
    payment_status = db.Column(db.String(100), default='INIT')

    def __repr__(self):
        return "<Order '{}'>".format(self.order_id)
