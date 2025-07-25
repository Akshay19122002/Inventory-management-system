from flask import Flask
from .models import db
from .auth.routes import auth as auth_blueprint
from .products.routes import products as products_blueprint

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