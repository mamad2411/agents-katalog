---
name: taruvi-functions
description: >
  Use this skill when the user needs to write, edit, debug, or understand a
  Taruvi serverless function — including backend logic that spans multiple
  resources, event-driven triggers, scheduled cron jobs, async long-running
  tasks, webhook receivers, or calling external APIs with stored secrets.
  Also use when the user has multi-step backend operations chained in frontend
  code that should be moved server-side, even if they don't mention "functions."
metadata:
  author: taruvi-ai
  version: "1.0.0"
---

## Overview

Guide for authoring Taruvi serverless functions — deciding when a function is needed, which execution mode to use, how to call the injected `sdk_client`, and how to invoke functions from the frontend.

**Compliance rule:** This skill's prescribed patterns (exact function signature, SDK usage, mode selection) are mandatory. Do not invent SDK methods, skip validation, or hardcode secrets. If a requirement cannot be met, stop and ask the user.

## When to Use This Skill

- Any action that touches **2 or more resources** (database + storage, users + database, etc.)
- Custom backend logic beyond simple CRUD
- Reacting to data events (`RECORD_CREATE`, `RECORD_UPDATE`, `RECORD_DELETE`)
- Reacting to user lifecycle events (`POST_USER_CREATE`, `POST_USER_DELETE`, etc.)
- Scheduled / cron background jobs
- Calling external APIs using stored secrets
- Long-running tasks (>30s) that must not block the UI
- Public unauthenticated endpoints
- Function-to-function pipelines
- Authorization-gated operations

**Do not use functions for:** single-table CRUD, file serving, login/logout, simple filtered lists, or single-source KPI queries. Use Refine provider hooks instead.

## Step-by-Step Instructions

### Step 1 — Confirm a function is needed

Open and read `references/when-not-to-use-functions.md`. If the task is single-resource CRUD with no side effects, stop — use Refine provider hooks instead.

### Step 2 — Read core references (always)

1. Open and read `references/guardrails.md` — non-negotiables before any code.
2. Open and read `references/modes-and-triggers.md` — pick APP / PROXY / SYSTEM and the right trigger.
3. Open and read `references/sdk-in-functions-key-points.md` — runtime contract details.

### Step 3 — Read conditional references (only when relevant)

- If calling `sdk_client` modules → read `references/sdk-surfaces.md` and `references/resources.md`
- If the function is event-triggered → read `references/events-and-filters.md`
- If calling the function from frontend → read `references/frontend-calling.md`
- If you need a worked example → read `references/scenarios.md`
- If unsure about SDK method names → read `references/sdk-docs-workflow.md`

### Step 4 — Write the function

Write function code only after reading the relevant references above.

### Step 5 — Verify before finishing

- [ ] Signature is exactly `def main(params, user_data, sdk_client):`
- [ ] Return value is JSON-serializable (no datetime, set, or custom objects)
- [ ] No hardcoded secrets — all secrets use `sdk_client.secrets.get()`
- [ ] No re-authentication of `sdk_client`
- [ ] Correct execution mode set (`app`, `proxy`, or `system`)
- [ ] If async: `is_async=True` is set for tasks >30s
- [ ] Uses `log()` not `print()` for structured logging
- [ ] Input params are validated before any side effects

## Examples

**APP mode — minimal valid function:**
```python
def main(params, user_data, sdk_client):
    record = sdk_client.database.get("orders", record_id=params["order_id"])
    return {"success": True, "data": record}
```

**Frontend call — wait for result:**
```typescript
const result = await executeFunction("calculate-total", { items: [1, 2, 3] });
```

**Frontend call — fire and forget:**
```typescript
executeFunctionAsync("cleanup-deleted-tasks", { task_ids: ids }).catch(console.warn);
```

See `references/scenarios.md` for 8 complete end-to-end examples.

## Gotchas

- **Wrong signature** — `main` must accept exactly `(params, user_data, sdk_client)`. Not `(event, context)`, not `(request)`, not `(**kwargs)`. Any deviation causes an immediate `SandboxError` before any code runs.
- **Trying to re-authenticate** — `sdk_client` is already authenticated. Never call `client.auth()`, `client.login()`, or pass API keys to it. It just works.
- **Hardcoded secrets** — always use `sdk_client.secrets.get("KEY")`. Hardcoded values are a security violation and will be rejected in review.
- **PROXY vs APP confusion** — if you only need to forward a payload to an external URL with no Python logic, use PROXY mode with `webhook_url`. APP mode is for custom Python logic with `code`.
- **Sync timeout** — tasks that may take >30s must use `is_async=True`. Synchronous calls will time out at 30s and leave the UI spinner stuck.
- **`print()` vs `log()`** — `print()` is unstructured stdout only and not queryable. `log()` produces structured, leveled, queryable entries on the invocation record. Always use `log()`.
- **Frontend cascade** — if you see multi-resource operations chained in frontend code (delete task → delete attachments → delete activities), that is a bug. Move the chain to a single function.
- **Returning non-serializable types** — `datetime`, `set`, `Decimal`, and custom class instances will crash the return. Convert to `str`, `list`, `float`, or `dict` before returning.
- **Missing `execution_mode` on create** — `manage_function` requires `execution_mode` at creation time. Without it, the function cannot be routed and creation silently fails.

## References

- `references/guardrails.md` — core non-negotiables
- `references/modes-and-triggers.md` — APP/PROXY/SYSTEM and trigger types
- `references/sdk-surfaces.md` — available sdk_client modules
- `references/sdk-in-functions-key-points.md` — runtime contract
- `references/resources.md` — per-resource operation patterns
- `references/sdk-docs-workflow.md` — how to validate SDK behavior
- `references/frontend-calling.md` — executeFunction / executeFunctionAsync
- `references/when-not-to-use-functions.md` — decision table
- `references/events-and-filters.md` — event triggers and CEL filters
- `references/scenarios.md` — 8 complete worked examples
