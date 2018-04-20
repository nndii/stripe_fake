import asyncio

from aiohttp import web

from stripe_fake.hooks import _create_source, _create_charge, _capture_charge


async def create_source(request: web.Request):
    body, status = await asyncio.shield(_create_source(request))
    return web.json_response(body, status=status)


async def retrieve_source(request: web.Request):
    s_id = request.match_info.get('s_id', None)
    source = request.app['sources'][s_id]
    return web.json_response(source.jsonify(), status=200)


async def create_charge(request: web.Request):
    body, status = await asyncio.shield(_create_charge(request))
    return web.json_response(body, status=status)


async def retrieve_charge(request: web.Request):
    c_id = request.match_info.get('c_id', None)
    charge = request.app['charges'][c_id]
    return web.json_response(charge.jsonify(), status=200)


async def capture_charge(request: web.Request):
    c_id = request.match_info.get('c_id', None)
    body, status = await asyncio.shield(_capture_charge(request, c_id))
    return web.json_response(body, status=status)


def setup(app: web.Application):
    app.router.add_post('/v1/sources', create_source)
    app.router.add_post('/v1/charges', create_charge)
    app.router.add_get('/v1/sources/{s_id}', retrieve_source)
    app.router.add_get('/v1/charges/{c_id}', retrieve_charge)
    app.router.add_post('/v1/charges/{c_id}/capture', capture_charge)