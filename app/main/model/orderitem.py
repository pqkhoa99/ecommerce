from .. import db

class OrderItem(db.Model):
    __tablename__ = 'orderitem'

    order_item_id = db.Column(db.String(100), primary_key=True)
    order_id = db.Column(db.String(100), db.ForeignKey('order.order_id'))
    product_id = db.Column(db.String(100), db.ForeignKey('product.product_id'))
    quantity = db.Column (db.Integer, default=0)
    subtotal_ex_tax = db.Column(db.Float, default=0)
    tax_total = db.Column(db.Float, default=0)
    total = db.Column(db.Float, default=0)

    def __repr__(self):
        return (self.order_item_id)