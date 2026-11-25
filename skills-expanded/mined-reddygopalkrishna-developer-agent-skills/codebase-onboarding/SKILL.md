---
name: codebase-onboarding
description: Maps an unfamiliar repository before changing it - stack, build/test/run commands, entry points, data flow, conventions and how changes ship - and writes a short map. Use when starting work in a repo you have not seen, when asked to explain how a codebase works, onboard to a project, find where something lives, or before a first change in a large or legacy codebase. Not for reviewing a specific diff.
license: MIT
---

# Codebase Onboarding

Never change code you have not located in its context. Spend the first minutes building a map: what the system is, how it is built and tested, where requests enter, and what conventions the existing code follows. Then prove the map by building and running the tests before you edit anything.

## When to use

- First task in a repository you have not worked in.
- The user asks "how does this work?", "where is X handled?", or "explain this codebase".
- A change touches an area you have not read yet in a large or legacy repo.

Not for: reviewing a pull request (see the code-review-changes skill) or debugging a known failure (see the root-cause-debugging skill), though both start faster with a map.

## Workflow

1. **Read the human-written guidance first.** In this order, if present: `README*`, `CONTRIBUTING*`, project instruction files for agents (`AGENTS.md`, `CLAUDE.md`, `.cursor/rules`, `.github/copilot-instructions.md`), `docs/`, architecture decision records (`docs/adr`, `adr/`). Note stated rules ("never edit generated files", "run make check before commit").
2. **Identify the stack from manifests, not guesses.** Use the table below. Lockfiles tell you the package manager; version files (`.nvmrc`, `.python-version`, `.tool-versions`, `go.mod` `go` directive, `global.json`, `rust-toolchain.toml`) tell you the runtime version.
3. **Find the real commands.** Treat CI configuration as the source of truth: it is what actually runs. Check, in order: CI files (`.github/workflows/`, `.gitlab-ci.yml`, `azure-pipelines.yml`, `Jenkinsfile`), task runners (`Makefile`, `justfile`, `Taskfile.yml`), package scripts (`package.json` `scripts`, `pyproject.toml` tool sections, `build.gradle`), then README. Record build, test, lint, format, type-check and run commands.
4. **Locate entry points.** Where execution starts: `main` functions, `cmd/` (Go), `src/main/java/**/Application.java`, `Program.cs`, `manage.py`/`wsgi.py`/`asgi.py`, `app/` or `pages/` (Next.js), `bin/`, `index.ts`/`server.ts`, `Dockerfile` `CMD`/`ENTRYPOINT`, serverless handler configs.
5. **Trace one request or job end to end.** Pick one representative feature (the one the user cares about, if known). Follow it: route/handler or consumer, validation, business logic, data access, external calls, response. Note file paths at each hop. One real trace teaches more than reading folders.
6. **Learn the conventions from existing code.** Find two or three files similar to what you will write. Note naming, error handling, logging, dependency injection, test style, and folder placement. New code must look like its neighbours.
7. **Map tests.** Where unit, integration and end-to-end tests live; how fixtures and test data work; which tests need services (database, queue) and how CI provides them (service containers, docker compose, testcontainers).
8. **Map config and environments.** Config files, env var loading (`.env.example`, settings modules), feature flags, secrets source. Never print or copy real secret values into notes.
9. **Learn how changes ship.** Branching model, PR template, required checks, release/deploy process (CI deploy jobs, release scripts, changelog tooling), generated code and how to regenerate it.
10. **Write the map** using [references/map-template.md](references/map-template.md). Keep it to one page. Put it where the user wants it (reply, or a notes file if asked); don't commit it unless asked.
11. **Verify the map.** Install dependencies, build, and run the test suite (or the fastest meaningful subset) with the commands you found. If they fail before you changed anything, record that as the baseline and tell the user; don't "fix" unrelated failures silently.

## Stack identification

| File | Tells you |
| --- | --- |
| `package.json` + `pnpm-lock.yaml` / `yarn.lock` / `package-lock.json` / `bun.lock*` | Node/TS; package manager is the one whose lockfile exists |
| `pnpm-workspace.yaml`, `nx.json`, `turbo.json`, `lerna.json` | JS monorepo (see the monorepo-management skill) |
| `pyproject.toml`, `uv.lock`, `poetry.lock`, `requirements*.txt`, `setup.cfg` | Python; `uv.lock`/`poetry.lock` name the tool |
| `go.mod`, `go.work` | Go module / workspace |
| `pom.xml`, `build.gradle(.kts)`, `settings.gradle(.kts)` | Java/Kotlin with Maven or Gradle |
| `*.sln`, `*.csproj`, `Directory.Build.props` | .NET |
| `Cargo.toml`, `Cargo.lock` | Rust (a `[workspace]` table means multiple crates) |
| `Gemfile`, `composer.json`, `mix.exs` | Ruby, PHP, Elixir |
| `Dockerfile`, `docker-compose.yml`, `compose.yaml` | How it runs locally / in production |
| `*.tf`, `Chart.yaml`, `kustomization.yaml`, `*.bicep` | Infrastructure as code and deployment |
| `openapi.*`, `*.proto`, `schema.graphql` | API contracts, often used for code generation |

## Fast ways to find things

- Search for the user-visible string (error message, UI label, route path) to find where a feature lives.
- Search for route registrations: `@GetMapping`, `app.get(`, `router.`, `[HttpGet]`, `@app.route`, `urlpatterns`, `http.HandleFunc`.
- List the largest and most-changed files: `git log --format= --name-only | sort | uniq -c | sort -rn | head -20` shows hot spots; they are usually the core.
- `git log --oneline -20` and recent merged PRs show what the team is working on and how they write commits.
- `git shortlog -sn --since="1 year ago" -- <path>` shows who to ask about an area.

## When the baseline build fails

Work through these before concluding the repo is broken:

1. **Runtime version mismatch** (the most common cause). Compare your runtime with the version files from step 2 and switch to the pinned version with the repo's version manager (nvm, pyenv, asdf/mise, SDKMAN, `rustup`).
2. **Wrong package manager.** Use the one whose lockfile exists, with its frozen/locked install mode (`npm ci`, `pnpm install --frozen-lockfile`, `yarn install --immutable` on Yarn Berry, `uv sync --locked`, `poetry install`). Don't regenerate or delete the lockfile to make an install pass.
3. **Missing services.** Look for `compose.yaml`/`docker-compose.yml`, `.devcontainer/devcontainer.json`, or testcontainers usage; CI service definitions show exactly what tests need.
4. **Missing configuration.** Copy `.env.example` (or similar) with placeholder values. Ask the user for real values; never invent credentials or reuse secrets found elsewhere.
5. **Private registries or access.** If installs fail on authentication, stop and ask the user. Don't try to work around access controls.
6. Record every fix you needed in the map's "Commands" section so the next person (or agent) doesn't repeat the investigation.

## Placing a change

- Find the existing feature most similar to what you are building and mirror its structure, file placement and tests.
- Search for existing helpers before writing new ones: search by verb (`parse`, `format`, `validate`, `retry`) and by domain noun.
- Find the tests that cover the area and run them before and after the change.
- Check `CODEOWNERS` (or equivalent) to know whose conventions and review apply.

## Questions to ask the user

Ask only what the repo cannot answer, and batch them:

- Which part of the system matters for this task?
- Are there environments or services I must not touch (production databases, shared staging)?
- Are the failing tests (if any) known failures?
- Any conventions not written down (preferred libraries, banned patterns)?

## Anti-patterns

- **Editing before mapping** - writing code in the first minutes and then discovering an existing helper, a generator, or a convention you violated.
- **Trusting the README over CI** - READMEs go stale; CI is what runs. When they disagree, follow CI and mention the drift.
- **Reading every file** - breadth-first folder reading burns time. Trace one real path instead.
- **Inventing commands** - running `npm test` when the repo uses `pnpm turbo test`, or `pytest` when tests run through `tox` or `nox`.
- **Editing generated code** - files with "DO NOT EDIT" headers, `generated/` folders, or outputs of OpenAPI/protobuf generators. Change the source and regenerate.
- **Fixing unrelated failures silently** - a red baseline is information for the user, not a license to change unrelated code.

## Done when

- You can state the stack, runtime versions and package manager with the file that proves each.
- Build and test commands are recorded and you have run them (or explained why you could not).
- One representative request/job is traced end to end with file paths.
- Conventions for the area you will change are written down.
- The one-page map exists and the user has it.

## References

- [references/map-template.md](references/map-template.md) - read when writing the codebase map in step 10.
