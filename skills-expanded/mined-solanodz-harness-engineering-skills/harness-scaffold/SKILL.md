---
name: harness-scaffold
description: >-
  Sets up a new project so the agent can start, verify, and resume anytime —
  AGENTS.md, feature list, progress log, init.sh, handoff. Use when adopting
  harness engineering or the user asks to set up an agent-ready project.
---

# Harness Scaffold

## What this does for you

- **Start in minutes** — minimum files an agent needs on day one
- **Resume across sessions** — progress and feature list on disk, not in chat
- **Built-in verification** — `init.sh` and done criteria from the start

Creates the minimum harness package so an agent can start, maintain scope, verify work, and resume across sessions.

Based on [Learn Harness Engineering](https://walkinglabs.github.io/learn-harness-engineering/) — Project 01 and resource library.

## Five-subsystem model

| Subsystem | Artifact | Purpose |
|-----------|----------|---------|
| Instructions | `AGENTS.md` or `CLAUDE.md` | Startup path, rules, definition of done |
| State | `feature_list.json`, `progress.md` | Active feature, evidence, next step |
| Verification | `init.sh` | Commands the agent must run before declaring done |
| Scope | Dependencies and criteria in feature_list | Prevents over-scoping and half-finished work |
| Lifecycle | `session-handoff.md`, clean-state checklist | Clean restart in the next session |

## First step

1. Inspect what exists: instruction files, state, verification commands, docs, manifests.
2. Ask only what you cannot infer: target agent (Cursor/Claude Code), file name, overwrite tolerance.
3. Prefer a minimal harness. Add complexity only when the problem requires it.

## Create harness

If you have access to the skills repo:

```bash
node scripts/create-harness.mjs --target /path/to/project
```

Useful options:

- `--agent-file CLAUDE.md` for Claude Code projects
- `--package-manager npm|pnpm|yarn|bun`
- `--commands "cmd one,cmd two"` for custom verification
- `--force` only with explicit user confirmation

If you cannot run scripts, create these files manually using templates in `templates/` from the skills repo.

## Minimum AGENTS.md content

Keep ~100 lines. Must include:

1. **Startup flow**: read progress → feature_list → git log → run init.sh
2. **Working rules**: one feature at a time, do not mark done without evidence
3. **Definition of done**: behavior + verification executed + evidence recorded
4. **End of session**: update progress and feature_list, safe commit

Full template: [templates/agents.md](../../templates/agents.md)

## feature_list.json

Each feature needs:

- `id`, `priority`, `title`, `user_visible_behavior`
- `status`: `not_started` | `in_progress` | `blocked` | `passing`
- `verification`: concrete, observable steps
- `evidence`: empty array until verification passes

Global rules in the JSON:

```json
"rules": {
  "single_active_feature": true,
  "passing_requires_evidence": true,
  "do_not_skip_verification": true
}
```

## init.sh

Must: sync dependencies → run baseline verification → show startup command.

Do not stack new work on a broken baseline.

## After creating

1. Explain what was created and where
2. Tell the user to replace example features with real project features
3. Suggest running `harness-audit` to validate

## Additional resources

- [Memory Persistence](../../references/course/memory-persistence-pattern.md)
- [Lifecycle & Bootstrap](../../references/course/lifecycle-bootstrap-pattern.md)
- [Gotchas](../../references/course/gotchas.md)
