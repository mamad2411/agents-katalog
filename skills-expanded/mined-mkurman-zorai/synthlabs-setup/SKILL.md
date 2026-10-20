---
name: synthlabs-setup
description: Use when you need to locate, start, and verify a local SynthLabs backend before API-dependent work.

tags: [synthlabs, synthlabs-setup, api]
---

# SynthLabs Setup

## Overview

Use this skill to locate a real SynthLabs checkout, start the documented local services, and prove the backend is healthy before doing anything else.

## When to Use

Use this skill when:

- the task depends on a local SynthLabs checkout being present and healthy,
- generation, review, or curation work cannot start until the backend answers `/health`,
- you need to decide whether to use `npm`, `bun`, or the repo's Docker Compose path,
- or the operator asks you to start, verify, or troubleshoot a local SynthLabs instance.

Do not use this skill when:

- the task is not about SynthLabs,
- a healthy SynthLabs instance is already known and the work should move directly into generation, curation, or UI operation,
- or the operator is asking for backend route usage or verifier work rather than local setup.

## Key Requirements

- Verify backend health with `GET /health` before any session, generation, curation, or UI step.
- Never overwrite an existing `.env.local`.
- Never fabricate API keys, Firebase values, database credentials, or service-account paths.
- API keys may be required for provider-backed generation.
- Backend DB and Firebase settings are optional and depend on the workflow; leave them unset unless the operator or task explicitly needs backend persistence or cloud sync.

## Find the Checkout

Look for a repository root that contains all of these anchors:

- `package.json` with `"name": "synthlabs-reasoning-generator"`
- `server/index.js`
- `.env.example`

If the checkout location is not already known, verify the candidate repo before running commands there.

If no local checkout exists yet, clone the public repository first:

```bash
git clone https://github.com/mkurman/synthlabs.git
cd synthlabs
```

After cloning, re-check the repo anchors before continuing with install or startup work.

## Check Available Launch Paths

Confirm which package manager, runtime, and container tooling are installed before choosing commands:

```bash
command -v node
command -v npm
command -v bun
command -v docker
docker compose version
test -x ./mc.sh
```

- `npm` workflow: requires `node` and `npm`
- `bun` workflow: requires `bun`
- Docker workflow: requires `docker`, `docker compose`, and the repo's `./mc.sh` wrapper script
- If none of these launch paths are available, stop and ask the operator to install the needed tooling.

## Install Dependencies

From the SynthLabs checkout:

```bash
# npm path
npm install

# bun path
bun install
```

Use the package manager that is actually available. Do not invent lockfile or package-manager switches that the repo does not document.

## Prepare Local Environment

Check whether `.env.local` already exists before copying anything:

```bash
test -f .env.local
```

- If `.env.local` already exists, keep it and inspect it instead of replacing it.
- If `.env.local` is missing, copy from `.env.example`:

```bash
cp .env.example .env.local
```

Populate only the variables required for the chosen workflow:

- Provider-backed generation may require one or more API keys such as `VITE_GEMINI_API_KEY`, `VITE_OPENAI_API_KEY`, or other provider entries already present in `.env.example`.
- Backend DB and Firebase settings such as `FIREBASE_PROJECT_ID`, `FIREBASE_CLIENT_EMAIL`, `FIREBASE_PRIVATE_KEY`, `FIREBASE_SERVICE_ACCOUNT_PATH`, and related `VITE_FIREBASE_*` values are optional unless the task explicitly needs backend persistence, Firebase Admin operations, or cloud sync.

If you are using the Docker Compose path, check whether `.env` exists before starting `./mc.sh`:

```bash
test -f .env
```

- If `.env` is missing, copy from `.env.example`:

```bash
cp .env.example .env
```

- Do not overwrite an existing `.env`.

Do not add placeholder secrets or fake values.

## Start the Documented Scripts

From the SynthLabs checkout, use the documented scripts that match the task:

```bash
# frontend + backend together
npm run dev

# frontend only
npm run dev:client

# backend only
npm run dev:server

# bun frontend dev flow
bun run bun:dev

# Docker Compose manager
./mc.sh up

# Docker Compose backend only
./mc.sh up backend

# Docker Compose status and logs
./mc.sh status
./mc.sh logs backend
```

- Prefer `npm run dev` when the task needs the standard local stack.
- Use `npm run dev:server` when you only need the backend for API checks.
- Use `npm run dev:client` or `bun run bun:dev` when the task is frontend-only, but still verify whether a backend is already running before assuming API-dependent features will work.
- Use `./mc.sh up` when the task should run through the repo's Docker Compose stack, especially if it needs the bundled CockroachDB service.
- `./mc.sh` wraps `docker compose -f docker/docker-compose.yml ...` and exposes `up`, `down`, `stop`, `build`, `restart`, `logs`, `ps`, and `status`.

## Readiness Contract

The real backend port behavior comes from `server/index.js`:

- Default development backend port: `8787`
- Default production backend port: `8900`
- `PORT` overrides either default
- `PORT_RANGE` enables auto-increment when the requested port is busy
- A successful backend start logs `Backend listening on http://localhost:${port}`; use that line when it is available.

The Docker Compose path is different from the normal local dev path:

- `./mc.sh up` publishes the frontend on `http://localhost:3000`
- `./mc.sh up` publishes the backend on `http://localhost:8900`
- `./mc.sh up` also starts CockroachDB with admin UI on `http://localhost:8080`
- the compose backend runs with `NODE_ENV=production` and `PORT=8900`

When finding the selected port, check in this order:

1. A port explicitly set through `PORT`
2. Docker Compose backend `8900` when the repo was started through `./mc.sh`
3. Development default `8787` unless the task is clearly using production mode
4. Production default `8900` only when the environment is explicitly production
5. Higher ports opened by the backend because `PORT_RANGE` allowed auto-increment

Verify readiness with the health route before any other API call:

```bash
curl -fsS http://localhost:8787/health
```

For the Docker Compose path, verify the published backend directly:

```bash
curl -fsS http://localhost:8900/health
```

Healthy output must decode to JSON equivalent to:

```json
{"ok":true,"service":"synthlabs-rg"}
```

If the expected port does not answer, probe the configured or incremented range until `/health` returns the required payload.

## Common Mistakes

- Assuming a local checkout already exists when the repo still needs to be cloned.
- Starting `./mc.sh` without checking whether `.env` exists for the compose path.
- Replacing an existing `.env.local` instead of inspecting it first.
- Assuming `8787` is always correct even when `PORT` or `PORT_RANGE` changed the selected port.
- Assuming the containerized backend still listens on `8787` instead of the compose-published `8900`.
- Treating a running frontend as proof that backend APIs are ready without checking `/health`.
- Adding placeholder API keys, Firebase values, or database credentials just to unblock a task.

## If No Healthy Instance Is Found

- Confirm the SynthLabs repo was actually cloned locally if no checkout can be found.
- Confirm you are in the correct SynthLabs checkout.
- Confirm `node` and `npm` or `bun` are actually installed.
- Confirm dependencies were installed successfully.
- Confirm `.env.local` exists if the chosen workflow requires local configuration.
- Restart with the documented script that matches the needed surface.
- If `/health` never returns the required JSON, stop and report the exact command, port, and failure instead of guessing at follow-up API steps.