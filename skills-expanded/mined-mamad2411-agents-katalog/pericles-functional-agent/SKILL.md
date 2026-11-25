---
name: pericles-functional-agent
version: 2026.10.0
description: >
  How to build a Functional Agent/Skill and declare its pipeline position. Use this
  WHENEVER you create or modify a Mastra agent (Monitoring, Validation, Impact
  Assessment, Summarization, or a new one) or set a Skill's
  data_access.pattern. Encodes the §4 pre_validation / post_validation /
  cross_pipeline rules, the audited gateway path, and how the four design-level agents map to
  those positions. Misclassifying pipeline position is a doctrine violation.
doctrine_refs: [§3, §4; Agent Library]
depends_on: [pericles-doctrine, pericles-skill-authoring, pericles-mastra-tool]
last_reconciled: 2026-10-09
---

# Pericles Functional Agent (build skill)

A Functional Agent does pipeline work — establishing truth or acting on it. In the
codebase it's a Mastra `Agent` (`@mastra/core/agent`) composing tools + scorers (see
`backend/src/mastra/agents/monitoring-agent.ts`). Every Functional Skill MUST declare
its **pipeline position** (`data_access.pattern`), because that determines what data it
may touch and prevents cost, consistency, and auditability failures (§4).

## When to use this skill

Building/modifying any of the four agents or a new Functional Agent; setting or
reviewing a Skill's `data_access.pattern`; deciding whether a Skill may compose
Topical/Regional/Industry Skills.

## The three pipeline positions (§4)

- **`pre_validation`** — establishes the truth. MAY compose Topical/Regional/Industry
  Skills and query raw signal. Examples: **Monitoring** (detect across 10 categories),
  **Validation** (multi-source confirmation that must reach sources Monitoring did not).
- **`post_validation`** — acts on the established truth. Consumes **pipeline inputs
  only** (validated Events/Incidents); **never re-queries Topicals**. Examples:
  **Impact Assessment** (financial impact from ERP/SAP on validated events),
  **Summarization** (event summaries/updates).
- **`cross_pipeline`** — spans positions. Consumes pipeline inputs by default; composes
  a Topical/Regional/Industry Skill only by exception, via the **audited gateway path**
  (`gateway_path: true`, logged with reasons). Example: the **Co-Pilot / Orchestrator**
  surface that routes requests and occasionally needs fresh signal.

## Mapping the four agents (from .claude/rules/03-agents.md)

Of these four, only Monitoring is implemented today; the other three are design positions.
(The Mastra index also registers `eventQaAgent`, a per-event Q&A agent that is not one of
the four.) See the implementation status note in `.claude/rules/03-agents.md`.

| Agent | Position | Why |
|---|---|---|
| Monitoring | `pre_validation` | detects/deduplicates raw events; composes the 13 tools |
| Validation (PoC) | `pre_validation` | must reach sources Monitoring didn't — proves truth |
| Impact Assessment | `post_validation` | financial impact on validated events via ERP/SAP |
| Summarization | `post_validation` | summaries/updates over validated truth |

## The audited gateway path

When a `cross_pipeline` Skill genuinely needs fresh signal (not the validated record),
it does NOT call a Topical Skill directly. It goes through the gateway path, which:
sets `gateway_path: true` in the manifest, logs `gateway_path_used: true` with the
reason on the invocation, and surfaces on the Gateway-path dashboard
(`pericles-observability`). This keeps "act on the one defensible truth" intact while
allowing rare, audited exceptions.

## Supervisor vs executor (§3 boundary)

A Functional Agent is an LLM **supervisor**: it reasons and **proposes**. It must not
commit a consequential action (notification, freight, outreach, customer message,
audit record) from its own reasoning — that flows to a deterministic Execution Node
(`pericles-execution-node`). Notifications are proposed by the owning agent or a
deterministic trigger; the NotificationHandler commits (`pericles-notifications`).

## Build notes from the codebase

- Use `Agent` from `@mastra/core/agent`, composing tools (`../tools/index.js`) and
  scorers (`../scorers/...`).
- Agents are currently **stateless** by design (Memory is disabled — see the note in
  `monitoring-agent.ts` about the OpenAI Responses API `item_reference` bug). Don't
  rely on agent memory until that's resolved; pass needed context explicitly.
- Establish org context first (`erpContextTool`) and validate `organization_id`
  (`pericles-tenant-isolation`).

## What this forbids

A Functional Skill without `data_access.pattern`; a `post_validation` agent re-querying
Topicals (re-fetching raw signal at action time); a `cross_pipeline` agent composing
Topicals without the gateway path; an agent committing a consequential action without
an Execution Node; classifying Validation as `post_validation` (it must reach beyond
Monitoring — `pericles-evals-scorers`).

## Verification

`data_access.pattern` is declared and the registry accepts it
(`pericles-skill-registry`); dependencies are consistent with the pattern; consequential
actions route through Execution Nodes; Validation's eval suite includes confirm/reject
divergence cases; `organization_id` validated.

## Existing standards (read alongside)

Doctrine §4 + Agent Library (Notion); `.claude/rules/03-agents.md`;
`.cursor/rules/001-application/001-agents/*` (monitoring, validation, impact-assessment,
summarization, orchestrator).

## Open questions

- The Co-Pilot (`pericles-copilot-ui`) is the intended canonical `cross_pipeline` consumer.
  Neither the Co-Pilot nor the Orchestrator (`.cursor` rule 006) is implemented in
  `backend/src` yet; confirm the gateway path UX and the router role as they land.
- When agent Memory is re-enabled, how statefulness interacts with per-invocation
  lineage.

## Changelog

- 2026.10.0 — Removed the deprecated Controller agent; mapped the four design-level agents.

- 2026.05.0 — Initial draft. §4 positions mapped to the five real agents; gateway path
  and supervisor/executor boundary grounded in the codebase.
