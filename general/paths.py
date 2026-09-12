from enum import Enum


class Path:
    def __init__(self, method, path):
        self.method = method.upper()
        self.path = path


class MyEnum(Enum):
    @property
    def method(self):
        return self.value.method

    @property
    def path(self):
        return self.value.path


class Auth(MyEnum):
    REGISTER = Path("POST", "/api/1/register")
    LOGIN = Path("POST", "/api/1/autorize")


class Item(MyEnum):
    CREATE = Path("POST", "/api/1/item")
    GET = Path("GET", "/api/1/item/{id}")
    GET_ALL = Path("GET", "/api/1/{sellerID}/item")
    STATS_V1 = Path("GET", "/api/1/statistic/{id}")
    STATS_V2 = Path("GET", "/api/2/statistic/{id}")
    DELETE = Path("DELETE", "/api/2/item/{id}")
