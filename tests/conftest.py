from io import BytesIO

import pytest

from wsgi_rest import App
from wsgi_rest.application import Route
from wsgi_rest.http import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from wsgi_rest.responses import Response


@pytest.fixture(scope='session')
def test_body():
    return 'Long test response body'


@pytest.fixture(scope='session')
def test_status_code():
    return HTTP_200_OK


@pytest.fixture()
def test_response():
    return Response(test_status_code, body=test_body)


@pytest.fixture(scope='session')
def test_environ():
    return {
        'CONTENT_LENGTH': 1024,
        'wsgi.input': BytesIO(('a' * 1024).encode('utf-8')),
        'REQUEST_METHOD': 'POST',
        'PATH_INFO': '/',
        'QUERY_STRING': 'a=1&b=2&c=3'
    }


@pytest.fixture()
def test_routes():
    r1 = Route('test_path_1', 'GET', lambda req: Response(HTTP_200_OK))
    r2 = Route('test_path_1', 'POST', lambda req: Response(HTTP_201_CREATED))
    r3 = Route('test_path_2', 'DELETE', lambda req: Response(HTTP_204_NO_CONTENT))

    return [r1, r2, r3]


@pytest.fixture()
def test_app_with_no_routes():
    app = App(use_default_routes=False)
    return app


@pytest.fixture()
def test_app_with_3_routes(test_routes):
    app = App(use_default_routes=False)
    app.routes = test_routes
    return app
