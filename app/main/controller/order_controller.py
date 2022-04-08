from flask import request
from flask_restx import Resource
from app.main.service.order_service import change_order_status
from app.main.util.decorator import admin_token_required
from ..util.dto import OrderDto

api = OrderDto.api
_order = OrderDto.order

@api.route('/status')
class Order(Resource):
    #@admin_token_required
    @api.expect(_order, validate=True)
    @api.doc(responses={
        200: 'Success',
        400: 'Bad Request',
        403: 'Forbidden'
    })
    @api.doc('change order status')
    #@admin_token_required
    def post(self):
        """Updata order status"""
        data = request.json
        return change_order_status(data)
