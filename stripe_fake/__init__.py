import asyncio
import logging
import os
import sys
from queue import Queue

from aiohttp import web

from stripe_fake.hooks import process_capture_webhook, process_to_chargeable
from stripe_fake.routes import setup
from stripe_fake.utils import signed_request

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
            await asyncio.sleep(0.05)
    except asyncio.CancelledError:
        app['log']('Cancel capture webhook listener..')


async def to_chargeable_task(app: web.Application):
    try:
        await asyncio.sleep(0.01)
        while True:
            if not app['to_chargeable'].empty():
                await process_to_chargeable(app, app['to_chargeable'].get())
            await asyncio.sleep(0.05)
    except asyncio.CancelledError:
        app['log']('Cancel chargeable webhook listener..')


async def request_task(app: web.Application):
    try:
        await asyncio.sleep(0.01)
        while True:
            if not app['request_queue'].empty():
                await signed_request(**app['request_queue'].get())
            await asyncio.sleep(0.02)
    except asyncio.CancelledError:
        app['log']('Cancel request task listener..')


async def start_bg_tasks(app: web.Application):
    app['captured_task_'] = app.loop.create_task(captured_task(app))
    app['to_chargeable_task_'] = app.loop.create_task(to_chargeable_task(app))
    app['request_task_'] = app.loop.create_task(request_task(app))


async def cleanup_bg_tasks(app: web.Application):
    app['log']('cleanup background tasks')
    app['captured_task_'].cancel()
    app['to_chargeable_task_'].cancel()
    app['request_task_'].cancel()


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
    app['to_chargeable'] = Queue()
    app['request_queue'] = Queue()
    app['log'] = log.debug

    app.on_startup.append(start_bg_tasks)
    app.on_cleanup.append(cleanup_bg_tasks)

    return app
