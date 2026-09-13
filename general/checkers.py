from uuid import UUID

from pydantic import TypeAdapter, ValidationError


def assert_equal(actual, expected):
    assert actual == expected, f"Actual result: {actual}\tExpected result: {expected}"


def assert_not_equal(actual, expected):
    assert actual != expected, f"Actual result: {actual}\tExpected different results"


def assert_isinstance(actual, expected):
    assert isinstance(actual, expected), (
        f"Actual result: {actual}\tExpected result: {expected}"
    )


def assert_not_empty_string(actual):
    assert isinstance(actual, str), f"Expected string, got: {type(actual).__name__}"
    assert actual != "", "Expected non-empty string"


def assert_not_in_response(response, key):
    assert key not in response, f"Unexpected field in response: {key!r}"


def assert_schema(actual, expected):
    try:
        return TypeAdapter(expected).validate_python(actual)
    except ValidationError as e:
        raise AssertionError(e) from e


def assert_create_item_status(actual):
    assert isinstance(actual, str), f"Expected string, got: {type(actual).__name__}"
    uuid_value = actual.split()[-1]
    try:
        return str(UUID(uuid_value))
    except ValueError as e:
        raise AssertionError(f"Invalid UUID in status: {uuid_value!r}") from e
