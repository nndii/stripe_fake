import asyncio

from aiohttp import web

from stripe_fake.hooks import _create_source


async def create_source(request: web.Request):
    body, status = await asyncio.shield(_create_source(request))
    return web.json_response(body, status=status)


async def retrieve_source(request: web.Request):
    s_id = request.match_info.get('s_id', None)
    try:
        source = request.app['sources'][s_id]
    except KeyError:
        return web.Response(status=404)
    else:
        return web.json_response(source.jsonify(), status=200)


def setup(app: web.Application):
    app.router.add_post('/v1/sources', create_source)
    app.router.add_get('/v1/sources/{s_id}', retrieve_source)
