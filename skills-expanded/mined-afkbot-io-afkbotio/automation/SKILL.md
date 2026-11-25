---
name: automation
description: "Automation management via `automation.*` tools. Use when the user explicitly wants to create, inspect, update, list, or delete cron or webhook automations."
aliases: automation-cron, automation-webhook, automation-list, automation-get, automation-edit, automation-delete, cron, webhook
triggers:
  - cron
  - schedule
  - scheduled
  - webhook
  - automation
  - automate
  - create cron
  - create webhook
  - создай крон
  - создай крон
  - создай cron
  - настрой cron
  - автоматизацию
  - автоматизация
  - расписание
  - по расписанию
tool_names:
  - automation.list
  - automation.get
  - automation.create
  - automation.update
  - automation.delete
preferred_tool_order:
  - automation.create
  - automation.update
  - automation.get
  - automation.list
  - automation.delete
execution_mode: executable
---
# automation

Manage automation entities via `automation.*` tools.

Use this skill only for explicit automation requests:
- schedule/cron jobs
- webhook automations
- automation list/get/update/delete

## Workflow
1. Clarify target operation (`create`, `list`, `get`, `update`, `delete`).
2. For `create`, collect required fields:
   - `name`
   - `prompt`
   - `trigger_type` (`cron` or `webhook`)
   - if `cron`: `cron_expr` (+ optional `timezone`, default `UTC`)
   - rewrite the user's ask into a self-contained automation `prompt` that states the task, desired outcome, and any constraints; do not include schedule details in the stored prompt
   - the rewritten prompt should be explicit enough that a later automation run can understand it without the original chat context
   - if the task requires external side effects (for example posting in GitLab/GitHub, calling APIs, or sending messages), encode required tool usage directly in the automation prompt
3. For `update`, require `id` and include only changed fields.
4. For `delete`, require `id` and restate target before execution.
5. After tool call, return short factual result from payload:
   - `id`, `name`, `status`, `trigger_type`
   - for cron: `cron.cron_expr`, `cron.timezone`
   - for webhook create/rotate: `webhook.webhook_path`, `webhook.webhook_url`, `webhook.webhook_token`, and `webhook.webhook_token_masked`; create/rotate still reveal the fresh endpoint directly
   - for webhook get/list: only `webhook.webhook_token_masked` and execution status fields are available; these are non-secret status reads
   - explain that external webhook providers should call the returned path/URL directly; the token is embedded into the webhook path, not passed via headers
6. For read-only webhook questions such as “what is the webhook URL/token/path?”:
   - use `automation.get`/`automation.list` only to identify the automation and report masked status fields
   - explain that current live webhook URL/path is not available from generic automation tool reads
   - do not call `automation.update` or rotate webhook tokens unless the user explicitly asked to rotate/regenerate them

## Rules
- Never call `automation.*` for plain integration tasks (e.g. send Telegram message once).
- For requests that mix automation + integration (e.g. “create cron that sends Telegram message”), automation owns the current turn. Use `automation.create` or `automation.update` now; the referenced channel/app skill is only input to the automation prompt.
- Prefer prompts that name the expected tool path explicitly when side effects are required, for example:
  - `Use app.run with the telegram app to send ...`
  - `Use http.request to POST ...`
  - `Use bash.exec to run ...`
- Do not invent missing required fields when user can provide them.
- Never claim success without successful `automation.*` tool result in current turn.
