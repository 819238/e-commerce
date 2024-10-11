from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), '..', 'templates'), static_folder=os.path.join(os.path.dirname(__file__), '..', 'static'))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'dH9zW4xP7yT2rL5qF3mJ8nK1cA6vE0uB'

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'routes.login'

    from .models import User, Product  # Import models here

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .routes import routes as routes_blueprint
    app.register_blueprint(routes_blueprint)

    with app.app_context():
        db.create_all()  # Buat semua tabel

    return app
