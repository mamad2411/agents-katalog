---
name: dockerfile-production
description: Dockerfiles de producción para el stack (API NestJS con yarn 4, Angular SSR, Astro) — multi-stage, base mínima fijada, usuario no root, .dockerignore, caché con Corepack y BuildKit, solo deps de producción al final, HEALTHCHECK con curl/wget presente, señales y PID 1, sin secretos en capas ni ARG, tamaño y escaneo de vulnerabilidades. Usar al escribir o revisar un Dockerfile, al pasar de Nixpacks a Dockerfile, cuando la imagen pesa o el build es lento, o cuando el contenedor no se apaga limpio.
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# Dockerfile de producción

La imagen es el artefacto que se despliega: si está mal, Coolify no lo arregla. Cómo la corre
Coolify (puertos, healthcheck, variables) está en `coolify-deployment`; seguridad general en
`security-guardrails`. Sintaxis verificada contra docs.docker.com/reference/dockerfile.

## 1. Principios

1. **Multi-stage**: una etapa construye con todo; la final lleva solo runtime + artefactos.
2. **Base mínima y fijada**: `node:22-alpine` o `node:22-slim` por versión mayor (definí la
   versión en el CLAUDE.md del proyecto y mantenela igual a CI y `.nvmrc`). Nunca `latest`.
3. **Usuario no root**: la imagen `node` trae el usuario `node`; usalo en la etapa final.
4. **Reproducible**: `yarn install --immutable` con lockfile; el build falla si el lock cambia.
5. **Sin secretos**: nada en `ENV`, `ARG`, `COPY .env`. Los `ARG` quedan visibles en
   `docker history` y en las attestations de provenance; usá `RUN --mount=type=secret`.
6. **Chico**: cada MB extra es tiempo de deploy y superficie de ataque.
7. **Apagado limpio**: el proceso recibe `SIGTERM` (forma exec de `CMD`) y cierra conexiones.

## 2. `.dockerignore` (obligatorio)

```
node_modules
dist
.git
.env*
*.md
coverage
test
playwright-report
.yarn/cache
```
Sin él, `COPY . .` mete `node_modules` local, `.env` y `.git` en la imagen e invalida la caché.

## 3. Yarn 4 con Corepack

- `corepack enable` en la etapa base. Desde Node 25 Corepack ya no viene incluido: instalalo con
  `npm install -g corepack` (verificar según la versión de Node que uses).
- El `packageManager` del `package.json` fija la versión de Yarn; Corepack la respeta.
- Yarn 4 no tiene `yarn install --production`. Para la etapa final:
  `yarn workspaces focus --all --production` (no acepta `--immutable`; el lock ya quedó validado
  en la etapa de build). Alternativa: copiar `node_modules` completos si el peso es aceptable.
- Con `nodeLinker: node-modules` el runtime no necesita `.pnp.cjs`; con PnP copiá `.pnp.*`,
  `.yarn/` y `.yarnrc.yml`. Definí el linker en el proyecto y no lo mezcles.

## 4. API NestJS (ESM)

```dockerfile
# syntax=docker/dockerfile:1
FROM node:22-alpine AS base
RUN corepack enable
WORKDIR /app

FROM base AS deps
COPY package.json yarn.lock .yarnrc.yml ./
COPY .yarn ./.yarn
RUN --mount=type=cache,target=/root/.yarn/berry/cache yarn install --immutable

FROM deps AS build
COPY . .
RUN yarn build && yarn workspaces focus --all --production

FROM node:22-alpine AS runtime
RUN apk add --no-cache curl
ENV NODE_ENV=production
WORKDIR /app
COPY --from=build --chown=node:node /app/dist ./dist
COPY --from=build --chown=node:node /app/node_modules ./node_modules
COPY --from=build --chown=node:node /app/package.json ./
USER node
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
  CMD curl --fail http://localhost:3000/health || exit 1
CMD ["node", "dist/main.js"]
```
Ajustá `dist/main.js` al `outDir` real del proyecto. Si la app necesita compilar nativos,
agregá `python3 make g++` **solo** en la etapa `deps`.

## 5. Angular SSR

El build con el application builder genera `dist/<app>/browser/` (estático) y
`dist/<app>/server/server.mjs` (proceso Node). Es un **servidor**, no un sitio estático.

```dockerfile
FROM node:22-alpine AS build
RUN corepack enable
WORKDIR /app
COPY package.json yarn.lock .yarnrc.yml ./
COPY .yarn ./.yarn
RUN yarn install --immutable
COPY . .
RUN yarn build

FROM node:22-alpine AS runtime
RUN apk add --no-cache wget
ENV NODE_ENV=production PORT=4000
WORKDIR /app
COPY --from=build --chown=node:node /app/dist/<app> ./dist/<app>
USER node
EXPOSE 4000
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
  CMD wget -qO- http://localhost:4000/ >/dev/null || exit 1
CMD ["node", "dist/<app>/server/server.mjs"]
```
El puerto lo lee tu `server.ts` (el scaffold del CLI usa la variable `PORT`; verificalo en el
proyecto). Si el `server.mjs` importa dependencias no bundleadas, copiá también `node_modules`
de producción como en §4. Astro estático: no necesita Dockerfile (Static pack); Astro con
adapter Node se trata igual que esta receta.

## 6. `HEALTHCHECK`

Opciones: `--interval` (30s), `--timeout` (30s), `--start-period` (0s), `--start-interval`
(5s), `--retries` (3). La imagen final **debe traer `curl` o `wget`** (Alpine no trae `curl`;
`wget` de busybox sí, pero verificá). Coolify usa el `HEALTHCHECK` de la imagen si existe; el
endpoint debe fallar hasta que la app pueda servir (base conectada), no devolver 200 fijo.

## 7. Señales y PID 1

- `CMD ["node", "..."]` en forma **exec**: con forma shell, `sh` es PID 1 y no reenvía `SIGTERM`.
- Nada de `npm start`/`yarn start` como entrypoint: agregan un proceso intermedio.
- La app maneja `SIGTERM`: en NestJS `app.enableShutdownHooks()`; cerrar servidor HTTP, pool de
  base y colas dentro del Stop Grace Period configurado en Coolify.
- Si hay procesos hijos o zombies, `--init` en las opciones de run o `tini` como entrypoint.

## 8. Secretos en build

```dockerfile
RUN --mount=type=secret,id=npm_token,env=NPM_TOKEN yarn install --immutable
```
Se pasa con `docker build --secret id=npm_token,env=NPM_TOKEN`; en Coolify activá **Use Docker
Build Secrets** (BuildKit). Nunca `ARG NPM_TOKEN`.

## 9. Tamaño y vulnerabilidades

- Medí: `docker image ls` y `docker history <img>`; una capa gigante = algo sobró.
- Escaneo en CI: `docker scout cves <img>` o Trivy (`trivy image <img>`), fallar por severidad
  alta/crítica con excepciones justificadas y con fecha.
- Reconstruí periódicamente aunque no cambie el código: la base recibe parches.

## 10. Anti-patrones

- `FROM node` sin tag; `COPY . .` antes de instalar deps (rompe la caché en cada cambio).
- `RUN yarn install` sin `--immutable`; `npm` y `yarn` mezclados.
- `USER root` en la final "porque el puerto 80"; escuchá en >1024 y dejá el proxy.
- `.env` copiado; secretos en `ENV`.
- `CMD yarn start`; sin `HEALTHCHECK`; healthcheck que siempre responde 200.
- Devtools, tests y Playwright en la imagen final.

## Checklist

- [ ] Multi-stage; base fijada por versión mayor; final con usuario `node`.
- [ ] `.dockerignore` presente; deps instaladas antes de copiar el código.
- [ ] `yarn install --immutable` en build; solo producción en la final.
- [ ] Sin `ARG`/`ENV`/`COPY` de secretos; Build Secrets si hacen falta.
- [ ] `HEALTHCHECK` real y `curl`/`wget` en la imagen final.
- [ ] `CMD` en forma exec; `SIGTERM` manejado; apagado dentro del grace period.
- [ ] Imagen escaneada en CI; tamaño revisado con `docker history`.
- [ ] Probado localmente: `docker build` + `docker run -p` + healthcheck `healthy` antes de Coolify.
