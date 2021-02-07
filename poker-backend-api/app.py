from chalice import Chalice, AuthResponse
from chalicelib.noauth import noauth  # blueprints
import json
import time
from uuid import uuid4
# for importing .env variables
import os
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env accessible with os.environ.get['NAME']

app = Chalice(app_name='poker-backend-api')
app.register_blueprint(noauth, url_prefix="/noauth")  # blueprints
app.debug = True  # DEBUG
# app.log.info(somethingGoesHere)


@app.middleware('http')
def inject_time(event, get_response):
    start = time.time()
    response = get_response(event)
    body = response.body
    body_obj = json.loads(body) if type(body) == str else body
    total = time.time() - start
    body_obj.setdefault('metadata', {})['duration'] = total
    body_obj.setdefault('metadata', {})['uuid'] = str(uuid4())
    response.body = body_obj
    return response


@app.authorizer()
def basic_auth_insecure(auth_request):
    token = auth_request.token
    if token == 'Basic YWRtaW46YWxsb3c=':  # "admin:allow"
        # A principal id may be a username, email address, or userid
        # routes=['*'] would allow any route
        return AuthResponse(routes=['/auth'], principal_id='user')
    else:
        # routes=[] would mean there are no valid routes for them
        return AuthResponse(routes=[], principal_id='invalid')


@app.route('/')
def index():
    return {'hello': 'world'}


@app.route('/auth', authorizer=basic_auth_insecure)
def index():
    return {'app.current_request.context': app.current_request.context}


@app.route('/auth-user', authorizer=basic_auth_insecure)
def index():
    return {'app.current_request.context': app.current_request.context}


# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#
