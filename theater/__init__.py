from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db = SQLAlchemy() 
bcrypt = Bcrypt()

def create_app(test_config=None):
    app = Flask(__name__) 

    app.config["SECRET_KEY"] = b"\x8c\xa5\x04\xb3\x8f\xa1<\xef\x9bY\xca/*\xff\x12\xfb"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myDB.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
    
    db.init_app(app)


    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    from . import model
    @login_manager.user_loader
    def load_user(user_id):
        return model.User.query.get(int(user_id))

    
    from . import main
    from . import auth
    from . import manager
    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(manager.bp)

    with app.app_context():
        db.create_all()

    return app

