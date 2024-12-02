from flask import jsonify, request
from app.products import products
from app.products.models import Category, Store, Product, products_store
from app.utils.security import Security


@products.route('/', methods=['GET'])
def get_products():
    has_access = Security.verify_token(request.headers)

    if has_access:
        try:
            products = Product.query.all()
            if (len(products) > 0):
                return jsonify(products_list=[i.serialize for i in products]), 200
            else:
                return jsonify({'message': "NOT FOUND"}), 404
        except Exception as e:
            return jsonify({'message': "ERROR", 'success': False}), 400
    else:
        return jsonify({'message': 'UnAuthorized'}), 401