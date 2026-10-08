# AI Agent Guidance for ColorPhoto

## Project overview
- Django 6.0 project with a root app `colorphoto` and feature apps: `services`, `portfolio`, `package`, `gallery`, `video`, `service_details`, and `accounts`.
- Uses custom user model `accounts.Account` with `AUTH_USER_MODEL = 'accounts.Account'`.
- Database is SQLite at `db.sqlite3`.
- Media files are served from `media/`; static assets are in `colorphoto/static/` and `static/`.
- Templates are loaded from `colorphoto/templates/` plus app template folders.

## How to run
- Activate the virtual environment in the workspace root: `env\Scripts\Activate.ps1` on Windows PowerShell.
- Run Django commands from `manage.py`:
  - `python manage.py runserver`
  - `python manage.py migrate`
  - `python manage.py makemigrations`

## Important structure
- `colorphoto/urls.py`: root URL configuration
- `colorphoto/views.py`: home page controller and top-level view functions
- `services/urls.py`, `portfolio/urls.py`, `package/urls.py`, `gallery/urls.py`, `video/urls.py`: app URL routes
- `accounts/models.py`: custom authentication model
- `colorphoto/settings.py`: settings, installed apps, static/media config, custom user model

## Project conventions and notes
- The homepage uses `colorphoto.views.home` and aggregates lists from `services`, `portfolio`, `package`, `gallery`, and `video`.
- App views generally use Django function-based views and render templates with context dictionaries.
- The project currently includes a duplicate URL route: `path('protfolio/', include('portfolio.urls'))` in `colorphoto/urls.py`.
- `colorphoto/settings.py` is configured with `DEBUG = True` and a hard-coded `SECRET_KEY`; this is acceptable for local development but should not be used for production deployments.

## When editing
- Preserve the `AUTH_USER_MODEL` setting whenever touching authentication or account models.
- Use template names and app-specific template directories rather than assuming a single unified template folder.
- Keep the existing `media` and `static` configuration in sync with `MEDIA_ROOT`, `STATIC_ROOT`, and `STATICFILES_DIRS`.
- Confirm that new views or template references use the correct app route and template path.

## Useful checks for AI-generated changes
- Verify that URL patterns are not duplicated or mis-spelled.
- Confirm template names exist before changing view render targets.
- Ensure migration files are updated when models change.
- Avoid introducing production secrets or publishing the current `SECRET_KEY`.

## Why this file exists
This file helps AI coding agents understand the application boundaries, runtime commands, and repository conventions so they can make safe, context-aware code changes.
