import hashlib
import hmac
import typing
from datetime import datetime
from uuid import uuid4

import requests
from faker import Faker

fake = Faker()


def resource_id(prefix: str) -> str:
    return f"{prefix}_{uuid4()}"


def fake_card(type: str) -> typing.Mapping:
    if type == 'three_ds_secure':
        return {'three_d_secure': 'required'}
    else:
        return {'three_d_secure': 'optional'}


def fake_owner() -> typing.Mapping:
    return {
        'address': fake.address(),
        'email': fake.email(),
        'name': fake.name(),
        'phone': fake.phone_number()
    }


async def signed_request(url: str, data: typing.Mapping, secret: str) -> requests.Response:
    headers = {'Stripe-Signature': ''}
    request_ = requests.Request('POST', url, json=data, headers=headers)
    prepped = request_.prepare()

    timestamp = int(datetime.utcnow().timestamp())
    signed_payload = f'{timestamp}.{prepped.body.decode("utf-8")}'
    signature = hmac.new(
        secret.encode('utf-8'),
        signed_payload.encode('utf-8'),
        digestmod=hashlib.sha256
    ).hexdigest()

    prepped.headers['Stripe-Signature'] = f't={timestamp},v1={signature}'

    with requests.Session() as s:
        return s.send(prepped)
