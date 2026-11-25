---
name: beads-linear-sync
description: Use when configuring or operating Beads Linear sync in Darkmatter repos, especially choosing Linear team/project scope, mapping Beads prefixes to Linear identifiers, handling himitsu API keys, or dry-running bd linear sync safely.
---

# Beads Linear sync

## Overview

Use Beads as the repo-local task namespace and Linear as the org-visible planning surface. Treat Beads IDs like `infra-*` as local repository identifiers; treat Linear IDs like `LAB-*` as team-owned identifiers; connect them with `external_ref` after sync.

Default Darkmatter Linear team: **LAB**. Use another team only when the user explicitly names it or a repo already has a documented team owner.

## When to use

- User asks to connect Beads to Linear, enable Linear sync, or run `bd linear sync`.
- User asks how Beads prefixes map to Linear issue prefixes.
- A repo has `.beads/` and needs team/project/status/priority mapping configured.
- A Linear API key is available through `himitsu` or another approved secret store.
- Sync would create, import, or update issues and needs a dry-run safety pass first.

## When NOT to use

- Repo has no Beads database yet: use `beads-setup` first.
- User only wants local issue tracking with no Linear integration.
- User asks to create Linear tickets outside Beads sync; use the project’s normal Linear workflow.
- A required API key is missing and cannot be fetched from an approved secret store.

## Core model

| Concept | Owner | Example | Rule |
|---|---|---|---|
| Beads prefix | Repository | `infra-*`, `skills-*` | Local namespace only. Do not force it to match Linear. |
| Linear team key | Linear team | `LAB-*`, `ENG-*` | Determines Linear issue identifiers. |
| Linear project | Linear planning scope | `Platform Monorepo PoC` | Optional filter/grouping; does not change issue prefix. |
| Link field | Beads issue | `external_ref` | Durable bridge from Beads issue to Linear issue. |

Preferred default:

```bash
bd config set linear.team_id "295ca234-4223-4c86-9e26-85b74968c77a" # LAB
```

Do not store personal Linear tokens in Beads config. Inject them for each command:

```bash
LINEAR_API_KEY=<REDACTED>
```

## Configuration checklist

1. Confirm the secret points at Darkmatter Linear without printing the token.

   ```bash
   LINEAR_API_KEY=<REDACTED>
   ```

2. Configure LAB as the default team unless the repo documents a different owner.

   ```bash
   bd config set linear.team_id "295ca234-4223-4c86-9e26-85b74968c77a"
   bd config unset linear.team_ids || true
   ```

3. Configure one Linear state per Beads status. This avoids ambiguous push fallbacks when Linear has both `In Progress` and `In Review` as `started` states.

   ```bash
   bd config set "linear.state_map.Todo" open
   bd config set "linear.state_map.In Progress" in_progress
   bd config set "linear.state_map.Done" closed
   ```

4. Configure reusable priority, type, relation, and ID rules.

   ```bash
   bd config set linear.id_mode hash
   bd config set linear.priority_map.0 4
   bd config set linear.priority_map.1 0
   bd config set linear.priority_map.2 1
   bd config set linear.priority_map.3 2
   bd config set linear.priority_map.4 3
   bd config set linear.label_type_map.bug bug
   bd config set linear.label_type_map.feature feature
   bd config set linear.label_type_map.epic epic
   bd config set linear.relation_map.blocks blocks
   bd config set linear.relation_map.blockedBy blocks
   bd config set linear.relation_map.duplicate duplicates
   bd config set linear.relation_map.related related
   ```

5. Use `linear.project_id` only when the repo has a clearly owned Linear project. Leaving it unset is safer for a team-wide default.

## Safety workflow

Run dry-runs before any real sync.

```bash
LINEAR_API_KEY=<REDACTED>
LINEAR_API_KEY=<REDACTED>
LINEAR_API_KEY=<REDACTED>
```

Interpret dry-runs before proceeding:

- Pull imports unrelated Linear issues: narrow by team/project or stop and ask.
- Pull imports many closed/canceled issues: ask before real pull.
- Push creates expected local issues: proceed only if user wants real Linear tickets.
- Push says no-op while status says local-only: investigate before trusting sync.
- State map ambiguity appears: keep exactly one Linear state mapped to each Beads status.

## Common mistakes

- **Assuming `infra-*` must become `INFRA-*`.** Beads prefixes are repo-local. Linear prefix comes from the Linear team key.
- **Using ENG by default.** Use LAB unless ownership says otherwise.
- **Setting all Linear state types.** Mapping `backlog`, `unstarted`, and custom `In Review` all to `open` makes push ambiguous. Pick a single target state for each Beads status.
- **Storing `linear.api_key`.** Prefer `LINEAR_API_KEY="$(himitsu read ...)"` so secrets stay in the secret store.
- **Running bidirectional sync first.** Use separate pull and push dry-runs so the direction and blast radius are visible.

## Commit hygiene

Beads writes configuration into its Dolt database and may update `.beads/issues.jsonl`. Before claiming the integration is ready, inspect both Git and Beads state:

```bash
bd config show | rg "linear\."
bd config validate
git status --short
```

Commit only intentional Beads config/export changes. Do not include unrelated issue exports or user worktree changes.
