from datetime import timedelta
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import HTTPException

from app.core.config import settings
from app.core.google_client import get_service
from app.main import app
from app.services.google_api import spreadsheets_create, spreadsheets_update_value


def test_greenfund_openapi():
    schema = app.openapi()
    assert schema['info']['title'] == 'GreenFund'
    assert 'экологических' in schema['info']['description'] or 'озеленение' in schema['info']['description']
    assert schema['paths']['/charity_project/']['get']['tags'] == ['Экологические инициативы']


async def test_google_not_configured(monkeypatch):
    monkeypatch.setattr(settings, 'private_key', None)
    generator = get_service()
    with pytest.raises(HTTPException) as error:
        await generator.__anext__()
    assert error.value.status_code == 503
    await generator.aclose()


async def test_green_report_titles_and_closed_initiatives():
    sheets = MagicMock()
    services = MagicMock()
    services.discover = AsyncMock(return_value=sheets)
    services.as_service_account = AsyncMock(return_value={'spreadsheetId': 'test-sheet'})
    assert await spreadsheets_create(services) == 'test-sheet'
    body = sheets.spreadsheets.create.call_args.kwargs['json']
    assert body['properties']['title'].startswith('GreenFund — отчет на ')
    await spreadsheets_update_value('test-sheet', [
        {'name': 'Чистый берег', 'duration': timedelta(days=2), 'description': 'Уборка берега'}
    ], services)
    update = sheets.spreadsheets.values.update.call_args.kwargs
    assert update['json']['values'][3] == ['Чистый берег', '2 days, 0:00:00', 'Уборка берега']
    assert update['range'] == 'A1:C4'
