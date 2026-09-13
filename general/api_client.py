from http import HTTPMethod
from uuid import UUID

import requests
from requests import HTTPError, JSONDecodeError

from general.paths import Auth, Item


def _make_request(method=HTTPMethod.GET, url=None, headers=None, json=None):
    try:
        response = requests.request(method, url, headers=headers, json=json)
        status_code = response.status_code
        try:
            response = response.json()
        except JSONDecodeError:
            response = response.text
        return response, status_code
    except HTTPError as e:
        raise Exception(f"unexpected error: {e}") from e


class ApiClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def _make_url(self, path, **kwargs):
        if kwargs:
            return (self.base_url + path).format(**kwargs)
        return self.base_url + path

    def register(self, body: dict):
        path = Auth.REGISTER
        url = self._make_url(path.path)
        return _make_request(method=path.method, url=url, json=body)

    def login(self, body: dict):
        path = Auth.LOGIN
        url = self._make_url(path.path)
        return _make_request(method=path.method, url=url, json=body)

    def create_item(self, headers: dict, body: dict):
        path = Item.CREATE
        url = self._make_url(path.path)
        return _make_request(method=path.method, url=url, headers=headers, json=body)

    def get_item(self, headers: dict, item_id: UUID):
        path = Item.GET
        url = self._make_url(path.path, id=item_id)
        return _make_request(method=path.method, url=url, headers=headers)

    def get_all_items(self, headers: dict, seller_id: UUID):
        path = Item.GET_ALL
        url = self._make_url(path.path, sellerID=seller_id)
        return _make_request(method=path.method, url=url, headers=headers)

    def get_stats_v1(self, headers: dict, item_id: UUID):
        path = Item.STATS_V1
        url = self._make_url(path.path, id=item_id)
        return _make_request(method=path.method, url=url, headers=headers)

    def get_stats_v2(self, headers: dict, item_id: UUID):
        path = Item.STATS_V2
        url = self._make_url(path.path, id=item_id)
        return _make_request(method=path.method, url=url, headers=headers)

    def delete_item(self, headers: dict, item_id: UUID):
        path = Item.DELETE
        url = self._make_url(path.path, id=item_id)
        return _make_request(method=path.method, url=url, headers=headers)
