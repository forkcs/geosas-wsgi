import json
from dataclasses import dataclass, field
from typing import List, Tuple


def get_default_headers() -> List[Tuple[str, str]]:
    headers = [
        ('Server', 'GEOSAS'),
        ('Connection', 'keep-alive')
    ]
    return headers


@dataclass
class Response:
    code: str
    body: str = ''
    headers: List[Tuple[str, str]] = field(default_factory=get_default_headers)


@dataclass
class JsonResponse:
    code: str
    json_dict: dict = field(default_factory=lambda: {})
    headers: List[Tuple[str, str]] = field(default_factory=get_default_headers)

    @property
    def body(self) -> str:
        return json.dumps(self.json_dict)


HELLO_WORLD = JsonResponse(code='200', json_dict={'message': 'Have an exciting hackaton!\nWith <3, by GEOSAS'})
ERROR_404 = Response(code='404', body='URL NOT FOUND')
