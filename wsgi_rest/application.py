from collections import namedtuple
from functools import wraps
from typing import Callable
from urllib.parse import parse_qs

from wsgi_rest.responses import ERROR_404, HELLO_WORLD


class Route(namedtuple('Route', ('path', 'method', 'handler'))):

    def __eq__(self, other):
        if self.path == other.path and self.method == other.method:
            return True
        return False


Request = namedtuple('Request', [
    'method',
    'path',
    'query_params',
    'body'
])


def get_request_from_environ(environ: dict) -> Request:
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except ValueError:
        request_body_size = 0
    request_body = environ['wsgi.input'].read(request_body_size).decode('utf-8')
    method = environ['REQUEST_METHOD']
    path = environ.get('PATH_INFO', '/')
    query_string = environ.get('QUERY_STRING', '')
    query_params = parse_qs(query_string)

    request = Request(
        method=method,
        path=path,
        query_params=query_params,
        body=request_body
    )
    return request


DEFAULT_ROUTES = [
    Route(path='/', method='POST', handler=lambda req: HELLO_WORLD)
]


class App:
    """Represents wsgi-application."""

    def __init__(self, use_default_routes: bool = True):
        self.routes = []
        if use_default_routes:
            self.routes.extend(DEFAULT_ROUTES)

    def route(self, path: str, method: str):
        def wrapper(view: Callable):
            @wraps(view)
            def wrapped(*args, **kwargs):
                return view(*args, **kwargs)

            if self.route_exists(path, method):
                route_to_replace = self.get_route(path, method)
                self.routes.remove(route_to_replace)
            self.routes.append(Route(path, method, view))
            return wrapped

        return wrapper

    def route_exists(self, path: str, method: str) -> bool:
        if Route(path, method, None) in self.routes:
            return True
        return False

    def get_route(self, path: str, method: str) -> Route:
        route_to_find = Route(path, method, None)
        for route in self.routes:
            if route == route_to_find:
                return route
        raise ValueError(f'Path {method, path} does not exists.')

    def dispatch(self, request: Request):
        """Find and pass request to appropriate handler.

        If there is no such handler, return 404 response.
        """

        try:
            route = self.get_route(request.path, request.method)
        except ValueError:
            return ERROR_404
        view = route.handler
        return view(request)

    def get_application(self):
        def wsgi_application(environ, start_response):
            request = get_request_from_environ(environ)
            response = self.dispatch(request)
            headers = response.headers.items()
            status_code = response.code
            start_response(status_code, headers)
            return response.body.encode('utf-8')

        return wsgi_application
