from flask import request
from flask_restx import Resource

from app.main.util.decorator import admin_token_required
from ..util.dto import ProductDto
from ..service.product_service import add_new_product, get_all_products, get_a_product, update_a_product
from typing import Dict

api = ProductDto.api
_product = ProductDto.product

@api.route('/')
class ProductList(Resource):

    @api.expect(_product, validate=True)
    @api.response(201, 'Product successfully created.')
    @api.doc('create a new product')
    @admin_token_required
    def post(self):
        """Creates a new Product """
        data = request.json
        return add_new_product(data=data)
    
    @api.doc('list_of_all_products')
    @admin_token_required
    @api.marshal_list_with(_product, envelope='data')
    def get(self):
        """List all products"""
        return get_all_products()


@api.route('/<name>')
@api.param('name', 'The Product identifier')
@api.response(404, 'Product not found.')
class Product(Resource):
    @api.doc('get a product')
    @api.marshal_with(_product)
    def get(self, name):
        """get a product given its name"""
        product = get_a_product(name)
        if not product:
            api.abort(404)
        else:
            return product

    @api.doc('update a product')
    @admin_token_required
    def patch(self, name):
        """update a product given its name"""
        data = request.json
        return update_a_product(data=data, name=name)