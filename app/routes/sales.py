from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required
from datetime import datetime
from app.models import Product, db, InventoryLog, User
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