---
name: renovate-43-self-hosting
description: Reviews and designs safe self-hosted Renovate 43 runs. Use when working with Renovate CLI, Docker, CI schedules, config.js, RENOVATE_* environment variables, tokens, caches, logs, unsafe execution settings, or Renovate 43 upgrades.
license: MIT
compatibility: Requires Renovate 43 knowledge. Runtime validation may require Docker or Node.js with npx.
---

# Renovate 43 Self-Hosting

Use this skill for self-hosted Renovate 43 CLI, Docker, CI schedules, tokens, cache/logging, global config, and unsafe execution review.

## Workflows

- `workflows/renovate-43-self-hosted-run-review-workflow.md`
- `workflows/renovate-43-upgrade-workflow.md`

## Resources

- `resources/renovate-43-self-hosted-security-matrix.md`

## Scripts

Run `python3 scripts/guard-renovate-unsafe-command.py --help` before relying on it.
