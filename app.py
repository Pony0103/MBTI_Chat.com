from flask import Flask, request, redirect, url_for, jsonify, render_template, flash, current_app
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
import os
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
import pymysql
pymysql.install_as_MySQLdb()

# Initialize Flask extensions
db = SQLAlchemy()
migrate = Migrate()
bootstrap = Bootstrap()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')
    
    # Basic configurations
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key')
    app.config['SESSION_PROTECTION'] = 'strong'
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
    app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=7)
    app.config['SESSION_TYPE'] = 'filesystem'
    
    # Database configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Upload configurations
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'uploads')
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)
    csrf.init_app(app)
    
    # Initialize login manager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login_page'
    
    # Register blueprints
    from auth import auth_bp
    from chat import chat_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(chat_bp, url_prefix='/chat')
    
    # Database models
    class Message(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        room = db.Column(db.String(50))
        sender = db.Column(db.String(50))
        content = db.Column(db.String(500))
        timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    @login_manager.user_loader
    def load_user(user_id):
        from dbmodels import UserACC
        try:
            return UserACC.query.get(int(user_id))
        except:
            return None
    
    return app

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))