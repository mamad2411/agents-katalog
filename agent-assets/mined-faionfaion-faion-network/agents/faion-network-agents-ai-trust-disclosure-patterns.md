# AI Trust Disclosure Patterns

## Summary

**One-sentence:** Checklist for shipping copilot / chat / inline-AI features without trust collapse: source citation, uncertainty surface, model identity, opt-out, regulatory disclosure.

**One-paragraph:** Shipping AI features (copilot, chat, inline) without explicit trust patterns triggers user backlash and regulatory exposure (EU AI Act Article 50 mandates AI-generated content disclosure from 2026). This methodology codifies five disclosure axes — model identity, uncertainty surface, source citation, opt-out path, error reporting — into a per-feature checklist. Output is a YAML/JSON artefact validated by CI that pre-launch reviewers (legal, design, eng) sign off against.

**Ефективно для:**

- Будь-який consumer-facing AI feature, що шипиться в ЄС після Feb 2026 — Art. 50 mandate.
- Copilot / inline-suggestion UX: source citation + uncertainty bar усуває trust collapse.
- B2B chat-боти, які отримують user complaints на 'AI lies to me' — disclosure pattern зменшує churn.
- Команди, які мають design + legal review перед launch — checklist синхронізує обидві сторони.

## Applies If (ALL must hold)

- Feature is user-facing AI (chat, suggestions, summarization, generation).
- Users are end-consumers or external (not internal-only ML tooling).
- Product ships in jurisdictions with AI-disclosure regulation (EU, NY local laws, etc.) OR brand cares about trust.

## Skip If (ANY kills it)

- Internal-only ML pipeline with no UI surface.
- AI is invisible plumbing (ranking, fraud-detection) with no per-decision user-visible output.
- Feature is in private alpha with &lt;50 friend-and-family users (apply at beta gate instead).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Feature spec | Markdown | PM |
| UX wireframes | Figma / PNG | Design |
| Jurisdiction map | table of markets + regulations | Legal |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| none | This methodology is self-contained; no upstream artefact required. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: model-identity-visible, uncertainty-signal-required, source-citation-on-claim, opt-out-one-click, error-report-path | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for checklist + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `map-axes-to-ui` | sonnet | Visual scan + design judgment. |
| `draft-confidence-bands` | sonnet | Picks band thresholds from distribution. |
| `legal-signoff-prep` | haiku | Mechanical doc generation. |

## Templates

| File | Purpose |
|------|---------|
| `templates/confidence-band-spec.md.j2` | Confidence-band-to-UI mapping spec template |
| `templates/confidence-band-spec.md` | Confidence-band-to-UI mapping spec template Generated from `templates/confidence-band-spec.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/opt-out-ux-pattern.md.j2` | Reference opt-out UX pattern (settings + per-surface toggle) |
| `templates/opt-out-ux-pattern.md` | Reference opt-out UX pattern (settings + per-surface toggle) Generated from `templates/opt-out-ux-pattern.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-trust-disclosure-patterns.py` | Validate the checklist artefact against the schema | CI on each artefact change; pre-commit |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[ai-usage-policy-team]]
- [[ai-feature-eval-set-design]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, eval scores, stakes, noise ratio, etc.) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
