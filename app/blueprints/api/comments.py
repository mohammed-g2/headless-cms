from flask import jsonify, request, g, url_for, abort, current_app
from app import db
from app.models import Comment, Permission, Post
from . import api_bp as bp
from .authentication import auth
from .decorators import permission_required


@bp.route('/comments/')
@auth.login_required
@permission_required(Permission.MODERATE)
def get_comments():
    page = request.args.get('page', 1, type=int)
    pagination = Comment.query.paginate(
        page=page,
        per_page=current_app.config['ENTRIES_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    prev = None
    next = None
    if pagination.has_prev:
        prev = url_for('api.get_posts', page=page-1)
    if pagination.has_next:
        next = url_for('api.get_posts', page=page+1)

    return jsonify({
        'comments': [comment.serialize() for comment in comments],
        'prev_url': prev,
        'next_url': next,
        'count': pagination.total,
        'per_page': current_app.config['ENTRIES_PER_PAGE']})


@bp.route('/comments/<int:id>')
def get_comment(id):
    comment = Comment.query.get_or_404(id)
    return jsonify(comment.serialize())


@bp.route('/comments/<int:id>', methods=['POST'])
@auth.login_required
@permission_required(Permission.COMMENT)
def new_comment(id):
    post = Post.query.get_or_404(id)
    comment = Comment.deserialize(request.json)
    comment.user = g.current_user
    comment.post = post
    db.session.add(comment)
    db.session.commit()
    return (
        jsonify(comment.serialize()),
        201,
        {'Location': url_for('api.get_comment', id=comment.id)})


@bp.route('/comments/<int:id>', methods=['PUT'])
@auth.login_required
@permission_required(Permission.COMMENT)
def edit_comment(id):
    comment = Comment.query.get_or_404(id)
    if g.current_user != comment.user:
        abort(403)
    comment.body = request.json.get('body', comment.body)
    db.session.add(comment)
    db.session.commit()
    return jsonify(comment.serialize()), 202


@bp.route('/comments/<int:id>', methods=['DELETE'])
@auth.login_required
@permission_required(Permission.COMMENT)
def delete_comment(id):
    comment = Comment.query.get_or_404(id)
    post = comment.post
    if g.current_user != comment.user and \
            not g.current_user.can(Permission.MODERATE):
        abort(403)
    db.session.delete(comment)
    db.session.commit()
    return jsonify({}), 202, {'Location': url_for('api.get_post', id=post.id)}
