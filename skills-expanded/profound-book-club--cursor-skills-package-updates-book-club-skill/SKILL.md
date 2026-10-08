---
name: package-updates-book-club
description: >-
  Runs the profound-book-club package update workflow (root and infrastructure pnpm updates, lint/build checks, GitHub
  Actions pins), then deploys to dev per deploy-dev-book-club. Use when updating dependencies, refreshing action SHAs, or
  when the user invokes package maintenance plus a dev deploy.
---

# package-updates-book-club

## Workflow

1. **Package updates** — Read and carry out every step in
   [.cursor/commands/package-updates-book-club.md](../../commands/package-updates-book-club.md).
   That file requires broad permissions (`all`); use the same scope when running shell commands.
   Do not skip verification steps (lint, site build, infrastructure build/synth, action checks).
2. **Deploy to dev** — After package updates are complete and verified, read and carry out every step in
   [.cursor/commands/deploy-dev-book-club.md](../../commands/deploy-dev-book-club.md), including AWS profile,
   infrastructure script, site build, S3 sync, and CloudFront invalidation.

If either phase fails, stop and report the failure before continuing.
