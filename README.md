# GreenFund

API сбора средств на экологические инициативы: озеленение, уборку территорий и восстановление парков. Администратор открывает сборы, пользователи регистрируют пожертвования. Средства автоматически распределяются по очереди создания инициатив; остаток переходит к следующему открытому сбору. Закрытые сборы доступны в отчете Google Sheets по длительности сбора.

Автор адаптации и доработок — Рябуха Олег.

Стек: Python 3.11, FastAPI, SQLAlchemy 1.4, SQLite/aiosqlite, Alembic, FastAPI Users, aiogoogle. Суммы — целые положительные числа в одной принятой фондом единице учета. API ведет учет пожертвований; платежной интеграции нет.

## Локальный запуск

Из каталога проекта в PowerShell:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
Copy-Item .env.example .env
# Задайте SECRET. Для администратора заполните FIRST_SUPERUSER_EMAIL/PASSWORD.
.\.venv\Scripts\python -m alembic upgrade head
.\.venv\Scripts\python -m uvicorn app.main:app --reload --port 8004
```

Linux/macOS: `python3.11 -m venv .venv`, затем `.venv/bin/python` вместо `.\.venv\Scripts\python`. SQLite создается в текущем каталоге. Администратор создается при заполнении обеих переменных. Без SECRET ключ выбирается случайно на процесс, поэтому после перезапуска потребуется повторный вход; для постоянной установки задайте свой ключ.

Swagger: <http://127.0.0.1:8004/docs>, ReDoc: <http://127.0.0.1:8004/redoc>. Актуальная OpenAPI-схема — `/openapi.json`.

## Основные запросы

Пути и поля стабильны; `charity_project` обозначает экологическую инициативу.

| Путь | Назначение и доступ |
| --- | --- |
| `POST /auth/register` | Регистрация: `email`, `password` |
| `POST /auth/jwt/login` | Вход формой: `username` (email), `password` |
| `GET /charity_project/` | Все инициативы, публично |
| `POST /charity_project/` | Создание инициативы, администратор |
| `PATCH/DELETE /charity_project/{id}` | Изменение/удаление с учетом вложений, администратор |
| `POST /donation/` | Пожертвование, авторизованный пользователь |
| `GET /donation/my` | Собственные пожертвования |
| `GET /donation/` | Полный учет, администратор |
| `GET /users/me` | Собственный профиль |
| `GET /google/` | Создание отчета Google Sheets, администратор |

Тело создания инициативы (Bearer-токен администратора):

```json
{"name":"Чистый берег","description":"Перчатки, мешки и вывоз мусора","full_amount":25000}
```

Тело пожертвования:

```json
{"full_amount":1500,"comment":"На восстановление городских парков"}
```

Еще три примера — `examples/initiatives.json`. Это тела независимых POST-запросов, а не дамп базы.

## Google Sheets

Создайте сервисный аккаунт в своем Google Cloud-проекте, включите Sheets API и Drive API. Заполните поля аккаунта в `.env`, в `PRIVATE_KEY` сохраните PEM с `\n` внутри кавычек. `EMAIL` — получатель доступа к отчету. Пустые параметры дают ответ 503 только на `/google/`. Создается таблица `GreenFund — отчет на ...` с закрытыми инициативами, временем сбора и описаниями; получателю выдается доступ на запись. Секретный JSON аккаунта в репозиторий не помещайте.

## Проверки

```powershell
.\.venv\Scripts\python -m pip install -r requirements-dev.txt
.\.venv\Scripts\python -m pytest
.\.venv\Scripts\python -m alembic check
```

Тесты используют отдельную `test.db`, проверяют FIFO-распределение, закрытие, ограничения сумм, доступ и оформление отчета. Фактические результаты — `REVIEW.md`.

Условия использования — в файле `MIT License`; дополнительные сведения — в `NOTICE.md`.
