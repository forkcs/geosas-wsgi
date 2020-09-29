import json
from typing import Union, Dict

from wsgi_rest.http import HTTP_200_OK, HTTP_404_NOT_FOUND


__all__ = ['Response', 'JsonResponse', 'ERROR_404', 'HELLO_WORLD']


def get_default_headers() -> Dict[str, str]:
    headers = {
        'Server': 'GEOSAS'
    }
    return headers


class BaseResponse:
    def __init__(self, code: str):
        if not isinstance(code, str):
            raise TypeError('code must be a string.')
        self.code = code

        self._headers: Dict[str, str] = get_default_headers()

    def set_header(self, name: str, value: str) -> None:
        """Add new header or replace existing."""

        if not isinstance(name, str):
            raise TypeError('name must be a string.')
        if not isinstance(value, str):
            raise TypeError('value must be a string.')

        self._headers[name] = value


class Response(BaseResponse):
    def __init__(self, *args, body: str = '', **kwargs):
        super().__init__(*args, **kwargs)

        if not isinstance(body, str):
            raise TypeError('body must be a string')

        self.body = body


class JsonResponse(BaseResponse):
    def __init__(self, *args, json_data: Union[list, dict] = None, **kwargs):
        super().__init__(*args, **kwargs)

        if json_data is None:
            json_data = {}

        if not isinstance(json_data, (list, dict)):
            raise TypeError('json_data must be either list or dictionary.')

        self.json_data = json_data

    @property
    def body(self) -> str:
        return json.dumps(self.json_data)


HELLO_WORLD = JsonResponse(code=HTTP_200_OK, json_data={'message': 'Have an exciting hackaton!\nWith <3, by GEOSAS'})
ERROR_404 = Response(code=HTTP_404_NOT_FOUND, body='URL NOT FOUND')
