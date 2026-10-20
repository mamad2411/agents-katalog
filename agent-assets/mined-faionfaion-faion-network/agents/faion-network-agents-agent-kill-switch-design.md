# Agent Kill-Switch Design

## Summary

**One-sentence:** Produces a runtime kill-switch spec for an agent: per-tenant + global + per-tool kill paths, latency budget <5s end-to-end, recovery / rollback path documented, both directions tested.

**One-paragraph:** How to design and test a runtime kill switch for an agent (per-tenant, global, per-tool). Required for production rollout but absent in most stacks. Output: kill-switch spec + test recipe (kill + recovery) + observability hooks + escalation runbook.

**Ефективно для:** agents exposed to non-internal users; agents with destructive tools (create / delete / pay); agents subject to safety review or regulatory scrutiny.

## Applies If (ALL must hold)

- You expose or operate the system to non-internal users (customers, paying or pilot)
- Failure of the safety control results in user-visible damage (cost, data, trust)
- Pre-prod verification of the control is feasible and budgeted
- Roll-forward and roll-back paths are both tested, not just documented

## Skip If (ANY kills it)

- Internal-only, dev-tier tools with no external blast radius
- Trivially reversible actions (DRAFT-only outputs, dry-run flags) where safety is implicit
- Cost of safety control > expected loss × probability over the next 90 days

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Agent deployment with traffic | service | eng |
| Feature-flag system or config store | vendor | platform |
| Observability hooks (kill-event topic) | OTel + queue | observability |
| On-call rota | PagerDuty / Opsgenie | on-call |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `[[agent-observability-stack-blueprint]]` | Hooks for kill-event signal |
| `[[agent-ga-readiness-checklist]]` | GA gate that requires kill-switch test |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules (r1-r5 plus the documented-skip rule) with rationale and source | ~550 |
| `content/02-output-contract.xml` | essential | JSON-schema output shape + valid/invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom/root-cause/fix | ~800 |
| `content/04-procedure.xml` | medium | 5-step procedure with input/action/output per step | ~900 |
| `content/05-examples.xml` | medium | worked end-to-end example | ~700 |
| `content/06-decision-tree.xml` | essential | decision tree gating whether this methodology applies | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Author kill-switch spec | sonnet | Pattern application. |
| Tune latency | opus | System-design trade-off. |
| Author recovery runbook | sonnet | Composition. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-agent-kill-switch-design.py` | Validates an output document against the 02-output-contract schema. | Pre-commit and CI before merge. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- parent skill: `geek/ai/ai-agents/`
- `[[agent-ga-readiness-checklist]]`
- `[[agent-customer-zero-pilot-protocol]]`
- `[[agent-observability-stack-blueprint]]`

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters whether agent-kill-switch-design applies: root question — "Is the agent exposed to non-internal users with non-trivial blast radius?". Branches lead to a specific core rule (e.g., `rule:r1`) when the methodology fits, or to a `skip:` conclusion when it does not.
