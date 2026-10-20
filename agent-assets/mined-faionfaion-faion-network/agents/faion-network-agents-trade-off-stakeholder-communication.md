# Trade-off Stakeholder Communication

## Summary

**One-sentence:** Generates a stakeholder-tailored trade-off briefing that preserves the key risk for every audience (exec, PM, engineer, ops) and writes the ADR Consequences section.

**One-paragraph:** Architecture trade-offs must be communicated differently to executives, product managers, engineers, and operations — but the key risk must survive every translation. This methodology emits four artefacts from one trade-off: an exec-summary (≤120 words, lists the gain + the survivable downside), a PM-brief (impact on roadmap + dependencies), an engineer-note (the chosen option's mechanics + what we sacrificed), and an ops-runbook-delta (what changes in oncall). All four MUST converge on the same risk paragraph — divergence is the bug.

**Ефективно для:**

- Solo architect presenting a Type-1 (irreversible) decision to non-technical founders before commit.
- Generating the ADR Consequences section from a decision matrix or ATAM scorecard.
- Post-mortem of a decision where the trade-off materialised — communicating what we knew vs what happened.
- Briefing a junior engineer on why the simpler option was rejected.

## Applies If (ALL must hold)

- Decision affects ≥2 stakeholder roles (not just an internal refactor).
- Decision is Type-1 (hard/expensive to reverse) OR involves a multi-month commitment.
- An ADR or decision record will be created as the durable artefact.
- Stakeholders have been identified by role (not generic personas).

## Skip If (ANY kills it)

- Type-2 reversible small-scope decision — a 3-line ADR comment is enough; full briefing is noise.
- Stakeholder roles not yet identified — the agent will invent personas and the briefing binds nobody.
- Pure code-style debate (tabs vs spaces) — not an architecture trade-off.
- Solo project with no external stakeholders — write the engineer-note only.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Decision record (options + criteria + chosen) | markdown / table | architect's draft ADR |
| Stakeholder map | role → name → primary concern | from PM or project lead |
| Quality-attribute scorecard | option × attribute matrix | trade-off-analysis methodology |
| Reversibility classification | Type-1 / Type-2 + cost-to-reverse | architect |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[architecture-decision-records]] | Defines the ADR shell this Consequences section drops into. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules (risk preservation, role-fit, single-source-of-truth, ≤120-word exec, no-omission gate) | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for the 4-artefact bundle + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: risk-laundering, persona-drift, single-author-no-review, hidden-trade-off | 700 |
| `content/04-procedure.xml` | essential | 5-step procedure (extract risk → draft per-role → cross-check convergence → ADR insert → review) | 700 |
| `content/05-examples.xml` | essential | Worked example: monolith → microservices ADR briefing for 4 roles | 600 |
| `content/06-decision-tree.xml` | essential | Routes by reversibility + stakeholder count + risk severity | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `trade_off_stakeholder_communication_extract_risk` | sonnet | Cross-input synthesis to compress the survivable downside. |
| `trade_off_stakeholder_communication_draft_per_role` | sonnet | Role-tailored prose; mechanical but judgement-heavy. |
| `trade_off_stakeholder_communication_convergence_check` | opus | Reads all 4 drafts and verifies the same risk paragraph survives. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema (draft-07) for the 4-artefact briefing bundle |
| `templates/briefing-bundle.md.j2` | Markdown skeleton with exec/PM/engineer/ops sections + the shared risk paragraph |
| `templates/briefing-bundle.md` | Markdown skeleton with exec/PM/engineer/ops sections + the shared risk paragraph Generated from `templates/briefing-bundle.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/adr-consequences.md.j2` | Drop-in Consequences block for the parent ADR |
| `templates/adr-consequences.md` | Drop-in Consequences block for the parent ADR Generated from `templates/adr-consequences.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.json` | Minimum viable filled-in bundle for validator round-trip |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-trade-off-stakeholder-communication.py` | Validate briefing bundle against schema + check risk convergence | Pre-commit; CI on each ADR change |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[architecture-decision-records]]
- [[trade-off-technical-debt]]
- [[quality-attributes-analysis]]

## Decision tree

See `content/06-decision-tree.xml`. The tree gates on (a) reversibility — Type-2 short-circuits to engineer-note-only, (b) stakeholder count — <2 roles skips full bundle, and (c) risk severity — high-severity decisions force the convergence-check rule. Every leaf references a rule in `01-core-rules.xml`.
