---
name: productivity-onboard
description: Genera ONBOARDING.md para un proyecto a partir de su especificación (productivity-spec) y scaffolding (productivity-scaffold). Incluye quick start (<5 min), stack con enlaces a dev-kits, arquitectura explicada por módulo, setup manual, cómo testear, cómo deployar, y recursos. Úsala después de productivity-scaffold, al entregar un proyecto, o cuando un dev nuevo se une al equipo. Dispara con "genera onboarding", "guía para nuevo dev", "cómo levantar el proyecto", "README de arquitectura", "onboarding doc".
requires-devkits: auto-detect
---

# Productivity Onboard — Guía de Arranque

Genera `ONBOARDING.md`: todo lo que un dev nuevo necesita para ser productivo en <30 minutos.

---

## Workflow

### Paso 1: Recolectar contexto

Si viene de `productivity-spec` + `productivity-scaffold`, el stack y la estructura ya están definidos. Si no, pregunta en un solo mensaje:

1. **Stack** (si no se detecta automáticamente)
2. **Servicios externos**: ¿Redis, Stripe, AWS S3, Azure Blob, correos, etc.?
3. **URLs**: staging, producción, Swagger/OpenAPI, dashboards (Grafana, Sentry)
4. **Contactos**: ¿Quién es el tech lead? ¿Canal de Slack/Teams del equipo?
5. **¿Qué es lo más difícil de entender del proyecto?** (el usuario puede dar contexto que el código no revela)

### Paso 2: Analizar la estructura del proyecto

Para cada módulo/carpeta de primer nivel:

| Artefacto | Cómo analizarlo |
|-----------|----------------|
| `src/modules/orders/` | Leer `controller`, `service`, `repository`. 1-2 funciones clave. Comentarios/JSDoc si existen. |
| `src/modules/catalog/` | Ídem. Identificar diferencias con otros módulos (ej: usa Redis, usa Elasticsearch) |
| `src/shared/` | Middleware, utilidades, errores comunes, helpers de paginación |
| `config/` | Variables de entorno, archivos de configuración, secrets |
| `tests/` | Estructura de tests, comandos para ejecutar, tipos de tests |
| `.github/` | CI pipeline, stages, secrets necesarios |
| `k8s/` / `infra/` | Manifiestos, Helm charts, ArgoCD apps |
| `Dockerfile` | Multi-stage? Base image? Healthcheck? |
| `docker-compose.yml` | Servicios locales, dependencias entre ellos |

### Paso 3: Generar ONBOARDING.md

Estructura obligatoria:

```markdown
# 🚀 Onboarding — [Nombre del Proyecto]

> ⏱️ Tiempo estimado de setup: [5-15 minutos]
> 👤 Tech lead: [nombre / contacto]
> 💬 Canal del equipo: [Slack/Teams]

---

## ⚡ Quick Start (< 5 min)

```bash
git clone [repo-url] && cd [proyecto]
cp .env.example .env
docker compose up
```
Abrir http://localhost:[puerto]

[Si no usa Docker, lista los pasos manuales mínimos]

---

## 🧱 Stack

| Capa | Tecnología | Dev-Kit |
|------|-----------|---------|
| Backend | Node.js 24 + Express 5 | `nodejs-core`, `nodejs-express` |
| Frontend | React 19 + Ant Design 5.29 | `react-core`, `react-antdesign` |
| Database | PostgreSQL 18 | `postgresql-core` |
| ORM | Drizzle | `nodejs-database` |
| CI/CD | GitHub Actions + ArgoCD | `devops-cicd` |

---

## 🏗️ Arquitectura

### Vista general

```mermaid
graph TD
    Web[React Frontend :5173] --> API[Express API :3000]
    API --> Orders[Orders Module]
    API --> Catalog[Catalog Module]
    Orders --> DB[(PostgreSQL :5432)]
    Orders --> Redis[(Redis :6379)]
    Catalog --> DB
```

### Módulos

#### `orders/` — Órdenes de compra
**Patrón**: Controller-Service-Repository (Vertical Slice).
- `orders.controller.ts`: endpoints REST — POST (crear), GET (listar/obtener), DELETE (cancelar)
- `orders.service.ts`: lógica de negocio — validación de estados, cálculo de totales, integración con Stripe
- `orders.repository.ts`: queries Drizzle — findMany con filtros, create con transacción
- `orders.schema.ts`: Zod schemas compartidos (CreateOrder, OrderResponse)

#### `catalog/` — Catálogo de productos
Similar a orders, pero con:
- Cache Redis en lecturas (TTL 5 min)
- Índice GIN en PostgreSQL para full-text search
- Endpoint de búsqueda con paginación keyset

### Shared
- `middleware/auth.ts`: JWT verification — extrae `req.user`
- `middleware/error-handler.ts`: captura `AppError` y devuelve JSON estructurado
- `errors/app-error.ts`: `AppError` base con statusCode y code

---

## 🔧 Setup Manual

### Variables de entorno (.env)
| Variable | Descripción | Ejemplo | Obligatoria |
|----------|------------|---------|-------------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@localhost:5432/miapp` | ✅ |
| `JWT_SECRET` | Secret para firmar tokens | `openssl rand -hex 32` | ✅ |
| `STRIPE_API_KEY` | API key de Stripe (test mode) | `sk_test_...` | Solo para pagos |
| `REDIS_URL` | Redis connection string | `redis://localhost:6379/0` | Solo para caché |
| `CORS_ORIGIN` | Frontend URL | `http://localhost:5173` | ✅ |

### Base de datos
```bash
# Crear migraciones (si no existen)
npx drizzle-kit generate

# Aplicar migraciones
npx drizzle-kit migrate

# (Opcional) Seed data de prueba
npm run db:seed
```

### Servicios externos
- **Stripe**: webhook local con `stripe listen --forward-to localhost:3000/api/webhooks/stripe`
- **Redis**: incluido en `docker compose up`. Si no usas Docker: `redis-server`

---

## 🧪 Testing

| Comando | Qué hace |
|---------|----------|
| `npm test` | Unit + integration tests (Vitest) |
| `npm run test:watch` | Watch mode |
| `npm run test:e2e` | E2E tests (Playwright) |
| `npm run test:coverage` | Coverage report |

**Convenciones:**
- Tests en `src/**/*.test.ts` (co-ubicados con el código)
- Integration tests usan Testcontainers (PostgreSQL real, no mock)
- E2E en `tests/e2e/` con Playwright
- MSW para mock de APIs externas (Stripe)

---

## 🚀 Deploy

### CI/CD Pipeline
```
Push a main
  → GitHub Actions: lint + typecheck + test
  → Build Docker image + push a ghcr.io
  → ArgoCD sync en staging
  → Smoke tests en staging
  → (manual) Promote a producción
```

### Ambientes
| Ambiente | URL | Branch |
|----------|-----|--------|
| Local | http://localhost:5173 | `main` (con --watch) |
| Staging | https://staging.miapp.com | `main` |
| Producción | https://miapp.com | `production` |

### Acceder a logs
- **Local**: `docker compose logs -f app`
- **Staging/Prod**: Grafana → Explore → Loki → `{app="miapp-api"}`

---

## 📚 Recursos

- **Spec técnica**: [docs/spec.md](docs/spec.md)
- **Dev-Kits**: `dotnet-core`, `react-core`, `postgresql-core` — cargados en Pi
- **Postman Collection**: [docs/api.postman_collection.json](docs/api.postman_collection.json)
- **Arquitectura detallada**: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
```

### Paso 4: Adaptar al lector

Detectar si el lector es backend, frontend o full-stack (preguntar o inferir) y marcar secciones relevantes:

```markdown
> 🎯 **Eres backend?** Enfócate en `src/modules/` y `API.md`.
> 🎨 **Eres frontend?** Enfócate en `src/app/` y `ARCHITECTURE.md` (diagrama).
```

### Paso 5: Guardar y ofrecer next steps

```
✅ ONBOARDING.md generado en la raíz del proyecto.
📄 6 secciones: quick start, stack, arquitectura, setup, testing, deploy.

¿Quieres...?
1. Agregar sección de "Preguntas frecuentes" (FAQs del equipo)
2. Agregar contactos del equipo
3. Generar también ARCHITECTURE.md detallado (productivity-docs)
```

---

## Reglas

- **Quick start DEBE ser <5 min.** Si requiere más pasos, el proyecto no está listo para onboardear.
- **Una sección por módulo.** No agrupar módulos no relacionados.
- **Lenguaje humano.** Nada de "el controlador inyecta el servicio vía DI con Scoped lifetime". Decir "el controlador usa el servicio para la lógica de negocio".
- **Variables de entorno todas listadas.** Si falta una y el dev se entera en runtime, el onboarding falló.
- **Comandos copiables.** Todo en bloques `bash`.
