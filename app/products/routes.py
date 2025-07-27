from app.products.logs import log_inventory_action
from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required
from datetime import datetime
from ..models import Product, db, InventoryLog, User
from app.products.forms import ProductForm

# Optional: Import email alert function (handle if missing in dev)
try:
    from app.utils.email import send_low_stock_email
except ImportError:
    send_low_stock_email = None

products_bp = Blueprint('products', __name__)

# GET all products
@products_bp.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([product.to_dict() for product in products])

# ADD new product
@products_bp.route('/products', methods=['POST'])
@login_required
def add_product():
    form = ProductForm(request.form)
    if form.validate_on_submit():
        product = Product(
            name=form.name.data,
            price=form.price.data,
            quantity=form.quantity.data,
            sku=form.sku.data,
            barcode=form.barcode.data,
            category=form.category.data,
            threshold=form.threshold.data,
            expiry_date=form.expiry_date.data
        )
        db.session.add(product)
        db.session.commit()
        return jsonify(product.to_dict()), 201
    return jsonify(form.errors), 400

# UPDATE existing product
@products_bp.route('/products/<int:product_id>', methods=['PUT'])
@login_required
def update_product(product_id):
    product = Product.query.get_or_404(product_id)
    form = ProductForm(request.form)
    if form.validate_on_submit():
        product.name = form.name.data
        product.price = form.price.data
        product.quantity = form.quantity.data
        product.sku = form.sku.data
        product.barcode = form.barcode.data
        product.category = form.category.data
        product.threshold = form.threshold.data
        product.expiry_date = form.expiry_date.data
        db.session.commit()
        return jsonify(product.to_dict())
    return jsonify(form.errors), 400

# DELETE a product
@products_bp.route('/products/<int:product_id>', methods=['DELETE'])
@login_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return '', 204

@products_bp.route('/api/stock/sale', methods=['POST'])
def sale_product():
    data = request.get_json()
    product = Product.query.get(data['product_id'])
    
    if product.stock >= data['quantity']:
        product.stock -= data['quantity']
        db.session.commit()

        # Log the action
        log = InventoryLog(
            product_id=product.id,
            user_id=current_user.id,
            action_type='sale',
            quantity=data['quantity']
        )
        db.session.add(log)
        db.session.commit()

        # Check stock level
        if product.stock < product.threshold:
            send_low_stock_email(product)

        return jsonify({'message': 'Sale successful'}), 200
    else:
        return jsonify({'error': 'Insufficient stock'}), 400



@products_bp.route('/api/stock/restock', methods=['POST'])
@login_required
def restock_product():
    data = request.get_json()
    product = Product.query.get_or_404(data['product_id'])
    quantity = data['quantity']

    product.stock += quantity
    db.session.commit()

    log = InventoryLog(
        product_id=product.id,
        user_id=current_user.id,
        action_type='restock',
        quantity=quantity
    )
    db.session.add(log)
    db.session.commit()

    return jsonify({'message': 'Restock successful'}), 200


@products_bp.route('/api/stock/restock', methods=['POST'])
@login_required
def return_product():
    data = request.get_json()
    product = Product.query.get_or_404(data['product_id'])
    quantity = data['quantity']

    product.stock += quantity
    db.session.commit()

    log = InventoryLog(
        product_id=product.id,
        user_id=current_user.id,
        action_type='return',
        quantity=quantity
    )
    db.session.add(log)
    db.session.commit()

    return jsonify({'message': 'Return successful'}), 200


# Add this near your existing product routes

@products_bp.route('/update_stock', methods=['POST'])
@login_required
def update_stock():
    data = request.json
    product_id = data.get('product_id')
    quantity = data.get('quantity')
    action = data.get('action')  # "sale", "restock", "return"

    product = Product.query.get(product_id)
    if not product:
        return jsonify({'message': 'Product not found'}), 404

    if action == 'sale':
        product.stock -= quantity
    elif action == 'restock':
        product.stock += quantity
    elif action == 'return':
        product.stock += quantity
    else:
        return jsonify({'message': 'Invalid action'}), 400

    db.session.commit()

    # Log this action (next step)
    log_inventory_action(product_id, current_user.id, action, quantity)

    # Check for low stock and send alert (later step)
    if product.stock < product.low_stock_threshold:
        send_low_stock_alert(product)

    return jsonify({'message': 'Stock updated successfully'})

