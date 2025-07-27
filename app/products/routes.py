from flask import Blueprint, request, jsonify
from ..models import Product, User # Use relative import
from .. import db
from flask_jwt_extended import jwt_required, get_jwt
from functools import wraps

# --- Create the Blueprint ---
# This organizes all your product-related routes.
products_bp = Blueprint('products', __name__)

# --- Custom Decorator for Admin Role ---
# This is your security guard to check if a user is an Admin.
def admin_required():
    def wrapper(fn):
        @wraps(fn)
        @jwt_required() # First, ensure the user is logged in
        def decorator(*args, **kwargs):
            claims = get_jwt()
            # Then, check if their role is 'Admin'
            if claims.get("role") == 'Admin':
                return fn(*args, **kwargs)
            else:
                return jsonify(message="Admins only!"), 403
        return decorator
    return wrapper

# --- 1. GET /products (Read All Products) ---
# This is the highest priority for your frontend developer.
@products_bp.route('/', methods=['GET'])
@jwt_required() # Any logged-in user (Admin or Staff) can see the products.
def get_products():
    """Fetches all products from the database."""
    try:
        products = Product.query.all()
        # Convert the list of product objects into a list of dictionaries
        output = []
        for product in products:
            product_data = {
                'id': product.id,
                'SKU': product.SKU,
                'name': product.name,
                'category': product.category,
                'stock': product.stock,
                'threshold': product.threshold,
                'expiry_date': product.expiry_date.isoformat() if product.expiry_date else None
            }
            output.append(product_data)
        return jsonify(output), 200
    except Exception as e:
        return jsonify(message=f"An error occurred: {e}"), 500

# --- 2. POST /products (Create a New Product) ---
@products_bp.route('/', methods=['POST'])
@admin_required() # Only Admins can create products.
def create_product():
    """Creates a new product from incoming JSON data."""
    data = request.get_json()

    # Server-side validation
    if not data or not data.get('name') or not data.get('SKU'):
        return jsonify(message="Name and SKU are required fields."), 400
    
    if Product.query.filter_by(SKU=data['SKU']).first():
        return jsonify(message="A product with this SKU already exists."), 409

    # Create a new Product object from the data
    new_product = Product(
        SKU=data['SKU'],
        name=data['name'],
        category=data.get('category'),
        stock=int(data.get('stock', 0)),
        threshold=int(data.get('threshold', 10))
        # Note: Handling expiry_date would require converting a string to a date object
    )

    # Add to the database and save
    db.session.add(new_product)
    db.session.commit()

    return jsonify(message="Product created successfully."), 201

# --- 3. PUT /products/<id> (Update a Product) ---
@products_bp.route('/<int:product_id>', methods=['PUT'])
@admin_required() # Only Admins can update products.
def update_product(product_id):
    """Updates an existing product by its ID."""
    try:
        product = Product.query.get_or_404(product_id)
        data = request.get_json()

        # Update the product's fields with the new data
        product.name = data.get('name', product.name)
        product.SKU = data.get('SKU', product.SKU)
        product.category = data.get('category', product.category)
        product.stock = int(data.get('stock', product.stock))
        product.threshold = int(data.get('threshold', product.threshold))
        
        # Save the changes to the database
        db.session.commit()
        return jsonify(message="Product updated successfully."), 200
    except Exception as e:
        return jsonify(message=f"An error occurred: {e}"), 500

# --- 4. DELETE /products/<id> (Delete a Product) ---
@products_bp.route('/<int:product_id>', methods=['DELETE'])
@admin_required() # Only Admins can delete products.
def delete_product(product_id):
    """Deletes a product by its ID."""
    try:
        product = Product.query.get_or_404(product_id)
        
        # Delete the product from the database
        db.session.delete(product)
        db.session.commit()
        
        return jsonify(message="Product deleted successfully."), 200
    except Exception as e:
        return jsonify(message=f"An error occurred: {e}"), 500