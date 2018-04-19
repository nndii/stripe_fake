from aiohttp import web
import asyncio
from stripe_fake.hooks import _create_source, _retrieve_source


async def create_source(request: web.Request):
    body, status = await asyncio.shield(_create_source(request))
    pass


async def retrieve_source(request: web.Request):
    s_id = request.match_info.get('s_id', None)
    body, status = await asyncio.shield(_retrieve_source(request))


def setup(app: web.Application):
    app.router.add_post('/v1/sources/', create_source)
    app.router.add_get('/v1/sources/{s_id}/', retrieve_source)