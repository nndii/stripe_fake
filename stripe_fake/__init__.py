import asyncio
import logging
import os
import sys

from aiohttp import web
from stripe_fake.routes import setup


logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)7s: %(message)s',
    stream=sys.stdout,
)


def create_app() -> web.Application:
    log = logging.getLogger('')
    loop = asyncio.get_event_loop()
    app = web.Application(loop=loop)
    setup(app)

    app['sources'] = dict()
    app['log'] = log

    return app
