import json
import pytest
from app import app
from chalice.test import Client
# for importing .env variables
import os
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.


# Using the testing framework in Chalice tutorials
@pytest.fixture
def test_client():
    with Client(app) as client:
        yield client


def test_noauth_hello_world():
    with Client(app) as client:
        response = client.http.get('/noauth/hello/world')
        # app.log.info(response.json_body)
        assert response.status_code == 200
        assert response.json_body['hello'] == 'world'  # response.json_body returns a `dict`
        assert json.loads(response.body)['hello'] == 'world'  # response.body returns bytes


def test_noauth_treys():
    with Client(app) as client:
        response = client.http.get('/noauth/treys')
        assert response.status_code == 200
        assert len(response.json_body['winners']) > 0


def test_auth_allow_deny_missing():
    with Client(app) as client:
        assert client.http.get(
            '/auth', headers={'Authorization': 'allow'}).status_code == 200
        assert client.http.get(
            '/auth', headers={'Authorization': 'deny'}).status_code == 403
        assert client.http.get(
            '/auth', headers={}).status_code == 401


@pytest.mark.skipif(not os.path.isfile("../.env"),
                    reason="requires .env file to be present")
def test_env_domain():
    assert os.environ.get('DOMAIN') == 'pokermuster.com'

# using testing framework by some rando on the internet
"""
@pytest.fixture
def gateway_factory():
    from chalice.config import Config
    from chalice.local import LocalGateway

    def create_gateway(config=None):
        if config is None:
            config = Config()
        return LocalGateway(app, config)
    return create_gateway


class TestChalice(object):
    def test_hello_world(self, gateway_factory):
        gateway = gateway_factory()
        response = gateway.handle_request(method='GET',
                                          path='/noauth/hello/world',
                                          headers={},
                                          body='')
        assert response['statusCode'] == 200
        assert json.loads(response['body'])['hello'] == 'world'

    def test_basic_auth_insecure(self, gateway_factory):
        gateway = gateway_factory()
        response = gateway.handle_request(method='GET',
                                          path='/auth',
                                          headers={'Authorization': 'allow'},
                                          body='')
        assert response['statusCode'] == 200

    def test_basic_auth_missing(self, gateway_factory):
        from chalice.local import NotAuthorizedError
        gateway = gateway_factory()
        with pytest.raises(NotAuthorizedError):
            gateway.handle_request(method='GET',
                                   path='/auth',
                                   headers={},
                                   body='')

    def test_basic_auth_incorrect(self, gateway_factory):
        from chalice.local import ForbiddenError
        gateway = gateway_factory()
        with pytest.raises(ForbiddenError):
            gateway.handle_request(method='GET',
                                   path='/auth',
                                   headers={'Authorization': 'disallow'},
                                   body='')

    def test_treys(self, gateway_factory):
        gateway = gateway_factory()
        response = gateway.handle_request(method='GET',
                                          path='/noauth/treys',
                                          headers={},
                                          body='')
        assert response['statusCode'] == 200
        j = (json.loads(response['body']))
        assert len(j['winners']) > 0
"""
