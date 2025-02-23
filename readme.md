# Headless CMS
#### an API based content management system

### Installation
##### Instructions for Windows, run the following commands using cmd in root directory
- create virtual environment: `python -m venv .venv` and activate it `.venv\Scripts\activate`
- upgrade pip: `python.exe -m pip install --upgrade pip`
- upgrade setuptools: `pip install --upgrade setuptools`
- install poetry: `pip install poetry`
- install dependencies: `poetry install`
- rename `.env-example` to `.env` and edit the project's configurations
- set database `flask db migrate` then `flask db upgrade`
- initialize the application `flask init`
- run the application `flask run`

### API Doc
- POST `/token/` - get timed validation token
#### users
- GET `/user/` - get a list of all users, paginated, admin permission required
- GET `/user/<id>` - get user by id
- POST `/users/` - create a new user
- PUT `/users/<id>` - edit user, requires authorization or admin permission
- DELETE `/users/<id>` - delete user, requires authorization or admin permission
#### posts
- GET `/posts/` - get a list of all posts, paginated
- GET `/posts/<id>` ` get post by id
- POST `/posts/` - create a new post, requires authorization
- PUT `/posts/<id>` - edit post, requires authorization or admin permission
- DELETE `/posts/<id>` - delete post, requires authorization or admin permission
#### comments
- GET `/comments/` - get a list of all comments, paginated, moderator permission required
- GET `/comments/<id>` - get comment by id
- POST `/comments/<post_id>` - create a new comment for given post, requires authorization
- PUT `/comments/<id>` - edit comment, requires authorization or admin permission
- DELETE `/comments/` - delete comment, requires authorization or admin permission
