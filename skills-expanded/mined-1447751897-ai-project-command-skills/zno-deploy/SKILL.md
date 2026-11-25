---
name: zno-deploy
description: Use when the user writes /zno-deploy or asks about deployment, release, environments, migration, or rollback. Plans and executes the deployment change, updates docs/operations/08-deployment.md, and updates local-development docs when commands or env vars change.
---

# Zno-Deploy — Deployment / Release

`<skills-root>` below means the directory containing all zno-* skills (e.g. `~/.claude/skills` or `~/.agents/skills`).

## Workflow

1. Restate the deployment change: target environment, what is being released or migrated, and the expected outcome.
2. Clarify only what affects environments, data migration, secrets handling, downtime, or rollback strategy.
3. If the deployment involves choosing a platform, CI/CD, containerization, or monitoring stack, apply the technical selection gate from `references/tech-gate.md` first.
4. Plan the change across: build, environment config, migration steps, verification steps, and rollback path. Never deploy to production without an explicit user go-ahead.
5. Update `docs/operations/08-deployment.md` before or alongside the change. If it does not exist yet, scaffold it first:

   ```bash
   python <skills-root>/zno-init/scripts/init_project_docs.py <project-root> --scaffold deploy
   ```

6. If local commands or environment variables changed, also update `docs/operations/07-local-development.md` (`--scaffold local-dev` if missing).
7. Verify the deployment: health checks, smoke tests, or the project's verification commands. Report results factually per `references/verification.md`.
8. Record the release in `docs/development/03-feature-changelog.md` when it ships user-visible behavior.

## Shared references (read only when needed)

- `<skills-root>/zno-init/references/docs-map.md` — full doc set, doc update rules, scaffold triggers.
- `<skills-root>/zno-init/references/tech-gate.md` — technical selection gate and performance-aware design.
- `<skills-root>/zno-init/references/verification.md` — verification gate and final-response page test steps.
