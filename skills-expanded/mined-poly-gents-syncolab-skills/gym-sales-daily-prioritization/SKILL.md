---
name: gym-sales-daily-prioritization
description: "Triage open Arbox tasks and leads into a prioritized daily call list for gym sales reps"
---

# Gym Sales Daily Prioritization

## Purpose

Produce a **ranked daily work list** for gym sales staff from live Arbox tasks and leads, grouped by status category.

## When to Use

- Morning standup or “what should I call first?”
- End-of-day pipeline review.
- After a marketing push when lead volume spikes.

## When NOT to Use

- Manual lead creation (use **gym-lead-ingestion-exceptions**).
- Trial booking or measurements (use **gym-member-onboarding-flow**).

## Expected Outcome

- Numbered call list with name, status, last touch, suggested action, and optional draft opener.
- Follow-up tasks created in Arbox when the rep confirms.

## Workflow

1. Load status semantics via **gym-arbox-status-playbook** (`GET /v3/statuses`).
2. **`arbox_list_tasks`** (`from_date`/`to_date` = today) — open tasks due today or overdue.
3. **`arbox_list_leads`** — active pipeline; `leadsInProcessReport` via **`arbox_public_get`** on `v3/reports/leadsInProcessReport` when needed.
4. Group by status category using the tenant status table.
5. Apply default priority (adjust with owner if studio differs):

   1. Closing meetings today / overdue callbacks
   2. Fresh leads (<48h) and scheduled callbacks
   3. Due measurements before nutrition handoff
   4. Existing member touches only when on today's task list
   5. Catch-all / “other” only when explicitly assigned

6. Output numbered list; draft one-line opener in the owner's preferred language.
7. **WhatsApp follow-ups**: draft message text for the rep. Sending uses the agent's **WhatsApp channel** (Workforce → wacli session) — there is no `whatsapp_*` agent MCP tool, same as Telegram.
8. Create follow-up tasks via Arbox task APIs when confirmed.

## Tool Availability Rules

| Access | Behavior |
|--------|----------|
| Full Arbox | Pull tasks/leads, create tasks, propose status updates |
| Read-only | Prioritize and draft comms only |

### Related tool sets

- `arbox`

## Output Format

1. **Today’s top 5–10** — ranked with rationale
2. **Pipeline snapshot** — counts by status
3. **Draft openers** — optional, non-destructive
