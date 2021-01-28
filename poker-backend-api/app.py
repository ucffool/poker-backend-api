from chalice import Chalice
from chalicelib.noauth import noauth
import json
import time

app = Chalice(app_name='poker-backend-api')
app.register_blueprint(noauth, url_prefix="/noauth")
app.debug = True
# app.log.info(somethingGoesHere)


@app.middleware('http')
def inject_time(event, get_response):
    start = time.time()
    response = get_response(event)
    body = response.body
    body_obj = json.loads(body) if type(body) == str else body
    total = time.time() - start
    body_obj.setdefault('metadata', {})['duration'] = total
    response.body = body_obj
    return response


@app.route('/')
def index():
    return {'hello': 'world'}


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
