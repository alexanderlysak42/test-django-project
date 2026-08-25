# RenovationFlow — Project & Task Manager

A Django web application for managing renovation/construction projects and their tasks, with role-based access control (Admin / Manager / Worker).

## Features

- Role-based access control (`admin`, `manager`, `worker`) enforced server-side, not just hidden in templates.
- Project CRUD with client info, address, status, manager, and assigned workers.
- Task CRUD nested under projects, with assignee, status, search, filtering, sorting and pagination.
- Global "My tasks" view scoped to the current user's role.
- Search, filtering, sorting and pagination on both project and task lists, with the current query context preserved across navigation (`next` parameter, validated with `url_has_allowed_host_and_scheme`).
- Optimized querysets (`select_related` / `prefetch_related`) to avoid N+1 queries.
- Shared `templates/base.html` (Bootstrap 5) with navbar and Django messages support.

## Roles

| Role    | Projects list         | Create project | Edit project      | Delete project | Tasks                                  |
|---------|------------------------|----------------|--------------------|----------------|-----------------------------------------|
| admin   | all projects           | yes            | any project        | yes            | full access to all tasks                |
| manager | only own projects      | yes            | only own projects  | no             | manage tasks within own projects only   |
| worker  | only assigned projects | no             | no                 | no             | view only tasks assigned to them        |

## Tech stack

- Python / Django
- PostgreSQL (via `psycopg[binary]`)
- Django Templates + Bootstrap 5

## Project structure

```
TestDjangoProject/
├── manage.py
├── testdjangoproject/   # settings, root urls, wsgi/asgi
├── users/                # custom User model with role field
├── projects/              # Project model, views, forms, admin
├── tasks/                   # Task model, views, forms, admin
└── templates/                # base.html, registration/login.html
```

## Requirements

- Python 3.12+
- A running PostgreSQL instance (local install or any reachable server)

## Setup

```bash
python -m venv .venv
source .venv/bin/activate      # on Windows: .venv\Scripts\activate

pip install --upgrade pip
pip install django psycopg[binary]
```

## Environment variables

The app reads its database credentials from environment variables — set them in your shell or export them from a `.env` file you load yourself:

```
POSTGRES_DB=your_db_name
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_db_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

`SECRET_KEY`, `DEBUG` and `ALLOWED_HOSTS` fall back to development defaults if unset, but `POSTGRES_*` variables are required — there is no SQLite fallback, so a reachable PostgreSQL database is mandatory.

## Database setup

Create the database and user in PostgreSQL, then apply migrations:

```bash
python manage.py migrate
python manage.py createsuperuser
```

## Running the app

```bash
python manage.py runserver
```

The app will be available at `http://127.0.0.1:8000/`.

## Useful commands

```bash
python manage.py check              # run Django's system checks
python manage.py makemigrations     # generate new migrations after model changes
python manage.py migrate            # apply migrations
python manage.py test               # run the test suite
```

## Key URLs

| URL                                       | Description                                 |
|--------------------------------------------|-----------------------------------------------|
| `/admin/`                                    | Django admin                                  |
| `/login/`, `/logout/`                          | Authentication                                |
| `/projects/`                                     | Project list (search/filter/sort/paginate)    |
| `/projects/create/`                               | Create project (admin/manager)                |
| `/projects/<id>/`                                  | Project detail                                |
| `/projects/<id>/edit/`                              | Edit project (admin/manager, own only)        |
| `/projects/<id>/delete/`                             | Delete project (admin only, POST)             |
| `/projects/<id>/tasks/create/`                        | Create task within a project                  |
| `/projects/<id>/tasks/<task_id>/`                      | Task detail                                   |
| `/projects/<id>/tasks/<task_id>/edit/`                  | Edit task                                     |
| `/projects/<id>/tasks/<task_id>/delete/`                 | Delete task (POST)                            |
| `/tasks/`                                                 | Global "My tasks" list                        |
