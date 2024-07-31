from flask import jsonify, request, g, url_for, abort, current_app
from app import db
from app.models import Post, Permission
from . import api_bp as bp
from .authentication import auth
from .decorators import permission_required


@bp.route('/posts/')
def get_posts():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.paginate(
        page=page,
        per_page=current_app.config['ENTRIES_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    prev = None
    next = None
    if pagination.has_prev:
        prev = url_for('api.get_posts', page=page-1)
    if pagination.has_next:
        next = url_for('api.get_posts', page=page+1)

    return jsonify({
        'posts': [post.serialize() for post in posts],
        'prev_url': prev,
        'next_url': next,
        'count': pagination.total,
        'per_page': current_app.config['ENTRIES_PER_PAGE']})


@bp.route('/posts/<int:id>')
def get_post():
    post = Post.query.get_or_404(id)
    return jsonify(post.serialize())


@bp.route('/posts/', methods=['POST'])
@auth.login_required
@permission_required(Permission.WRITE)
def new_post():
    post = Post.deserialize(request.json)
    post.author = g.current_user
    db.session.add(post)
    db.session.commit()
    return (
        jsonify(post.serialize()),
        201,
        {'Location': url_for('api.get_post', id=post.id)})


@bp.route('/posts/<int:id>', methods=['PUT'])
@auth.login_required
@permission_required(Permission.WRITE)
def edit_post(id):
    post = Post.query.get_or_404(id)
    if g.current_user != post.author and \
            not g.current_user.is_admin():
        abort(403)
    post.title = request.json.get('title', post.title)
    post.body = request.json.get('body', post.body)
    db.session.add(post)
    db.session.commit()
    return jsonify(post.serialize()), 202


@bp.route('/posts/<int:id>', methods=['DELETE'])
@auth.login_required
@permission_required(Permission.WRITE)
def delete_post(id):
    post = Post.query.get_or_404(id)
    user = post.author
    if g.current_user != post.author and \
            not g.current_user.is_admin():
        abort(403)
    db.session.delete(post)
    db.session.commit()
    return (jsonify({}), 202, {'Location': url_for('api.get_user', id=user.id)})
