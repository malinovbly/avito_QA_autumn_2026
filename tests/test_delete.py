from http import HTTPStatus

import pytest

from general.checkers import assert_equal


@pytest.mark.id("TC-DELETE-001")
def test_delete_item_success(api_client, auth_header, created_item_data_and_uuid):
    _, item_uuid = created_item_data_and_uuid

    _, code = api_client.delete_item(auth_header, item_uuid)
    assert_equal(code, HTTPStatus.OK)

    _, code = api_client.get_item(auth_header, item_uuid)
    assert_equal(code, HTTPStatus.NOT_FOUND)


@pytest.mark.id("TC-DELETE-002")
def test_delete_item_not_exists(api_client, auth_header, random_uuid4):
    _, code = api_client.delete_item(auth_header, random_uuid4)

    assert_equal(code, HTTPStatus.NOT_FOUND)


@pytest.mark.id("TC-DELETE-003")
def test_delete_item_unauthorized(api_client, auth_header, created_item_data_and_uuid):
    _, item_uuid = created_item_data_and_uuid

    _, code = api_client.delete_item({}, item_uuid)
    assert_equal(code, HTTPStatus.UNAUTHORIZED)

    _, code = api_client.get_item(auth_header, item_uuid)
    assert_equal(code, HTTPStatus.OK)


@pytest.mark.id("TC-DELETE-004")
def test_delete_item_bad_access_token(
    api_client,
    auth_header,
    auth_header_with_bad_access_token,
    created_item_data_and_uuid,
):
    _, item_uuid = created_item_data_and_uuid

    _, code = api_client.delete_item(auth_header_with_bad_access_token, item_uuid)
    assert_equal(code, HTTPStatus.UNAUTHORIZED)

    _, code = api_client.get_item(auth_header, item_uuid)
    assert_equal(code, HTTPStatus.OK)


@pytest.mark.id("TC-DELETE-005")
def test_delete_another_user_item(
    api_client, auth_header, created_item_data_and_uuid, second_user_data_and_id
):
    _, item_uuid = created_item_data_and_uuid
    _, second_user_id = second_user_data_and_id

    second_user_auth_header = auth_header.copy()
    second_user_auth_header["Authorization"] = f"Bearer {second_user_id}"

    _, code = api_client.delete_item(second_user_auth_header, item_uuid)
    assert_equal(code, HTTPStatus.UNAUTHORIZED)

    _, code = api_client.get_item(auth_header, item_uuid)
    assert_equal(code, HTTPStatus.OK)


@pytest.mark.id("TC-DELETE-006")
def test_delete_item_twice(api_client, auth_header, created_item_data_and_uuid):
    _, item_uuid = created_item_data_and_uuid

    _, code = api_client.delete_item(auth_header, item_uuid)
    assert_equal(code, HTTPStatus.OK)

    _, code = api_client.delete_item(auth_header, item_uuid)
    assert_equal(code, HTTPStatus.NOT_FOUND)
