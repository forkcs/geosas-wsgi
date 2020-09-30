from wsgiref.simple_server import make_server
from threading import Thread, Event

import requests

from wsgi_rest import App
from wsgi_rest.http import HTTP_200_OK
from wsgi_rest.responses import Response


def test_simple_full_cycle():

    # Make application
    app = App(use_default_routes=False)

    # create view
    @app.route('/test_path', 'GET')
    def view(request):
        if 'hello' in request.query_params:
            data = '<h1>Hello, user!</h1>'
        else:
            data = 'Say hello to me'

        return Response(HTTP_200_OK, body=data)

    wsgi_app = app.get_application()

    started = Event()
    stop_server = Event()

    def start_server():
        with make_server('', 8000, wsgi_app) as httpd:
            started.set()
            while not stop_server.is_set():
                httpd.handle_request()
    Thread(target=start_server).start()

    started.wait()
    resp = requests.get('http://localhost:8000/test_path')
    assert resp.text == 'Say hello to me'

    resp = requests.get('http://localhost:8000/test_path?hello=1')
    assert resp.text == '<h1>Hello, user!</h1>'

    stop_server.set()
