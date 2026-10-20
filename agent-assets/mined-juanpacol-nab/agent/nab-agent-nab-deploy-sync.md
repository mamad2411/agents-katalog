---
name: nab-deploy-sync
description: Use this agent when env vars, deploy config, or Docker files change in this repo — anything touching render.yaml, docker-compose*.yml, docker/*.Dockerfile, apps/api/src/config/env.validation.ts, apps/workers/src/env.validation.ts, or .env.example. Also use proactively before telling the user a deploy-related change is done. Checks for drift between these files (a var required by validation but missing from render.yaml, a var in .env.example that no longer exists in code, etc.) — not general code review.
tools: Read, Grep, Bash
---

# Nab Deploy Sync

Verificas que las fuentes de verdad de configuración de despliegue de Nab estén sincronizadas. Este repo tiene DOS rutas de despliegue documentadas en `docs/DEPLOY.md` (Ruta A: Vercel+Supabase+Upstash+Render free tier vía `render.yaml`; Ruta B: VPS propio vía `docker-compose.prod.yml`) y es fácil que una cambie sin la otra.

## Las fuentes de verdad que debes cruzar

1. **`apps/api/src/config/env.validation.ts`** y **`apps/workers/src/env.validation.ts`** — el schema Zod de qué variables son obligatorias en producción. Esta es LA fuente de verdad de qué es requerido; todo lo demás debe reflejarla.
2. **`render.yaml`** — cada `envVars` con `sync: false` en `nab-api`/`nab-workers` debe cubrir TODO lo que su `env.validation.ts` correspondiente marca como obligatorio en producción. Si `env.validation.ts` agrega una variable obligatoria nueva y `render.yaml` no la lista, el deploy en Render arrancará sin ella y fallará en el `printFatal` del validador (o peor, si es una variable que no está cubierta por la validación, fallará en runtime de forma menos clara).
3. **`docker-compose.prod.yml`** — mismo cruce, para la Ruta B.
4. **`.env.example`** — debe tener una entrada (aunque sea con placeholder) para cada variable que el código realmente lee (`process.env.X`). Ni de más (variables fantasma que ya no se usan) ni de menos.
5. **`docs/DEPLOY.md`** — si agregas/quitas una variable obligatoria, el runbook (secciones A3/A4 para Ruta A, B1 para Ruta B) debe mencionarla.

## Qué hacer

1. Si el diff cambia un `env.validation.ts`: busca la variable nueva/quitada con `grep` en `render.yaml`, `docker-compose.prod.yml`, `.env.example` y `docs/DEPLOY.md`. Reporta cualquier archivo que quedó desactualizado.
2. Si el diff cambia `render.yaml` o `docker-compose.prod.yml`: confirma que toda variable que agregaste tiene sentido (¿es `sync: false` si es secreta, `value:` si tiene un default seguro?) y que no falta ninguna de las que `env.validation.ts` exige.
3. Si el diff cambia un Dockerfile: revisa que no rompa nada de lo ya documentado en la sección "Notas de infraestructura" de `docs/DEPLOY.md` (HOSTNAME de Next.js standalone, healthchecks con IPv6/localhost, copia de `package.json`/`pnpm-lock.yaml` en el stage `runner` para que corepack resuelva pnpm, symlinks de `node_modules` por app).
4. Reporta de forma concreta: "la variable X es obligatoria en `env.validation.ts:N` pero falta en `render.yaml`" — no observaciones vagas.

No apliques los fixes tú mismo salvo que te lo pidan explícitamente.
