from flask import request
from flask_restx import Resource
from app.main.service.cart_service import add_new_cart, checkout_cart

from app.main.util.decorator import admin_token_required
from ..util.dto import CartDto
from typing import Dict


api = CartDto.api
_cart = CartDto.cart

@api.route('/add')
class Cart(Resource):
    @admin_token_required
    @api.expect(_cart, validate=True)
    @api.doc(responses={
        200: 'Success',
        400: 'Bad Request',
        403: 'Forbidden'
    })
    @api.doc('create a new cart')
    @admin_token_required
    def post(self):
        """Creates a new Cart """
        data = request.json
        return add_new_cart(data=data)


@api.route('/checkout')
class CartCheckout(Resource):
    @admin_token_required
    @api.doc(responses={
        200: 'Success',
        400: 'Bad Request',
        403: 'Forbidden'
    })
    @api.doc('checkout a cart')
    @admin_token_required
    def post(self):
        """Checkout a Cart """
        data = request.json
        return checkout_cart(data=data)