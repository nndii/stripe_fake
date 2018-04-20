import datetime
import typing

from faker import Faker


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


class Charge(typing.NamedTuple):
    id: str
    status: str
    amount: float
    description: str
    paid: bool = True
    balance_transaction: str = ''
    object: str = 'charge'
    captured: bool = False
    refunded: bool = False
    source: typing.Mapping = dict()
    metadata: typing.Mapping = dict()
    refunds: typing.Mapping = dict()
    amount_refunded: float = 0
    currency: str = 'RUB'
    created: int = int(datetime.datetime.utcnow().timestamp())

    def jsonify(self) -> typing.Mapping:
        return {field: getattr(self, field) for field in self._fields}


class BalanceTransaction(typing.NamedTuple):
    id: str
    status: str
    amount: float
    fee: float
    net: float
    source: str
    fee_details: typing.Sequence = []
    type: str = 'charge'
    object: str = 'balance_transaction'
    currency: str = 'RUB'

    def jsonify(self) -> typing.Mapping:
        return {field: getattr(self, field) for field in self._fields}
