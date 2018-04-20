from setuptools import setup

setup(
    name='stripe_fake',
    version='1.0',
    description='',
    classifiers=[
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.6',
    ],
    author='Andrey Maksimov',
    author_email='midnightcowboy@rape.lol',
    url='https://github.com/nndii/stripe_fake',
    keywords=['ticketscloud', 'stripe'],
    packages=['stripe_fake'],
    install_requires=['aiohttp', 'requests', 'faker'],
)
