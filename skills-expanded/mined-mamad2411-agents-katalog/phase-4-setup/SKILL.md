---
name: phase-4-setup
description: Phase 4 of the development cycle. Scaffolds the codebase for the chosen stack — project structure, formatter, linter, type checks, test runner, environment config, CI pipeline — fills in CLAUDE.md with the real commands, and proves everything works with a first passing test.
disable-model-invocation: true
---

# Phase 4 — Plan → Project setup

Inputs: the accepted ADRs in `docs/adr/` (stack, database, hosting) and `docs/architecture/ARCHITECTURE.md`. If no stack has been decided, stop and tell the user to run `/phase-2-architecture`.

Goal: a codebase where `install`, `test`, `lint`, and `run` all work on day one, and where CI runs them on every push.

## Steps

```
Phase 4 progress:
- [ ] 1. Scaffold the structure
- [ ] 2. Quality tooling
- [ ] 3. Configuration and secrets
- [ ] 4. Local development environment
- [ ] 5. CI pipeline
- [ ] 6. Fill in CLAUDE.md
- [ ] 7. Prove it works
```

**1. Scaffold.**
- Use the framework's official generator when one exists (for example `npm create vite@latest`, `dotnet new`, `django-admin startproject`, Spring Initializr, `cargo new`).
- Organize the code to match the containers and modules in ARCHITECTURE.md. Group by feature or domain, not by technical layer.
- Put tests where the ecosystem expects them.

**2. Quality tooling.** Use the ecosystem's standard tool for each job, with almost-default settings:
- formatter
- linter
- type checker
- test runner with coverage
- `.editorconfig`
- optionally, pre-commit hooks that run format and lint

**3. Configuration.**
- Load all config from environment variables, following the twelve-factor app approach.
- Commit a `.env.example` that has every variable name but no real values.
- Make sure `.env` is in `.gitignore`.
- Never commit secrets.

**4. Local environment.**
- If the app needs services such as a database, queue, or cache, add a `docker-compose.yml` so one command starts them all.
- Add a database migration tool, if the app has a database (`designing-data-models`).

**5. CI.** Follow the `setting-up-ci-cd` skill. The pipeline runs on every push and pull request: install → lint → type-check → test → build.

**6. CLAUDE.md.** Replace every placeholder with the real project name, stack, and exact commands. Keep the file short.

**7. Prove it.**
- Write one smoke test, for example a health endpoint that returns 200, or the app renders.
- Run install, lint, test, and run locally, and show the user the output.
- Commit with `chore: project setup` (`writing-commits-and-prs`).
- Mark T-000 done in `docs/plan/BACKLOG.md`.

Ask the user before creating any remote repository, pushing, or connecting cloud accounts.

Finish with: "Next: `/phase-5-build` (picks up T-001)".
