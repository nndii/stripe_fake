from uuid import uuid4
from faker import Faker
import typing

fake = Faker()


def resource_id(prefix: str) -> str:
    return f"{prefix}_{uuid4()}"


def fake_card(type: str) -> typing.Mapping:
    if type == 'three_ds_secure':
        return {'three_d_secure': 'required'}
    else:
        return {'three_d_secure': 'optional'}


def fake_owner() -> typing.Mapping:
    return {
        'address': fake.address(),
        'email': fake.email(),
        'name': fake.name(),
        'phone': fake.phone_number()
    }