from http import HTTPStatus

import pytest

from general.checkers import assert_equal, assert_not_empty_string, assert_schema
from general.schemas import AuthResponse


@pytest.mark.id("TC-AUTH-001")
def test_authorize_success(api_client, registered_user_data_and_id):
    data, _ = registered_user_data_and_id

    response, code = api_client.login(data)

    assert_equal(code, HTTPStatus.OK)

    data = assert_schema(response, AuthResponse)
    assert_not_empty_string(data.accessToken)
    assert_equal(data.tokenType, "Bearer")


@pytest.mark.id("TC-AUTH-002")
def test_authorize_wrong_password(
    api_client, registered_user_data_and_id, wrong_password
):
    registered_user_data, _ = registered_user_data_and_id

    data = registered_user_data.copy()
    data["password"] = wrong_password

    _, code = api_client.login(data)

    assert_equal(code, HTTPStatus.UNAUTHORIZED)


@pytest.mark.id("TC-AUTH-003")
def test_authorize_not_existing_user(api_client, random_user_data):
    _, code = api_client.login(random_user_data)

    assert_equal(code, HTTPStatus.UNAUTHORIZED)


@pytest.mark.parametrize(
    "field_to_remove",
    [
        pytest.param("username", id="TC-AUTH-004"),
        pytest.param("password", id="TC-AUTH-005"),
    ],
)
def test_authorize_partial_body(
    api_client, registered_user_data_and_id, field_to_remove
):
    registered_user_data, _ = registered_user_data_and_id

    data = registered_user_data.copy()
    data.pop(field_to_remove)

    _, code = api_client.login(data)

    assert_equal(code, HTTPStatus.BAD_REQUEST)
