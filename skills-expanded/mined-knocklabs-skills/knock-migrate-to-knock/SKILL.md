---
name: knock-migrate-to-knock
description: Investigate existing messaging infrastructure in a codebase and recommend how it maps to Knock. Use when migrating from Braze, Courier, Customer.io, Iterable, SendGrid, or custom notification code, or when planning a move to Knock.
---

# Migrate to Knock skill

Discover the current messaging stack in this codebase, map it to Knock concepts, and produce an ordered migration plan. This is a **discovery and recommendation** skill.

## Hard constraint

**Do not create, update, push, commit, or delete Knock resources** (workflows, guides, users, tenants, preferences, partials, layouts) via MCP or CLI unless the user explicitly asks after reviewing the plan. Do not run production imports. Output plans, inventories, and optional local app-code suggestions only.

## Output contract (hard)

Write the inventory and migration plan to **`knock-plan.md`** at the repo root (the shared plan file used by `knock-product-messaging-strategy` and `knock-lifecycle-opportunities`; create or update — do not create a second plan). Keep chat **minimal** — status + confirmation only.

Do **not** paste the inventory table or the full phased plan into chat.

Allowed chat content:

1. One short status line (path + counts, e.g. platforms detected and message types found)
2. Optional one-line blocker
3. Bold confirmation question as the **last line**

Example:

Wrote `knock-plan.md`: Courier + SendGrid detected, 14 message types inventoried, 8-phase plan drafted.

**Which migration phase should we plan in more detail next?**

## Docs to use (link in your output)

Always ground recommendations in Knock docs. Prefer these:

| Situation | Doc |
| --- | --- |
| Braze → Knock | https://docs.knock.app/tutorials/migrate-from-braze |
| Courier → Knock | https://docs.knock.app/tutorials/migrate-from-courier |
| Email templates via MCP (only if user asks to execute) | https://docs.knock.app/tutorials/migrate-email-with-mcp-server |
| Workflows | https://docs.knock.app/concepts/workflows |
| Channels | https://docs.knock.app/concepts/channels |
| Users | https://docs.knock.app/concepts/users |
| Preferences | https://docs.knock.app/preferences/overview |
| Tenants / multi-tenancy | https://docs.knock.app/multi-tenancy/overview |
| Subscriptions | https://docs.knock.app/concepts/subscriptions |
| Translations | https://docs.knock.app/template-editor/translations |
| Triggering workflows | https://docs.knock.app/send-notifications/triggering-workflows |
| Sources (CDP) | https://docs.knock.app/integrations/sources/overview |

## Overview

1. **Inventory the current stack** (`rules/inventory-existing-messaging.md`)
2. **Map concepts to Knock** (`rules/map-concepts-to-knock.md`)
3. **Produce a phased migration plan** (`rules/migration-plan.md`)

## How to use this skill

1. Search the repo for providers, SDKs, templates, and send call sites (see inventory rule) — record findings in `knock-plan.md`, not chat.
2. Identify the source platform(s): Braze, Courier, Customer.io, Iterable, Novu, ESP-direct (SendGrid/Postmark/Resend/SES), Slack bots, custom queues, etc.
3. Open the matching migration tutorial when Braze or Courier; otherwise use the generic mapping table in `rules/map-concepts-to-knock.md`.
4. Write the phased migration plan (phases, risks, Knock concept links) into `knock-plan.md`. In chat, ask which phase to plan or execute next — do not execute Knock writes unless asked.

## Rule files reference

- `rules/inventory-existing-messaging.md` — what to find in the codebase
- `rules/map-concepts-to-knock.md` — platform concepts → Knock
- `rules/migration-plan.md` — phased plan output format

## Quick reference

Recommended resource migration order (from Knock Braze / Courier tutorials):

1. Channels / provider connections
2. Workflows and templates (logic + content)
3. Translations
4. Tenants (and branding context, if multi-tenant)
5. Users / identify
6. Subscriptions (lists → object subscriptions)
7. Preferences (after users exist; map topics/groups → workflow categories)
8. Cut over triggers in application code
9. Retire old sends
