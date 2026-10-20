<!-- agent-notes: { ctx: "devcontainer setup for any stack", deps: [CLAUDE.md], state: active, last: "ines@2026-02-12" } -->
Set up a devcontainer for this project: $ARGUMENTS

You are configuring a development container so this project can be developed in a consistent, reproducible environment. This command is typically run AFTER the tech stack has been chosen (via scaffolding or manual setup).

## 1. Detect the Current Stack

Read the repo to understand what's already here. Check for:

- **Node/TypeScript**: `package.json`, `tsconfig.json`, `pnpm-workspace.yaml`, `bun.lockb`, `yarn.lock`
- **Python**: `pyproject.toml`, `requirements.txt`, `uv.lock`, `poetry.lock`, `Pipfile`
- **Rust**: `Cargo.toml`, `rust-toolchain.toml`
- **Go**: `go.mod`, `go.sum`
- **Java/Kotlin**: `pom.xml`, `build.gradle`, `build.gradle.kts`
- **.NET**: `*.csproj`, `*.sln`, `global.json`
- **Docker**: `Dockerfile`, `docker-compose.yml`
- **CI**: `.github/workflows/`, `.gitlab-ci.yml`
- **Existing devcontainer**: `.devcontainer/`

Also check `CLAUDE.md` and `docs/adrs/` for documented tech stack decisions.

Summarize what you found. If nothing is detected, tell the user and ask what they're building before proceeding.

## 2. Gather Additional Requirements

Based on what was detected, ask the user targeted questions. Only ask what's relevant — don't present a wall of options.

**Base image strategy:**
- **Language-specific image** (e.g., `mcr.microsoft.com/devcontainers/python:3.12`) — Simpler, pre-configured for one language (Recommended for single-language projects)
- **Universal image** (`mcr.microsoft.com/devcontainers/universal:2`) — Multiple languages pre-installed, heavier
- **Minimal base + features** (`mcr.microsoft.com/devcontainers/base:ubuntu`) — Lightweight, compose what you need via features
- **Custom Dockerfile** — Full control, for complex setups

**Services (only ask if the project likely needs them):**
- Database? (PostgreSQL, MySQL, MongoDB, SQLite-no-container, Redis, none)
- Message broker? (RabbitMQ, Kafka, none)
- Search? (Elasticsearch, Meilisearch, none)

If services are selected, use Docker Compose to define them alongside the dev container.

**Developer tooling:**
- Claude Code CLI (pre-install in container?)
- GitHub CLI (`gh`)
- Cloud CLIs (AWS, Azure, GCP — only ask if infra config detected)

**VS Code extensions** — Propose a sensible set based on the detected stack.

**Port forwarding** — Propose ports based on detected frameworks (3000 for Next.js, 8000 for FastAPI, 5173 for Vite, etc.).

## 3. Build the Devcontainer Configuration

Create `.devcontainer/devcontainer.json` (and `docker-compose.yml` if services are needed).

### Key Principles

- **Prefer features over custom Dockerfiles.** Features are composable, cacheable, and maintained upstream.
- **Pin versions.** Don't use `latest` — pin language versions, feature versions, and base image tags.
- **Include postCreateCommand.** Install dependencies and do first-time setup so the container is ready immediately.
- **Keep it fast.** A dev container that takes 10 minutes to build won't get used. Prefer pre-built images and cached layers.
- **Don't duplicate CI.** The dev container is for development, not for running the full CI pipeline.

## 4. Update Project Docs

- Add `.devcontainer/` to the project structure in `CLAUDE.md`.
- Add a "Development Environment" section to `README.md`.
- If significant choices were made, create an ADR.

## 5. Verify

- Validate that `devcontainer.json` is valid JSON.
- If a `docker-compose.yml` was created, validate its syntax with `docker compose config` if Docker is available.
- Check that all referenced files exist.
- Confirm that `postCreateCommand` references correct package manager commands.

## 6. Summary

Tell the user:
- What was created and why.
- How to open the dev container (VS Code: "Reopen in Container", Codespaces: push and open, CLI: `devcontainer up`).
- What services are included and how to access them.
- Any manual steps needed.
