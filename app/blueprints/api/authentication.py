from flask import g, abort, jsonify, request
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth, MultiAuth
from app.models import User
from . import api_bp as bp

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth(scheme='Bearer')
auth = MultiAuth(basic_auth, token_auth)


@basic_auth.verify_password
def verify_password(email: str, password: str):
    if email == '':
        return False
    user = User.query.filter_by(email=email).first()
    if not user:
        return False
    g.current_user = user
    g.token_used = False
    if user.verify_password(password):
        return user
    else:
        return False


@token_auth.verify_token
def verify_token(token):
    user = User.verify_auth_token(token)
    if user:
        g.current_user = user
        g.token_used = True
        return user
    else:
        return False


@bp.route('/token/', methods=['POST'])
@auth.login_required
def token():
    if g.current_user is None or g.token_used:
        abort(401)
    return jsonify({
        'token': g.current_user.generate_auth_token(expires_in=600), 
        'expires_in': 600})
