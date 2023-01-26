from flask import request
from . import api, Blueprint
from app.models import Post, User

@api.route('/')
def index():
    return 'Hello this is the API'


# Endpoint to get all of the posts
@api.route('/posts', methods=['GET'])
def get_posts():
    posts = Post.query.all()
    return [p.to_dict() for p in posts]


# Endpoint to get a single post
@api.route('/posts/<int:post_id>')
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    return post.to_dict()


# Endpoint to create a new post
@api.route('/posts', methods=['POST'])
def create_post():
    # Check to see that the request sent a request body that is JSON
    if not request.is_json:
        return {'error': 'Your request content-type must be application/json'}, 400
    # Get the data from the request body
    data = request.json
    # Validate the incoming data
    for field in ['title', 'body', 'user_id']:
        if field not in data:
            # If the field is not in the request body, throw an error saying they are missing that field
            return {'error': f"{field} must be in request body"}, 400
    
    # pull the fields from the request data
    title = data.get('title')
    body = data.get('body')
    user_id = data.get('user_id')

    # Create a new Post instance with data from request
    new_post = Post(title=title, body=body, user_id=user_id)
    # Return the new post as a JSON response
    return new_post.to_dict(), 201


@api.route('/users/<id>', methods = ['GET'])
def get_user():
    if not request.is_json:
        return {'error': 'Your request content-type must be application/json'}, 400
    data = request.json
    check_user = User.query.filter( (User.username == username) | (User.email == email) ).all()
    if check_user:
        return {'some part of your input is already taken'}
    for field in ['id', 'email', 'username', 'password']:
        if field not in data:
            return {'error': f'{field} not a valid answer'}, 400
    id = data.get('id')
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')
    
    check_user = User.query.filter( (User.username == username) | (User.email == email) ).all()
    user = User.query.get_or_404(id)
    return user.to_dict()



@api.route('/users', methods = ['POST'])
def create_user():
    if not request.is_json:
        return {'error': 'Your request content-type must be application/json'}, 400
    data = request.json

    for field in ['id', 'email', 'username', 'password']:
        if field not in data:
            return {'error': f'{field} not a valid answer'}, 400
    id = data.get('id')
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')

    new_user = User( id=id, email=email, username=username, password=password)
    return new_user.to_dict(), 201