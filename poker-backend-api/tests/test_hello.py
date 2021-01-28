import json
import pytest
from app import app


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

    def test_treys(self, gateway_factory):
        gateway = gateway_factory()
        response = gateway.handle_request(method='GET',
                                          path='/noauth/treys',
                                          headers={},
                                          body='')
        assert response['statusCode'] == 200
        j = (json.loads(response['body']))
        assert len(j['winners']) > 0
