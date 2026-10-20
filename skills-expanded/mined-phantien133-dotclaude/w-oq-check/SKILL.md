---
description: Phase 0b helper for w-task — scan the project's Open Questions doc and surface OQs relevant to the current task. Flags blockers prominently. Generic version of streaming-oq-check.
argument-hint: <module-or-keywords>
allowed-tools: Bash, Read
---

# w-oq-check

Read `workflow.oq_docs_path` (e.g. `docs/overview/open-questions.md`) and return
the OQs that could affect the current task — flagging any that BLOCK it.

Reads `.claude/workflow.yaml`:
- `workflow.oq_docs_path`

---

## Inputs

- `$1` — module name OR comma-separated keywords. Used to filter OQ entries
  by relevance.

---

## Step 1 — Preconditions

If `oq_docs_path` is null: print "OQ tracking not configured. Skipping." and exit 0.

If file does not exist at the configured path: print warning, exit 0.

---

## Step 2 — Parse OQ table

The convention (from streaming-docs governance) is a markdown table with rows
like:

```
| OQ-001 | Payment Gateway Selection | BLOCKS Monetization |
| OQ-009 | WebSocket Reconnect | Low urgency |
```

Parse rows into:
- `id` (OQ-XXX)
- `title`
- `impact` (BLOCKS <module> | Affects <module> | Low urgency | …)

Also support sectioned format (## OQ-001) — parse each `## OQ-` heading.

---

## Step 3 — Filter

Match each OQ row against the input keywords/module:
- Case-insensitive substring match on title + impact text
- Special: if impact text starts with "BLOCKS" or "Blocks", always include
  when the module name matches; flag as BLOCKER.

---

## Step 4 — Output

Print to chat (and return to caller skill — w-task / w-context-load will quote
this output into context.md § Known Constraints):

```
## OQs touching this task

### Blockers
- OQ-001: Payment Gateway Selection — BLOCKS Monetization
  → Consider documenting your decision in <oq_docs_path> before proceeding.

### Relevant (non-blocking)
- OQ-009: WebSocket Reconnect Strategy — Low urgency

### No OQs relevant
(this section appears when filter returns empty)
```

If blockers found, also print a final line:
```
⚠️ 1 OQ would block this task. Pause and resolve before continuing.
```
Then exit non-zero (1) so the caller skill knows to stop. Otherwise exit 0.

---

## Notes

- Do NOT resolve OQs unilaterally. The skill only surfaces them.
- If the developer decides to resolve an OQ during the task, Phase 5 should
  invoke `w-adr` to record the decision and the developer should manually
  update `oq_docs_path` to mark the OQ as RESOLVED.
