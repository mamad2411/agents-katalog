---
name: design-style-distiller
description: Use when you want to learn from design references without storing raw copyrighted assets in the skill repo, by extracting reusable style knowledge (layout rules, visual tokens, and transfer briefs) into structured style cards.
version: 0.1.0
---

# Design Style Distiller

Distill visual references into reusable, open-safe style knowledge.

## When to use
- Build long-term aesthetic memory from paper figures, slides, diagrams, UI screenshots, or PDFs.
- Convert "this looks good" into explicit and reusable design rules.
- Decide what can be open-sourced vs what must stay local/private.
- Prepare structured style inputs for `$research-plot-stylist`, `$matplotlib-base-style`, `$paper-illustration`, `$research-ppt-figure`, and `$web-frontend-aesthetic`.

## Core boundary
- Do not commit raw third-party reference assets into this skill repo.
- Commit only distilled artifacts: style cards, design tokens, and transfer briefs.
- Keep original files in a local private library outside git.

## Inputs
- Local reference images, PDFs, or screenshots (private by default).
- Target domain: `research_plot`, `paper_figure`, `diagram`, `slides`, `frontend`.
- Reuse goal: theme extraction, layout extraction, or full style card creation.
- Optional local registry: `design-references-local/index.yaml`.

## Workflow
1. Classify source privacy.
   Decide if the source is private-only or safe to keep in repo.
2. Analyze visual structure.
   Use the rubric in `references/extraction-rubric.md` to score layout, hierarchy, typography, color, shapes, annotation density, and overall tone.
3. Create style card.
   Use schema `references/style-card-schema.md` and template `assets/style_card_template.yaml`.
4. Derive transfer brief.
   Generate a compact, model-friendly prompt using `assets/transfer_brief_template.md`.
5. Enforce open-source boundary.
   Check against `references/open-source-boundary.md` before committing.
6. Register local outputs.
   If `design-references-local/index.yaml` exists, add distilled style cards and briefs there before promoting anything into git-tracked references.
7. Handoff to downstream skills.
   Feed style card + transfer brief into plotting/illustration/frontend skills.

## Recommended outputs
- Local private references (not in git): see `references/private-library-layout.md`
- Distilled style cards (safe): `references/style-cards/*.yaml`
- Transfer briefs (safe): `references/briefs/*.md`

## Scripts
- `scripts/init_style_card.sh <style-name> [output-dir]`
  Create a new style card from template with basic metadata.

## Quality bar
- Distilled artifacts are reusable across at least 2 tasks.
- Style card captures both constraints (`dos/donts`) and mood (`impression`).
- No raw copyrighted assets or near-replica vectors are committed.
- Transfer brief is compact, domain-specific, and executable by downstream skills.

## References
- `references/style-card-schema.md`
- `references/extraction-rubric.md`
- `references/open-source-boundary.md`
- `references/private-library-layout.md`
