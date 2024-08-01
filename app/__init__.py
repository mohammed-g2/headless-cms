from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import options


db = SQLAlchemy()
cors = CORS()


def create_app(config_name: str) -> Flask:
    """Create and configure the application"""
    app = Flask(__name__)
    app.config.from_object(options[config_name])

    db.init_app(app)
    cors.init_app(app)

    from app.blueprints import api_bp
    app.register_blueprint(api_bp, url_prefix='/api/v1')

    
    @app.route('/')
    def index():
        return render_template('test.html')
    
    return app
