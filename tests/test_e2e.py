from http import HTTPStatus

import pytest

from general.checkers import (
    assert_create_item_status,
    assert_equal,
    assert_not_empty_string,
    assert_schema,
)
from general.schemas import (
    AuthResponse,
    CreateItemResponse,
    GetItemResponse,
    RegisterResponse,
    StatsResponse,
)


@pytest.mark.id("TC-E2E-001")
def test_full_item_lifecycle(
    api_client, random_user_data, random_item_data, created_item_factory
):
    # 1. Регистрация пользователя
    response, code = api_client.register(random_user_data)
    assert_equal(code, HTTPStatus.CREATED)
    register_data = assert_schema(response, RegisterResponse)
    user_id = register_data.id
    assert_not_empty_string(register_data.username)

    # 2. Авторизация пользователя
    response, code = api_client.login(random_user_data)
    assert_equal(code, HTTPStatus.OK)
    auth_data = assert_schema(response, AuthResponse)
    assert_not_empty_string(auth_data.accessToken)
    assert_not_empty_string(auth_data.tokenType)
    auth_header = {"Authorization": f"Bearer {auth_data.accessToken}"}

    # 3. Создание объявления
    item_data = random_item_data.copy()
    item_data["sellerID"] = user_id
    response, code = created_item_factory(auth_header, item_data)
    assert_equal(code, HTTPStatus.OK)
    create_data = assert_schema(response, CreateItemResponse)
    item_uuid = assert_create_item_status(create_data.status)

    # 4. Получение объявления
    response, code = api_client.get_item(auth_header, item_uuid)
    assert_equal(code, HTTPStatus.OK)
    item_data_response = assert_schema(response, list[GetItemResponse])
    assert_equal(len(item_data_response), 1)
    item = item_data_response[0]
    assert_equal(str(item.id), item_uuid)
    assert_equal(item.name, item_data["name"])
    assert_equal(item.price, item_data["price"])
    assert_equal(item.sellerID, user_id)

    # 5. Получение статистики v1
    response, code = api_client.get_stats_v1(auth_header, item_uuid)
    assert_equal(code, HTTPStatus.OK)
    stats_v1 = assert_schema(response, list[StatsResponse])
    assert_equal(len(stats_v1), 1)

    # 6. Получение статистики v2
    response, code = api_client.get_stats_v2(auth_header, item_uuid)
    assert_equal(code, HTTPStatus.OK)
    stats_v2 = assert_schema(response, list[StatsResponse])
    assert_equal(len(stats_v2), 1)

    # 7. Получение списка объявлений продавца
    response, code = api_client.get_all_items(auth_header, user_id)
    assert_equal(code, HTTPStatus.OK)
    seller_items = assert_schema(response, list[GetItemResponse])
    assert any(str(item.id) == item_uuid for item in seller_items)

    # 8. Удаление объявления
    response, code = api_client.delete_item(auth_header, item_uuid)
    assert_equal(code, HTTPStatus.OK)

    # 9. Проверка удаления объявления
    response, code = api_client.get_item(auth_header, item_uuid)
    assert_equal(code, HTTPStatus.NOT_FOUND)
