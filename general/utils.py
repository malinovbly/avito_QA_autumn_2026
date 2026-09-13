import random
import string
import uuid


def make_random_uuid4():
    return str(uuid.uuid4())


def make_random_string():
    return str(
        random.sample(string.ascii_letters + string.digits + string.punctuation, 10)
    )


def make_random_username():
    return f"student_{make_random_uuid4()}"


def make_random_item_name():
    return f"Test item {make_random_uuid4()}"
