from flask import g, abort, jsonify, request
from flask_httpauth import HTTPBasicAuth
from app.models import User
from . import api_bp as bp

auth = HTTPBasicAuth()


@bp.route('/tokens/', methods=['POST'])
def get_token():
    if g.get('current_user') is not None or g.get('token_used'):
        abort(401)
    return jsonify(
        {'token': g.get('current_user') .generate_auth_token(expires_in=600), 'expires_in': 600})


@auth.verify_password
def verify_password(email_or_token: str, password: str='') -> bool:
    if email_or_token == '':
        return False
    if password == '':
        g['current_user'] = User.verify_auth_token(email_or_token)
        g['token_used'] = True
        return g['current_user'] is not None
    
    user = User.query.filter_by(email=email_or_token).first()
    if not user and request.endpoint != 'api.new_user':
        return False
    g['current_user'] = user
    g['token_used'] = False
    return user.verify_password(password)
