# AI Feature UX Pattern Library

## Summary

**One-sentence:** Catalogue of UX patterns specific to AI features — confidence indicators, refusal surfaces, edit-the-output, "why did the model say this" trails, undo gates — selectable per feature with a one-page picker.

**One-paragraph:** Generic component libraries (buttons, modals, lists) don't cover the AI-specific UX choices that make or break user trust: how to surface confidence, what to render when the model refuses, how to give users editable hand-off, how to explain a prediction, how to undo an AI-generated action. This methodology catalogues seven core patterns, prescribes a per-feature picker (which patterns are mandatory, which are optional), and outputs one UX spec attached to the feature brief that designers can hand to engineering.

**Ефективно для:** Команд, де AI-фічі ходять у production з generic UX («Sure, here's your output») і потім скаржаться, що користувачі їм не довіряють; pattern library дає чек-лист — і Designer закриває гепи до релізу, не після першого incident.

## Applies If (ALL must hold)

- AI feature is user-facing (not a backend pipeline).
- A design owner exists for the feature.
- The feature has at least one of: model refusal, confidence variability, irreversible action.
- A component library / design system exists to extend.
- Feature is past pre-MVP — UX iteration is on the critical path.

## Skip If (ANY kills it)

- Backend-only AI feature (no UI surface).
- Greenfield with no design system — establish one first.
- Single-user prototype where UX is intentionally rough.
- Feature is read-only deterministic (no refusal / no action / no confidence).

## Prerequisites

| Artifact | Format | Source |
|---|---|---|
| Feature brief | Markdown | PM |
| Design system | Figma + tokens | Design |
| Hallucination policy | from `ai-feature-brief-extension-pack` | PM |
| Named design owner | handle | Design lead |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `geek/ai/ai-agents/ai-feature-brief-extension-pack/AGENTS.md` | Hallucination policy section anchors which refusal surfaces are needed. |
| `geek/ai/ai-agents/ai-governance-compliance/AGENTS.md` | Compliance dictates which explanation patterns are mandatory. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 4 rules: per-feature picker, mandatory subset, confidence shown, undo for irreversible | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema for the UX spec | ~700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns (no confidence, hidden refusal, no undo, etc.) | ~900 |
| `content/04-procedure.xml` | medium | 5-step procedure: list patterns → classify feature → mandate subset → spec → review | ~900 |
| `content/05-examples.xml` | medium | Worked example: UX spec for a content-suggestion feature | ~900 |
| `content/06-decision-tree.xml` | essential | Tree: surface? → refusal? → irreversible? → mandatory pattern set | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `classify_feature_surfaces` | haiku | Structured tagging of UI surfaces. |
| `pick_patterns` | sonnet | Per-feature judgment from the catalogue. |
| `compose_ux_spec` | sonnet | Final composition. |
| `design_review` | opus | High-stakes when irreversible actions are involved. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema for the UX spec. |
| `templates/output.example.json` | Filled example. |
| `templates/pattern-picker.md.j2` | One-page picker template (seven core patterns × mandatory/optional). |
| `templates/pattern-picker.md` | One-page picker template (seven core patterns × mandatory/optional). Generated from `templates/pattern-picker.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-output.py` | Validate the UX spec. | After draft, before design review. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- parent skill: `geek/ai/ai-agents/`
- peer: [[ai-feature-brief-extension-pack]] — brief feeds policy into UX choices.
- peer: [[ai-governance-compliance]] — explainability requirements.

## Decision tree

See `content/06-decision-tree.xml`. Asks: (1) does the feature have user-facing UI surfaces? (2) is model refusal possible? (3) is the action irreversible? Leaves point to the mandatory pattern subset (confidence + refusal-surface + undo gate) plus optional adds.
