from oauth2_provider.models import Application
from django.contrib.auth import get_user_model
from oauth2_provider.settings import oauth2_settings
from oauthlib.common import generate_token
from datetime import timedelta
from django.utils import timezone
from oauth2_provider.models import AccessToken, RefreshToken
from django.conf import settings


def get_authentication_code(username: str) -> tuple[str, str]:
    User = get_user_model()

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Exception("User does not exist!")

    app, created = Application.objects.get_or_create(
        name="Test",
        user=user,
        client_type=Application.CLIENT_CONFIDENTIAL,
        authorization_grant_type=Application.GRANT_PASSWORD
    )

    expires = timezone.now() + timedelta(seconds=oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS)
    scope = "read write"

    access_token = AccessToken.objects.create(
        user=user,
        application=app,
        token=generate_token(),
        expires=expires,
        scope=scope
    )

    refresh_token = RefreshToken.objects.create(
        user=user,
        token=generate_token(),
        application=app,
        access_token=access_token
    )

    return access_token.token, refresh_token.token