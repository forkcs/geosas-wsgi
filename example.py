from application import App
from response import Response, JsonResponse

app = App()


@app.route('/echo', 'GET')
def echo_view(request):
    return Response(code='200', body=f'{request["query_params"]}')


@app.route('/echo', 'POST')
def echo_view(request):
    return JsonResponse(code='200', json_dict={'request_body': request["body"]})


application = app.get_application()
