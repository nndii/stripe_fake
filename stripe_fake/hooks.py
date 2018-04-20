import json

from aiohttp import web

from stripe_fake.resources import SourceCard, Charge, BalanceTransaction, WebhookCaptured
from stripe_fake.utils import resource_id, fake_owner, fake_card, signed_request, parse_params


async def _create_source(request: web.Request):
    params = await request.post()
    metadata = parse_params('metadata', params)
    redirect = parse_params('redirect', params)
    three_d_secure = parse_params('three_d_secure', params)
    if params.get('type', None) == 'three_d_secure':
        source = SourceCard(
            id=resource_id('src'),
            amount=int(params['amount']),
            currency=params['currency'],
            flow='redirect',
            redirect=redirect,
            metadata=metadata,
            three_d_secure=three_d_secure,
            type='three_d_secure',
            status='pending',
            owner=fake_owner()
        )
    else:
        source = SourceCard(
            id=resource_id('src'),
            status='pending',
            card=fake_card(params['token']),
            owner=fake_owner()
        )

    request.app['log'](f'SOURCE: {source}')
    request.app['log'](f'SOURCE: {source.jsonify()}')

    request.app['sources'][source.id] = source

    if source.type == 'three_d_secure':
        request.app['to_chargeable'].put(source)

    return source.jsonify(), 200


async def _create_charge(request: web.Request):
    params = await request.post()

    try:
        source = request.app['sources'][params.get('source')]
    except KeyError:
        return None, 404

    metadata = parse_params('metadata', params)
    charge = Charge(
        id=resource_id('ch'),
        status='pending',
        amount=int(params.get('amount')),
        currency=params.get('currency'),
        description=params.get('description'),
        metadata=metadata,
        source={"id": source.id, "object": source.object}
    )

    balance_transaction = BalanceTransaction(
        id=resource_id('txn'),
        status='pending',
        amount=charge.amount,
        currency=charge.currency,
        source=charge.id,
        fee=int(charge.amount * 0.1),
        net=int(charge.amount - charge.amount * 0.1),
        fee_details=[{"amount": int(charge.amount * 0.1),
                      "type": "stripe_fee",
                      "currency": charge.currency}]
    )
    request.app['transactions'][balance_transaction.id] = balance_transaction
    charge = charge._replace(balance_transaction=balance_transaction.id)

    request.app['log'](f'SOURCE: {charge}')
    request.app['log'](f'SOURCE: {charge.jsonify()}')

    request.app['charges'][charge.id] = charge
    return charge.jsonify(), 200


async def _capture_charge(request: web.Request, c_id: str):
    try:
        charge = request.app['charges'][c_id]
    except KeyError:
        return None, 404

    charge = charge._replace(captured=True)
    request.app['charges'][charge.id] = charge
    request.app['capture_webhook'].put(charge)
    return charge.jsonify(), 200


async def process_capture_webhook(app: web.Application, charge: Charge):
    event = WebhookCaptured(
        id=resource_id('evt'),
        data={
            'object': charge.jsonify()
        }
    )

    result = await signed_request(
        app['webhook_url'],
        event.jsonify(),
        app['webhook_secret'],
    )

    app['log'](f'Captured Webhook Result: {result} -> {result.content}')


async def process_to_chargeable(app: web.Application, source: SourceCard):
    source = source._replace(status='chargeable')
    app['sources'][source.id] = source
    event = WebhookCaptured(
        id=resource_id('evt'),
        data={
            'object': source.jsonify()
        },
        type='source.chargeable'
    )

    result = await signed_request(
        app['webhook_url'],
        event.jsonify(),
        app['webhook_secret'],
    )

    app['log'](f'Captured Webhook Result: {result} -> {result.content}')
