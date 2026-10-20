# BA Strategic Partnership

## Summary

**One-sentence:** Produces a stance review naming what BA-as-partner means in this engagement — decision rights, escalation paths, value contracts.

**One-paragraph:** Produces a stance review naming what BA-as-partner means in this engagement — decision rights, escalation paths, value contracts. This methodology codifies the rules, output contract, antipatterns, and decision tree so the artefact is reproducible across teams and audits.

**Ефективно для:**

- Engagement-renewal або new-engagement розмова з C-level, де BA треба позиціонувати як partner, а не requirements-gatherer.
- Multi-vendor програма, де BA accountability/consultancy boundary треба зафіксувати документально.
- Pivot у scope (наприклад, BA → product-strategy), де стара стanca застаріла.
- Внутрішній conflict між sponsor view (clerk-of-works) і BA view (thinking partner) — потрібен письмовий arbiter.

## Applies If (ALL must hold)

- BA is being inserted into a senior leadership conversation (board, exec, founder) where positioning matters.
- BA scope is contested — sponsor wants a 'requirements gatherer', BA wants strategic partnership.
- Engagement renewal where BA value contribution must be articulated.
- Multi-vendor program where BA accountability vs. consultancy boundary needs to be drawn.

## Skip If (ANY kills it)

- Tactical task-level work where strategic posture is irrelevant.
- Pure execution engagement where decision rights are already named elsewhere.
- BA role is junior / supporting — strategic stance does not apply.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Engagement brief / SOW | Markdown / contract | sponsor |
| Sponsor expectations note | Email / interview transcript | sponsor |
| BA self-assessed positioning | Markdown | BA |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[ba-planning]] | T1 approach informs partnership boundaries |
| [[stakeholder-analysis]] | stakeholder power map shapes partnership stance |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + skip-this-methodology guard | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid/forbidden examples | 800 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns: symptom / root-cause / fix | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with inputs/actions/outputs | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 700 |
| `content/06-decision-tree.xml` | essential | Decision tree on observable signals → conclusion refs to rule ids | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `gather-positioning-inputs` | haiku | Collect SOW, expectations, self-assessment. |
| `draft-stance-review` | opus | Synthesise narrative under conflicting signals. |
| `redline-and-iterate` | sonnet | Refine wording against sponsor feedback. |

## Templates

| File | Purpose |
|------|---------|
| `templates/stance-review.md.j2` | Stance review skeleton: what BA-as-partner means here, decision rights, escalation. |
| `templates/stance-review.md` | Stance review skeleton: what BA-as-partner means here, decision rights, escalation. Generated from `templates/stance-review.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/partnership-charter.md.j2` | One-page partnership charter signed by BA + sponsor. |
| `templates/partnership-charter.md` | One-page partnership charter signed by BA + sponsor. Generated from `templates/partnership-charter.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/stance-review-schema.json` | JSON Schema draft-07 for the ba-stance-reviewer agent output (axes, auto_block, kill_criterion). |
| `templates/ba-frame.sh` | Helper that frames a stakeholder ask into 3 questions + strawman outcome JSON. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[ba-planning]]
- [[stakeholder-analysis]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input fields, scores, thresholds) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
