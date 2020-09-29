from wsgiref.simple_server import make_server

from wsgi_rest import App
from wsgi_rest.http import HTTP_200_OK
from wsgi_rest.responses import Response, JsonResponse

app = App(use_default_routes=False)


@app.route('/echo', 'GET')
def echo_view(request):
    return Response(code=HTTP_200_OK, body=f'{request.query_params}')


@app.route('/echo', 'POST')
def echo_json_view(request):
    return JsonResponse(code=HTTP_200_OK, json_data={'request_body': request.body})


# make wsgi-compatible application, which should be passed to wsgi server
application = app.get_application()

with make_server('', 8000, application) as httpd:
    print('Listening on 8000 port...')
    httpd.serve_forever()
