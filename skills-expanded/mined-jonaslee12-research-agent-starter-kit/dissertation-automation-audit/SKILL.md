---
name: dissertation-automation-audit
description: Evidence-first audit of dissertation automations, hooks, scheduled checks, MCP/connectors, browser/LMS monitors, and workflow wrappers to identify what is live, broken, redundant, missing, or unsafe before enabling anything.
---

# Dissertation Automation Audit

Use this skill when auditing whether automations, hooks, monitors, MCP servers, connectors, scheduled tasks, or wrapper workflows are actually live and useful for the dissertation system.

## Purpose

Adapt ECC automation-audit-ops to this dissertation project. It is read-only by default and should produce an evidence-backed inventory before any fix or new automation is proposed.

## Activate For

- "what automations are live?"
- "is LMS monitoring set up?"
- "are there hooks running?"
- "which reminders or recurring jobs exist?"
- "did a connector/MCP/plugin actually get installed?"
- "are there overlapping automation rules?"

## Audit Categories

| Category | Examples |
|---|---|
| Local hooks | pre/post tool hooks, shell scripts, app-specific triggers |
| Codex automations | heartbeat or cron automations |
| Browser/LMS monitors | page watchers, deadline checks |
| MCP/connectors | installed apps, connected services, exposed tools |
| Document pipeline | Word/PDF rendering helpers, batch converters |
| Knowledge sync | Obsidian, research-wiki, source register synchronization |

## Live-State Labels

For every item, mark:

- `configured`
- `authenticated`
- `recently verified`
- `stale or broken`
- `missing`
- `not intentionally enabled`

## Workflow

1. Inventory real files/configs/tools.
2. Check proof path:
   - file path
   - automation definition
   - tool output
   - task-state record
   - recent successful verification
3. Identify overlap or redundancy.
4. Recommend one of:
   - `keep`
   - `merge`
   - `cut`
   - `fix next`
   - `do not enable`

## Output Format

```text
Current automation surface:
- item | source | live state | proof

Findings:
- active breakage:
- overlap:
- stale status:
- missing capability:

Recommendation:
- keep:
- merge:
- cut:
- fix next:
```

## Guardrails

- Read-only unless the user explicitly asks to create/update/delete an automation.
- Do not assume a config is live.
- Do not create recurring tasks silently.
- Do not connect external services or install plugins during audit.
- Do not monitor LMS or email without explicit user confirmation.
