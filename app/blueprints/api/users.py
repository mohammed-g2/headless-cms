from flask import jsonify, request, g, url_for, abort, current_app
from app import db
from app.models import User, Role
from . import api_bp as bp
from .authentication import auth
from .decorators import admin_required


@bp.route('/users/')
@auth.login_required
@admin_required
def get_users():
    page = request.args.get('page', 1, type=int)
    pagination = User.query.paginate(
        page=page,
        per_page=current_app.config['ENTRIES_PER_PAGE'],
        error_out=False)
    users = pagination.items
    prev = None
    next = None
    if pagination.has_prev:
        prev = url_for('api.get_users', page=page-1)
    if pagination.has_next:
        next = url_for('api.get_users', page=page+1)
    
    return jsonify({
        'users': [user.serialize() for user in users],
        'prev_url': prev,
        'next_url': next,
        'count': pagination.total,
        'per_page': current_app.config['ENTRIES_PER_PAGE']})


@bp.route('/users/<int:id>')
def get_user(id):
    user = User.query.get_or_404(id)
    if g.current_user.is_admin():
        return jsonify(user.admin_serialize())
    return jsonify(user.serialize())


@bp.route('/users/', methods=['POST'])
def new_user():
    user = User.deserialize(request.json)
    user.location = request.json.get('location')
    user.about_me = request.json.get('about_me')
    db.session.add(user)
    db.session.commit()
    return jsonify(user.serialize()), 201


@bp.route('/user/<int:id>', methods=['PUT'])
@auth.login_required
def edit_user(id):
    user = User.query.get_or_404(id)
    if g.current_user != user and \
            not g.current_user.is_admin():
        abort(403)
    if g.current_user == user or \
            g.current_user.is_admin():
        user.username = request.json.get('username', user.username)
        user.email = request.json.get('email', user.email)
        if request.json.get('password'):
            user.password = request.json.get('password')
        user.location = request.json.get('location', user.location)
        user.about_me = request.json.get('about_me', user.about_me)
        if g.current_user.is_admin():
            user.confirmed = request.json.get('confirmed', user.confirmed)
            role = request.json.get('role')
            if role:
                user.role = Role.query.filter_by(name=request.json.get('role')).first()

    db.session.add(user)
    db.session.commit()
    return jsonify(user.serialize()),


@bp.route('/user/<int:id>', methods=['DELETE'])
@auth.login_required
def delete_user(id):
    user = User.query.get_or_404(id)
    if g.current_user != user and \
            not g.current_user.is_admin():
        abort(403)
    db.session.delete(user)
    db.session.commit()
    return jsonify({}), 202
