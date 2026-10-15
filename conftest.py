from copy import deepcopy
from http import HTTPStatus

import pytest

from general.api_client import ApiClient
from general.checkers import (
    assert_create_item_status,
    assert_equal,
    assert_not_empty_string,
    assert_schema,
)
from general.config import BASE_URL
from general.schemas import AuthResponse, CreateItemResponse, RegisterResponse
from general.utils import (
    make_random_item_name,
    make_random_string,
    make_random_username,
    make_random_uuid4,
)


@pytest.fixture
def api_client():
    return ApiClient(BASE_URL)


@pytest.fixture
def random_string():
    return make_random_string()


@pytest.fixture
def random_username():
    return make_random_username()


@pytest.fixture
def random_item_name():
    return make_random_item_name()


@pytest.fixture
def random_uuid4():
    return make_random_uuid4()


@pytest.fixture
def password():
    return "strong-password"


@pytest.fixture
def wrong_password():
    return "wrong-password"


@pytest.fixture
def random_user_data(random_username, password):
    return {
        "username": random_username,
        "password": password,
    }


@pytest.fixture
def item_statistics():
    return {
        "likes": 21,
        "viewCount": 11,
        "contacts": 43,
    }


@pytest.fixture
def random_item_data(random_item_name, item_statistics):
    return {
        "sellerID": "user_id",
        "name": random_item_name,
        "price": 9900,
        "statistics": item_statistics.copy(),
    }


@pytest.fixture
def created_item_data(registered_user_data_and_id, random_item_name, item_statistics):
    _, user_id = registered_user_data_and_id
    return {
        "sellerID": user_id,
        "name": random_item_name,
        "price": 9900,
        "statistics": item_statistics.copy(),
    }


@pytest.fixture
def registered_user_data_and_id(api_client, random_user_data):
    response, code = api_client.register(random_user_data)
    assert_equal(code, HTTPStatus.CREATED)

    data = assert_schema(response, RegisterResponse)
    assert_equal(data.username, random_user_data["username"])

    return random_user_data, data.id


@pytest.fixture
def second_user_data_and_id(api_client, password):
    user_data = {
        "username": make_random_username(),
        "password": password,
    }

    response, code = api_client.register(user_data)
    assert_equal(code, HTTPStatus.CREATED)

    data = assert_schema(response, RegisterResponse)
    assert_equal(data.username, user_data["username"])

    return user_data, data.id


@pytest.fixture
def second_user_id_and_auth_header(api_client, second_user_data_and_id):
    user_data, user_id = second_user_data_and_id

    response, code = api_client.login(user_data)
    assert_equal(code, HTTPStatus.OK)

    auth_data = assert_schema(response, AuthResponse)
    assert_not_empty_string(auth_data.accessToken)

    auth_header = {
        "Authorization": f"Bearer {auth_data.accessToken}",
    }

    return user_id, auth_header


@pytest.fixture
def access_token(api_client, registered_user_data_and_id):
    data, _ = registered_user_data_and_id
    response, code = api_client.login(data)

    assert_equal(code, HTTPStatus.OK)
    data = assert_schema(response, AuthResponse)
    assert_not_empty_string(data.accessToken)

    return data.accessToken


@pytest.fixture
def auth_header(access_token):
    return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture
def auth_header_with_bad_access_token(random_string):
    return {"Authorization": f"Bearer {random_string}"}


@pytest.fixture
def created_item_factory(api_client):
    created_items = []

    def create_item(headers, item_data, cleanup_headers=None):
        response, code = api_client.create_item(headers, item_data)

        if code == HTTPStatus.OK:
            data = assert_schema(response, CreateItemResponse)
            item_uuid = assert_create_item_status(data.status)

            headers_for_cleanup = (
                cleanup_headers if cleanup_headers is not None else headers
            )

            created_items.append((headers_for_cleanup.copy(), item_uuid))

        return response, code

    yield create_item

    errors = []

    for headers, item_uuid in reversed(created_items):
        try:
            _, code = api_client.delete_item(headers, item_uuid)

            if code not in (HTTPStatus.OK, HTTPStatus.NOT_FOUND):
                errors.append(f"{item_uuid}: unexpected status {code}")

        except Exception as e:
            errors.append(f"{item_uuid}: {e}")

    if errors:
        pytest.fail(f"Failed to clean up items: {errors}")


@pytest.fixture
def created_item_data_and_uuid(created_item_factory, auth_header, created_item_data):
    response, code = created_item_factory(auth_header, created_item_data)
    assert_equal(code, HTTPStatus.OK)

    data = assert_schema(response, CreateItemResponse)
    item_uuid = assert_create_item_status(data.status)

    return created_item_data, item_uuid


@pytest.fixture
def created_items_data_and_uuids(created_item_factory, auth_header, created_item_data):
    created_items = []

    for i in range(3):
        item_data = deepcopy(created_item_data)
        item_data["name"] += f"_{i}"

        response, code = created_item_factory(auth_header, item_data)
        assert_equal(code, HTTPStatus.OK)

        data = assert_schema(response, CreateItemResponse)
        item_uuid = assert_create_item_status(data.status)

        created_items.append((item_data, item_uuid))

    return created_items
