---
name: geometry-notebook-qc
description: Quality-check visualization-first geometry notebooks. Use when Codex needs to review geometry notebooks, artifacts, and helper changes for standalone teaching quality, visual relevance, executable correctness, artifact integrity, stale paths, and dependency fit.
---

# Geometry Notebook QC

## Purpose

Use this skill after authoring or revising a geometry notebook chapter. The goal is to catch weak standalone explanations, generic generated sameness, decorative visuals, missing artifacts, execution failures, stale paths, source-map gaps, and dependency/library mistakes.

Read `references/geometry-library-catalog.md` when evaluating whether a notebook uses the available stack appropriately.

## Chapter-First Rule

- Inspect the course `AGENTS.md`, assigned source map/span, changed notebook, helper changes, generated artifacts, and relevant scripts before judging the work.
- A canonical teaching notebook must read as a direct chapter-specific lesson, not as a generic script-generated template.
- Scripts may support indexing, auditing, validation, artifact helpers, and small reproducible assets.
- Scripts must not mass-populate teaching notebooks with repeated generic markdown/code cells.
- Bootstrap scripts may create folder skeletons only unless the user explicitly asked for a rough bootstrap draft.
- Copyright safeguards remain required: no copied textbook prose, long exercise text, screenshots, page crops, figures, or page layouts.

## Review Workflow

1. Check source grounding:
   - source span or source map is present
   - chapter-specific terms, definitions, constructions, examples, and proof moves appear
   - the reader can learn the chapter without opening the textbook
2. Check standalone delivery:
   - motivation, translation guide, examples, pitfalls, checks, labs, and takeaways are present where appropriate
   - useful existing work was preserved during improvement passes
   - prose near each visual explains what to inspect
3. Check visualization quality:
   - visuals are concept-specific, not decorative or quota-filling
   - proof-heavy sections use dependency views, diagrams, symbolic experiments, finite models, deformation/limit views, counterexamples, or invariant trackers when useful
   - labels, scale, aspect ratio, color, legends, and annotations make the geometry inspectable
   - major concepts with no visual have a documented reason
4. Check library fit:
   - notebook includes chapter-specific library routing or clear library rationale
   - Matplotlib-only treatment is flagged when the chapter calls for 3D mesh/surface, topology/TDA, projective/CV, geometric algebra, manifold/statistical, transport, or GIS tools
   - optional/external tools are documented rather than silently imported
5. Check artifacts:
   - outputs live under the matching book-local `artifacts/` subtree
   - filenames name the concept, not the renderer
   - artifacts are displayed inline or linked near the relevant prose
   - paths are current, relative/book-local, and not stale root paths
   - artifacts have nonzero size and appropriate formats: PNG/SVG/HTML plus JSON/CSV checks when useful
6. Check computation:
   - final cells assert core symbolic, numeric, or geometric invariants
   - JSON/CSV summaries record reproducible checks when useful
   - notebook executes with the narrowest relevant course validation command

## Anti-Generic Audit Guidance

When several chapter notebooks are in scope, check for:

- repeated markdown shingles across unrelated chapters
- repeated code-cell fingerprints or identical setup-to-display blocks
- identical notebook outlines with only chapter names changed
- repeated artifact names such as `concept-dependency-map.png` without chapter-specific companions
- missing chapter-specific terms from headings, markdown, checks, and artifact names
- missing library-routing notes
- visuals with no nearby explanatory markdown
- notebooks driven primarily by one monolithic `generate_*` or `author_*` script
- shared helper calls that hide the chapter pedagogy, such as one `create_chapter_visuals(...)` cell standing in for the lesson

Treat these as warnings first, then fail the work when they make the notebook generic, decorative, or not standalone.

## Command Guidance

Use the commands listed in each course `AGENTS.md`. For quick checks, prefer:

- `uv run python -m compileall -q <course>/utils <course>/scripts`
- course notebook audit script
- course visual audit script when present
- limited `validate_*_course.py` execution before full validation
- `git diff --check`

Run full notebook validation when shared utilities, setup cells, artifact helpers, or many notebooks changed.

## Final QC Report

Return a compact report with:

- `pass/fail summary`
- `standalone teaching issues`
- `visualization issues`
- `artifact issues`
- `execution issues`
- `generic-generation warnings`
- `recommended fixes`

Lead with actionable findings. For each issue, include the file path, tight location when possible, why it weakens the notebook, and the concrete fix. If there are no findings, state that and list checks not run.
