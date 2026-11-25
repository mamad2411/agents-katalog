---
name: cosmosmith-devops-release
description: Prepare build, CI, environment, deployment, monitoring, rollback, and release readiness for a Cosmosmith project. Use when tasks approach release, when setup/deploy commands are missing, or when current platform docs are needed.
---

# Cosmosmith DevOps Release

## Purpose

Make the system buildable, testable, deployable, observable, and reversible.

## Workflow

1. Read `task.md`, `design.md`, QA evidence, and project configuration.
2. Use web research for current platform, CI, hosting, container, runtime, or cloud provider docs when needed.
3. Identify setup, build, lint, test, run, deploy, and rollback commands.
4. Document environment variables without exposing secrets.
5. Define monitoring, logging, smoke checks, and rollback plan.
6. Write `docs/cosmosmith/release-readiness.md` or update release tasks.
7. Update `task.md` with remaining release blockers or evidence.

## Standards

- Prefer reproducible setup over local folklore.
- Automate checks before relying on manual confidence.
- Treat developer experience as part of production quality.
- Keep secrets out of commits and generated docs.

## Completion

Stop when release readiness is explicit or blockers are recorded in `task.md`.

