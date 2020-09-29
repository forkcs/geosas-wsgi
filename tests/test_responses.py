import json

import pytest

from wsgi_rest.responses import Response, JsonResponse
from wsgi_rest.http import HTTP_200_OK


class TestResponse:
    @pytest.mark.parametrize(
        'body', [
            '',
            'abcde',
            '12345'
        ]
    )
    def test_create_valid_response(self, body, test_status_code):
        response = Response(test_status_code, body=body)
        assert response.code == test_status_code
        assert response.body == body

    @pytest.mark.parametrize(
        'code, body', [
            (200, ''),
            (None, ''),
            (b'200 OK', ''),
            (HTTP_200_OK, b'body'),
            (HTTP_200_OK, None),
            (HTTP_200_OK, 200),
            (HTTP_200_OK, [])
        ]
    )
    def test_create_invalid_response(self, code, body):
        with pytest.raises(Exception):
            Response(code, body=body)


class TestJsonResponse:
    @pytest.mark.parametrize(
        'json_data', [
            [],
            {},
            [{}],
            [{'a': 1}, {'b': 2}],
            {'a': [1, 2, 3]},
            None
        ]
    )
    def test_create_valid_json_response(self, json_data, test_status_code):
        response = JsonResponse(test_status_code, json_data=json_data)
        assert response.code == test_status_code
        if json_data is None:
            expected_body = '{}'
        else:
            expected_body = json.dumps(json_data)
        assert response.body == expected_body

    @pytest.mark.parametrize(
        'code, json_data', [
            (200, {}),
            (None, {}),
            (b'200 OK', {}),
            (HTTP_200_OK, 'data'),
            (HTTP_200_OK, 200)
        ]
    )
    def test_create_invalid_json_response(self, code, json_data):
        with pytest.raises(TypeError):
            JsonResponse(code, json_data=json_data)


class TestHeaders:
    @pytest.mark.parametrize(
        'name, value', [
            ('Connection', 'keep-alive'),
            ('123', '456'),
        ]
    )
    @pytest.mark.parametrize('response_class', (Response, JsonResponse))
    def test_set_new_valid_header(self, name, value, response_class):
        response = response_class(HTTP_200_OK)

        assert name not in response._headers.keys()
        response.set_header(name, value)
        assert response._headers[name] == value

    @pytest.mark.parametrize(
        'name, value', [
            ('Connection', None),
            (None, 'keep-alive'),
            (None, None),
            ('Name', 123)
        ]
    )
    @pytest.mark.parametrize('response_class', (Response, JsonResponse))
    def test_set_new_invalid_header(self, name, value, response_class):
        response = response_class(HTTP_200_OK)
        with pytest.raises(TypeError):
            response.set_header(name, value)
