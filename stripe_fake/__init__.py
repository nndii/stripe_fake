import asyncio
import logging
import os
import sys
from queue import Queue

from aiohttp import web

from stripe_fake.hooks import process_capture_webhook
from stripe_fake.routes import setup

logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)7s: %(message)s',
    stream=sys.stdout,
)


async def captured_task(app: web.Application):
    try:
        await asyncio.sleep(0.01)
        while True:
            if not app['capture_webhook'].empty():
                await process_capture_webhook(app, app['capture_webhook'].get())
            await asyncio.sleep(0.01)
    except asyncio.CancelledError:
        app['log']('Cancel capture webhook listener..')


async def start_bg_tasks(app: web.Application):
    app['captured_task_'] = app.loop.create_task(captured_task(app))


async def cleanup_bg_tasks(app: web.Application):
    app['log']('cleanup background tasks')
    app['captured_task_'].cancel()


def create_app() -> web.Application:
    log = logging.getLogger('')
    loop = asyncio.get_event_loop()
    app = web.Application(loop=loop)
    setup(app)

    # VAR
    app['webhook_url'] = os.environ['WEBHOOK_URL']
    app['webhook_secret'] = os.environ['WEBHOOK_SECRET']

    # DB
    app['sources'] = dict()
    app['charges'] = dict()
    app['transactions'] = dict()
    app['capture_webhook'] = Queue()
    app['log'] = log.debug

    app.on_startup.append(start_bg_tasks)
    app.on_cleanup.append(cleanup_bg_tasks)

    return app
