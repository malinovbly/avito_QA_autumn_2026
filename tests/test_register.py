from http import HTTPStatus

import pytest

from general.checkers import assert_equal, assert_schema
from general.schemas import RegisterResponse


@pytest.mark.id("TC-REG-001")
def test_register_success(api_client, random_user_data):
    response, code = api_client.register(random_user_data)

    assert_equal(code, HTTPStatus.CREATED)

    data = assert_schema(response, RegisterResponse)

    assert_equal(data.username, random_user_data.get("username"))


@pytest.mark.id("TC-REG-002")
def test_register_duplicated_username(
    api_client, random_user_data, registered_user_data_and_id
):
    user_data, _ = registered_user_data_and_id

    _, code = api_client.register(user_data)

    assert_equal(code, HTTPStatus.CONFLICT)


@pytest.mark.parametrize(
    "field_to_remove",
    [
        pytest.param("username", id="TC-REG-003"),
        pytest.param("password", id="TC-REG-004"),
    ],
)
def test_register_partial_body(api_client, random_user_data, field_to_remove):
    data = random_user_data.copy()
    data.pop(field_to_remove)

    _, code = api_client.register(data)

    assert_equal(code, HTTPStatus.BAD_REQUEST)


@pytest.mark.parametrize(
    "field_to_clear",
    [
        pytest.param("username", id="TC-REG-005"),
        pytest.param("password", id="TC-REG-006"),
    ],
)
def test_register_invalid_body(api_client, random_user_data, field_to_clear):
    data = random_user_data.copy()
    data[field_to_clear] = ""

    _, code = api_client.register(data)

    assert_equal(code, HTTPStatus.BAD_REQUEST)
