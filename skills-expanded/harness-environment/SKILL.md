---
name: harness-environment
description: >-
  Makes the project environment reproducible for agents — toolchain, env vars,
  services, and init.sh health checks. Use when setup fails, .env is missing,
  Docker/DB will not start, or a fresh checkout cannot run.
---

# Harness Environment

## What this does for you

- **Fresh checkout works** — toolchain, deps, and services documented
- **Secrets stay out of git** — `.env.example` lists required vars; real values stay local
- **Fail fast before features** — `init.sh` checks health; if it fails, fix the environment first

`harness-lifecycle` says *when* to run `init.sh`. This skill says *what must be healthy* before any feature work.

Based on Lesson 06 (initialization as its own phase) and the course bootstrap pattern.

## When to use

- Agent cannot install or start the project
- Missing or undocumented environment variables
- Database, Redis, or Docker not running
- "Works on my machine" but fails on a clean clone
- `harness-diagnose` attributed the failure to the **environment** layer

## Inspect first

Do not invent a stack. Infer from the repo:

| Signal | Likely stack |
|--------|----------------|
| `package.json` | Node (npm / pnpm / yarn / bun) |
| `pyproject.toml` / `requirements.txt` | Python |
| `docker-compose.yml` / `compose.yaml` | Local services |
| `supabase/`, `prisma/`, `drizzle/` | Database + migrations |
| `.nvmrc` / `.node-version` / `engines` | Runtime pin |

Ask only what you cannot infer: required secrets, which services must be up, whether Docker is expected.

## Bootstrap order

Always this sequence. Skip a step only if it does not apply:

```
1. Toolchain     — language runtime version matches the project pin
2. Dependencies  — lockfile install (do not invent versions)
3. Env files     — copy .env.example → .env if missing; never commit secrets
4. Services      — docker compose / managed DB as documented
5. Migrations    — schema matches the checked-out code
6. Health check  — one observable command (HTTP, CLI, or test smoke)
```

If any step fails, **stop**. Do not start feature work. Record the failing step in `progress.md`.

## init.sh health checks

`init.sh` must use `set -euo pipefail` and fail with a named step:

```bash
#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

echo "=== toolchain ==="
# Example: node --version matches .nvmrc if present

echo "=== dependencies ==="
# npm ci / pnpm install / python -m pip install

echo "=== env ==="
if [ ! -f .env ] && [ -f .env.example ]; then
  echo "Missing .env — copy .env.example and fill required values"
  exit 1
fi

echo "=== services (optional) ==="
# docker compose ps  or  skip if no compose file

echo "=== health ==="
# curl -sf http://localhost:3000/api/health   or   npm test -- --runInBand
```

Do not launch the long-running dev server by default. Print the start command instead.

## Environment section in AGENTS.md

Add a short, copy-pasteable block (keep root `AGENTS.md` under ~100 lines):

```markdown
## Environment

| Need | Command / file |
|------|----------------|
| Runtime | Node 22 (`engines.node` in package.json) |
| Install | `npm ci` |
| Env file | Copy `.env.example` → `.env` |
| Services | `docker compose up -d` (if compose file exists) |
| Health | `./init.sh` |
| Start (do not auto-run) | `npm run dev` |

Required env vars are listed in `.env.example`. Do not invent values for secrets.
```

## .env.example contract

- Every required variable appears once, with a comment
- Mark `required` vs `optional`
- Use placeholders (`changeme`, empty, or `your-…`), never real secrets
- If a var is only for CI or production, say so

Template: [templates/env.example](../../templates/env.example)

## Environment checklist

Walk [templates/environment-checklist.md](../../templates/environment-checklist.md) once per project (or after stack changes):

- [ ] Runtime version pinned and checked
- [ ] Install command documented and used in `init.sh`
- [ ] `.env.example` exists and matches real required vars
- [ ] Services documented (or explicitly "none")
- [ ] One health check that fails if the app cannot run
- [ ] `AGENTS.md` Environment table is copy-pasteable

## Node / Next.js (common)

```bash
node --version          # match engines or .nvmrc
test -f .env || { echo "copy .env.example → .env"; exit 1; }
npm ci                  # or pnpm install --frozen-lockfile
# docker compose up -d  # if compose exists
# npx prisma migrate deploy
curl -sf http://localhost:3000/api/health || echo "start app, then re-check"
```

## Python (common)

```bash
python --version
test -f .env || { echo "copy .env.example → .env"; exit 1; }
python -m pip install -r requirements.txt
# docker compose up -d
# alembic upgrade head
python -m pytest -q
```

## Diagnostic split

| Symptom | Layer | Skill |
|---------|-------|--------|
| Wrong Node / pip / Docker version | Environment | this skill |
| Tests never ran | Verification | `harness-verification` |
| Session start is chaotic | Lifecycle | `harness-lifecycle` |
| Failure repeats, unsure why | Diagnose | `harness-diagnose` (environment layer) |

## Anti-patterns

- Starting features while `init.sh` fails
- Committing `.env` or real API keys
- Documenting env vars only in chat
- Launching `npm run dev` inside `init.sh` by default
- Assuming Docker is running without checking
- Inventing secret values so the agent can "continue"

## Related skills

- `harness-lifecycle` — when to run init and how to hand off
- `harness-verification` — tests and evidence after the environment is healthy
- `harness-diagnose` — attribute repeated failures to a layer
- `harness-scaffold` — create missing harness files, then fill environment details here

## Templates

- [templates/environment-checklist.md](../../templates/environment-checklist.md)
- [templates/env.example](../../templates/env.example)
- [templates/init.sh](../../templates/init.sh)

## Course reference

- Lesson 06: Why initialization needs its own phase
- Lifecycle & bootstrap pattern: dependency-ordered stages, secrets after trust
