---
name: human-approval-gate
description: The core gate protocol every agent must follow — how to recognize decisions that require human approval, how to route through the human-approval gate (status `Blocked` + metadata `gate=human-approval`), and how to handle gate violations. Attach to every agent; consult before starting any issue and whenever a decision surfaces mid-task.
---

# Human Approval Gate

The most important process skill in the factory, attached to every agent. Multica has no built-in approval feature — this protocol *is* the gate. Read before starting any issue.

## The approval matcher (used everywhere below)

A member-authored comment starting `APPROVED` (case-insensitive; `APPROVED: <name>` preferred, a bare `APPROVED` counts — the author is the signature) is the approval artifact. `author_type` must be `member` — an agent comment never counts, and cannot be faked. No agent ever self-approves; an agent may only *record* an approval a human already gave (bookkeeping: set `adr_approved=<name from the comment, or its author>`, remove `gate`, comment citing it — the only case an agent touches the `gate` key). When in doubt whether something is gated, treat it as gated — one unnecessary approval costs minutes; one bad unreviewed decision costs weeks.

## What's gated vs. self-triaged

**Gated** (needs an ADR + human approval): introducing/removing a service, database, queue, cache, or third-party dependency with system-wide reach; data-model/schema design for new domains or breaking migrations; API contracts exposed to clients/partners; auth, authorization, session, payment, or PII design; framework/hosting/infra choice for a new component; cross-cutting patterns (event flows, caching, multi-tenancy).

**Not gated — self-triage** (routine, proceed with `no_adr_needed="<one-line justification>"`): bug fixes within existing patterns, copy/UI tweaks, endpoints/screens/sections following an established pattern, contract-free refactors.

**Self-triage is the default and anyone may do it — but do it, don't just decide it.** The agent assigned to the work triages the issue itself: if it clearly matches the not-gated list, **actually set** `no_adr_needed` on the issue with the justification and comment it, then proceed immediately — no architecture round-trip, no human confirmation. Route to architecture only when the change plausibly touches the gated list or you're genuinely unsure. Reasoning about the triage internally and then skipping the metadata write is not self-triage, it's a skipped gate check with extra steps: **an issue with no `gate`/`adr_approved`/`no_adr_needed` metadata at hand-off is presumptively a skipped check**, not a routine pass, regardless of what actually happened in the work.

## Deciding-agent protocol (system-architect, tech-lead-*) — for genuinely gated decisions

1. Write an ADR as an issue comment (`adr-writing` skill: Context / Options ≥2 / Decision / Consequences / Rollback).
2. Set `needs_adr=true`, then `gate=human-approval`, then move to `Blocked`.
3. Comment tagging human approvers: what's being decided, recommended option, what you need.
4. **STOP.** Never self-approve or touch the `gate` key again except the bookkeeping above.

## Downstream-agent gate check (developers, reviewers, QA) — do this before starting ANY issue

1. Carries `gate=human-approval`? No member approval comment (matcher above) → **frozen, do not touch it** regardless of status/assignment. Comment present → do the bookkeeping, then proceed.
2. Carries `adr_approved` or `no_adr_needed` (on itself or a linked design issue), or a member approval comment? Proceed.
3. Neither → self-triage (see above): routine → set `no_adr_needed`, comment, start work, don't wait. Plausibly gated or unsure → comment exactly:

> Gate check failed: this change may involve an architectural decision and has no approved ADR or `no_adr_needed` triage. Routing to architecture.

...then move to `In Progress`, set `phase=architecture`, and stop.

## Mid-task discovery

Implementation uncovers a gated decision (approved design doesn't survive contact with the code)? Stop coding immediately — never improvise architecture. Write it up as a new ADR section, set `gate=human-approval`, move to `Blocked`, wait.

## The human approver (app-UI only — humans never edit metadata)

- **Approve**: comment starting `APPROVED` → move to `Todo`.
- **Request changes**: `CHANGES REQUESTED: <what>` → back to `In Progress`.
- **Reject**: `REJECTED: <why>` → `Backlog` or `Cancelled`.

The comment is the approval artifact regardless of what status a human also happens to set — a gated issue with no member `APPROVED` comment stays frozen no matter what status it's in.

## Secondary human gates

| Gate | Who stops | Human action to proceed |
|---|---|---|
| Production deploy / release | devops-engineer, release-manager | Triggers/approves the deploy |
| Incident mitigation / rollback | incident-responder | Approves before execution |
| Destructive data migration | database-engineer | `APPROVED` on the migration plan |
| Scope change mid-task | any agent | product-manager + human re-scope |
| Urgent-priority security finding | security-reviewer | Human ack before merge |
| External communication / publishing | any agent | Human sends/publishes |

## Gate violations

A violation: changing status of / removing `gate` from an issue with no member approval on record; starting work without `adr_approved`/`no_adr_needed`/approval; merging an architectural change with no ADR. Any agent noticing one sets `gate_violation=true` and comments what it saw — legitimate self-triage (a routine change with `no_adr_needed` set before starting) is never a violation. program-tracker surfaces all `gate_violation=true` issues in every status report until resolved; auditors treat these as the highest-severity finding class.
