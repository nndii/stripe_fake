import datetime
import typing

from faker import Faker

fake = Faker()


class SourceCard(typing.NamedTuple):
    id: str
    # client_secret: str
    status: str
    flow: str = 'receiver'  # TODO: I dunno what does it mean, lol
    object: str = 'source'
    metadata: typing.Mapping = dict()
    receiver: typing.Mapping = dict()
    owner: typing.Mapping = dict()
    card: typing.Mapping = dict()
    created: int = int(datetime.datetime.utcnow().timestamp())
    currency: str = 'rub'
    usage: str = 'reusable'
    type: str = 'card'

    def jsonify(self) -> typing.Mapping:
        return {field: getattr(self, field) for field in self._fields}


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
