---
name: discover-capability-and-request-access
description: "Inspect your current tools, browse the PolyGents catalog for a capability you might be missing, and ask a human admin to file a support ticket so PolyGents support can grant the missing tool/skill. The actual ticket-creation step requires explicit human-in-the-loop approval and lands in the internal Help & Support system under the `agent-capability-request` category."
---

# Discover capability & request access

PolyGents agents sometimes hit a wall because a particular tool or skill they would benefit from is not in their assigned capability set. This skill is the **only** correct way to escalate that gap — do NOT silently retry, do NOT pivot to an unrelated workaround, and **never** file the gap as a customer Jira ticket or an internal bug. Use the trio below instead.

## When to use this skill

Trigger when **all** of the following are true:
1. You need a capability to complete the task (writing to a system, calling a specific API, reading from a specific data source, etc.).
2. You cannot find a tool you have access to that fits.
3. You have **not** simply forgotten a tool you already have — confirm first with `list_my_capabilities`.

Do NOT trigger when:
- You can accomplish the task with the tools you already have (LLM laziness is not a missing-capability reason).
- The blocker is a transient platform issue (Docker timeout, integration outage, etc.) — use the `self-report-agent-issue` skill and the `report_incident` tool instead.
- The user explicitly forbade external systems for this task.

## The loop

### Step 1 — reflect with `list_my_capabilities`

Call `list_my_capabilities` first (read-only, no approval prompt). The response includes every tool you have access to in the current run plus the catalog metadata when available (description, category, risk level). If the capability you thought you were missing is in fact in the list, use it and stop.

### Step 2 — search the catalog with `discover_capability`

Call `discover_capability` (also read-only) with a `query` describing what you need (e.g. `"send programmatic SMS"`, `"sentiment analysis"`). You can also constrain by `kind` (`tool` vs `skill` vs `any`) and `category`. Each result item is flagged with `available_to_me: true` when you already have it. The catalog is filtered by the initiative's category allowlist when configured — if nothing comes back, the capability either does not exist or the customer narrowed the allowlist.

### Step 3 — request access with `request_tool_or_skill_access` (WRITE, requires approval)

This step is a **write action**. The runtime will pause the run and surface a tool-approval prompt to the admin showing exactly what you intend to file. The support ticket is **only** created if the admin approves; on rejection nothing is written. Plan your message accordingly so the admin can decide without follow-up:

- `kind` — `tool` or `skill`.
- `name` — the exact catalog name returned by `discover_capability` (e.g. `pubmed_search`).
- `category` — when known.
- `justification` — **required**. 1–2 paragraphs explaining what task is currently blocked and why this capability unblocks it. Be specific; PolyGents support rejects vague "would be nice" requests.
- `context_snippet` — optional 1–3 sentences quoting the user message / task that triggered the request. Keep PII out — it is visible to the admin and to PolyGents support.

On success the response contains the support ticket id and number (e.g. `TKT-481`) and a `dedupeKey`. The ticket is filed under the `agent-capability-request` category and is visible in the customer's **Help & Support** page as well as in the PolyGents super-admin ticket queue. PolyGents support replies on that ticket. Duplicate requests (same `kind`+`name` for this account in the last 14 days) are **deduped** — you'll get `status: 'reused_existing'` and the original ticket id back instead of creating a copy.

After filing the request, **continue with the best partial work you can** using your current tool set, and explicitly tell the user that you filed support ticket `TKT-…` so they know what to expect.

## Anti-patterns

- ❌ Calling `request_tool_or_skill_access` without first running `list_my_capabilities` + `discover_capability`. The admin needs to see that you already checked.
- ❌ Filing the request with a vague justification. PolyGents support rejects those.
- ❌ Using this skill to ask for someone else's customer data — PolyGents only grants platform-level capabilities, not tenant data.
- ❌ Repeatedly retrying the same request name when you already got `status: 'reused_existing'`. Wait for support to reply on the existing ticket.
- ❌ Trying to file the support ticket via `request_tool_or_skill_access` for a *non*-capability issue (e.g. an outage). Use `report_incident` instead.
