from app.main import db
from app.main.model.product import Product
from app.main.model.orderitem import OrderItem

def add_new_order_item(order_item_id, order_id, product_id, quantity, subtotal_ex_tax, tax_total, total):
    orderitem = OrderItem.query.filter_by(order_item_id=order_item_id).first()
    if not orderitem:
        new_order_item = OrderItem(
            order_item_id = order_item_id,
            order_id = order_id,
            product_id = product_id,
            quantity = quantity,
            subtotal_ex_tax = subtotal_ex_tax,
            tax_total = tax_total,
            total = total
        )
        save_changes(new_order_item)
        response_object = {
            'status': 'success',
            'message': 'successfully add new order.',
            'order': {
                "order_item_id" : new_order_item.order_item_id,
                "order_id" : new_order_item.order_id,
                "product_id" : new_order_item.product_id,
                "quantity" : new_order_item.quantity,
                "subtotal_ex_tax" : new_order_item.subtotal_ex_tax,
                "tax_total" : new_order_item.tax_total,
                "total" : new_order_item.total
            }
        }
        return response_object, 200
    else:
        response_object = {
            'status': 'fail',
            'message': 'Order already exists.',
        }
        return response_object, 403

def save_changes(data: OrderItem):
    db.session.add(data)
    db.session.commit()