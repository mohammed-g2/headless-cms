import os
from dotenv import load_dotenv
from flask_migrate import Migrate
from app import create_app, db
from app.models import User, Role, Post, Comment, Permission
from config import basedir

load_dotenv(os.path.join(basedir, '.env'))

app = create_app(os.environ.get('APP_CONFIG', 'default'))
migrate = Migrate(app, db)


@app.cli.command('init')
def init():
    """initialize the application"""
    Role.set_roles()


@app.shell_context_processor
def shell_context():
    return dict(
        db=db, User=User, Role=Role, Post=Post, Comment=Comment, Permission=Permission)
