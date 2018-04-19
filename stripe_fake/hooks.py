from aiohttp import web

from stripe_fake.resources import SourceCard, fake_card, fake_owner
from stripe_fake.utils import source_id


async def _create_source(request: web.Request):
    params = await request.json()

    source = SourceCard(
        id=source_id(),
        status='pending',
        card=fake_card(params['token']),
        owner=fake_owner()
    )

    request.app['sources'][source.id] = source
    return source.jsonify(), 200


