from flask import request
from flask_restx import Resource
from app.main.service.cartitem_service import change_quantity,delete_cart_item

from app.main.util.decorator import admin_token_required
from ..util.dto import CartItemDto
from typing import Dict

api = CartItemDto.api
_cartitem = CartItemDto.cartitem

@api.route('/<cart_item_id>/changeqty')
class CartItem(Resource):
    @admin_token_required
    @api.expect(_cartitem, validate=True)
    @api.doc(responses={
        200: 'Success',
        400: 'Bad Request',
        403: 'Forbidden'
    })
    @api.doc('change quantity a cart item')
    @admin_token_required
    def put(self, cart_item_id):
        """Change quantity a cart item"""
        data = request.json
        return change_quantity(data=data, cart_item_id=cart_item_id)

@api.route('/<cart_item_id>/')
class CartItem(Resource):
    @api.doc('delete_cart_item')
    @admin_token_required
    @api.doc(responses={
        200: 'Success',
        400: 'Bad Request',
        403: 'Forbidden'
    })
    @admin_token_required
    def delete(self, cart_item_id):
        """Delete a cart item"""
        data = request.json
        return delete_cart_item(cart_item_id=cart_item_id)