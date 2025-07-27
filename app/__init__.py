from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'frontend.login'
login_manager.login_message_category = 'info'

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI='sqlite:///your_database.db',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SECRET_KEY='your_secret_key_here'
    )

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Import blueprints here to avoid circular imports
    from app.auth.routes import auth as auth_blueprint
    from app.products.routes import products_bp as products_blueprint
    from app.routes.frontend_routes import frontend_bp

    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(products_blueprint, url_prefix='/products')
    app.register_blueprint(frontend_bp)
    app.register_blueprint(products_blueprint, url_prefix='/products')
    # Import User model for user_loader
    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app
