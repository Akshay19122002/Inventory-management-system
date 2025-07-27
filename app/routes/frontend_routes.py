from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, login_user, logout_user, current_user
from app.models.user import User
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

frontend_bp = Blueprint('frontend', __name__)

# Home/Login Page
@frontend_bp.route('/', methods=['GET', 'POST'])
@frontend_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('frontend.dashboard'))
        else:
            flash("Invalid credentials", "danger")
    return render_template("login.html")

# Register Page
@frontend_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        role = request.form.get('role')

        if password != confirm_password:
            flash("Passwords do not match!", "danger")
        else:
            hashed_pw = generate_password_hash(password)
            new_user = User(name=name, email=email, password=hashed_pw, role=role)
            db.session.add(new_user)
            db.session.commit()
            flash("Registered successfully!", "success")
            return redirect(url_for('frontend.login'))
    return render_template("register.html")

# Dashboard Page
@frontend_bp.route('/dashboard')
@login_required
def dashboard():
    from app.models.product import Product  # import here to avoid circular imports

    if current_user.role == 'admin':
        products = Product.query.all()
    else:
        products = Product.query.with_entities(
            Product.id, Product.sku, Product.name,
            Product.quantity, Product.threshold, Product.expiry_date
        ).all()

    return render_template("dashboard.html", products=products, user=current_user)

# Logout
@frontend_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('frontend.login'))
