---
name: project-scaffolding
description: |
  Project setup and scaffolding for new apps. Apply when starting a new project, adding a
  new service, or setting up a new module. Covers directory structure templates for
  React+Vite frontend, Django backend, FastAPI backend, and full-stack setups.
---

# Project Scaffolding

## React + Vite + TypeScript Frontend
```bash
npm create vite@latest my-app -- --template react-ts
cd my-app
npm install

# Core dependencies
npm install \
  @tanstack/react-query @tanstack/react-query-devtools \
  zustand \
  framer-motion \
  react-hook-form @hookform/resolvers zod \
  axios \
  lucide-react \
  clsx tailwind-merge

# Dev dependencies
npm install -D \
  @types/node \
  vitest @testing-library/react @testing-library/user-event \
  playwright \
  eslint @typescript-eslint/eslint-plugin @typescript-eslint/parser \
  tailwindcss postcss autoprefixer

npx tailwindcss init -p
```

### Directory Structure
```
src/
├── assets/              # Static files: fonts, images, icons
├── components/
│   ├── atoms/           # Button, Input, Badge, Spinner, Avatar
│   ├── molecules/       # Card, Modal, SearchBar, FormField
│   ├── organisms/       # Header, Sidebar, DataTable, ProductGrid
│   └── templates/       # PageLayout, AuthLayout, DashboardLayout
├── hooks/               # useDebounce, useLocalStorage, useMediaQuery
├── lib/
│   ├── api.ts           # Axios instance + interceptors
│   ├── queryClient.ts   # TanStack Query client config
│   └── utils.ts         # cn(), formatPrice(), formatDate()
├── pages/               # Route-level components
├── router/              # React Router setup
├── stores/              # Zustand stores
└── types/               # Shared TypeScript interfaces
```

## Django + DRF Backend
```bash
python -m venv venv && source venv/bin/activate
pip install django djangorestframework django-cors-headers \
  djangorestframework-simplejwt django-filter drf-spectacular \
  celery redis django-redis Pillow python-magic \
  structlog sentry-sdk psycopg2-binary python-dotenv \
  gunicorn whitenoise

django-admin startproject config .
python manage.py startapp users
python manage.py startapp orders
```

### App Directory Structure
```
backend/
├── config/
│   ├── settings/
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   ├── urls.py
│   ├── wsgi.py
│   └── celery.py
├── apps/
│   ├── core/            # Base models, pagination, exceptions, utils
│   ├── users/           # Auth, profiles, permissions
│   ├── orders/          # Order management
│   └── notifications/   # Email, Telegram, push
├── requirements/
│   ├── base.txt
│   ├── development.txt
│   └── production.txt
├── Dockerfile
├── docker-compose.yml
└── .env.example
```

## Telegram Bot (aiogram)
```bash
pip install aiogram redis aioredis sqlalchemy aiosqlite \
  python-dotenv structlog

mkdir -p bot/{handlers,keyboards,middlewares,states,database,utils}
touch bot/{main.py,config.py}
touch bot/handlers/{__init__.py,start.py,admin.py}
touch bot/keyboards/{reply.py,inline.py}
touch bot/states/forms.py
touch bot/database/{models.py,crud.py}
```

## .env.example Template
```bash
# App
DEBUG=true
SECRET_KEY=change-me-in-production
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=myapp
DB_USER=myapp_user
DB_PASSWORD=change-me
DB_HOST=localhost
DB_PORT=5432
DATABASE_URL=postgresql://myapp_user:change-me@localhost:5432/myapp

# Redis
REDIS_URL=redis://localhost:6379/0
REDIS_PASSWORD=

# Telegram
BOT_TOKEN=
BOT_WEBHOOK_URL=

# Payments
PAYME_MERCHANT_ID=
PAYME_SECRET_KEY=
CLICK_SERVICE_ID=
CLICK_SECRET_KEY=

# Storage
S3_ENDPOINT=
S3_ACCESS_KEY=
S3_SECRET_KEY=
S3_BUCKET=
CDN_URL=

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=

# Sentry
SENTRY_DSN=
```
