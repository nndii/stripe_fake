import datetime
import typing


class SourceCard(typing.NamedTuple):
    id: str
    # client_secret: str
    status: str
    flow: str = 'receiver'
    object: str = 'source'
    metadata: typing.Mapping = dict()
    receiver: typing.Mapping = dict()
    owner: typing.Mapping = dict()
    card: typing.Mapping = dict()
    created: int = int(datetime.datetime.utcnow().timestamp())
    currency: str = 'rub'
    usage: str = 'reusable'
    type: str = 'card'
    three_d_secure: typing.Mapping = dict()
    redirect: typing.Mapping = dict()
    amount: int = 0

    def jsonify(self) -> typing.Mapping:
        return {field: getattr(self, field) for field in self._fields}


class Charge(typing.NamedTuple):
    id: str
    status: str
    amount: int
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
    amount: int
    fee: int
    net: int
    source: str
    fee_details: typing.Sequence = []
    type: str = 'charge'
    object: str = 'balance_transaction'
    currency: str = 'RUB'

    def jsonify(self) -> typing.Mapping:
        return {field: getattr(self, field) for field in self._fields}


class WebhookCaptured(typing.NamedTuple):
    id: str
    type: str = 'charge.captured'
    pending_webhooks: int = 0
    data: typing.Mapping = dict()
    created: int = int(datetime.datetime.utcnow().timestamp())
    object: str = 'event'

    def jsonify(self) -> typing.Mapping:
        return {field: getattr(self, field) for field in self._fields}
