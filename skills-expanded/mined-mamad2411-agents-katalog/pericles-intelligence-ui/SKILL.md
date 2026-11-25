---
name: pericles-intelligence-ui
version: 2026.05.0
description: >
  How to build the Intelligence surface — the events feed, event/incident detail, the
  Insights chat with document viewer, and generated briefs/memos. Use this WHENEVER you
  build or change the events feed, an event sub-page, the Insights conversational view,
  or brief/memo generation. Encodes the feed, the chat + document viewer, persona
  framing, and that consequential outputs (e.g. sending a memo) go through Execution
  Nodes.
doctrine_refs: [§3, §6; Intelligence PRD]
depends_on: [pericles-frontend-foundations, pericles-persona-layer, pericles-copilot-ui, pericles-execution-node]
last_reconciled: 2026-05-28
---

# Pericles Intelligence UI (build skill)

Intelligence is where the customer reads and reasons about risk: the live events feed,
the detail behind each event/incident, an **Insights** conversational view with a
document viewer, and generated **briefs/memos**. `components/monitoring` is the existing
seed.

## When to use this skill

Building/changing the events feed, event/incident detail pages, the Insights chat +
document viewer, or brief/memo generation.

## Surfaces

- **Events feed** — tenant-scoped, live over socket.io, filterable; shares the feed
  model with Atlas (`pericles-atlas-ui`). Click → event/incident sub-page.
- **Event / incident sub-page** — the validated record + `RiskAssessment` (severity/
  confidence, financial impact subject to persona data scope), lineage of how it was
  detected/validated (`pericles-observability`).
- **Insights chat** — conversational Q&A over the customer's risk picture and
  Organizational Memory (`pericles-org-memory`), with a **document viewer** for cited
  sources. This is the read/reason surface; the cross-pipeline Co-Pilot
  (`pericles-copilot-ui`) is the action-capable one.
- **Briefs / memos** — generated summaries (e.g. CFO-ready impact memo). Generation is
  fine to render inline; **sending/distributing** a memo is a consequential action that
  goes through an Execution Node (`pericles-execution-node`), never an auto-send.

## Persona framing

Output shape and data scope follow the Persona Layer (`pericles-persona-layer`): a
Business Stakeholder sees an executive summary; a Risk Manager sees full financial
impact. One underlying answer, persona-rendered — no forked views.

## Untrusted content

Insights renders customer documents and feed content — treat as untrusted in any
LLM-backed feature (boundary-marked, schema-validated; `pericles-prompts`).

## What this forbids

Auto-sending/distributing a brief or memo without an Execution Node + approval gate;
showing financial impact to a persona outside its data scope; client-trusted
`organization_id`; per-persona forked pages; rendering cited documents as trusted
instructions.

## Verification

Feed is tenant-scoped and live; event detail shows assessment + lineage; Insights cites
sources in the document viewer; persona data scope enforced; memo distribution routes
through an Execution Node.

## Existing standards (read alongside)

`.cursor/rules/001-application/{005-pericles-insights,007-pericles-events}-*`;
Intelligence PRD (Notion); `frontend/src/components/monitoring`.

## Open questions

- Whether Insights chat is the same surface as Co-Pilot or a separate read-only view —
  reconcile with `pericles-copilot-ui`.
- Brief/memo template ownership (Industry Pack vs per-tenant) — confirm.

## Changelog

- 2026.05.0 — Initial draft from the Intelligence PRD; feed/detail/Insights/memo, with
  memo distribution via Execution Node.
