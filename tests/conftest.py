import pytest

from wsgi_rest.responses import Response
from wsgi_rest.http import HTTP_200_OK


@pytest.fixture(scope='session')
def test_body():
    return 'Long test response body'


@pytest.fixture(scope='session')
def test_status_code():
    return HTTP_200_OK


@pytest.fixture()
def test_response():
    return Response(test_status_code, body=test_body)
