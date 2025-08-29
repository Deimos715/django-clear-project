# Django Clear Project

## Короткое описание

Это чистый шаблонный проект на Django с разделением на Backend (Django) и Frontend (Gulp/npm). Репозиторий содержит минимальную структуру для быстрого старта разработки и деплоя.

## Структура репозитория (основное)

-   `backend/` — серверная часть на Django (проекты `core`, `main`, `seo` и т.д.).
-   `frontend/` — клиентская часть, сборка через Gulp/npm.
-   `static/`, `staticfiles/`, `media/` — ассеты и собранные статические файлы.
-   `templates/` — общие шаблоны Django.

---

## Backend (Django)

Расположение: `backend/`.

Кратко

-   Проект использует Django (в `backend/requirements.txt` указаны версии, например Django==5.2.1).
-   В корне `backend/` есть `manage.py` и файл базы `db.sqlite3` (по умолчанию — sqlite).
-   Конфигурация настроек разбита: в `core/settings/` есть `dev.py`, `prod.py` и `base.py`. В `backend/settings.exemple.py` по умолчанию импортируется `core.settings.dev`.

Быстрый старт (локальная разработка)

1. Создать виртуальное окружение и установить зависимости:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
```

2. Перейти в папку с Django и выполнить миграции:

```bash
cd backend
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

3. Собрать статические файлы (при необходимости):

```bash
python manage.py collectstatic --noinput
```

Настройки окружения

-   По умолчанию `backend/settings.exemple.py` подключает `core.settings.dev`. Для продакшена переключите на `core.settings.prod` или установите переменную окружения `DJANGO_SETTINGS_MODULE=core.settings.prod`.
-   В проекте используется `python-dotenv` — можно добавить файл `.env` и загружать секреты/параметры.

Где что находится

-   `backend/requirements.txt` — список Python-зависимостей.
-   `backend/manage.py` — точка входа для команд Django.
-   `core/settings/` — разбитые файлы настроек (dev/prod/base).

Замечание по БД

-   В репозитории есть `backend/db.sqlite3` — если вы хотите чистую БД, удалите/переместите её и выполните миграции заново.

---

## Frontend

Расположение: `frontend/`.

Кратко

-   Frontend основан на Gulp + npm. Файл `frontend/package.json` содержит devDependencies (gulp, webpack, sass и пр.).
-   Исходники находятся в `frontend/` (пути `app/`, `js_src/`, `scss/` и т.д.).
-   Сборка, складывает результат в `frontend/dist`.

Быстрый старт (локальная разработка)

1. Установить зависимости и запустить сборку:

```bash
cd frontend
npm install
# Запуск gulp через npx (если gulp не установлен глобально):
npx gulp
```

2. После сборки скопировать / синхронизировать полученные статические ресурсы в бэкенд (если это не автоматизировано). Часто это `static/` или `staticfiles/` в корне репозитория.

Полезные примечания

-   Если в `frontend/` есть команды или скрипты в `package.json`, используйте их (например `npm run build`), но в данном репозитории видно только devDependencies — посмотрите `frontend/gulpfile.js` для деталей конвейера сборки.

---

## Деплой

-   В `backend/` присутствует скрипт `deploy_my.sh` — он может содержать шаблон для деплоя (проверьте и настройте под окружение).
-   В production рекомендуется:
    -   использовать `core.settings.prod`;
    -   задать переменные окружения (секреты, настройки БД, DEBUG=False);
    -   использовать внешнюю СУБД (Postgres и т.д.) вместо sqlite;
    -   настроить web-сервер (nginx/gunicorn или uwsgi);
    -   собрать front и разместить статические файлы через `collectstatic`.

---

## Полезные команды (сводка)

```bash
# Backend
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
cd backend
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
python manage.py collectstatic --noinput

# Frontend
cd frontend
npm install
npx gulp
```

---
