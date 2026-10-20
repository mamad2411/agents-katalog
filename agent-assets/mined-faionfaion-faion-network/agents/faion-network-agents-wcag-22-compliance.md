# WCAG 2.2 Compliance

## Summary

**One-sentence:** Delta methodology covering the 9 new WCAG 2.2 success criteria (focus not obscured, dragging movements, target size 24×24, redundant entry, accessible authentication, etc.).

**One-paragraph:** WCAG 2.2 (October 2023) adds 9 new success criteria and removes 4.1.1 Parsing. Most teams miss the 5 new AA criteria: 2.4.11 Focus Not Obscured, 2.5.7 Dragging Movements, 2.5.8 Target Size (24×24 CSS px minimum), 3.3.7 Redundant Entry, and 3.3.8 Accessible Authentication. This methodology audits a product against the 2.2 delta and emits a 2.2-delta conformance record validated against the schema.

**Ефективно для:**

- Delta-only audit avoids re-running full 2.1 sweep.
- Per-SC tracking for the 9 new criteria.
- Target-size rule catches mobile-only regressions before launch.
- Accessible-authentication rule replaces cognitive function tests with alternatives.

## Applies If (ALL must hold)

- Existing WCAG 2.1 AA baseline; upgrading to 2.2.
- New components (drag, auth, multi-step forms) being designed or shipped.
- Acceptance criteria reference 2.2 SC numbers.
- Compliance preparation for ADA Title II / EAA / EN 301 549 update cycle.

## Skip If (ANY kills it)

- Greenfield project with no 2.1 baseline — start with `a11y-testing`.
- AT runtime testing — use `testing-with-assistive-technology`.
- VPAT-only paperwork — use `regulatory-compliance-2026`.
- XR / spatial — use `spatial-accessibility`, `vr-design-patterns`, `ar-design-patterns`.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Product / flows | URL list | product |
| WCAG 2.1 baseline | existing audit report | audit |
| Target conformance level | default AA | team policy |
| Component inventory | design system list | design |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| a11y-basics | Provides WCAG POUR / conformance vocabulary used across the accessibility-specialist domain. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with sourced rationale + skip-this-methodology + run-the-checklist | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the artefact + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure (input / action / output / decision-gate) | 800 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs (preconditions, severity, modality) to a rule from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `triage-inputs` | haiku | Mechanical scrape from inputs. |
| `apply-rules` | sonnet | Per-rule judgement on inputs. |
| `synthesise-artefact` | sonnet | Aggregates rule outcomes into the final artefact. |

## Templates

| File | Purpose |
|------|---------|
| `templates/wcag-22-delta-record.json` | JSON delta record skeleton. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-wcag-22-compliance.py` | Validate the artefact against the JSON Schema in `content/02-output-contract.xml`. | After draft, before downstream consumer reads. |

## Related

- [[a11y-testing]]
- [[regulatory-compliance-2026]]
- [[ada-title-ii-compliance-2026]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip, choice of variant, and the verdict label.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/wcag-22-delta-record.json`

```json
{}
```
