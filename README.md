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
-   Конфигурация настроек разбита: в `core/settings/` есть `base.py` + окружения `dev.py` и `prod.py`. В `core/settings/__init__.py` автоматически подхватывается нужный модуль по переменной `DJANGO_ENV`.

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

-   Для явного выбора окружения есть файлы `backend/settings_dev.exemple.py` и `backend/settings_prod.exemple.py` — раскомментируйте нужный импорт в рабочей копии `settings.py`, если не хотите использовать `DJANGO_ENV`.
-   В корне `core/settings/` лежат примеры `.env.dev.exemple` и `.env.prod.exemple`. Переименуйте `.env.dev.exemple` в `.env.dev` или `.env.prod.exemple` в `.env.prod` при деплое и заполните значения (`SECRET_KEY`, креды БД и т.д.).
-   В проекте используется `python-dotenv`, поэтому значения из `.env.*` подхватываются автоматически.

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

1. Создайте файлы окружений на основе `core/settings/.env.dev.exemple` и `core/settings/.env.prod.exemple`.  
2. Заполните обязательные значения (`SECRET_KEY`, параметры PostgreSQL).  
3. Короткий пример:

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

4. В `docker-compose.dev.yml` и `docker-compose.prod.yml` теперь явно прописаны `env_file`, поэтому просто храните рядом `.env.dev`/`.env.prod` и обновите путь при необходимости.
5. Для Docker-контейнеров Django задана переменная `DJANGO_ENV` (`dev` или `prod`), чтобы `core/settings/__init__.py` подгружал правильный модуль.

### Запуск Docker (dev)

```bash
cd backend
cp core/settings/.env.dev.exemple core/settings/.env.dev && $EDITOR core/settings/.env.dev
docker compose -f docker-compose.dev.yml up --build
```

- `web_dev` запускает `python manage.py runserver` и монтирует исходники, поэтому правки подхватываются моментально.
- `db_dev` поднимает PostgreSQL 17 с именованным томом `postgres_dev_data`.
- Для выполнения миграций или создания суперпользователя используйте `docker compose -f docker-compose.dev.yml exec web_dev python manage.py migrate` и т.п.
- Остановить окружение: `docker compose -f docker-compose.dev.yml down` (добавьте `-v`, чтобы удалить том БД).

### Запуск Docker (prod)

```bash
cd backend
cp core/settings/.env.prod.exemple core/settings/.env.prod && $EDITOR core/settings/.env.prod
docker compose -f docker-compose.prod.yml up --build -d
```

- `web_prod` теперь использует образ из GHCR (`image: ghcr.io/<owner>/...`), автоматически прогоняет миграции и `collectstatic`, после чего стартует gunicorn. Задайте свой `image` или используйте собранный из CI.
- `db_prod` — PostgreSQL 17 с томом `postgres_prod_data`.
- В `docker-compose.prod.yml` добавлены проверки состояния и проброс `DJANGO_ENV=prod`. Путь к статике и медиа ожидает примонтированные директории `/var/www/...`.
- Проверить статус: `docker compose -f docker-compose.prod.yml ps`.
- Посмотреть логи nginx или Django: `docker compose -f docker-compose.prod.yml logs -f nginx` / `web_prod`.
- Приложение доступно, если внешняя панель (например FastPanel) проксирует на порт `8001`, указанный в compose. При нескольких сайтах скорректируйте порт.

### Обновление prod

1. `docker compose -f docker-compose.prod.yml pull` — подтягивает свежий образ из GHCR (см. CI/CD ниже).
2. `docker compose -f docker-compose.prod.yml up -d --force-recreate web_prod`.
3. При необходимости выполните команды управления: `docker compose -f docker-compose.prod.yml exec web_prod python manage.py createsuperuser`.

---

## CI/CD

В каталоге `backend/github_ci-cd.zip` лежит архив со стартовой конфигурацией GitHub Actions:

- `.github/workflows/ci.yml` — быстрый CI, который валидационно выполняет шаги на `push`/`pull_request`.
- `.github/workflows/deploy.yml` — полноценный конвейер, который:
    - собирает и пушит Docker-образ в GitHub Container Registry (`ghcr.io/<owner>/webdevlabs`);
    - подключается по SSH к серверу, обновляет код и перезапускает `docker-compose.prod.yml`.

Чтобы включить конвейеры, распакуйте архив в корень репозитория:

```bash
cd backend
unzip github_ci-cd.zip -d ..
```

Далее создайте секреты в настройках GitHub:

- `SSH_HOST`, `SSH_PRIVATE_KEY`, `REMOTE_COMPOSE_DIR` — данные для деплоя;
- `GHCR_PAT` — токен с правами `packages:write` для скачивания образа на сервере. На этапе сборки используется дефолтный `GITHUB_TOKEN`.

После распаковки скорректируйте имя образа в `docker-compose.prod.yml` и в Actions (`IMAGE_NAME`/`tags`), чтобы совпадали с тем, что будет запускаться на сервере.
