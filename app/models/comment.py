from flask import url_for
from app import db
from app.util import utcnow
from app.exceptions import ValidationError


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text())
    created_at = db.Column(db.DateTime(), default=utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

    def __repr__(self):
        return f'<Comment {self.id}>'
    

    def serialize(self) -> dict:
        json = {
            'url': url_for('api.get_comment', id=self.id),
            'body': self.body,
            'created_at': self.created_at,
            'user_url': url_for('api.get_user', id=self.id),
            'post_url': url_for('api.get_post', id=self.id)
        }
        return json
    
    @staticmethod
    def deserialize(json: dict) -> 'Comment':
        body = json.get('body')
        if body is None or body == '':
            raise ValidationError('comment does not have a body')
        return Comment(body=body)
