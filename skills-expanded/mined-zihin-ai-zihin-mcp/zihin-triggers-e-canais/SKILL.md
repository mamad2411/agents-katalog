---
name: zihin-triggers-e-canais
description: Use this guide to connect an agent to webhooks, schedules or email, choose session and response behavior, and validate delivery to the intended external channel.
---

# Configure triggers and channels

Read `zihin://schemas/trigger_config` and the tool input schema. Establish the source
system, message field, expected response format and session continuity requirements.

For webhooks, configure message extraction, response adapter, session strategy, sender
access and execution mode. Derived session fields must resolve through `context_mapping`;
otherwise continuity may be lost. Use only documented sender-access modes. Choose
synchronous responses or asynchronous execution with a configured callback.

Use the returned `call` block for the callable URL and authentication header. Do not guess
the route or authentication mode. API-key and signature authentication require different
headers. Trigger responses do not disclose the account API key. Store callback credentials
as tenant secrets and reference them by `secret_ref`.

For schedules, supply a cron expression, time zone and query template. Choose a supported
output channel. Scheduled runs open new sessions by default; use persistent memory or a
supported delivery target when continuity is needed. Dynamic event templates do not
resolve without event context: use a literal target for a schedule.

Output channels differ by trigger type. Check the schema and documentation before
assuming a webhook and schedule implement the same delivery options. Do not select
reserved channels. For email, configure allowed senders and filtering as required.

`test_trigger` executes the agent using a temporary session and can consume credits or
cause external effects. Inspect execution history and delivery results. Use
`toggle_trigger` to disable automation without deleting its configuration.
