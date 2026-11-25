---
name: automating
description: Build automated actions, server actions, scheduled jobs, and email triggers in Odoo. Use when the user wants "when X happens, do Y", or a scheduled/recurring task.
triggers: [automate, automation, automated action, server action, trigger, cron, schedule, recurring, webhook, rule]
---

# Automating

When X happens → do Y. Without writing a custom module.

## Key models

- `base.automation` — "automated action": trigger + server action on a model
- `ir.actions.server` — server action (Python code, record update, email, ...)
- `ir.cron` — scheduled job (runs every N minutes/hours/days)
- `mail.template` — email body + subject for notification actions
- `ir.model` — target model of the automation

## Trigger types (`base.automation.trigger`)

- `on_create` — record is created
- `on_write` — record is updated (optionally on a specific field via `trigger_field_ids`)
- `on_create_or_write` — either
- `on_unlink` — record deleted
- `on_time` — scheduled (e.g. "3 days after deadline")
- `on_time_created` — relative to create_date
- `on_time_updated` — relative to write_date

## Typical workflows

1. **Notify on deal won** — `base.automation` on `crm.lead`, trigger `on_write` with `stage_id = Won`, action sends `mail.template`
2. **Auto-assign** — `on_create` on a model, server action sets `user_id` based on a rule
3. **Recurring job** — `ir.cron` with `interval_number/type`, calls a server action or model method
4. **Multi-step** — chain via `ir.actions.server.child_ids`

## Gotchas

- Python code in server actions runs in a restricted sandbox — no imports, limited builtins.
- `on_write` fires on every field change unless you set `trigger_field_ids` — can cascade.
- `ir.cron` runs as `user_id` — watch permissions; use a dedicated automation user.
- Filters on automations use the same domain syntax as search — test before enabling.
- Disable vs delete: toggle `active` to pause, don't delete, so audit trail stays.
