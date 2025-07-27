from flask import Flask
from .models import db
from .auth.routes import auth as auth_blueprint
from .products.routes import products_bp as products_blueprint
from .routes.frontend_routes import frontend_bp  # ✅ New
from flask_login import LoginManager
from app.models import User  # ✅ Your User model

login_manager = LoginManager()
login_manager.login_view = 'frontend.login'  # ✅ points to the correct route function
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    login_manager.init_app(app)

    # Register Blueprints
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(products_blueprint, url_prefix='/products')
    app.register_blueprint(frontend_bp)  # ✅ Register frontend pages (login, dashboard, etc.)

    return app
<<<<<<< HEAD
=======

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
>>>>>>> 69b00c0ee3e94f86dcba1689ea03969cf1e1b759
