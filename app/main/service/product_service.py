import uuid

from app.main import db
from app.main.model.product import Product
from typing import Dict

def add_new_product(data: Dict[str, str]):
    product = Product.query.filter_by(name=data['name']).first()
    if not product:
        new_product = Product(
            product_id=str(uuid.uuid4()),
            name=data['name'],
            description=data['description'],
            price=int(data['price'])
        )
        save_changes(new_product)
        response_object = {
            'status': 'success',
            'message': 'successfully add new product.',
            'product': {
                "product_id": new_product.product_id,
                "name": new_product.name,
                "description": new_product.description,
                "price": new_product.price
            }
        }
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'Product name already exists.',
        }
        return response_object, 409

def get_all_products():
    return Product.query.all()

def get_a_product(name):
    return Product.query.filter_by(name=name).first()

def update_a_product(data: Dict[str, str], name):
    product = Product.query.filter_by(name=name).first()   
    print(product) 
    if not product:
        response_object = {
            'status': 'fail',
            'message': 'Product name does not exists.',
        }
        print(response_object)
        return response_object, 409    
    else:
        if 'name' in data:
            product_new_name = Product.query.filter_by(name=data['name']).first()
            if product_new_name:
                response_object = {
                'status': 'fail',
                'message': 'Product name exists.',
                }
                print(response_object)
                return response_object, 404  
            else:
                product.name = data['name']
        

        if 'description' in data:
            product.description = data['description']

        if 'price' in data:
            product.price = data['price']

        db.session.commit()

        response_object = {
            'status': 'successfully',
            'message': 'update product successfully.',
        }
        print(response_object)
        return response_object, 200

def save_changes(data: Product):
    db.session.add(data)
    db.session.commit()