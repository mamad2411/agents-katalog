# Cloud Architecture

## Summary

**One-sentence:** Well-Architected-Framework-bound cloud-native design pass — six pillars (operational excellence, security, reliability, performance, cost, sustainability), provider selection, landing zone, VPC, zero-trust, FinOps, DR — emitting an ADR + IaC scaffold before any cloud resource is created.

**One-paragraph:** Well-Architected-Framework-bound cloud-native design pass — six pillars (operational excellence, security, reliability, performance, cost, sustainability), provider selection, landing zone, VPC, zero-trust, FinOps, DR — emitting an ADR + IaC scaffold before any cloud resource is created. The methodology pins the discipline that turns folklore into a reviewable, owned, version-controlled operating artefact: rule-bound output contract, evidence anchors, named owner, published review cadence. Outputs of the wrong shape are rejected at review; outputs without evidence are demoted to hypotheses; outputs without owners are tagged stale.

## Applies If (ALL must hold)

- A team is producing decision-record for the topic 'Cloud Architecture'.
- Output is reviewed by a named human on a published cadence.
- Inputs and constraints fit the rules in `content/01-core-rules.xml`.

## Skip If (ANY kills it)

- One-shot work with no recurrence — write a single doc, not a versioned artefact.
- Regulated context that mandates a different template — use the regulator's.
- No named owner is available — defer until ownership is resolved.

**Ефективно для:**

- Greenfield cloud-native design or lift-and-shift migration with explicit RTO/RPO targets.
- Provider selection (AWS / Azure / GCP) under organisational + technical constraints.
- Landing-zone bootstrap: accounts, VPC CIDR, IAM, logging, baseline guardrails.
- FinOps + DR planning (Backup-Restore → Pilot-Light → Warm-Standby → Active-Active).
- Six-pillar Well-Architected review before a major release or refresh.

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
| `content/01-core-rules.xml` | essential | 7 testable rules with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom / root-cause / fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure to apply the methodology end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-adr` | haiku | Template fill from header + section list. |
| `draft-rationale` | sonnet | Per-decision rationale + rejected alternatives. |
| `review-class-and-tradeoff` | opus | Cross-decision synthesis + reversibility judgment. |

## Templates

| File | Purpose |
|------|---------|
| `templates/adr-skeleton.md.j2` | ADR skeleton with status / decision_class / context / decision / alternatives-rejected / consequences / rollback / signers. |
| `templates/adr-skeleton.md` | ADR skeleton with status / decision_class / context / decision / alternatives-rejected / consequences / rollback / signers. Generated from `templates/adr-skeleton.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.md.j2` | Minimum viable filled-in ADR. |
| `templates/_smoke-test.md` | Minimum viable filled-in ADR. Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-cloud-architecture.py` | Validate artefact against the JSON Schema in `content/02-output-contract.xml`. Stdlib-only. | CI on artefact change; pre-commit. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[architecture-decision-records]]
- [[stride-threat-model-template]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, cadence status) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
