# Agent Customer-Zero Pilot Protocol

## Summary

**One-sentence:** Produces a customer-zero pilot playbook: scope contract, success criteria with thresholds, kill switches, billing model, GA exit gate — for a single vertical agent.

**One-paragraph:** Customer-zero is the single highest-leverage moment for a vertical agent. Builders need a protocol covering pilot scope, success criteria, kill switches, billing, and exit-to-GA. No methodology covers this end-to-end today. This produces a 1-page playbook plus a 5-checkpoint checklist (week-1 scope, week-2 deploy, week-4 mid-pilot review, week-8 success-gate, week-12 GA exit or sunset).

**Ефективно для:** first paying customer for a new vertical agent; design partner programs; agencies running pilots for client agents.

## Applies If (ALL must hold)

- Executing a customer-zero pilot for a new vertical agent
- All inputs reachable (people, data, artefacts)
- Output consumed by a named downstream owner with a deadline
- Deviations from the protocol are logged with rationale

## Skip If (ANY kills it)

- Highly contextual one-shot work where playbook constrains the wrong axes
- Pre-discovery — playbook assumes the problem is named
- Teams already running a well-tuned variant — re-tooling friction outweighs upside

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Customer-zero contract / signed LOI | PDF | sales |
| Vertical agent v1 in pre-prod | deployed service | eng |
| Eval suite ≥30 in-domain trajectories | JSONL | eval owner |
| Kill-switch design | spec | `[[agent-kill-switch-design]]` |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `[[agent-kill-switch-design]]` | Safety control wired before launch |
| `[[agent-ga-readiness-checklist]]` | GA gate inputs |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale and source | ~550 |
| `content/02-output-contract.xml` | essential | JSON-schema output shape + valid/invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom/root-cause/fix | ~800 |
| `content/04-procedure.xml` | medium | 6-step procedure with input/action/output per step | ~900 |
| `content/06-decision-tree.xml` | essential | decision tree gating whether this methodology applies | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Author scope contract | sonnet | Template application. |
| Define numeric thresholds | opus | Cross-criterion reasoning. |
| Run mid-pilot review | opus | Traffic-light judgement. |

## Templates

| File | Purpose |
|------|---------|
| `templates/_smoke-test.md.j2` | Filled example for a customer-support pilot. |
| `templates/_smoke-test.md` | Filled example for a customer-support pilot. Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-agent-customer-zero-pilot-protocol.py` | Validates an output document against the 02-output-contract schema. | Pre-commit and CI before merge. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- parent skill: `geek/ai/ai-agents/`
- `[[agent-kill-switch-design]]`
- `[[agent-ga-readiness-checklist]]`
- `[[agent-eval-cost-budget-policy]]`

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters whether agent-customer-zero-pilot-protocol applies: root question — "Is this a customer-zero pilot for a vertical agent?". Branches lead to a specific core rule (e.g., `rule:r1`) when the methodology fits, or to a `skip:` conclusion when it does not.
