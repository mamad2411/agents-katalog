---
name: pericles-copilot-ui
version: 2026.05.0
description: >
  How to build the persistent Co-Pilot — the cross-pipeline assistant present across
  Pericles. Use this WHENEVER you build or change the Co-Pilot surface, its streaming,
  its action proposals, or the gateway-path affordance. Encodes the persistent surface,
  persona framing, the §4 cross_pipeline + audited gateway-path UX, and the §3 rule that
  Co-Pilot proposes while Execution Nodes commit.
doctrine_refs: [§3, §4, §6]
depends_on: [pericles-frontend-foundations, pericles-functional-agent, pericles-execution-node, pericles-persona-layer]
last_reconciled: 2026-05-28
---

# Pericles Co-Pilot UI (build skill)

The Co-Pilot is the persistent assistant across every surface — ask about the risk
picture, get a Plan drafted, kick off an assessment. It is the canonical
**`cross_pipeline`** consumer (`pericles-functional-agent`): it works from validated
pipeline inputs by default and reaches fresh signal only via the audited gateway path.

## When to use this skill

Building/changing the Co-Pilot panel, its streaming responses, its action proposals, or
the gateway-path affordance.

## Surface

- **Persistent** — available across Atlas, Intelligence, Plans, Admin (a docked panel),
  carrying context for the active surface and persona.
- **Streaming** — responses stream over socket.io; show tool/skill activity so the user
  sees what's happening.
- **Persona-framed** — shape, vocabulary, and data scope from the Persona Layer
  (`pericles-persona-layer`); not forked per persona.

## The gateway-path affordance (§4 step 5)

When the Co-Pilot needs **fresh signal** (not the validated record) it goes through the
**audited gateway path** — and the UI makes that visible: indicate that it's fetching
fresh data, why, and that the access is logged (`gateway_path_used`,
`pericles-observability`). This keeps the "act on the one defensible truth" model honest
and the rare exception transparent to the user.

## Propose, don't commit (§3)

The Co-Pilot **proposes** consequential actions (send a notification, activate a Plan,
contact a supplier) as structured proposals; it never commits them itself. The user
confirms, and the commit runs through a deterministic **Execution Node**
(`pericles-execution-node`) with its approval gate. Render the proposal + a clear
confirm step; show the trial/run distinction where relevant.

## What this forbids

Co-Pilot committing a consequential action directly (must route to an Execution Node +
confirm); reaching fresh signal without the gateway path + its visible affordance;
per-persona forked Co-Pilots; trusting a client `organization_id`; rendering
model/tool output as trusted instructions (`pericles-prompts`).

## Verification

The Co-Pilot is persistent and persona-framed; fresh-signal use goes through the gateway
path and is surfaced + logged; consequential actions are proposals confirmed by the user
and committed by an Execution Node; streaming shows activity.

## Existing standards (read alongside)

Doctrine §3/§4/§6; `.cursor/rules/001-application/008-pericles-user-personas-*`;
`pericles-functional-agent`, `pericles-execution-node`.

## Open questions

- Whether Co-Pilot and the Intelligence "Insights" chat share one surface or are
  distinct (read-only vs action-capable) — reconcile with `pericles-intelligence-ui`.
- The exact gateway-path UX (inline banner vs explicit confirm) — design with the
  platform team.

## Changelog

- 2026.05.0 — Initial draft; cross_pipeline + gateway-path UX and the propose/commit
  boundary grounded in §3/§4.
