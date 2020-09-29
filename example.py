from wsgi_rest.application import App
from wsgi_rest.responses import Response, JsonResponse
from wsgi_rest.http import HTTP_200_OK

app = App()


@app.route('/echo', 'GET')
def echo_view(request):
    return Response(code=HTTP_200_OK, body=f'{request.query_params}')


@app.route('/echo', 'POST')
def echo_view(request):
    return JsonResponse(code=HTTP_200_OK, json_data={'request_body': request.query_params})


application = app.get_application()
