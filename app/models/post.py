from flask import url_for
from app import db
from app.util import utcnow
from app.exceptions import ValidationError


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), unique=True, index=True)
    body = db.Column(db.Text())
    created_at = db.Column(db.DateTime(), index=True, default=utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments = db.relationship('Comment', backref='post', lazy='dynamic')

    def __repr__(self):
        return f'<Post {self.id}>'
    
    def serialize(self) -> dict:
        json = {
            'url': url_for('api.get_post', id=self.id),
            'body': self.body,
            'created_at': self.created_at,
            'user_url': url_for('api.get_user', id=self.user_id),
            'comments_url': url_for('api.get_comments', id=self.id),
            'comments_count': self.comments.count()
        }
        return json
    
    @staticmethod
    def deserialize(json: dict) -> 'Post':
        title = json.get('title')
        body = json.get('body')
        if not title:
            raise ValidationError('post does not have a title')
        if not body:
            raise ValidationError('post does not have a body')
        return Post(title=title, body=body)
