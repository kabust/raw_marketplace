import os

import requests
from dotenv import load_dotenv
from oauth2_provider.models import Application
from django.contrib.auth import get_user_model
from oauth2_provider.settings import oauth2_settings
from oauthlib.common import generate_token
from datetime import timedelta, datetime
from django.utils import timezone
from oauth2_provider.models import AccessToken, RefreshToken

load_dotenv()

PAYU_CLIENT_ID = os.getenv("PAYU_CLIENT_ID")
PAYU_CLIENT_SECRET = os.getenv("PAYU_CLIENT_SECRET")


def get_authentication_code(email: str) -> tuple[str, str]:

    try:
        user = get_user_model().objects.get(email=email)
    except get_user_model().DoesNotExist:
        raise Exception("User does not exist!")

    app, created = Application.objects.get_or_create(
        name="Test",
        user=user,
        client_type=Application.CLIENT_CONFIDENTIAL,
        authorization_grant_type=Application.GRANT_PASSWORD,
    )

    expires = timezone.now() + timedelta(seconds=oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS)
    scope = "read write"

    access_token = AccessToken.objects.create(
        user=user, application=app, token=generate_token(), expires=expires, scope=scope
    )

    refresh_token = RefreshToken.objects.create(
        user=user, token=generate_token(), application=app, access_token=access_token
    )

    return access_token.token, refresh_token.token


def get_authentication_code_payu():
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(
        "https://secure.snd.payu.com/pl/standard/user/oauth/authorize",
        headers=headers,
        data={
            "client_id": PAYU_CLIENT_ID,
            "client_secret": PAYU_CLIENT_SECRET,
            "grant_type": "client_credentials",
        },
    )
    token_data = response.json()
    token = token_data.get("access_token")
    exp_time = timedelta(seconds=token_data.get("expires_in")) + datetime.now()
    return token, exp_time


def create_order_payu(token, exp_time, customer_ip, total_amount, products, buyer):
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    merchant_id = str(PAYU_CLIENT_ID)
    description = "Order for name surname buying product"
    currency_code = "PLN"
    totalAmount = str(int(total_amount * 100))

    data = {
        "continueUrl": "",
        "customerIp": customer_ip,
        "merchantPosId": merchant_id,
        "description": description,
        "currencyCode": currency_code,
        "totalAmount": totalAmount,
        "buyer": buyer,
        "products": products,
    }
    print(token)
    url_sandbox = "https://secure.snd.payu.com/api/v2_1/orders"
    response = requests.post(url_sandbox, headers=headers, json=data, allow_redirects=False)
    return response.json()
