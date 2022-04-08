import uuid
from flask import request
from app.main import db
from app.main.model.cart import Cart
from app.main.model.cartitem import CartItem
from typing import Dict
from app.main.model.product import Product

def add_new_cart_item(cart_id, data: Dict[str, str]):
    cart_item_id=str(uuid.uuid4())
    cart_id = cart_id
    product_id=data['product_id']
    quantity=int(data['quantity'])
    product = Product.query.filter_by(product_id = data['product_id']).first()
    subtotal_ex_tax=product.price*quantity
    tax_total = subtotal_ex_tax*10/100
    total = subtotal_ex_tax+tax_total
    new_card_item = CartItem(
        cart_item_id=cart_item_id,
        cart_id=cart_id,
        product_id=product_id,
        quantity=quantity,
        subtotal_ex_tax=subtotal_ex_tax,
        tax_total=tax_total,
        total=total
    )
    save_changes(new_card_item)
    response_object = {
            'status': 'success',
            'message': 'successfully add new cart item.',
            'data': {
                "cart_item_id": new_card_item.cart_item_id,
                "cart_id": new_card_item.cart_id,
                "product_id": new_card_item.product_id,
                "quantity": new_card_item.quantity,
                "subtotal_ex_tax": new_card_item.subtotal_ex_tax,
                "tax_total": new_card_item.tax_total,
                "total": new_card_item.total
            }
        }
    return response_object, 200

def change_quantity(data: Dict[str, str], cart_item_id):
    cart_item = CartItem.query.filter_by(cart_item_id=cart_item_id).first()   
    if not cart_item:
        response_object = {
            'status': 'fail',
            'message': 'Cart item name does not exists.',
        }
        return response_object, 403
    else:
        product = Product.query.filter_by(product_id=cart_item.product_id).first()
        cart_item.quantity = data['quantity']
        cart_item.subtotal_ex_tax = product.price * cart_item.quantity
        cart_item.tax_total = cart_item.subtotal_ex_tax * 10/100
        cart_item.total = cart_item.subtotal_ex_tax + cart_item.tax_total
        db.session.commit()
        

        cart = Cart.query.filter_by(cart_id=cart_item.cart_id).first()
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

        cart.quantity = quantity
        cart.subtotal_ex_tax = subtotal_ex_tax
        cart.tax_total = tax_total
        cart.total = total
        db.session.commit()

        response_object = {
            'status': 'successfully',
            'message': 'change quantity of cart item successfully.',
            'cart_item': {
                "card_id": cart_item.cart_id,
                "product_id": cart_item.product_id,
                "quantity": cart_item.quantity,
                "subtotal_ex_tax": cart_item.subtotal_ex_tax,
                "tax_total": cart_item.tax_total,
                "total": cart_item.total
            }
        }

        return response_object, 200


def delete_cart_item(cart_item_id):
    cart_item = CartItem.query.filter_by(cart_item_id=cart_item_id).first()   
    if not cart_item:
        response_object = {
            'status': 'fail',
            'message': 'Cart item name does not exists.',
        }
        return response_object, 409  
    else:
        db.session.delete(cart_item)
        db.session.commit()
        all_cart_item = CartItem.query.filter_by(cart_id = cart_item.cart_id).all()
        cart = Cart.query.filter_by(cart_id=cart_item.cart_id).first()
        quantity = 0
        subtotal_ex_tax = 0
        tax_total = 0
        total = 0

        for cart_item_id in all_cart_item:
            cart_item_id = str(cart_item_id)
            cart_item_tmp = CartItem.query.filter_by(cart_item_id = cart_item_id).first()
            quantity += cart_item_tmp.quantity
            subtotal_ex_tax += cart_item_tmp.subtotal_ex_tax
            tax_total += cart_item_tmp.tax_total
            total += cart_item_tmp.total

        cart.quantity = quantity
        cart.subtotal_ex_tax = subtotal_ex_tax
        cart.tax_total = tax_total
        cart.total = total
        db.session.commit()

        response_object = {
            'status': 'successfully',
            'message': 'delete cart item successfully.',
        }

        cart_item = CartItem.query.filter_by(cart_id=cart.cart_id).first()   
        if not cart_item:
            db.session.delete(cart)
            db.session.commit()

        return response_object, 200


def save_changes(data: CartItem):
    db.session.add(data)
    db.session.commit()