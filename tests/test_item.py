from http import HTTPStatus

import pytest

from general.checkers import (
    assert_create_item_status,
    assert_equal,
    assert_not_equal,
    assert_schema,
)
from general.schemas import CreateItemResponse, GetItemResponse

# region Create Item


@pytest.mark.id("TC-ITEM-001")
def test_create_item_success(created_item_factory, auth_header, created_item_data):
    response, code = created_item_factory(auth_header, created_item_data)

    assert_equal(code, HTTPStatus.OK)

    data = assert_schema(response, CreateItemResponse)
    assert_create_item_status(data.status)


@pytest.mark.id("TC-ITEM-002")
def test_create_item_another_user_id(
    api_client, auth_header, second_user_data_and_id, created_item_data
):
    _, second_user_id = second_user_data_and_id

    data = {**created_item_data, "sellerID": second_user_id}
    _, code = api_client.create_item(auth_header, data)

    assert_equal(code, HTTPStatus.BAD_REQUEST)


@pytest.mark.id("TC-ITEM-003")
def test_create_item_without_auth_token(
    created_item_factory, auth_header, created_item_data
):
    _, code = created_item_factory({}, created_item_data, cleanup_headers=auth_header)

    assert_equal(code, HTTPStatus.UNAUTHORIZED)


@pytest.mark.id("TC-ITEM-004")
def test_create_item_with_invalid_auth_token(
    created_item_factory,
    auth_header,
    auth_header_with_bad_access_token,
    created_item_data,
):
    _, code = created_item_factory(
        auth_header_with_bad_access_token,
        created_item_data,
        cleanup_headers=auth_header,
    )

    assert_equal(code, HTTPStatus.UNAUTHORIZED)


@pytest.mark.parametrize(
    "field_to_remove",
    [
        pytest.param("sellerID", id="TC-ITEM-005"),
        pytest.param("name", id="TC-ITEM-006"),
        pytest.param("price", id="TC-ITEM-007"),
        pytest.param("statistics", id="TC-ITEM-008"),
        pytest.param("likes", id="TC-ITEM-009"),
        pytest.param("viewCount", id="TC-ITEM-010"),
        pytest.param("contacts", id="TC-ITEM-011"),
    ],
)
def test_create_item_partial_body(
    created_item_factory, auth_header, created_item_data, field_to_remove
):
    data = created_item_data.copy()

    if field_to_remove in ("likes", "viewCount", "contacts"):
        data["statistics"] = data["statistics"].copy()
        data["statistics"].pop(field_to_remove)
    else:
        data.pop(field_to_remove)

    _, code = created_item_factory(auth_header, data)

    assert_equal(code, HTTPStatus.BAD_REQUEST)


@pytest.mark.id("TC-ITEM-012")
def test_create_same_item_twice(created_item_factory, auth_header, created_item_data):
    response1, code1 = created_item_factory(auth_header, created_item_data)
    assert_equal(code1, HTTPStatus.OK)

    response2, code2 = created_item_factory(auth_header, created_item_data)
    assert_equal(code2, HTTPStatus.OK)

    data1 = assert_schema(response1, CreateItemResponse)
    uuid1 = assert_create_item_status(data1.status)

    data2 = assert_schema(response2, CreateItemResponse)
    uuid2 = assert_create_item_status(data2.status)

    assert_not_equal(uuid1, uuid2)


@pytest.mark.id("TC-ITEM-013")
def test_item_uuid_uniqueness(created_item_factory, auth_header, created_item_data):
    uuids = set()

    for _ in range(5):
        body = created_item_data.copy()

        response, code = created_item_factory(auth_header, body)

        assert_equal(code, HTTPStatus.OK)

        data = assert_schema(response, CreateItemResponse)
        uuid = assert_create_item_status(data.status)

        assert uuid not in uuids
        uuids.add(uuid)

    assert_equal(len(uuids), 5)


# endregion

# region Get Item


@pytest.mark.id("TC-GET-ITEM-001")
def test_get_item_success(api_client, auth_header, created_item_data_and_uuid):
    item_data, item_uuid = created_item_data_and_uuid
    response, code = api_client.get_item(auth_header, item_uuid)

    assert_equal(code, HTTPStatus.OK)

    data = assert_schema(response, list[GetItemResponse])
    assert_equal(len(data), 1)

    item = data[0]

    assert_equal(str(item.id), item_uuid)
    assert_equal(item.sellerID, item_data["sellerID"])
    assert_equal(item.name, item_data["name"])
    assert_equal(item.price, item_data["price"])
    assert_equal(item.statistics, item_data["statistics"])


@pytest.mark.id("TC-GET-ITEM-002")
def test_get_item_not_exists(api_client, auth_header, random_uuid4):
    _, code = api_client.get_item(auth_header, random_uuid4)

    assert_equal(code, HTTPStatus.NOT_FOUND)


@pytest.mark.id("TC-GET-ITEM-003")
def test_get_item_bad_uuid(api_client, auth_header, random_string):
    _, code = api_client.get_item(auth_header, random_string)

    assert_equal(code, HTTPStatus.BAD_REQUEST)


@pytest.mark.id("TC-GET-ITEM-004")
def test_get_item_unauthorized(api_client, created_item_data_and_uuid):
    _, item_uuid = created_item_data_and_uuid

    _, code = api_client.get_item({}, item_uuid)

    assert_equal(code, HTTPStatus.UNAUTHORIZED)


# endregion
