---
name: knock-lifecycle-opportunities
description: Scan a product codebase for activation, engagement, and retention moments and recommend lifecycle messaging opportunities. Use when finding onboarding, churn, trial, or habit-forming notification candidates without creating Knock resources.
---

# Lifecycle opportunities skill

Find where users activate, stall, pay, invite, or churn in **this** product’s code and data model. Recommend messaging opportunities tied to real events and UI states.

## Hard constraint

**Do not create, update, push, or delete Knock resources** via MCP or CLI. Output an opportunity backlog and event/trigger sketches only. Hand off to `knock-setup` or `knock-product-messaging-strategy` only if the user asks to build.

## Output contract (hard)

Write all detailed findings to **`knock-plan.md`** at the repo root (create or update). Keep chat **minimal** — status + confirmation only.

Do **not** paste opportunity briefs, code-path inventories, or long rationale into chat. Follow `rules/opportunity-brief-format.md`.

Allowed chat content:

1. One short status line (path + count)
2. Optional one-line blocker
3. Bold confirmation question as the **last line**

Example:

Wrote `knock-plan.md` with 6 ranked opportunities.

**Which opportunities should we take next?**

## Overview

1. **Map the product lifecycle in code** (`rules/map-product-lifecycle.md`) — write signals into the file
2. **Select high-value opportunities** (`rules/select-opportunities.md`) — rank in the file
3. **Write opportunity briefs** (`rules/opportunity-brief-format.md`) — full briefs in the file only

## How to use this skill

1. Infer personas, accounts/workspaces, and key funnels from the repo — capture in the file, not chat.
2. Locate signup, onboarding, invite, billing, usage, and inactivity signals — same.
3. Propose at most 8 prioritized lifecycle messages in `knock-plan.md`.
4. Chat: status line + ask which to advance. Do not dump the list body in chat.
5. When the user asks to build in Knock or deepen strategy, hand off with a structured payload — do **not** invite re-ranking:

```markdown
### Setup handoff
- **plan.** knock-plan.md
- **confirmed.** [names or indexes]
- **skipped.** [names or indexes]
- **deferred / blocked.** [names + reason]
```

`knock-setup` must treat `confirmed` as authoritative, read detail from `knock-plan.md`, and skip rediscovery. For fuller strategy design, hand off confirmed items to `knock-product-messaging-strategy` (same `knock-plan.md`).

## Rule files reference

- `rules/map-product-lifecycle.md` — where to look in code
- `rules/select-opportunities.md` — prioritization
- `rules/opportunity-brief-format.md` — plan file structure and chat brevity

## Docs

- https://docs.knock.app/concepts/workflows
- https://docs.knock.app/concepts/guides
- https://docs.knock.app/concepts/audiences
- https://docs.knock.app/send-notifications/triggering-workflows/audiences
- https://knock.app/manuals/product-leaders-guide-to-effective-notifications/the-product-leaders-guide-to-effective-notifications
