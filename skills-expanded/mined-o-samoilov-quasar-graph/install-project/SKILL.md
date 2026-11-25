---
name: install-project
description: "Internal skill used by quasar-graph:clone sub-agents. Installs dependencies for ONE cloned project, choosing the command (incl. container path) from its config/docs. Do NOT invoke directly — only via the clone orchestrator."
user-invocable: false
---

# /quasar-graph:install-project

You install dependencies for ONE freshly cloned project for the quasar-graph `clone` skill. The orchestrator dispatches you as a sub-agent with these inputs in the prompt:

- `project_name(s)` — the project name, or for a monorepo the list of contained project names.
- `target_path` — absolute path to the cloned directory (for a monorepo, the common-prefix directory).
- `agent_context` — the graph node's curated install/context blob, or `null`. For a monorepo this is a list of `{ name, agentContext }`.

You do NOT prompt the user (you run inside a parallel batch). You run only **known** install commands and **return** everything else for the orchestrator to confirm.

## What to read (config + docs only — NEVER source code)

Read only these, at or under `target_path` (depth 1–3, skipping `node_modules`, `.venv`, `vendor`, `dist`, `build`, `target`, `.git`):

- Container/build: `docker-compose*.yml`, `Dockerfile*`
- Task runners / docs: `Makefile`, `CLAUDE.md`, `AGENTS.md`, root `README*`
- Manifests + lockfiles: `package.json`, `pnpm-lock.yaml`, `yarn.lock`, `package-lock.json`, `bun.lockb`, `composer.json`, `pyproject.toml`, `Pipfile`, `Pipfile.lock`, `requirements.txt`, `go.mod`, `Cargo.toml`, `pubspec.yaml`, `Gemfile`
- Env: `.env`, `.env.example`, `.env.*` (names/structure only — never echo secret values)

Scripts referenced by a Makefile (`scripts/*.sh`) may be **read so you can quote them to the user**, but MUST NOT be executed by you. Do not read application source code.

## How to decide the install command

Pick the install approach by this priority:

1. **`agent_context`** — trusted, curated. If it states how to install (e.g. "deps run in the `app` container: `docker compose run --rm app composer install`"), follow it.
2. **Project docs/config** — a `Makefile` target, a `docker-compose.yml` service, or a root `README` setup section. (read these to learn the intended installer; a bare `make <target>` is still non-standard and goes to `proposed`).
3. **Lockfile baseline** — if nothing above is decisive, fall back to the manifest/lockfile at the root:
   | Signal at root | Command |
   | --- | --- |
   | `pnpm-lock.yaml` | `pnpm install` |
   | `yarn.lock` | `yarn install` |
   | `bun.lockb` | `bun install` |
   | `package-lock.json` | `npm ci` |
   | `package.json` (no lockfile) | `npm install` |
   | `poetry.lock` / `pyproject.toml [tool.poetry]` | `poetry install` |
   | `Pipfile.lock` / `Pipfile` | `pipenv install` |
   | `requirements.txt` | `pip install -r requirements.txt` |
   | `go.mod` | `go mod download` |
   | `Cargo.toml` | `cargo fetch` |
   | `composer.json` | `composer install` |
   | `pubspec.yaml` (with `flutter:` → flutter) | `dart pub get` / `flutter pub get` |
   | `Gemfile` | `bundle install` |

**Containers:** if the project has no local runtime expectation (e.g. a PHP/Node service whose `docker-compose.yml` defines the app service and there is no indication deps install on the host), wrap the installer in the compose service: `docker compose run --rm <service> <installer>`. Choose `<service>` from the compose file (the one whose build context is this project / mounts the code).

If nothing recognizable is found, do not guess — mark `no-install`.

## Known vs non-standard

- **Known (you RUN these):** a direct package-manager installer from the table above, OR `docker compose run --rm <service> <one of those installers>` (a container wrapper whose inner command is itself a known installer).
- **Non-standard (you DO NOT run — add to `proposed`):** `make <target>`, `./scripts/*.sh`, `curl ... | sh`, DB migrations, build/compile steps, or anything that is not purely dependency install. Include a short `rationale` and the `source` (which file/line or `agent_context`).

## Running

Run each Known command from inside `target_path` (e.g. `cd <target_path> && <command>`). Capture success/failure. On failure (missing binary, lockfile drift, network) record the error and continue — never abort. A missing `docker`/`pnpm`/etc. binary is a recorded failure, not fatal. Set `method` to `container` if you ran a `docker compose run` command, `local` for a host installer, `none` if you ran nothing. If you ran both container and local commands, prefer `container`.

## Return shape

Your final message is the return value — return ONLY this JSON object, no prose around it:

```json
{
  "targetPath": "<target_path>",
  "projects": ["<name>", "..."],
  "method": "local | container | none",
  "ran": [{ "cmd": "<command>", "ok": true, "error": null }],
  "proposed": [{ "cmd": "<command>", "rationale": "<why>", "source": "<file or agent_context>" }],
  "status": "installed | no-install | failed",
  "notes": "<one line: anything the orchestrator/user should know>"
}
```

- `status: installed` — at least one Known command ran OK.
- `status: failed` — every Known command you ran failed.
- `status: no-install` — you found nothing recognizable to run (and `ran` is empty).
`proposed` may be non-empty even when `status` is `installed` or `no-install`.
