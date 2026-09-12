from http import HTTPStatus

import pytest

from general.checkers import assert_equal, assert_schema
from general.schemas import GetItemResponse


@pytest.mark.id("TC-SELLER-001")
def test_get_all_items_success(
        api_client, auth_header, registered_user_data_and_id, created_items_data_and_uuids):
    _, seller_id = registered_user_data_and_id

    response, code = api_client.get_all_items(auth_header, seller_id)

    assert_equal(code, HTTPStatus.OK)

    data = assert_schema(response, list[GetItemResponse])

    expected_uuids = {item_uuid for _, item_uuid in created_items_data_and_uuids}
    actual_uuids = {str(item.id) for item in data}

    for item in data:
        assert_equal(item.sellerID, seller_id)

    assert expected_uuids.issubset(actual_uuids), (
        f"Created items are missing. "
        f"Expected: {expected_uuids}, actual: {actual_uuids}"
    )


@pytest.mark.id("TC-SELLER-002")
def test_get_all_items_zero_count(api_client, auth_header, registered_user_data_and_id):
    _, seller_id = registered_user_data_and_id

    response, code = api_client.get_all_items(auth_header, seller_id)
    assert_equal(code, HTTPStatus.OK)

    data = assert_schema(response, list[GetItemResponse])
    assert_equal(data, [])


@pytest.mark.id("TC-SELLER-003")
def test_get_all_items_user_not_exists(api_client, auth_header):
    nonexistent_seller_id = 99999999

    _, code = api_client.get_all_items(auth_header, nonexistent_seller_id)

    assert_equal(code, HTTPStatus.NOT_FOUND)


@pytest.mark.id("TC-SELLER-004")
def test_get_all_items_unauthorized(api_client, registered_user_data_and_id):
    _, seller_id = registered_user_data_and_id

    _, code = api_client.get_all_items({}, seller_id)

    assert_equal(code, HTTPStatus.UNAUTHORIZED)


@pytest.mark.id("TC-SELLER-005")
def test_get_all_items_invalid_seller_id(api_client, auth_header):
    invalid_seller_id = "invalid"

    _, code = api_client.get_all_items(auth_header, invalid_seller_id)

    assert_equal(code, HTTPStatus.BAD_REQUEST)
