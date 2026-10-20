# Security by Design Feature Checklist

## Summary

**One-sentence:** STRIDE-lite per-feature threat-model checklist that runs during a normal design review and produces a 1-page feature-stm.md attached to the design doc.

**One-paragraph:** STRIDE-lite per-feature threat-model checklist that runs during a normal design review and produces a 1-page feature-stm.md attached to the design doc. The methodology pins the discipline that turns folklore into a reviewable, owned, version-controlled operating artefact: rule-bound output contract, evidence anchors, named owner, published review cadence. Outputs of the wrong shape are rejected at review; outputs without evidence are demoted to hypotheses; outputs without owners are tagged stale.

## Applies If (ALL must hold)

- A team is producing checklist for the topic 'Security by Design Feature Checklist'.
- Output is reviewed by a named human on a published cadence.
- Inputs and constraints fit the rules in `content/01-core-rules.xml`.

## Skip If (ANY kills it)

- One-shot work with no recurrence — write a single doc, not a versioned artefact.
- Regulated context that mandates a different template — use the regulator's.
- No named owner is available — defer until ownership is resolved.

**Ефективно для:**

- Per-feature design reviews where a full STRIDE workshop is overkill.
- Features touching identity, data flow, persistence, external integration, or trust boundary.
- Architecture-review meetings that want a security artefact attached to every feature.
- Teams that already adopted STRIDE template and need a per-feature lite variant.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Versioned space for the artefact | Git repo / wiki with history | team |
| Named owner | Person + role | team / RACI |
| Trigger event | Event / threshold / schedule | operating cadence |
| Upstream methodologies in `Assumes Loaded` | Already routine for the role | team training |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `solo/dev/software-architect/architecture-decision-records` | Base ADR format the output extends. |
| `pro/dev/software-architect` | Role/operating context. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom / root-cause / fix | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `apply-checklist` | haiku | Per-item binary check against artefact. |
| `classify-decision` | sonnet | Mitigated / accepted / deferred / N-A judgment. |
| `escalate-stride-conflict` | opus | Cross-category interaction analysis. |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.md.j2` | Checklist with category headings + decision-per-prompt rows. |
| `templates/skeleton.md` | Checklist with category headings + decision-per-prompt rows. Generated from `templates/skeleton.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.md.j2` | Minimum viable filled-in instance. |
| `templates/_smoke-test.md` | Minimum viable filled-in instance. Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-security-by-design-feature-checklist.py` | Validate artefact against the JSON Schema in `content/02-output-contract.xml`. Stdlib-only. | CI on artefact change; pre-commit. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[architecture-decision-records]]
- [[stride-threat-model-template]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, cadence status) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
