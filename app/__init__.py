from flask import Flask
from .models import db
from .auth.routes import auth as auth_blueprint
from .products.routes import products_bp as products_blueprint
from flask_login import LoginManager
from app.models import User  # Assuming you have a User model

login_manager = LoginManager()
login_manager.login_view = 'auth.login'  # 🔐 This redirects to login if not authenticated
login_manager.login_message_category = 'info'  # Optional: flash message category

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_app():
    app = Flask(__name__)
    
    # Load configuration from config.py
    app.config.from_object('config.Config')
    
    # Initialize the database
    db.init_app(app)
    
    # Register blueprints
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(products_blueprint, url_prefix='/products')
    
    return app
