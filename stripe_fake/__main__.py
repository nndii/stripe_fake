from aiohttp import web

from stripe_fake import create_app


if __name__ == '__main__':
    web.run_app(create_app(), host='localhost', port=7979)