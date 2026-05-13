# from backend.app.urls import register_routes
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from datetime import datetime, timedelta
import os
from flask_mail import Mail, Message
from .models import db ,User 
# from celery import Celery
# from .tasks import send_daily_reminders, send_monthly_report, export_user_csv, beat_schedule
# from .user_routes import user_bp
SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///quiz_master.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
    
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-string'
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

mail = Mail()
# celery = Celery(__name__, broker='redis://localhost:6379/0')

# from .authdghdr.Login  import login
# from .authdghdr.Register import register

def create_app(config_name='development'):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
    # JWT config — must be in app.config, not module-level variables
    app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = JWT_ACCESS_TOKEN_EXPIRES
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = JWT_REFRESH_TOKEN_EXPIRES
    app.config['JWT_TOKEN_LOCATION'] = ['headers']
    app.config['JWT_HEADER_NAME'] = 'Authorization'
    app.config['JWT_HEADER_TYPE'] = 'Bearer'
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = "xxxxxxxx@gmail.com"
    app.config['MAIL_PASSWORD'] = "xxxxxxxxxxxx"
    app.config['MAIL_DEFAULT_SENDER'] = "xxxxxxx@gmail.com"

    db.init_app(app)
    jwt = JWTManager(app)
    CORS(app, resources={r"/api/*": {"origins": "*", "allow_headers": ["Content-Type", "Authorization"], "expose_headers": ["Authorization"], "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"]}})

    # JWT error handlers — print message to help debug
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        print(f"[JWT] Invalid token: {error}")
        return jsonify({"msg": f"Invalid token: {error}"}), 422

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        print(f"[JWT] Missing token: {error}")
        return jsonify({"msg": f"Missing token: {error}"}), 401

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        print(f"[JWT] Token expired for user {jwt_payload.get('sub')}")
        return jsonify({"msg": "Token has expired"}), 401

    mail.init_app(app)
    # celery.conf.update(app.config)

    # from .tasks import beat_schedule
    # celery.conf.beat_schedule = beat_schedule


    # app.add_url_rule('/login', view_func=login, methods=['POST'])
    # app.add_url_rule('/register', view_func=register, methods=['POST'])
    
    # @app.route('/api/register', methods=['POST'])
    
    
    # @app.route('/api/login', methods=['POST'])
    from .admin_routes import admin_bp
    from .user_routes import user_bp
    from .auth import auth_bp
    from .quiz_routes import quiz_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth') 
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(user_bp, url_prefix='/api/user')
    app.register_blueprint(quiz_bp, url_prefix='/api/quiz')



    
    @app.route('/api/profile', methods=['GET'])
    @jwt_required()
    def get_profile():
        try:
            current_user_id = int(get_jwt_identity())
            user = User.query.get(current_user_id)
            
            if not user:
                return jsonify({'error': 'User not found'}), 404
            
            return jsonify(user.to_dict()), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    
    # Create tables and admin user
    with app.app_context():
        db.create_all()
        create_admin_user()

        # create_admin_user()
    
    return app


from .models import db, User

def create_admin_user():
    """Create admin user if it doesn't exist"""
    admin = User.query.filter_by(role='admin').first()
    if not admin:
        admin = User(
            username='admin',
            email = 'admin@gmail.com',
            full_name='System Administrator',
            role='admin'
        )
        admin.set_password('admin123') 
        
        db.session.add(admin)
        db.session.commit()
        print("Admin user created successfully")
    else:
        print("Admin user already exists")


# Register routes
# from .urls import register_routes
# register_routes(app)
if __name__ == '__main__':
    app = create_app()

    app.run(debug=True)








