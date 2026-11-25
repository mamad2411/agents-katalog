---
name: coppice-collaboration
description: mentionAgents / agentRequests / assignTo semantics, one-hop consultation rules, and completion rules for done results and handoffs (field roles, implementer completion).
---

## Coppice platform rules — collaboration fields (required)

- `mentionAgents` draws attention and creates notifications only. It never starts a response run after a successful result.
- `agentRequests` is the only successful-result field that can auto-start a consultation. Each entry must use `intent: "consult"` and contain one focused, non-empty request.
- `mentionAgents` and `agentRequests` share the per-run target limit. Unknown, disabled, duplicate, self, and over-limit targets are ignored without failing the source run.
- `assignTo` is the only ownership or handoff field. Assignment wins when the same target also appears in `mentionAgents` or `agentRequests`.
- Automatic consultations are one hop: a `respond_to_mention` result may notify agents but cannot auto-start another consultation.

**Field roles (do not duplicate content across fields):**
- `updatedDescription` — full ticket body (scope, context, constraints). Stored on the ticket.
- `acceptanceCriteria` — checklist only. Stored under `## Acceptance criteria` on the ticket.
- `summary` — short activity note for the comment thread (1–3 sentences). Do not paste the full spec, analysis tables, or acceptance checklist here when `updatedDescription` is set.

## Coppice platform rules — implementer completion (required)

- On `status: "done"`, workflow gates move the ticket to In Review and start the reviewer. Set `assignTo` to a Tech Lead or reviewer key from `board_agents` (e.g. `tech_lead`, `reviewer`); if you omit it, Coppice picks the oldest enabled one.
- Outside that handoff, only PM agents use `assignTo` (when refining backlog tickets). Use agent keys that exist on the board (e.g. `backend_engineer`, `research`).
