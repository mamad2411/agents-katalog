---
name: django-fullstack
description: >
  Comprehensive guide for building a full-stack Django web application from scratch.
  Use this skill whenever building any Django project — especially when it involves
  user authentication, profiles, real-time WebSocket features, filtering/search,
  Tailwind UI, or running under Daphne/ASGI. Also use it when debugging common Django
  pitfalls like AppRegistryNotReady, unstyled admin panels, WebSocket auth errors,
  or template context conflicts.
---

# Django Full-Stack App

Follow this guide top to bottom for a new project, or jump to the relevant section when debugging or extending.

---

## Workflow Overview

1. Set up venv and install dependencies (including `django-tailwind`)
2. Create project and apps
3. Configure settings (ASGI, Channels, static files, auth, Tailwind)
4. Write models
5. Set up URLs and views
6. Build templates with Tailwind
7. Run migrations, seed data, start server

---

## 1. Environment & Project Setup

Always use a venv. Invoke the binaries directly rather than sourcing it — this keeps the environment explicit and works consistently across shells and scripts.

```bash
python3 -m venv venv
venv/bin/pip install django daphne channels
venv/bin/pip freeze > requirements.txt

venv/bin/django-admin startproject myproject .
venv/bin/python manage.py startapp myapp
# create one app per logical domain of your project
```

---

## 2. Settings

Key configuration for a local dev project with Channels:

```python
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

INSTALLED_APPS = [
    'daphne',   # must be first — patches runserver to use ASGI
    'channels',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myapp',
    # add your apps here
]

ASGI_APPLICATION = 'myproject.asgi.application'

# In-memory channel layer works for local dev; swap for Redis in production
CHANNEL_LAYERS = {
    'default': {'BACKEND': 'channels.layers.InMemoryChannelLayer'},
}

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [BASE_DIR / 'templates'],  # top-level templates/ folder
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
        ],
    },
}]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'   # target for collectstatic
STATICFILES_DIRS = [BASE_DIR / 'static'] # your own static assets

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/login/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
```

---

## 3. ASGI Configuration

The order of operations in this file matters — Django's app registry must be fully initialised before any app code is imported.

```python
# myproject/asgi.py
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

import django
django.setup()  # must come before any Django model or app imports

from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from myapp.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(        # populates scope['user'] from the session
            URLRouter(websocket_urlpatterns)
        )
    ),
})
```

> Skipping `django.setup()`, or placing imports above it, causes `AppRegistryNotReady`.
> Skipping `AuthMiddlewareStack` causes `KeyError: 'user'` inside consumers.

---

## 4. URL Configuration

```python
# myproject/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),
]

# Daphne does not serve static files the way runserver does.
# Adding this in DEBUG mode lets Django handle them so the admin panel gets its CSS.
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

Run `venv/bin/python manage.py collectstatic --noinput` before starting the server, and again after any static file changes.

---

## 5. Models

### Extending the built-in User

Never modify Django's `User` model directly. Attach extra data via a `OneToOneField` profile:

```python
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # add your fields here — bio, avatar, preferences, etc.

    def __str__(self):
        return self.user.username
```

This lets you access the profile anywhere you have a user: `user.profile.some_field`.

### Many-to-many relationships with extra attributes

When a link between two models carries its own data (e.g. a role, a status, a date joined), use an explicit through model rather than a plain `ManyToManyField`:

```python
class Membership(models.Model):
    user  = models.ForeignKey(User, on_delete=models.CASCADE, related_name='memberships')
    group = models.ForeignKey('Group', on_delete=models.CASCADE)
    role  = models.CharField(max_length=50, default='member')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'group')
```

---

## 6. Authentication

Reuse Django's built-in `LoginView` rather than reimplementing session handling and CSRF from scratch:

```python
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.shortcuts import redirect, render

class LoginView(DjangoLoginView):
    template_name = 'myapp/login.html'
    redirect_authenticated_user = True

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
            )
            Profile.objects.create(user=user)
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'myapp/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')
```

---

## 7. Filtering Querysets

Build filters dynamically with `Q` objects — this way absent form fields simply contribute nothing rather than requiring separate conditional branches:

```python
from django.db.models import Q

qs = MyModel.objects.select_related('related_model').filter(is_active=True)

filters = Q()
if request.GET.get('search'):
    filters &= Q(name__icontains=request.GET['search'])
if request.GET.get('category'):
    filters &= Q(category_id=request.GET['category'])

# .distinct() is required when filtering across joined tables — without it
# you get one row per matching related row, not one row per object
qs = qs.filter(filters).distinct()
```

When querying users for a public-facing list, always exclude staff accounts:

```python
users = User.objects.exclude(is_superuser=True).exclude(is_staff=True)
```

---

## 8. WebSocket Consumer

```python
# myapp/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

class MyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        if self.user.is_anonymous:
            await self.close()
            return

        self.group = f"room_{self.scope['url_route']['kwargs']['room_id']}"
        await self.channel_layer.group_add(self.group, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        # persist to DB, then broadcast
        await self.persist(data)
        await self.channel_layer.group_send(self.group, {
            'type': 'broadcast',
            **data,
            'sender_id': self.user.id,
        })

    async def broadcast(self, event):
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def persist(self, data):
        # do your DB write here — ORM calls must be wrapped in database_sync_to_async
        pass
```

```python
# myapp/routing.py
from django.urls import path
from .consumers import MyConsumer

websocket_urlpatterns = [
    path('ws/<str:room_id>/', MyConsumer.as_asgi()),
]
```

When two users share a room, derive a stable ID that's the same regardless of who opens it first: `f"{min(a_id, b_id)}_{max(a_id, b_id)}"`.

---

## 9. Templates & Tailwind

Use `django-tailwind` for a proper build pipeline without managing Node manually.

### Installation

```bash
venv/bin/pip install 'django-tailwind[reload]'
venv/bin/python manage.py tailwind init --no-input --app-name theme
venv/bin/python manage.py tailwind install
```

### Settings

```python
INSTALLED_APPS = [
    # ... existing apps ...
    'tailwind',
    'theme',
]

TAILWIND_APP_NAME = 'theme'

# Optional: live reload in development
if DEBUG:
    INSTALLED_APPS += ['django_browser_reload']
    MIDDLEWARE += ['django_browser_reload.middleware.BrowserReloadMiddleware']
```

### Base template

```html
<!-- templates/base.html -->
{% load tailwind_tags %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    {% tailwind_css %}
</head>
<body>
    <nav>...</nav>
    <main>
        {% if messages %}
            {% for msg in messages %}
                <div>{{ msg }}</div>
            {% endfor %}
        {% endif %}
        {% block content %}{% endblock %}
    </main>
</body>
</html>
```

### Development

```bash
# Runs Tailwind watcher alongside your server
venv/bin/python manage.py tailwind start
```

### Production

```bash
venv/bin/python manage.py tailwind build
venv/bin/python manage.py collectstatic --noinput
```

Put app templates at `templates/<appname>/<view>.html`. The `'DIRS': [BASE_DIR / 'templates']` setting in `TEMPLATES` makes Django find them.

---

## 10. Lightweight Polling for Notifications

For simple badges (e.g. unread counts, pending items), polling a JSON endpoint is simpler and more reliable than opening a dedicated WebSocket:

```python
# views.py
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

@login_required
def notification_count(request):
    count = Notification.objects.filter(user=request.user, is_read=False).count()
    return JsonResponse({'count': count})
```

```javascript
// base.html — only runs when logged in
const badge = document.getElementById('notif-badge');
function poll() {
    fetch('/notifications/count/')
        .then(r => r.json())
        .then(({ count }) => {
            badge.textContent = count > 9 ? '9+' : count;
            badge.classList.toggle('hidden', count === 0);
        });
}
poll();
setInterval(poll, 5000);
```

---

## 11. Management Commands (Seeding Data)

```
myapp/
  management/
    __init__.py        ← required (can be empty)
    commands/
      __init__.py      ← required (can be empty)
      seed_data.py
```

Both `__init__.py` files must exist or Django won't discover the command.

```python
from django.core.management.base import BaseCommand

SEED_DATA = [...]

class Command(BaseCommand):
    help = 'Seed initial data'

    def handle(self, *args, **kwargs):
        for item in SEED_DATA:
            MyModel.objects.get_or_create(name=item['name'], defaults=item)
        self.stdout.write(self.style.SUCCESS('Done'))
```

```bash
venv/bin/python manage.py seed_data
```

---

## 12. Running the Server

```bash
venv/bin/python manage.py migrate
venv/bin/python manage.py collectstatic --noinput
venv/bin/daphne -b 0.0.0.0 -p 8000 myproject.asgi:application
```

---

## 13. Common Pitfalls

| Symptom | Root cause | Fix |
|---|---|---|
| `AppRegistryNotReady` at startup | App imports in `asgi.py` before `django.setup()` | Move `os.environ.setdefault` + `django.setup()` to the very top, before all other imports |
| `KeyError: 'user'` in a consumer | `AuthMiddlewareStack` missing from ASGI routing | Wrap `URLRouter` with `AuthMiddlewareStack` in `asgi.py` |
| Admin panel has no CSS | Daphne doesn't serve static files like `runserver` does | Add `static()` to `urls.py` and run `collectstatic` |
| Template data rendered in the wrong place | Context variable named `messages` clashes with Django's messages framework | Rename the variable — use anything other than `messages` |
| Duplicate rows returned by a queryset | Filtering across a joined table without `.distinct()` | Add `.distinct()` after any `.filter()` that involves a join |
| Staff accounts visible to regular users | Not excluded from the queryset | Add `.exclude(is_superuser=True)` to public-facing queries |
| Custom management command not found | Missing `__init__.py` in `management/` or `management/commands/` | Add empty `__init__.py` to both directories |
