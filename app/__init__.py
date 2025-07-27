import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from flask_cors import CORS
from dotenv import load_dotenv

# --- Step 1: Load Environment Variables ---
load_dotenv()

# --- Step 2: Initialize Extensions Globally ---
# Create instances of your extensions here. They are not yet connected to an app.
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
jwt = JWTManager()
login_manager = LoginManager()
login_manager.login_view = 'frontend.login'

@login_manager.user_loader
def load_user(user_id):
    # This function reloads the user object from the user ID stored in the session.
    from .models import User # Import is done *inside* to prevent circular errors
    return User.query.get(int(user_id))

def create_app():
    """The main application factory."""
    app = Flask(__name__)

    # --- Step 3: Configure the App ---
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///inventory.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'default-jwt-secret-key')
    app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'default-flask-secret-key')

    # --- Step 4: Initialize Extensions with the App ---
    # This is the step that solves the RuntimeError by connecting db to app.
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)
    login_manager.init_app(app)
    CORS(app)

    # --- Step 5: Import and Register Blueprints ---
    # We do this inside the factory to make sure everything is set up first.
    from .auth.routes import auth
    from .products.routes import products_bp
    from .routes.frontend_routes import frontend_bp

    app.register_blueprint(auth)
    app.register_blueprint(products_bp)
    app.register_blueprint(frontend_bp)

    return app
