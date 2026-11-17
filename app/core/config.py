from typing import Optional
from secrets import token_urlsafe

from pydantic import BaseSettings, EmailStr, Field


class Settings(BaseSettings):
    app_title: str = 'GreenFund'
    app_description: str = (
        'Сбор средств на озеленение, уборку территорий и восстановление парков'
    )
    database_url: str = 'sqlite+aiosqlite:///./greenfund.db'
    secret: str = Field(default_factory=lambda: token_urlsafe(32))
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None
    type: Optional[str] = None
    project_id: Optional[str] = None
    private_key_id: Optional[str] = None
    private_key: Optional[str] = None
    client_email: Optional[str] = None
    client_id: Optional[str] = None
    auth_uri: Optional[str] = None
    token_uri: Optional[str] = None
    auth_provider_x509_cert_url: Optional[str] = None
    client_x509_cert_url: Optional[str] = None
    email: Optional[str] = None

    class Config:
        env_file = '.env'


settings = Settings()
