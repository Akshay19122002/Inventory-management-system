from flask import Blueprint, request, jsonify
from app.models import Product, db
from app.products.forms import ProductForm

products_bp = Blueprint('products', __name__)

@products_bp.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([product.to_dict() for product in products])

@products_bp.route('/products', methods=['POST'])
def add_product():
    form = ProductForm(request.form)
    if form.validate_on_submit():
        product = Product(name=form.name.data, price=form.price.data, quantity=form.quantity.data)
        db.session.add(product)
        db.session.commit()
        return jsonify(product.to_dict()), 201
    return jsonify(form.errors), 400

@products_bp.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = Product.query.get_or_404(product_id)
    form = ProductForm(request.form)
    if form.validate_on_submit():
        product.name = form.name.data
        product.price = form.price.data
        product.quantity = form.quantity.data
        db.session.commit()
        return jsonify(product.to_dict())
    return jsonify(form.errors), 400

@products_bp.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return '', 204



from flask_jwt_extended import jwt_required, get_jwt_identity
@products_bp.route('/products/sale', methods=['POST'])

@products_bp.route('/products/return', methods=['POST'])
@jwt_required()
def stock_return():
    return handle_stock_update('return')

@products_bp.route('/products/restock', methods=['POST'])
@jwt_required()
def stock_restock():
    return handle_stock_update('restock')




def handle_stock_update(action):
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity')

    if not product_id or not quantity or quantity <= 0:
        return jsonify({'error': 'Invalid input'}), 400

    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404

    if action == 'sale':
        if product.quantity < quantity:
            return jsonify({'error': 'Not enough stock'}), 400
        product.quantity -= quantity
    elif action in ['return', 'restock']:
        product.quantity += quantity

    db.session.commit()
    return jsonify({'message': f'Stock updated for {action}', 'current_quantity': product.quantity}), 200

