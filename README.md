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

## Docker

В `backend/` находятся готовые Docker-конфигурации: `Dockerfile.dev` + `docker-compose.dev.yml` для локальной разработки и `Dockerfile.prod` + `docker-compose.prod.yml` для продакшен-окружения (gunicorn + nginx + PostgreSQL). Ниже приведены рекомендации по настройке переменных окружения и запуску.

### Переменные окружения (.env)

1. Скопируйте `backend/settings.exemple.py`, чтобы понять набор переменных.  
2. Создайте два файла в каталоге `backend/core/settings/`:
   - `.env.dev` — значения для разработки;
   - `.env.prod` — значения для продакшена.
3. Пример содержимого:

   ```env
   SECRET_KEY=django-insecure-...
   DJANGO_SETTINGS_MODULE=core.settings.dev  # или core.settings.prod


   POSTGRES_DB=postgres
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres

   DB_NAME=postgres
   DB_USER=postgres
   DB_PASSWORD=postgres
   DB_HOST=db_dev   # имя контейнера из docker-compose.dev.yml
   DB_HOST=db_prod  # имя контейнера из docker-compose.prod.yml
   DB_PORT=5432
   ```

4. В `docker-compose.*.yml` можно указать соответствующий файл через параметр `env_file` (например, `core/settings/.env.dev`). По умолчанию оба compose-файла ожидают `core/settings/.env`, поэтому либо переименуйте нужный файл в `.env`, либо обновите путь в compose.
5. Добавьте в `.env.prod` секреты/пароли, отличные от дев-окружения, и обязательно установите `DJANGO_SETTINGS_MODULE=core.settings.prod`.

### Запуск Docker (dev)

```bash
cd backend
cp core/settings/.env.dev core/settings/.env  # если compose.dev использует .env
docker compose -f docker-compose.dev.yml up --build
```

- `web_dev` запускает `python manage.py runserver` и монтирует исходники, поэтому правки подхватываются моментально.
- `db_dev` поднимает PostgreSQL 17 с именованным томом `postgres_dev_data`.
- Для выполнения миграций или создания суперпользователя используйте `docker compose -f docker-compose.dev.yml exec web_dev python manage.py migrate` и т.п.
- Остановить окружение: `docker compose -f docker-compose.dev.yml down` (добавьте `-v`, чтобы удалить том БД).

### Запуск Docker (prod)

```bash
cd backend
cp core/settings/.env.prod core/settings/.env  # либо обновите путь в compose
docker compose -f docker-compose.prod.yml up --build -d
```

- `web_prod` на старте выполняет миграции + `collectstatic`, результаты сохраняются в volume `staticfiles_data`; затем запускает gunicorn (`0.0.0.0:8000`).
- `nginx` получает собранную статику из того же volume и проксирует запросы на `web_prod` (порт 80 внутри контейнера, наружный — 8081).
- `db_prod` — PostgreSQL 17 с томом `postgres_prod_data`.
- Проверить статус: `docker compose -f docker-compose.prod.yml ps`.
- Посмотреть логи nginx или Django: `docker compose -f docker-compose.prod.yml logs -f nginx` / `web_prod`.
- Приложение доступно на `http://127.0.0.1:8081/` (через nginx).

### Обновление prod

1. `docker compose -f docker-compose.prod.yml pull` (если используете registry) или `build web_prod`.
2. `docker compose -f docker-compose.prod.yml up -d web_prod nginx`.
3. При необходимости выполнить админ-команды: `docker compose -f docker-compose.prod.yml exec web_prod python manage.py createsuperuser`.
