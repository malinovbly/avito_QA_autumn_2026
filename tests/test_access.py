from http import HTTPStatus

import pytest

from general.checkers import assert_equal, assert_schema, assert_create_item_status
from general.schemas import GetItemResponse, CreateItemResponse


@pytest.mark.id("TC-ACCESS-001")
def test_create_item_cannot_impersonate_user(
        api_client, auth_header, registered_user_data_and_id, second_user_data_and_id, created_item_data):
    _, user_a_id = registered_user_data_and_id
    _, user_b_id = second_user_data_and_id

    body = created_item_data.copy()
    body["sellerID"] = user_b_id

    headers = auth_header.copy()
    headers["X-UserId"] = str(user_b_id)

    _, code = api_client.create_item(headers, body)

    assert_equal(code, HTTPStatus.BAD_REQUEST)


@pytest.mark.id("TC-ACCESS-002")
def test_get_item_x_user_id_does_not_change_user(
        api_client, auth_header, created_item_data_and_uuid, second_user_data_and_id):
    _, item_uuid = created_item_data_and_uuid
    _, user_b_id = second_user_data_and_id

    headers = auth_header.copy()
    headers["X-UserId"] = str(user_b_id)

    response_with_header, code_with_header = api_client.get_item(headers, item_uuid)
    response_without_header, code_without_header = api_client.get_item(auth_header, item_uuid)

    assert_equal(code_with_header, code_without_header)
    assert_equal(response_with_header, response_without_header)


@pytest.mark.id("TC-ACCESS-003")
def test_get_all_items_x_user_id_does_not_change_user(
        api_client, auth_header, registered_user_data_and_id, second_user_data_and_id):
    _, seller_id = registered_user_data_and_id
    _, user_b_id = second_user_data_and_id

    headers = auth_header.copy()
    headers["X-UserId"] = str(user_b_id)

    response_with_header, code_with_header = api_client.get_all_items(headers, seller_id)
    response_without_header, code_without_header = api_client.get_all_items(auth_header, seller_id)

    assert_equal(code_with_header, code_without_header)
    assert_equal(response_with_header, response_without_header)


@pytest.mark.id("TC-ACCESS-004")
def test_get_stats_v1_x_user_id_does_not_change_user(
        api_client, auth_header, created_item_data_and_uuid, second_user_data_and_id):
    _, item_uuid = created_item_data_and_uuid
    _, user_b_id = second_user_data_and_id

    headers = auth_header.copy()
    headers["X-UserId"] = str(user_b_id)

    response_with_header, code_with_header = api_client.get_stats_v1(headers, item_uuid)
    response_without_header, code_without_header = api_client.get_stats_v1(auth_header, item_uuid)

    assert_equal(code_with_header, code_without_header)
    assert_equal(response_with_header, response_without_header)


@pytest.mark.id("TC-ACCESS-005")
def test_get_stats_v2_x_user_id_does_not_change_user(
        api_client, auth_header, created_item_data_and_uuid, second_user_data_and_id):
    _, item_uuid = created_item_data_and_uuid
    _, user_b_id = second_user_data_and_id

    headers = auth_header.copy()
    headers["X-UserId"] = str(user_b_id)

    response_with_header, code_with_header = api_client.get_stats_v2(headers, item_uuid)
    response_without_header, code_without_header = api_client.get_stats_v2(auth_header, item_uuid)

    assert_equal(code_with_header, code_without_header)
    assert_equal(response_with_header, response_without_header)


@pytest.mark.id("TC-ACCESS-006")
def test_delete_item_cannot_impersonate_user(
        api_client, auth_header, second_user_id_and_auth_header, created_item_data):
    user_b_id, user_b_auth_header = second_user_id_and_auth_header

    item_data = created_item_data.copy()
    item_data["sellerID"] = user_b_id

    response, code = api_client.create_item(user_b_auth_header, item_data)
    assert_equal(code, HTTPStatus.OK)

    data = assert_schema(response, CreateItemResponse)
    item_uuid = assert_create_item_status(data.status)

    headers = auth_header.copy()
    headers["X-UserId"] = str(user_b_id)

    _, code = api_client.delete_item(headers, item_uuid)
    assert_equal(code, HTTPStatus.BAD_REQUEST)

    response, code = api_client.get_item(auth_header, item_uuid)
    assert_equal(code, HTTPStatus.OK)

    data = assert_schema(response, list[GetItemResponse])
    assert_equal(len(data), 1)
    assert_equal(str(data[0].id), item_uuid)
