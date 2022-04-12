import uuid
from flask import request
from app.main import db
from app.main.model.cart import Cart
from app.main.model.order import Order
from app.main.model.orderitem import OrderItem
from typing import Dict
from app.main.model.cartitem import CartItem
from app.main.service.auth_helper import Auth
from app.main.model.user import User
from app.main.model.product import Product
from app.main.service.cartitem_service import add_new_cart_item, delete_cart_item
from app.main.service.order_service import add_new_order
from app.main.service.orderitem_service import add_new_order_item

def add_new_cart(data: Dict[str, str]):
    auth_token = request.headers.get('Authorization')
    if auth_token:
        user_id = User.decode_auth_token(auth_token)
    cart = Cart.query.filter_by(user_id=user_id).first()

    if cart:
        product = Product.query.filter_by(product_id=data['product_id']).first()
        cart_item = CartItem.query.filter_by(cart_id = cart.cart_id, product_id=data['product_id']).first()
        if cart_item:
            cart_item.quantity = cart_item.quantity + data['quantity']
            cart_item.subtotal_ex_tax = product.price * cart_item.quantity
            cart_item.tax_total = cart_item.subtotal_ex_tax * 10/100
            cart_item.total = cart_item.subtotal_ex_tax + cart_item.tax_total
            db.session.commit()
            all_cart_item = CartItem.query.filter_by(cart_id = cart.cart_id).all()
            
            list_cart_item = []
            quantity = 0
            subtotal_ex_tax = 0
            tax_total = 0
            total = 0

            for cart_item_id in all_cart_item:
                cart_item_id = str(cart_item_id)
                cart_item_tmp = CartItem.query.filter_by(cart_item_id = cart_item_id).first()
                cart_item_dict = {
                    "cart_item_id": cart_item_tmp.cart_item_id,
                    "card_id": cart_item_tmp.cart_id,
                    "product_id": cart_item_tmp.product_id,
                    "quantity": cart_item_tmp.quantity,
                    "subtotal_ex_tax": cart_item_tmp.subtotal_ex_tax,
                    "tax_total": cart_item_tmp.tax_total,
                    "total": cart_item_tmp.total
                }
                list_cart_item.append(cart_item_dict)
                quantity += cart_item_tmp.quantity
                subtotal_ex_tax += cart_item_tmp.subtotal_ex_tax
                tax_total += cart_item_tmp.tax_total
                total += cart_item_tmp.total

            update_cart(user_id, quantity, subtotal_ex_tax, tax_total, total)

            response_object = {
                'status': 'success',
                'message': 'Cart already exists. Update cart and cart item successfully.',
                'card': {
                    "cart_item_id": cart_item_tmp.cart_item_id,
                    "card_id": cart.cart_id,
                    "user_id": cart.user_id,
                    "quantity": quantity,
                    "cart_item": list_cart_item,
                    "subtotal_ex_tax" : subtotal_ex_tax,
                    "tax_total" : tax_total,
                    "total" : total
                }
            }
            return response_object, 200
            
        else:
            data_cartitem_response = add_new_cart_item(cart.cart_id, data)
            all_cart_item = CartItem.query.filter_by(cart_id = cart.cart_id).all()

            list_cart_item = []
            quantity = 0
            subtotal_ex_tax = 0
            tax_total = 0
            total = 0

            for cart_item_id in all_cart_item:
                cart_item_id = str(cart_item_id)
                cart_item_tmp = CartItem.query.filter_by(cart_item_id = cart_item_id).first()
                cart_item_dict = {
                    "cart_item_id": cart_item_tmp.cart_item_id,
                    "card_id": cart_item_tmp.cart_id,
                    "product_id": cart_item_tmp.product_id,
                    "quantity": cart_item_tmp.quantity,
                    "subtotal_ex_tax": cart_item_tmp.subtotal_ex_tax,
                    "tax_total": cart_item_tmp.tax_total,
                    "total": cart_item_tmp.total
                }
                list_cart_item.append(cart_item_dict)
                quantity += cart_item_tmp.quantity
                subtotal_ex_tax += cart_item_tmp.subtotal_ex_tax
                tax_total += cart_item_tmp.tax_total
                total += cart_item_tmp.total

            update_cart(user_id, quantity, subtotal_ex_tax, tax_total, total)

            response_object = {
                'status': 'success',
                'message': 'successfully add new cart item.',
                'card': {
                    "card_id": cart.cart_id,
                    "user_id": cart.user_id,
                    "quantity": quantity,
                    "cart_item": list_cart_item,
                    "subtotal_ex_tax" : subtotal_ex_tax,
                    "tax_total" : tax_total,
                    "total" : total
                }
            }
            return response_object, 200
        
    else:
        product = Product.query.filter_by(product_id=data['product_id']).first()
        quantity = data['quantity']
        subtotal_ex_tax = product.price * quantity
        tax_total = subtotal_ex_tax*10/100
        total = subtotal_ex_tax + tax_total
        cart_id=str(uuid.uuid4())
        new_cart = Cart(
            cart_id=cart_id,
            user_id=user_id,
            quantity=data['quantity'],
            subtotal_ex_tax=subtotal_ex_tax,
            tax_total=tax_total,
            total=total
        )
        save_changes(new_cart)
        data_cartitem_response = add_new_cart_item(cart_id, data)
        data_cartitem = data_cartitem_response[0]
        cartitem = data_cartitem['data']
        response_object = {
                'status': 'success',
                'message': 'successfully add new cart.',
                'card': {
                    "card_id": new_cart.cart_id,
                    "user_id": new_cart.user_id,
                    "quantity": new_cart.quantity,
                    "cart_item": cartitem,
                    "subtotal_ex_tax" : new_cart.subtotal_ex_tax,
                    "tax_total" : new_cart.tax_total,
                    "total" : new_cart.total
                }
            }
        return response_object, 200


def update_cart(user_id, quantity, subtotal_ex_tax, tax_total, total):
    cart = Cart.query.filter_by(user_id=user_id).first()
    cart.quantity = quantity
    cart.subtotal_ex_tax = subtotal_ex_tax
    cart.tax_total = tax_total
    cart.total = total
    db.session.commit()


def save_changes(data: Cart):
    db.session.add(data)
    db.session.commit()


def checkout_cart(data):
    auth_token = request.headers.get('Authorization')
    if auth_token:
        user_id = User.decode_auth_token(auth_token)
    cart = Cart.query.filter_by(user_id=user_id).first()

    if cart:
        list_cart_item = CartItem.query.filter_by(cart_id=cart.cart_id).all()
        add_new_order(
            order_id = cart.cart_id,
            user_id = cart.user_id,
            quantity = cart.quantity,
            subtotal_ex_tax = cart.subtotal_ex_tax,
            tax_total = cart.tax_total,
            total = cart.total
        )

        for cart_item in list_cart_item:
            add_new_order_item(
                order_item_id = cart_item.cart_item_id,
                order_id = cart_item.cart_id,
                product_id = cart_item.product_id,
                quantity = cart_item.quantity,
                subtotal_ex_tax = cart_item.subtotal_ex_tax,
                tax_total = cart_item.tax_total,
                total = cart_item.total
            )
        


        order = Order.query.filter_by(order_id=cart.cart_id).first()
        all_order_item = OrderItem.query.filter_by(order_id=order.order_id).all()
        list_order_item = []
        for order_item in all_order_item:
            order_item_dict = {
                "order_item_id": order_item.order_item_id,
                "order_id": order_item.order_id,
                "product_id": order_item.product_id,
                "quantity": order_item.quantity,
                "subtotal_ex_tax": order_item.subtotal_ex_tax,
                "tax_total": order_item.tax_total,
                "total": order_item.total
            }
            list_order_item.append(order_item_dict)

        response_object = {
                'status': 'success',
                'message': 'successfully checkout cart.',
                'order': {
                    'order_id': order.order_id,
                    'user_id': order.user_id,
                    'quantity': order.quantity,
                    'order_item': list_order_item,
                    'subtotal_ex_tax': order.subtotal_ex_tax,
                    'tax_total': order.tax_total,
                    'total': order.total,
                    'payment_status': order.payment_status
                }
            }

        for cart_item in list_cart_item:
            delete_cart_item(cart_item.cart_item_id)

        db.session.delete(cart)
        db.session.commit()

        return response_object, 200

    else:
        response_object = {
            'status': 'fail',
            'message': 'cart does not exist.',
        }

        return response_object, 403

        

