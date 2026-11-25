---
name: dip-skill
description: Configure or update a project's local development environment with dip. Use when a user asks to set up dip, dipize a project, create or update root dip.yml, add Docker Compose/Dockerfile development workflows under .dockerdev, verify local development is isolated from critical resources, or provide dip commands for provisioning, shell access, tests, linting, and local services.
metadata:
  short-description: Configure local development with dip
---

# dip-skill

Use this skill to configure or update a project's local development environment with `dip` (`https://github.com/bibendi/dip`).

## Core behavior

1. At the start of work, report the skill version (from `skills/dip-skill/VERSION` in the active skill copy) and the installed `dip` version (`dip version`, or report that `dip` is not installed/not found if the command fails).
2. Detect the current tech stack.
3. Detect executable files in `bin/` or other stack-specific locations and plan corresponding `dip` commands.
4. Check that the development environment is isolated from production, staging, and other critical resources.
5. Select and execute the matching recipe.
6. Keep changes minimal and aligned with existing project conventions.

## Stack detection rules

Inspect repository files in this order:

1. **Ruby on Rails**
   - `Gemfile` includes `gem "rails"` (or equivalent)
   - `config/application.rb` exists
2. **Node.js**
   - `package.json` exists
   - If `package.json` contains `next`, prefer the **Next.js** recipe below
3. **Django**
   - `manage.py` exists, or
   - `pyproject.toml` / `requirements*.txt` contains `django`
4. **Python (non-Django)**
   - `pyproject.toml`, `requirements.txt`, or `setup.py` exists
5. **Unknown**
   - None of the above patterns match

If multiple stacks match, prioritize framework-specific recipes (`Rails`, `Django`, `Next.js`) over generic ones.

## Execution file detection

After identifying the stack, scan the project for executable files that developers typically run directly and expose each one as a `dip` command.

### Where to look

| Stack | Locations to scan |
|---|---|
| All stacks | `bin/` at the project root |
| Node.js / Next.js | `bin/`, plus the `bin` field in `package.json` |
| Django / Python | `bin/`, `scripts/` |
| Unknown | `bin/`, `scripts/` |

### What counts as an executable file

A file is considered an executable entry point when any of these is true:

- It has the executable permission bit set (`chmod +x`).
- It contains a recognized shebang on the first line: `#!/usr/bin/env ruby`, `#!/usr/bin/env node`, `#!/usr/bin/env python3`, `#!/bin/bash`, `#!/bin/sh`, or similar.
- It has no file extension and lives in `bin/` (common for Ruby binstubs and Unix-style wrappers).

Skip files with extensions `.md`, `.txt`, `.json`, `.yml`, `.yaml`, `.lock`, `.env`, `.example`, `.sample`.

### Mapping to `dip` commands

For each detected executable:

- Use the bare filename (no extension, no directory prefix) as the `dip` command name unless it conflicts with a command already defined in the recipe.
- If the name conflicts with an existing command (e.g., `setup` vs. a provisioning command), prefix it with the directory: `bin-<name>` or `scripts-<name>`.
- Run the command inside the primary application container (`app`, `web`, or the service that owns the runtime).
- Use the relative path from the project root as the `command` value so it works regardless of `WORKDIR`.
- Add `compose.run_options: [no-deps]` unless the script requires dependent services (e.g., a database migration script).

Example `dip.yml` entries:

```yaml
interaction:
  console:
    description: Open app console via bin/console
    service: app
    command: bin/console
    compose:
      run_options: [no-deps]

  ci:
    description: Run CI checks via bin/ci
    service: app
    command: bin/ci
```

### Stack-specific naming conventions

Common filenames and their conventional `dip` command names:

- `bin/setup` → `dip setup` (project bootstrap script)
- `bin/console` → `dip console` (interactive REPL)
- `bin/dev` → `dip dev` (start dev processes)
- `bin/ci` → `dip ci` (run CI checks locally)
- `bin/update` → `dip update` (update dependencies)
- `bin/<app-name>` → `dip <app-name>` (main CLI entry point)
- `scripts/<name>` → `dip <name>` (generic helper script)

For Node.js projects with a `bin` field in `package.json`, use the key name from that field as the `dip` command name and invoke it via the detected package manager (e.g., `npm exec <bin-name>`).

Include detected execution file commands in the README update alongside other `dip` commands.

## Mandatory Rails handoff

If the project is Ruby on Rails, do **not** continue with this skill recipes.  
Respond with:

- A clear recommendation to use `tramway-skill` instead:  
  `https://github.com/Purple-Magic/tramway-skill/`
- A short reason: it is purpose-built for Rails and provides better Rails-specific workflows.

## Mandatory: no direct Docker commands

Never use `docker` or `docker compose` commands directly. All container operations must go through `dip`. Use `dip compose` for any Compose sub-command (e.g. `dip compose build`, `dip compose up`, `dip compose run`, `dip compose exec`). If a workflow cannot be expressed through `dip`, stop and ask the user rather than falling back to raw Docker commands.

## Recipe execution policy

- Before running provisioning, migrations, seed tasks, or any command that can mutate data, complete the critical-resource safety check below.
- Put newly created development configuration files under `.dockerdev/`, except `dip.yml`, which must stay at the repository root.
- Prefer updating existing `dip.yml` / compose files over replacing them.
- Reuse existing service names and ports when possible.
- Avoid destructive edits.
- After changes, provide exact `dip` commands for provisioning and daily workflow.
- Update the target project's `README.md` with the `dip` commands this skill implemented or changed.
- Update the target project's `README.md` with OS-specific Dip installation instructions.

## Mandatory configuration placement

When creating new development configuration, place `dip.yml` at the repository root and place all supporting development configuration files in `.dockerdev/`.

Generated files include:

- `dip.yml`
- `.dockerdev/compose.yml`
- `.dockerdev/Dockerfile.dev`
- `.dockerdev/.env.example` and `.dockerdev/.env` when local env templates or local-only defaults are needed
- Any helper SQL, bootstrap, development-only config files, or scripts created for the `dip` workflow

Do not create new root-level `docker-compose.yml`, `compose.yml`, `Dockerfile.dev`, `.env.example`, or helper script files for this workflow. If a project already has root-level supporting development config, merge with or reference it only when that is safer than duplicating behavior, and document the decision.

Because `dip.yml` stays at the repository root, document normal `dip` commands such as `dip provision`, `dip up`, and `dip test`. Keep paths inside root `dip.yml` valid from the repository root; reference the compose file as `.dockerdev/compose.yml`. For the compose file at `.dockerdev/compose.yml`, use `context: ..`, `dockerfile: .dockerdev/Dockerfile.dev`, and bind mounts such as `..:/app`.

If scripts are needed for waiting on services, bootstrapping databases, applying migrations, or other repeatable development tasks, create them under `.dockerdev/scripts/`. These scripts must be written in the project's main language and must start with the matching executable shebang, for example `#!/usr/bin/env ruby` for Ruby projects, `#!/usr/bin/env node` for JavaScript/TypeScript projects, or `#!/usr/bin/env python3` for Python projects. Use shell scripts only when shell is the project's main language or when there is no practical runtime available in the app image. Reference those scripts from `dip.yml` with paths that work when commands execute from the repository root.

## Mandatory source volume mounting

Every development container must bind-mount the project source directory into the container working directory. This lets developers edit files locally and see changes immediately without rebuilding the image.

- In `.dockerdev/compose.yml`, always include a bind mount of the project root (e.g. `..:/app`) in every application service's `volumes` list.
- Never rely on `COPY` or `ADD` instructions in `Dockerfile.dev` to deliver source code; `Dockerfile.dev` installs system packages and tooling only.
- Do not omit the bind mount even when a named volume is used for a subdirectory such as `node_modules` or `.next`; both can coexist.
- If an existing compose file lacks the source bind mount, add it before running any provisioning or dev-server commands.

## Mandatory critical-resource safety check

Every generated or updated development workflow must be isolated from production, staging, and other critical environments.

Before writing final `dip` commands or running any mutable command:

1. Inspect existing local-development inputs, including `dip.yml`, compose files, Dockerfiles, `.env.example`, committed env templates, framework config, package scripts, and documented setup commands.
2. Look for references to critical resources, including production or staging database URLs, hosted Postgres/Supabase/Redis/Elasticsearch endpoints, cloud storage buckets, queues, payment providers, email/SMS providers, analytics projects, or any env var names/values that clearly target shared infrastructure.
3. Ensure generated defaults point to local containers or explicitly local emulators only, such as `db`, `localhost`, `127.0.0.1`, Docker service names, or placeholder local-only credentials.
4. Do not copy real secrets or critical URLs from `.env`, shell history, deployment files, CI variables, or ignored files into generated config or docs.
5. If a critical resource is detected or cannot be ruled out, stop before running mutable commands. Report the exact file/key or command that appears risky, replace generated defaults with local placeholders where safe, and ask the user to confirm the intended local resource before continuing.

For database and migration commands, the safety check is mandatory. Never run migrations, resets, seeds, destructive SQL, queue workers, sync jobs, or one-off scripts when the configured target appears to be production, staging, shared, or unknown.

The final response must state whether critical-resource isolation was verified, changed, or blocked by an unresolved risk.

## Mandatory provisioning verification

When a user asks to "dipize" a project or set up dockerization with `dip`, do not stop at generating files.

- After generating or updating the `dip` configuration, run `dip provision`.
- If it fails, diagnose the failure, fix the underlying `dip.yml` / `.dockerdev/` configuration, and re-run `dip provision`. Repeat until it succeeds. Do not report completion while `dip provision` is failing.
- If an `up` command (`dip up`) is appropriate for this project (i.e. the project has a long-running dev server/service rather than a one-shot task), run it after a successful `dip provision` and fix it the same way: diagnose, fix configuration, retry, until it works.
- Only fall back to asking the user when the fix requires information that cannot be determined from the repository (e.g., missing real credentials for a required external service) or requires a destructive/critical-resource decision covered by the safety check above.
- Keep applying the critical-resource safety check throughout this iteration; never loosen it to get a command to pass.

## Mandatory README command documentation

Whenever this skill creates or changes `dip.yml`, Docker Compose files, Dockerfiles, or command workflows, update the target project's `README.md` in the same task.

The README update must document the commands that actually exist after the change, including:

- Provisioning/setup command, usually `dip provision`.
- Start/stop commands, `dip up` and `dip down` (plain built-ins, never overridden), noting that `dip up` shows live logs from the main app container by default because it runs in the foreground; if a `logs` command was added for re-attaching to a backgrounded stack, document it and note it only tails recent output.
- Dependency-install command, `dip install`, for Node.js-based recipes, and that it replaces `dip provision` for `package.json` updates.
- Shell or package-manager pass-through commands, such as `dip shell`, `dip npm`, `dip pnpm`, or `dip yarn`, when implemented.
- Test, lint, database, framework CLI, or service commands, such as `dip test`, `dip lint`, `dip psql`, `dip manage`, or `dip next`, when implemented.

Keep README edits concise and aligned with the existing documentation style. If the target project has no README, create a minimal `README.md` section for local development commands.

## Mandatory Dip installation documentation

Whenever this skill creates or changes a project's `dip` workflow, update the target project's `README.md` with concise Dip installation instructions for common operating systems.

Document these options:

- macOS: Homebrew is preferred.
  ```bash
  brew tap bibendi/dip
  brew install dip
  ```
- Linux: use Homebrew on Linux when available, or install via RubyGems.
  ```bash
  brew tap bibendi/dip
  brew install dip
  ```
  ```bash
  gem install dip
  ```
- Windows: use WSL2 with a Linux distribution, then follow the Linux instructions inside WSL.
- Any OS with Ruby: `gem install dip`.

Also mention the precompiled binary option from Dip releases when Homebrew or RubyGems is not suitable, but avoid hardcoding a stale version unless the project explicitly pins one.

## Recipe: Next.js + Supabase/PostgREST

Apply when:

- `package.json` exists and dependencies include `next`.
- Supabase is detected by any of:
  - dependency `@supabase/supabase-js`
  - a `supabase/` directory
  - environment variables such as `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`, or `DATABASE_URL`

Goal:

- A fresh checkout should be runnable with one command: `dip provision`.
- `dip provision` should build images, install dependencies, prepare local env files when missing, start local database services, apply available SQL migrations, and leave the app running.

Target files (create if missing, merge carefully if present):

- `.dockerdev/Dockerfile.dev`
- `.dockerdev/compose.yml`
- `dip.yml`
- `.dockerdev/.env.example` (only add missing local-development variables)

Recommended defaults:

- App service name: `app`
- Database service name: `db`
- PostgREST service name: `rest`
- Node image: `node:22-bookworm-slim`
- Working dir: `/app`
- App port: `${NEXT_PORT:-3000}:3000`
- Postgres port: `${POSTGRES_PORT:-54322}:5432`
- PostgREST port: `${POSTGREST_PORT:-54321}:3000`
- Bind mount the project directory.
- Use Docker volumes for `node_modules`, `.next`, and database data.
- Run Next.js as `npm run dev -- --hostname 0.0.0.0` when `dev` script is present.

Package manager detection:

- `pnpm-lock.yaml` -> use `corepack enable && pnpm install --frozen-lockfile`; command prefix `pnpm`
- `yarn.lock` -> use `corepack enable && yarn install --frozen-lockfile`; command prefix `yarn`
- `package-lock.json` or `npm-shrinkwrap.json` -> use `npm ci`; command prefix `npm`
- otherwise -> use `npm install`; command prefix `npm`

Dockerfile.dev template:

```dockerfile
FROM node:22-bookworm-slim

WORKDIR /app

ENV NEXT_TELEMETRY_DISABLED=1

RUN apt-get update -qq \
  && apt-get install -y --no-install-recommends ca-certificates openssl postgresql-client \
  && rm -rf /var/lib/apt/lists/*

CMD ["sleep", "infinity"]
```

compose.yml template:

```yaml
services:
  app:
    build:
      context: ..
      dockerfile: .dockerdev/Dockerfile.dev
    command: npm run dev -- --hostname 0.0.0.0
    working_dir: /app
    ports:
      - "${NEXT_PORT:-3000}:3000"
    volumes:
      - ..:/app
      - node_modules:/app/node_modules
      - next_cache:/app/.next
    env_file:
      - .env
    environment:
      NEXT_TELEMETRY_DISABLED: "1"
      DATABASE_URL: ${DATABASE_URL:-postgresql://postgres:postgres@db:5432/postgres}
      NEXT_PUBLIC_SUPABASE_URL: ${NEXT_PUBLIC_SUPABASE_URL:-http://localhost:54321}
      NEXT_PUBLIC_SUPABASE_ANON_KEY: ${NEXT_PUBLIC_SUPABASE_ANON_KEY:-local-anon-key}
      SUPABASE_SERVICE_ROLE_KEY: ${SUPABASE_SERVICE_ROLE_KEY:-local-service-role-key}
    depends_on:
      db:
        condition: service_healthy
      rest:
        condition: service_started

  db:
    image: postgres:16-alpine
    ports:
      - "${POSTGRES_PORT:-54322}:5432"
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres -d postgres"]
      interval: 5s
      timeout: 5s
      retries: 20

  rest:
    image: postgrest/postgrest:v12.2.8
    ports:
      - "${POSTGREST_PORT:-54321}:3000"
    environment:
      PGRST_DB_URI: postgres://postgres:postgres@db:5432/postgres
      PGRST_DB_SCHEMAS: public
      PGRST_DB_ANON_ROLE: anon
      PGRST_JWT_SECRET: ${SUPABASE_JWT_SECRET:-local-development-jwt-secret-change-me}
    depends_on:
      db:
        condition: service_healthy

volumes:
  node_modules:
  next_cache:
  postgres_data:
```

If the app uses Supabase Auth, Storage, Realtime, Edge Functions, or relies on Supabase's `/rest/v1` gateway path, do not pretend plain PostgREST is a complete Supabase replacement. In that case, keep the Next.js `app` service but configure `dip provision` to call the official Supabase CLI workflow (`supabase start`, `supabase db reset`, etc.) and document that Docker plus Supabase CLI are required on the host.

For standalone PostgREST mode, add an idempotent database bootstrap before migrations:

```sql
create role anon nologin;
grant usage on schema public to anon;
grant select, insert, update, delete on all tables in schema public to anon;
alter default privileges in schema public grant select, insert, update, delete on tables to anon;
```

`dip.yml` command set should include:

- `provision` (built-in, via the `provision:` section): create `.dockerdev/.env` from `.dockerdev/.env.example` when missing, build images, install dependencies, start `db` and `rest`, wait for Postgres, apply SQL files from `supabase/migrations/*.sql` or `db/migrations/*.sql` when present, and start `app`.
- `up` (plain built-in, no `interaction` override): start the stack in the foreground and show live logs from `app` by default (see "Mandatory `dip up` log output").
- `install`: install/update dependencies in `app` after `package.json` changes, without re-provisioning (see "Mandatory `dip install` command for dependency updates").
- `down` (plain built-in, no `interaction` override): stop the app stack.
- `shell`: open shell in `app`.
- package-manager pass-through command (`npm`, `pnpm`, or `yarn`).
- `next`: run Next.js CLI through the detected package manager.
- `lint`: run configured lint script.
- `test`: run `test` script when present, otherwise omit or map to the closest configured test/regression script.
- `psql`: open `psql` against local Postgres.

Recommended `dip.yml` shape:

```yaml
# yaml-language-server: $schema=https://raw.githubusercontent.com/bibendi/dip/refs/heads/master/schema.json
version: '8.0'

compose:
  files:
    - .dockerdev/compose.yml
  project_name: my-next-app

interaction:
  shell:
    description: Open a shell in the app container
    service: app
    command: bash
    compose:
      run_options: [no-deps]

  install:
    description: Install/update dependencies after package.json changes
    service: app
    command: npm install
    compose:
      run_options: [no-deps]

  npm:
    description: Run npm in the app container
    service: app
    command: npm
    compose:
      run_options: [no-deps]

  next:
    description: Run Next.js CLI
    service: app
    command: npm exec next

  lint:
    description: Run lint
    service: app
    command: npm run lint

  psql:
    description: Open local Postgres
    service: db
    command: psql -U postgres -d postgres

provision:
  - test -f .dockerdev/.env || cp .dockerdev/.env.example .dockerdev/.env
  - dip compose build
  - dip compose run --rm app npm ci
  - dip compose up -d db rest
  - dip compose exec db sh -lc 'until pg_isready -U postgres -d postgres; do sleep 1; done'
  - dip compose exec db psql -U postgres -d postgres -c 'do $$ begin create role anon nologin; exception when duplicate_object then null; end $$;'
  - dip compose exec db psql -U postgres -d postgres -c 'grant usage on schema public to anon; grant select, insert, update, delete on all tables in schema public to anon; alter default privileges in schema public grant select, insert, update, delete on tables to anon;'
  - if ls supabase/migrations/*.sql >/dev/null 2>&1; then for f in supabase/migrations/*.sql; do dip compose exec -T db psql -U postgres -d postgres < "$f"; done; fi
  - if ls db/migrations/*.sql >/dev/null 2>&1; then for f in db/migrations/*.sql; do dip compose exec -T db psql -U postgres -d postgres < "$f"; done; fi
  - dip compose up -d app
```

Adjust the example before writing it:

- Replace `project_name` with a sanitized value from `package.json` `name`.
- Replace package-manager commands according to lockfile detection, including the `install` command (`npm install`, `pnpm install`, or `yarn install`).
- If no `lint` script exists, omit `lint`.
- If no useful `test` script exists, omit `test` and mention which scripts were available.
- If `next.config.*` includes custom image or env settings, leave them unchanged.
- If a project already has `.env.example`, copy only missing local-development keys into `.dockerdev/.env.example` and never overwrite secrets.
- Keep placeholder Supabase keys clearly local-only unless real keys already exist in ignored `.env` files.

## Recipe: Node.js

Apply when `package.json` is present and Rails/Django/Next.js are not detected.

Target files (create under `.dockerdev/` if missing):

- `.dockerdev/compose.yml` (or merge into existing compose file)
- `.dockerdev/Dockerfile.dev`
- `dip.yml`

Recommended defaults:

- Service name: `app`
- Working dir: `/app`
- Bind mount project directory
- `node_modules` Docker volume
- Container command for dev server if script exists, otherwise idle command

`dip.yml` command set should include:

- `provision` (built-in, via the `provision:` section): install dependencies (`npm ci` or package-manager equivalent)
- `up` (plain built-in, no `interaction` override): start the stack in the foreground and show live logs from `app` by default (see "Mandatory `dip up` log output")
- `install`: install/update dependencies in `app` after `package.json` changes (see "Mandatory `dip install` command for dependency updates")
- `shell`: open shell in app service
- `npm`: pass-through package manager command
- `test`: run project tests
- `lint`: run project linter if configured

## Recipe: Django

Apply when Django is detected and Rails is not detected.

Target files (create under `.dockerdev/` if missing):

- `.dockerdev/compose.yml` with:
  - `web` service for Django app
  - `db` service (PostgreSQL) when project requires database
- `.dockerdev/Dockerfile.dev`
- `dip.yml`

Recommended defaults:

- `web` command: `python manage.py runserver 0.0.0.0:8000`
- Code mounted into container
- Persistent volume for database data

`dip.yml` command set should include:

- `provision`: install Python dependencies and run migrations
- `shell`: shell in `web`
- `manage`: pass-through to `python manage.py`
- `test`: run Django tests (`python manage.py test`)

## Recipe: Generic Python (non-Django)

Configure `dip` for dependency install, shell, and tests using project's package manager and test tooling.

## Unknown stack behavior

If no known stack is detected:

- Explain what was checked.
- Ask the user which stack to target.
- Offer to scaffold a minimal generic `dip` setup once stack is confirmed.

## Output format to user

Always include:

1. Detected stack and evidence.
2. Execution files found in `bin/`, `scripts/`, or other stack-specific locations, and the `dip` command mapped to each.
3. Files created/updated.
4. Configuration location, especially root `dip.yml` and supporting files under `.dockerdev/`.
5. Exact commands to run next (for example: `dip provision`, `dip up`, `dip test`, plus any execution-file commands such as `dip console` or `dip ci`).
6. Critical-resource isolation check result.
7. README Dip installation and command documentation added or updated.
8. Any assumptions requiring user confirmation.

## Mandatory usage explanation after `dip compose`/`dip up`

After `dip provision` (which runs `dip compose` sub-commands) and/or `dip up` finishes successfully, always explain to the user, in plain terms, how to use the resulting workflow day-to-day:

- `dip up` (plain, built-in — never overridden with a custom `interaction` entry): starts the app stack in the foreground for daily development and shows live logs from the main app container from the moment it starts; explain when to use it (e.g., after the first `dip provision`, or whenever they want the services running again) and that it does not re-provision or reinstall dependencies. If a `logs` command was added for re-attaching to an already-backgrounded stack, explain that it only tails recent output and does not replay full history.
- `dip install` (Node.js-based recipes): explain that after editing `package.json`, they should run `dip install` to install/update dependencies, instead of re-running `dip provision`.
- Re-running `dip provision`: explain when they need to run it again — e.g., after pulling changes that alter environment variables, migrations, or the `dip.yml`/`.dockerdev/` configuration itself — versus using `dip install` for dependency changes or `dip up` for a normal day-to-day start.
- `dip down`: explain that it stops and removes the running containers for this stack, and when to use it (e.g., shutting down for the day, freeing ports, or before switching branches with a different stack).

Keep this explanation concise and tailored to the commands actually defined in the project's `dip.yml`.

## Mandatory `dip up` log output

`up`, `build`, `down`, and `provision` are reserved built-in `dip` commands (confirmed via `dip help` on dip 8.4.0: `build`, `compose`, `console`, `down`, `help`, `infra`, `ktl`, `ls`, `provision`, `run`, `ssh`, `stop`, `tree`, `up`, `validate`, `version`). An `interaction` entry in `dip.yml` named `up` (or any other reserved name) is silently ignored — `dip` runs its built-in instead, which is a plain foreground `docker compose up [SERVICE]`. Never add an `interaction` entry named `up`, `build`, `down`, or `provision`.

Before writing any `interaction` command name into `dip.yml`, run `dip help` (or `dip ls`/`dip tree` in the target environment) and confirm the name is not already a built-in. If it is, do not try to override it — pick a different, unused name instead.

Default workflow (no custom wrapper needed):

- `dip up` (plain, built-in): starts the stack in the foreground and streams logs from the main app container from the moment it starts. This is sufficient by default — do not add a custom `up:` entry to replace it.
- `dip down` (plain, built-in): stops the stack.
- If a developer wants to run the stack detached (`-d`) instead, or wants to re-attach to logs from a container that was already started in the background, add a separate, non-reserved command such as `logs`:

  ```yaml
  logs:
    description: Tail logs from the app container
    command: dip compose logs -f --tail=100 app
  ```

  Document the difference clearly: `dip up` is a foreground start that streams logs from a cold start; `dip up -d` backgrounds the stack without printing logs; `dip logs` tails the current output of an already-running container, but does not replay history the way a cold `dip up` does — if the container has been running quietly in the background, `dip logs --tail=100` only shows the last 100 lines, not a guaranteed full replay.
- Keep the service name in sync with whichever service is the main app service in each recipe (`app` for Next.js/Node.js, `web` for Django).
- Document this behavior in the README alongside other `dip` commands.

## Mandatory `dip install` command for dependency updates

Whenever this skill sets up or updates a Node.js-based recipe (Next.js or generic Node.js), it must provide a `dip install` command so developers never need to re-run `dip provision` just because `package.json` changed.

- Add an `install` entry to `dip.yml` that runs the detected package manager's install command inside the app container without rebuilding the whole environment, e.g.:

  ```yaml
  install:
    description: Install/update dependencies after package.json changes
    service: app
    command: npm install
    compose:
      run_options: [no-deps]
  ```

- Use the package-manager-specific install command from the lockfile detection rules (`npm install`, `pnpm install`, `yarn install`), not the frozen/CI variant, since this command is meant to update the lockfile when `package.json` changes.
- Document in the README and in the day-to-day usage explanation that after editing `package.json`, developers should run `dip install`, not `dip provision`. Reserve `dip provision` for first-time setup or changes to the `dip`/Docker configuration itself.

## Mandatory port check after `dip up`

After `dip up` runs successfully, verify that each port reported in its output (or declared in the relevant `ports:` entries of `.dockerdev/compose.yml`) is actually serving something, before telling the user the stack is ready.

- For each such port on `localhost`/`127.0.0.1`, check it with a lightweight local request (e.g., `curl -sS -o /dev/null -w '%{http_code}' http://localhost:<port>` or an equivalent simple TCP/HTTP check). Any HTTP response (including non-2xx, such as 404) counts as the port being up; a connection error/refused/timeout does not.
- If a port does not respond, treat this the same as a failed `dip up`: diagnose (check container logs via `dip compose logs <service>`, confirm the service's `ports:` mapping and bind mount, confirm the dev server binds to `0.0.0.0` not `127.0.0.1` inside the container), fix the configuration, and retry until it responds — following the same mandatory provisioning verification policy as `dip provision`.
- Report the result of this check to the user (which ports were verified reachable, and the URL to open) alongside the usage explanation above.
- Only skip this check for a port/service that is not meant to be reached from the host (e.g., an internal-only service with no host port mapping).
