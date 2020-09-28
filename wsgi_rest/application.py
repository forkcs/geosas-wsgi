from functools import wraps
from typing import Callable, Tuple
from urllib.parse import parse_qs

from wsgi_rest.response import ERROR_404, HELLO_WORLD


def get_request_dict_from_environ(environ: dict) -> dict:
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except ValueError:
        request_body_size = 0
    request_body = environ['wsgi.input'].read(request_body_size).decode('utf-8')
    method = environ['REQUEST_METHOD']
    path = environ.get('PATH_INFO', '/')
    query_string = environ.get('QUERY_STRING', '')
    query_params = parse_qs(query_string)

    request = {'method': method, 'path': path, 'query_params': query_params, 'body': request_body}
    return request


class App:
    def __init__(self):
        self.routes = [('/', 'GET', lambda req: HELLO_WORLD)]

    def route(self, path: str, method: str):
        def wrapper(view: Callable):
            @wraps(view)
            def wrapped(*args, **kwargs):
                return view(*args, **kwargs)
            if self.route_exists(path, method):
                route_to_replace = list(filter(lambda r: r[0] == path and r[1] == method, self.routes))[0]
                self.routes.remove(route_to_replace)
            self.routes.append((path, method, view))
            return wrapped
        return wrapper

    def route_exists(self, path: str, method: str) -> bool:
        existing_routes = [r[:2] for r in self.routes]
        if (path, method) in existing_routes:
            return True
        return False

    def get_route(self, path: str, method: str) -> Tuple[str, str, Callable]:
        for route in self.routes:
            if route[0] == path and route[1] == method:
                return route
        raise ValueError(f'Path {method, path} does not exists.')

    def dispatch(self, request: dict):
        """Find and pass request to appropriate handler.

        If there is no such handler, return 404 response.
        """

        try:
            route = self.get_route(request['path'], request['method'])
        except ValueError:
            return ERROR_404
        view = route[2]
        return view(request)

    def get_application(self):
        def wsgi_application(environ, start_response):
            request = get_request_dict_from_environ(environ)
            response = self.dispatch(request)
            headers = response.headers
            status_code = response.code
            start_response(status_code, headers)
            return response.body.encode('utf-8')
        return wsgi_application
