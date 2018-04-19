import typing
import datetime


class SourceCard(typing.NamedTuple):
    id: str
    client_secret: str
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


def fake_card(type: str) -> typing.Mapping:
    if type == 'three_ds_secure':
        return dict()
    else:
        return dict()


def fake_owner() -> typing.Mapping:
    return dict()