from flask import Flask
from .models import db, user
from .auth.routes import auth as auth_blueprint
from .products.routes import products_bp as products_blueprint
from .routes.frontend_routes import frontend_bp  # ✅ New
from flask_login import LoginManager
from flask_migrate import Migrate  # ✅ Import Flask-Migrate
from flask_sqlalchemy import SQLAlchemy

login_manager = LoginManager()
login_manager.login_view = 'frontend.login'  # ✅ points to the correct route function
login_manager.login_message_category = 'info'

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'  # or your actual DB URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


    db.init_app(app)
    migrate.init_app(app, db)  # ✅ Initialize Flask-Migrate
    from app.models import User  
    
    login_manager.init_app(app)
    

    # Register Blueprints
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(products_blueprint, url_prefix='/products')
    app.register_blueprint(frontend_bp)  # ✅ Register frontend pages (login, dashboard, etc.)

    return app


# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

