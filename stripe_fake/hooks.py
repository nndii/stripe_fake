from aiohttp import web

from stripe_fake.resources import SourceCard, Charge, BalanceTransaction
from stripe_fake.utils import resource_id, fake_owner, fake_card
import json


async def _create_source(request: web.Request):
    params = await request.post()

    source = SourceCard(
        id=resource_id('src'),
        status='pending',
        card=fake_card(params['token']),
        owner=fake_owner()
    )
    request.app['log'].debug(f'SOURCE: {source}')
    request.app['log'].debug(f'SOURCE: {source.jsonify()}')

    request.app['sources'][source.id] = source
    return source.jsonify(), 200


async def _create_charge(request: web.Request):
    params = await request.post()

    try:
        source = request.app['sources'][params.get('source')]
    except KeyError:
        return None, 404

    charge = Charge(
        id=resource_id('ch'),
        status='pending',
        amount=params.get('amount'),
        currency=params.get('currency'),
        description=params.get('description'),
        metadata=json.loads(params.get('metadata', '{}')),
        source={"id": source.id, "object": source.object}
    )

    balance_transaction = BalanceTransaction(
        id=resource_id('txn'),
        status='pending',
        amount=charge.amount,
        currency=charge.currency,
        source=charge.id,
        fee=charge.amount*0.05,
        net=charge.amount-charge.amount*0.05,
        fee_details=[{"amount": charge.amount*0.05,
                      "type": "stripe_fee",
                      "currency": charge.currency}]
    )
    request.app['transactions'][balance_transaction.id] = balance_transaction
    charge = charge._replace(balance_transaction=balance_transaction.id)

    request.app['log'].debug(f'SOURCE: {charge}')
    request.app['log'].debug(f'SOURCE: {charge.jsonify()}')

    request.app['charges'][charge.id] = charge
    return charge.jsonify(), 200


async def _capture_charge(request: web.Request, c_id: str):
    try:
        charge = request.app['charges'][c_id]
    except KeyError:
        return None, 404

    charge = charge._replace(captured=True)
    request.app['charges'][charge.id] = charge

    return charge.jsonify(), 200
