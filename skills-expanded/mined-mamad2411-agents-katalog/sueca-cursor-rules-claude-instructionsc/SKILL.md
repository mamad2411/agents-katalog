---
description: Sueca — Project Instructions (mirrors CLAUDE.md — keep in sync)
alwaysApply: true
---

# Sueca — Project Instructions

## Deploying to prod

Deploy to prod = **publish a release**, not a manual restart:

1. Commit your work (clean tree — a dirty tree BLOCKS auto-deploy).
2. `git tag vX.Y.Z` (semver, annotated ok) → `git push origin main --tags` (if a remote exists).
3. The server's deploy agent (`admin-deploy.timer`, every 5 min) picks up the
   new tag, fast-forwards the repo, runs the stack's restart, health-checks,
   and **auto-rolls-back** on failure.

Monitor at https://admin.peixotolabs.com. Manual `./app.sh restart prod` is for
emergencies only. Fleet registry: `/root/AdminPanel/registry.yml`. Full infra
docs: `/root/SERVER_INFRA.md` and `/root/CLAUDE.md`.
