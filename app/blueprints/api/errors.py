from flask import jsonify, abort
from app.exceptions import ValidationError
from . import api_bp as bp


# 201 Created
# 202 Accepted
# 400 Bad request
# 401 Unauthorized
# 403 Forbidden
# 404 Not found
# 405 Method not allowed
# 500 Internal server error


@bp.errorhandler(ValidationError)
def validation_error(e):
    abort(400, e.args[0])


@bp.app_errorhandler(400)
def bad_request(e):
    response = jsonify({'error': f'bad request, {e.description}'})
    response.status_code = 400
    return response


@bp.app_errorhandler(401)
def unauthorized(e):
    response = jsonify({'error': 'required or invalid credentials'})
    response.status_code = 401
    return response


@bp.app_errorhandler(403)
def forbidden(e):
    response = jsonify({'error': 'insufficient credentials'})
    response.status_code = 403
    return response


@bp.app_errorhandler(404)
def not_found(e):
    response = jsonify({'error': 'page not found'})
    response.status_code = 404
    return response


@bp.app_errorhandler(405)
def method_not_allowed(e):
    response = jsonify({'error': 'method not supported for given resource'})
    response.status_code = 405
    return response


@bp.app_errorhandler(500)
def internal_server_error(e):
    response = jsonify({'error': 'internal server error'})
    response.status_code = 500
    return response
