from flask import jsonify, request
from app.products import products
from app.products.models import Category, Store, Product, products_store
from app.utils.security import Security
from app import db


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

# init endpoints api rest category
@products.route('/categories', methods=['GET'])
def get_categories():
    has_access = Security.verify_token(request.headers)

    if has_access:
        try:
            categories = Category.query.all()
            if (len(categories) > 0):
                return jsonify(products_list=[cat.serialize for cat in categories]), 200
            else:
                return jsonify({'message': "There are no categories"}), 404
        except Exception as e:
            return jsonify({'message': "ERROR", 'success': False}), 400
    else:
        return jsonify({'message': 'UnAuthorized'}), 401

@products.route('/categories', methods=['POST'])
def create_category():
    if len(request.form) == 0:
        data = request.json
    else:
        data = request.form.to_dict(flat=True)

    if not 'category_name' in data:
        return jsonify({'message': "Category Name is required", 'success': False}), 400
    has_access = Security.verify_token(request.headers)

    if has_access:
        try:
            category = Category(category_name=data['category_name'])
            db.session.add(category)
            db.session.commit()
            return jsonify({'isSuccess': True, 'message': 'Category Created'}), 201
        
        except Exception as e:
            return jsonify({'message': "ERROR", 'success': False}), 400
    else:
        return jsonify({'message': 'UnAuthorized'}), 401

@products.route('/categories/<int:id>', methods=['GET'])
def get_category(id):
    has_access = Security.verify_token(request.headers)

    if has_access:
        try:
            category = Category.query.get(id)
            return jsonify(category.serialize), 200
        except Exception as e:
            return jsonify({'message': "Category not found", 'isSuccess': False}), 400
    else:
        return jsonify({'message': 'UnAuthorized'}), 401

@products.route('/categories/<int:id>', methods=['PUT', 'PATCH'])
def update_category(id):
    if len(request.form) == 0:
        data = request.json
    else:
        data = request.form.to_dict(flat=True)

    has_access = Security.verify_token(request.headers)

    if has_access:
        try:
            category = Category.query.get_or_404(id)
            if 'category_name' in data:
                category.category_name = data['category_name']
            db.session.commit()
            return jsonify(category.serialize), 200
        except Exception as e:
            return jsonify({'message': "Category not found", 'isSuccess': False}), 400
    else:
        return jsonify({'message': 'UnAuthorized'}), 401

@products.route('/categories/<int:id>', methods=['DELETE'])
def delete_category(id):
    has_access = Security.verify_token(request.headers)
    if has_access:
        try:
            category = Category.query.get_or_404(id)
            db.session.delete(category)
            db.session.commit()
            return jsonify({'isSuccess': True, 'message': 'Category eliminated'}), 200
        except Exception as e:
            return jsonify({'message': "Category not found", 'isSuccess': False}), 400
    else:
        return jsonify({'message': 'UnAuthorized'}), 401
# end endpoints api rest category        