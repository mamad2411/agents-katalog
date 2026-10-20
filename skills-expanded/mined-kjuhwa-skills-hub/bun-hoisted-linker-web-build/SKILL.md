---
name: bun-hoisted-linker-web-build
description: Use `bun install --linker=hoisted` in multi-stage Dockerfiles that build Vite/Rollup frontends, because Bun's default isolated linker places packages under `node_modules/.bun/` via symlinks that Rollup cannot resolve.
category: docker
version: 1.0.0
version_origin: extracted
tags: [bun, docker, vite, rollup, linker, monorepo]
confidence: high
source_type: extracted-from-git
source_url: https://github.com/coleam00/Archon.git
source_ref: dev
source_commit: d89bc767d291f52687beea91c9fcf155459be0d9
source_project: Archon
imported_at: 2026-04-18T00:00:00Z
---

# `bun install --linker=hoisted` for Vite Frontend Builds

## When to use

- You have a Bun-based monorepo with a Vite/Rollup-built web package (React/Vue/Svelte).
- Your production Dockerfile uses `bun install` in a builder stage, then `bun run build:web`.
- You're seeing Rollup errors: "Cannot resolve module X", "Failed to resolve entry for workspace", or silently-empty `dist/` output.

Bun's default linker is `isolated`: packages live in `node_modules/.bun/<name>@<version>/node_modules/<name>` and the top-level `node_modules/` has symlinks. This works at runtime for Bun, but **Vite/Rollup walk `node_modules` directly for resolution and cannot follow the `.bun/` indirection** during production builds.

## Steps

1. **In the deps/build stages**, switch to the hoisted linker:

   ```dockerfile
   RUN bun install --frozen-lockfile --linker=hoisted
   ```

2. **If the stage only needs production deps**, use the equivalent flags:

   ```dockerfile
   RUN bun install --frozen-lockfile --production --ignore-scripts --linker=hoisted
   ```

   `--ignore-scripts` suppresses `postinstall` / husky `prepare` hooks that shouldn't run in a container.

3. **Verify the web build actually emitted an `index.html`** right after it runs, so a silent failure is loud:

   ```dockerfile
   RUN bun run build:web && \
       test -f packages/web/dist/index.html || \
       (echo "ERROR: Web build produced no index.html" >&2 && exit 1)
   ```

4. **Copy the web dist from the build stage into the final stage** with an explicit multi-stage `COPY --from=`:

   ```dockerfile
   COPY --from=web-build /app/packages/web/dist/ ./packages/web/dist/
   ```

5. **Copy every workspace `package.json`** before running `bun install`. Bun's workspace lockfile resolves based on *all* workspace package manifests; missing even one causes lockfile mismatch and the build fails with `bun install --frozen-lockfile`.

   ```dockerfile
   COPY package.json bun.lock ./
   COPY packages/core/package.json ./packages/core/
   COPY packages/web/package.json ./packages/web/
   # … every workspace package.json …
   ```

## Counter / Caveats

- `--linker=hoisted` gives a classic flat `node_modules` — larger disk footprint than isolated, but portable across tools that expect that layout. For dev-only environments where Bun is the only runtime, isolated is fine.
- **Don't** toggle linker between builder and production stages — if you `bun install` in one mode then `bun install` again in the other, node_modules layout changes and cached layers invalidate.
- You do not need `--linker=hoisted` for Bun-only runtime paths (backend `bun run start`). Bun handles its own indirection at runtime.
- When migrating off Yarn / npm, you might have scripts that grep `node_modules/<pkg>/dist/...` — the hoisted linker matches that expectation too.

## Evidence

- `Dockerfile` lines 32-36: "--linker=hoisted: Bun's default 'isolated' linker stores packages in node_modules/.bun/ with symlinks that Vite/Rollup cannot resolve during production builds. Hoisted layout gives classic flat node_modules."
- Same Dockerfile uses the flag in both install stages: lines 36 (deps) and 148 (production).
- Web-build verification at lines 47-49: `test -f packages/web/dist/index.html || (echo "ERROR: …" && exit 1)`.
- All workspace `package.json` copies at lines 17-30 and 132-145, with a note that `docs-web/package.json` is still copied "only so Bun's workspace lockfile resolves correctly."
- Commit SHA: d89bc767d291f52687beea91c9fcf155459be0d9.
