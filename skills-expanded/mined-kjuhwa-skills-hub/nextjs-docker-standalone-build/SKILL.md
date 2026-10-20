---
name: nextjs-docker-standalone-build
description: Three-stage Docker build for a Next.js app with pnpm workspaces — deps / builder / runner stages, standalone output for a minimal production image.
category: devops
version: 1.0.0
tags: [docker, nextjs, pnpm, monorepo, standalone]
source_type: extracted-from-git
source_url: https://github.com/multica-ai/multica.git
source_ref: main
source_commit: 6cd49e132de7632b1f2aaa675c98e8eca9308bb7
source_project: multica
imported_at: 2026-04-18T00:00:00Z
version_origin: extracted
confidence: high
---

## When to use

- Deploying a Next.js app that lives inside a pnpm workspace with shared packages.
- You want the production image to contain only the traced node_modules, not the full monorepo.
- You need a deterministic reproducible build with `pnpm install --frozen-lockfile`.

## Steps

1. **Deps stage** — resolve dependencies from the full workspace but without copying source. This gets cached unless package.jsons change:
   ```dockerfile
   FROM node:22-alpine AS deps
   RUN corepack enable && corepack prepare pnpm@10.28.2 --activate
   WORKDIR /app
   COPY pnpm-lock.yaml pnpm-workspace.yaml package.json turbo.json .npmrc ./
   COPY apps/web/package.json apps/web/
   COPY packages/core/package.json packages/core/
   COPY packages/ui/package.json packages/ui/
   COPY packages/views/package.json packages/views/
   COPY packages/tsconfig/package.json packages/tsconfig/
   RUN pnpm install --frozen-lockfile
   ```
2. **Builder stage** — overlay the source, re-link pnpm symlinks, build:
   ```dockerfile
   FROM node:22-alpine AS builder
   RUN corepack enable && corepack prepare pnpm@10.28.2 --activate
   WORKDIR /app
   COPY --from=deps /app ./
   COPY package.json turbo.json pnpm-workspace.yaml ./
   COPY apps/web/ apps/web/
   COPY packages/ packages/
   RUN pnpm install --frozen-lockfile --offline
   ARG REMOTE_API_URL=http://backend:8080
   ENV REMOTE_API_URL=$REMOTE_API_URL
   ENV STANDALONE=true
   RUN pnpm --filter @org/web build
   ```
   The second install with `--offline` re-creates symlinks the COPY overwrote.
3. In `apps/web/next.config.ts`, enable standalone output:
   ```ts
   export default {
     output: process.env.STANDALONE ? "standalone" : undefined,
     transpilePackages: ["@org/core", "@org/ui", "@org/views"],
   };
   ```
4. **Runner stage** — copy only the standalone output + static + public:
   ```dockerfile
   FROM node:22-alpine AS runner
   WORKDIR /app
   ENV NODE_ENV=production
   RUN addgroup --system --gid 1001 nodejs && adduser --system --uid 1001 nextjs
   COPY --from=builder --chown=nextjs:nodejs /app/apps/web/.next/standalone ./
   COPY --from=builder --chown=nextjs:nodejs /app/apps/web/.next/static ./apps/web/.next/static
   COPY --from=builder --chown=nextjs:nodejs /app/apps/web/public ./apps/web/public
   USER nextjs
   EXPOSE 3000
   ENV PORT=3000 HOSTNAME=0.0.0.0
   CMD ["node", "apps/web/server.js"]
   ```

## Example

Image size: ~150-250 MB runner vs 1 GB+ for "copy the whole repo and run `pnpm start`". Build time: first ~3 min, subsequent ~45 s once deps stage caches.

## Caveats

- If you add or remove a shared package, update the deps-stage `COPY` list.
- Standalone output traces only what's imported from the app entrypoint — dynamic `require()` or runtime-loaded files may be missing and need explicit `outputFileTracingIncludes` config.
- The re-install in the builder is `--offline`; it fails if deps aren't already in the pnpm store from the deps stage.
