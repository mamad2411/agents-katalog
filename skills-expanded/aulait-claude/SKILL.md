# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

@AGENTS.md

## Teaching mode

TEACH. DO NOT WRITE ANY CODE.

When explaining something, give the idiomatic answer and link to resources to learn why. Do not over-explain each detail.

When writing commit messages, do not make them oververbose.

## Commands

- `npm run dev` — start the dev server
- `npm run build` — production build
- `npm run start` — run a production build
- `npm run lint` — ESLint (flat config via `eslint.config.mjs`, extends `eslint-config-next`)
- `npm run migrate` — run `app/api/database/migrations.ts` directly with `tsx` to (re)create SQLite tables

There is no test runner configured in this repo yet.

## Architecture

This is a Next.js App Router project (`app/` directory) using React 19, Tailwind v4, and TypeScript with the `@/*` path alias mapped to the repo root.

**Auth**: [auth.ts](auth.ts) is the single NextAuth (Auth.js v5 beta) config, exporting `handlers`, `signIn`, `signOut`, and `auth`. Google is currently the only provider. [proxy.ts](proxy.ts) re-exports `auth` as `proxy` — this project uses the `proxy` convention rather than a `middleware.ts` file, so check the version-pinned docs (see below) before assuming standard Next.js middleware behavior applies. Client components trigger sign-in via a server action that calls `signIn(...)` directly (see [components/ui/google-sign-in.tsx](components/ui/google-sign-in.tsx)) rather than hitting a route handler.

**Database**: SQLite via the callback-based `sqlite3` package, not `better-sqlite3` or the `sqlite` wrapper (despite `sqlite` being a dependency, it isn't used). [app/api/database/database.ts](app/api/database/database.ts) opens a single shared `db` connection at `database/database.db` (relative to `process.cwd()`) and exposes two promisified helpers:
- `apiGet(query)` — wraps `db.all`
- `apiPost(query, values)` — wraps `db.run` with parameterized values

All API routes should go through these helpers rather than calling `db` directly, to keep the callback-to-promise handling in one place. [app/api/database/migrations.ts](app/api/database/migrations.ts) defines schema (`CREATE TABLE IF NOT EXISTS ...`) and calls `migrate()` both on import and via the `migrate` npm script — importing this module has a side effect of running migrations.

**API routes**: Standard App Router route handlers under `app/api/**/route.ts` (e.g. [app/api/test/route.ts](app/api/test/route.ts)) exporting `GET`/`POST` functions that read `Request` and return `Response.json(...)`.

## Important note on Next.js version

Per [AGENTS.md](AGENTS.md), the pinned `next` version (16.2.12) is newer than this model's training data and may have breaking API/convention changes (the `proxy.ts` vs `middleware.ts` naming above is one observed example). Before relying on Next.js APIs from memory, check `node_modules/next/dist/docs/` for the installed version's own documentation — run `npm install` first if `node_modules` isn't present.
