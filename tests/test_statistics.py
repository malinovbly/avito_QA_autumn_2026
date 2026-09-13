from http import HTTPStatus

import pytest

from general.checkers import assert_equal, assert_schema
from general.schemas import StatsResponse

# region Stats v1


@pytest.mark.id("TC-STAT-V1-001")
def test_get_stats_v1_success(api_client, auth_header, created_item_data_and_uuid):
    item_data, item_uuid = created_item_data_and_uuid

    response, code = api_client.get_stats_v1(auth_header, item_uuid)

    assert_equal(code, HTTPStatus.OK)

    data = assert_schema(response, list[StatsResponse])
    assert_equal(len(data), 1)

    statistics = data[0]

    assert_equal(statistics.contacts, item_data["statistics"]["contacts"])
    assert_equal(statistics.likes, item_data["statistics"]["likes"])
    assert_equal(statistics.viewCount, item_data["statistics"]["viewCount"])


@pytest.mark.id("TC-STAT-V1-002")
def test_get_stats_v1_item_not_exists(api_client, auth_header, random_uuid4):
    _, code = api_client.get_stats_v1(auth_header, random_uuid4)

    assert_equal(code, HTTPStatus.NOT_FOUND)


@pytest.mark.id("TC-STAT-V1-003")
def test_get_stats_v1_unauthorized(api_client, created_item_data_and_uuid):
    _, item_uuid = created_item_data_and_uuid

    _, code = api_client.get_stats_v1({}, item_uuid)

    assert_equal(code, HTTPStatus.UNAUTHORIZED)


@pytest.mark.id("TC-STAT-V1-004")
def test_get_stats_v1_invalid_id(api_client, auth_header):
    invalid_item_id = "invalid"

    _, code = api_client.get_stats_v1(auth_header, invalid_item_id)

    assert_equal(code, HTTPStatus.BAD_REQUEST)


# endregion

# region Stats v2


@pytest.mark.id("TC-STAT-V2-001")
def test_get_stats_v2_success(api_client, auth_header, created_item_data_and_uuid):
    item_data, item_uuid = created_item_data_and_uuid

    response, code = api_client.get_stats_v2(auth_header, item_uuid)

    assert_equal(code, HTTPStatus.OK)

    data = assert_schema(response, list[StatsResponse])
    assert_equal(len(data), 1)

    statistics = data[0]

    assert_equal(statistics.contacts, item_data["statistics"]["contacts"])
    assert_equal(statistics.likes, item_data["statistics"]["likes"])
    assert_equal(statistics.viewCount, item_data["statistics"]["viewCount"])


@pytest.mark.id("TC-STAT-V2-002")
def test_get_stats_v2_item_not_exists(api_client, auth_header, random_uuid4):
    _, code = api_client.get_stats_v2(auth_header, random_uuid4)

    assert_equal(code, HTTPStatus.NOT_FOUND)


@pytest.mark.id("TC-STAT-V2-003")
def test_get_stats_v2_unauthorized(api_client, created_item_data_and_uuid):
    _, item_uuid = created_item_data_and_uuid

    _, code = api_client.get_stats_v2({}, item_uuid)

    assert_equal(code, HTTPStatus.UNAUTHORIZED)


@pytest.mark.id("TC-STAT-V2-004")
def test_get_stats_v2_invalid_id(api_client, auth_header):
    invalid_item_id = "invalid"

    _, code = api_client.get_stats_v2(auth_header, invalid_item_id)

    assert_equal(code, HTTPStatus.NOT_FOUND)


@pytest.mark.id("TC-STAT-V2-005")
def test_get_stats_v2_matches_v1(api_client, auth_header, created_item_data_and_uuid):
    item_data, item_uuid = created_item_data_and_uuid

    response_v1, code_v1 = api_client.get_stats_v1(auth_header, item_uuid)
    assert_equal(code_v1, HTTPStatus.OK)

    response_v2, code_v2 = api_client.get_stats_v2(auth_header, item_uuid)
    assert_equal(code_v2, HTTPStatus.OK)

    data_v1 = assert_schema(response_v1, list[StatsResponse])
    assert_equal(len(data_v1), 1)

    data_v2 = assert_schema(response_v2, list[StatsResponse])
    assert_equal(len(data_v2), 1)

    assert_equal(data_v1[0], data_v2[0])

    expected_statistics = item_data["statistics"]

    assert_equal(data_v2[0].contacts, expected_statistics["contacts"])
    assert_equal(data_v2[0].likes, expected_statistics["likes"])
    assert_equal(data_v2[0].viewCount, expected_statistics["viewCount"])


# endregion
