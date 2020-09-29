from unittest.mock import Mock

import pytest

from wsgi_rest import App
from wsgi_rest.application import get_request_from_environ, Request, DEFAULT_ROUTES
from wsgi_rest.responses import ERROR_404
from wsgi_rest.routes import Route


def test_get_request_from_environ(test_environ):
    request = get_request_from_environ(test_environ)
    assert request.method == 'POST'
    assert request.path == '/'
    assert request.body == 'a' * 1024
    assert request.query_params == {'a': ['1'], 'b': ['2'], 'c': ['3']}


def test_value_error_in_get_request_from_environ(test_environ):
    test_environ['CONTENT_LENGTH'] = 'bad_data'  # should be setted to 0
    request = get_request_from_environ(test_environ)
    assert request.method == 'POST'
    assert request.path == '/'
    assert request.body == ''
    assert request.query_params == {'a': ['1'], 'b': ['2'], 'c': ['3']}


@pytest.mark.parametrize(
    'path, method, expected', [
        ('test_path_1', 'GET', True),
        ('test_path_1', 'POST', True),
        ('test_path_2', 'DELETE', True),
        ('test_path_1', 'PUT', False),
        ('bad_path', 'GET', False),
        ('test_path_2', 'GET', False)
    ]
)
def test_route_exists(path, method, expected, test_app_with_3_routes):
    assert test_app_with_3_routes.route_exists(path, method) == expected


def test_get_existing_route(test_routes, test_app_with_3_routes):
    for route, expected in zip(test_app_with_3_routes.routes, test_routes):
        assert test_app_with_3_routes.get_route(expected.path, expected.method) == route


@pytest.mark.parametrize(
    'path, method', [
        ('test_path_1', 'BAD_METHOD'),
        ('test_path_2', 'BAD_METHOD'),
        ('bad_path', 'GET'),
        ('bad_path', 'POST')
    ]
)
def test_get_unexisting_route(path, method, test_app_with_3_routes):
    with pytest.raises(ValueError):
        test_app_with_3_routes.get_route(path, method)


@pytest.mark.parametrize(
    'use_default_routes, expected', [
        (True, DEFAULT_ROUTES),
        (False, [])
    ]
)
def test_default_routes(use_default_routes, expected):
    app = App(use_default_routes=use_default_routes)

    assert app.routes == expected


def test_dispatch(test_app_with_no_routes):
    handler = Mock()
    new_route = Route('/', 'POST', handler)
    test_app_with_no_routes.routes.append(new_route)

    request = Request(method='POST', path='/', query_params={}, body='')
    test_app_with_no_routes.dispatch(request)

    handler.assert_called_once_with(request)


def test_dispatch_404(test_app_with_no_routes):
    request = Request(method='POST', path='/', query_params={}, body='')
    response = test_app_with_no_routes.dispatch(request)

    assert response == ERROR_404


def test_get_application(test_app_with_no_routes, test_environ):
    wsgi_app = test_app_with_no_routes.get_application()
    assert hasattr(wsgi_app, '__call__')

    start_response = Mock()
    resp = wsgi_app(test_environ, start_response)

    assert isinstance(resp, list)
    start_response.assert_called_once()
