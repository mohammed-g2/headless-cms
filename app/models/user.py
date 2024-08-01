import time
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app, url_for
from app import db
from app.util import utcnow
from app.exceptions import ValidationError
from .role import Role, Permission


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(128), unique=True, index=True)
    location = db.Column(db.String(128))
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=utcnow)
    last_seen = db.Column(db.DateTime(), default=utcnow)
    confirmed = db.Column(db.Boolean(), default=False)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    comments = db.relationship('Comment', backref='user', lazy='dynamic')

    def __repr__(self) -> str:
        return f'<User {self.username}>'

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        if self.role is None:
            if self.email == current_app.config['APP_ADMIN']:
                self.role = Role.query.filter_by(name='administrator').first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()
            db.session.add(self)
    
    @property
    def password(self):
        raise AttributeError('password is not a readable property')
    
    @password.setter
    def password(self, password: str):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password: str) -> bool:
        """Check if given password matches the stored password hash"""
        return check_password_hash(self.password_hash, password)
    
    def can(self, permission: int) -> bool:
        """Check if user have the given permission"""
        return self.role is not None and self.role.has_permission(permission)

    def is_admin(self) -> bool:
        """Check if user have administrator access"""
        return self.can(Permission.ADMIN)

    def generate_token(self, payload: dict, expires_in: int=600) -> str:
        """Generate jwt token using given payload"""
        payload.update({'exp': time.time() + expires_in})
        token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
        return token
    
    def generate_auth_token(self, expires_in: int=600) -> str:
        return self.generate_token(
            payload={'id': self.id}, 
            expires_in=expires_in)
    
    @staticmethod
    def verify_auth_token(token: str):
        """return user based on id stored in token if token is valid"""
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms='HS256')
        except:
            return None
        if not data.get('id'):
            return None
        
        return User.query.get(data['id'])
    
    def ping(self):
        """Update user's last seen property"""
        self.last_seen = utcnow()
        db.session.add(self)
        db.session.commit()
    
    def serialize(self) -> dict:
        json = {
            'url': url_for('api.get_user', id=self.id),
            'username': self.username,
            'location': self.location,
            'about_me': self.about_me,
            'member_since': self.member_since,
            'last_seen': self.last_seen,
            'posts_url': url_for('api.get_posts', id=self.id),
            'posts_count': self.posts.count()
        }
        return json
    
    def admin_serialize(self) -> dict:
        json = {
            'url': url_for('api.get_user', id=self.id),
            'username': self.username,
            'email': self.email,
            'confirmed': self.confirmed,
            'role': self.role.name,
            'location': self.location,
            'about_me': self.about_me,
            'member_since': self.member_since,
            'last_seen': self.last_seen,
            'posts_url': url_for('api.get_posts', id=self.id),
            'posts_count': self.posts.count()
        }
        return json
    
    @staticmethod
    def deserialize(json: dict) -> 'User':
        print('here ---------------------', json)
        username = json.get('username')
        email = json.get('email')
        password = json.get('password')
        if not username:
            raise ValidationError('user does not have a username')
        if not email:
            raise ValidationError('user does not have an email')
        if not password:
            raise ValidationError('user does not have a password')
        return User(username=username, email=email, password=password)
