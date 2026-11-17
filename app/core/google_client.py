from aiogoogle import Aiogoogle
from aiogoogle.auth.creds import ServiceAccountCreds
from fastapi import HTTPException

from app.core.config import settings

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]
INFO = {
    'type': settings.type,
    'project_id': settings.project_id,
    'private_key_id': settings.private_key_id,
    'private_key': settings.private_key,
    'client_email': settings.client_email,
    'client_id': settings.client_id,
    'auth_uri': settings.auth_uri,
    'token_uri': settings.token_uri,
    'auth_provider_x509_cert_url': settings.auth_provider_x509_cert_url,
    'client_x509_cert_url': settings.client_x509_cert_url
}
cred = ServiceAccountCreds(scopes=SCOPES, **INFO)


async def get_service():
    if not all((settings.project_id, settings.private_key,
                settings.client_email, settings.email)):
        raise HTTPException(
            status_code=503,
            detail='Для отчета настройте сервисный аккаунт Google и EMAIL.',
        )
    async with Aiogoogle(service_account_creds=cred) as aiogoogle:
        yield aiogoogle
