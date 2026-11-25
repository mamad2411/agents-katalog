---
name: research-slide-deck-builder
description: Design and write reusable research slide decks. Use for advisor updates, lab talks, reading reports, proposals, conference talks, Slidev content, and slide structure.
allowed-tools: Read, Write, Edit, Bash, Glob
---

# Research Slide Deck Builder

## Purpose

Turn research content into a clear slide deck: story, slide order, page-level layout, figure placement, speaker notes, and the actual deck source.

This skill should use the external `progress-slides` template repo as the preferred implementation scaffold for progress, advisor, lab, and research-update decks:

```text
https://github.com/a-green-hand-jack/progress-slides.git
```

Do not duplicate that template inside this skill. Treat it as an external slides component or project template that should be cloned, inspected, installed, and edited in the user's project.

Use `presentation-dry-run` later when the user already has slides and wants timing, spoken transitions, rehearsal, or Q&A practice.

## When to Use

- The user needs slides for an advisor meeting, lab meeting, group update, paper reading report, conference talk, proposal, or defense segment.
- The user asks what the deck should look like, how many slides to make, what title page to use, or how to structure each page.
- The user asks to use `progress-slides` or a reusable slides template.
- A `project-init` project has a `slides/` component that needs content, setup, or maintenance.
- Research notes, figures, experiment reports, or project memory need to become a presentation.

## Template Policy

- Prefer `progress-slides` for research progress, advisor, lab, and project-update decks unless the user explicitly asks for another format.
- Keep template code upstream. Do not reimplement its CSS, components, theme, package config, or build pipeline in this skill.
- Before editing, inspect the cloned template's `README.md`, `package.json`, and existing slide source files because the external repo is the source of truth.
- If the repository is private or temporarily unavailable, record that blocker and still produce a deck outline or Markdown source that can be moved into the template later.
- If the user is inside a project-control-root layout, put or connect the template at `<ProjectName>/slides/` as an independent component repo.

## Installing or Connecting `progress-slides`

For a new slides component:

```bash
git clone https://github.com/a-green-hand-jack/progress-slides.git slides
cd slides
```

Then inspect the template:

```bash
ls
cat README.md
cat package.json
```

Install dependencies using the package manager indicated by the template lockfile or README. If there is no stronger local instruction, use:

```bash
npm install
```

Run the local preview command from `package.json`. Common Slidev-style commands are:

```bash
npm run dev
npx slidev
```

For an existing project:

- If `slides/` already exists and is the template repo, edit it in place.
- If `slides/` exists but is not the template, ask whether to migrate, add `progress-slides` as a new independent repo, or only write a compatible outline.
- If the template uses Git, preserve its history and use normal Git operations from inside `slides/`.

## Multi-Deck Component Model

A research project will usually need many decks over its lifetime. Treat `slides/` as a deck workspace, not as one permanent `slides.md`.

Recommended shape:

```text
slides/
├── slides.md                 # optional active/scratch deck or template index
├── decks/
│   ├── 2026-05-02-advisor-plan.md
│   ├── 2026-05-09-lab-update.md
│   ├── 2026-05-15-result-review.md
│   ├── neurips-rebuttal-risk-review.md
│   ├── assets/               # deck-local assets when Slidev root is decks/
│   ├── setup/
│   └── styles/
├── assets/
│   └── <shared-or-root-deck-assets>
├── templates/
├── snippets/
└── .agent/
    ├── slides-status.md      # component-level status
    ├── deck-index.md         # registry of decks
    └── decks/
        └── 2026-05-02-advisor-plan.md
```

Use this policy:

- For a real meeting, create a stable deck under `decks/<date>-<audience-or-purpose>-<slug>.md`.
- Use root `slides.md` only for the active default deck, a temporary working copy, or the template's sample/index deck.
- Do not overwrite an old meeting deck just because a new advisor/lab update starts.
- Keep reusable single-slide fragments in `snippets/`; keep full historical decks in `decks/`.
- Keep generated output in `dist/` or ignored export paths, not as the source of truth.
- For deck-specific assets, prefer assets under the active Slidev root. If the entry is `decks/<deck-id>.md`, use `decks/assets/<deck-id>/...` and reference it from the deck as `./assets/<deck-id>/...`. Use `assets/shared/...` only for assets proven to resolve from the active entry.
- If the template CLI only writes `slides.md`, initialize there first and then move or copy the finalized source into `decks/<deck-id>.md`, or use its `--out decks/<deck-id>.md` option when available.

Record deck memory:

- `slides/.agent/slides-status.md`: component status, active deck, recent decks, stale evidence, build/export policy
- `slides/.agent/deck-index.md`: one row per deck with id, path, audience, date, purpose, source evidence, validation status, and follow-up
- `slides/.agent/decks/<deck-id>.md`: optional per-deck notes for important decks, including deck contract, source evidence, visual validation, and unresolved risks

## Deck Design Principles

- One slide, one job. Every slide needs a sentence-level takeaway.
- Make the audience path explicit: context -> question -> evidence -> decision.
- For advisor updates, prioritize decisions, blockers, and evidence over polished storytelling.
- For research talks, prioritize motivation, problem framing, method intuition, and result interpretation.
- Figures are evidence, not decoration. Explain axes, setup, and takeaway.
- Keep slide titles specific. Avoid generic titles like "Results", "Method", or "Experiments".
- Put dense details in backup slides instead of shrinking text.
- Build success is not visual success. A Slidev deck can compile while the browser view still has overflow, broken frontmatter, missing assets, unreadable code highlighting, top-heavy layouts, or slides that are too dense to present.

## Deck Contract

Before writing slide source, establish a short deck contract:

- `deck_scope`: the one narrative lane this deck is allowed to cover
- `allowed_terms`: project names and presentation terms that should appear, such as `FK-Doob-PhysGen`
- `banned_terms`: implementation names, stale project names, or route words that must not appear in audience-facing text
- `one_sentence_claim`: the sentence the audience should remember
- `project_title`: the exact project name that must appear in the title slide and deck metadata

After writing, search the slide source for banned or stale terms. If an internal code name is useful during implementation but confusing for the audience, replace it with the presentation term in headings and takeaways while keeping the implementation term only where technically necessary.

Default naming rule: the title slide, browser/PDF metadata, and first H1 must include the project name. Do not use a method-only title unless the user explicitly asks for it.

## Workflow

### 1. Identify Presentation Type

Determine:

- deck id and target path under `decks/`
- audience: advisor, lab, committee, conference, interview, or class
- time limit
- goal: feedback, progress report, teaching, persuasion, or defense
- single most important takeaway
- available material: memory, notes, figures, reports, paper draft, code results, or existing slides
- deck contract: scope, allowed terms, banned terms, one-sentence claim, and exact project title

### 2. Choose the Deck Archetype

Use the closest archetype.

Advisor update deck:

1. Title / meeting goal
2. Last commitments
3. Progress summary
4. Key result or evidence
5. What is solved
6. What is stuck
7. Options / decision needed
8. Next-week plan

Lab meeting research update:

1. Title
2. Problem and motivation
3. Current research question
4. Method or setup
5. Experimental setup
6. Main result
7. Ablation / analysis
8. Limitation or failure case
9. Next steps and questions

Paper reading report:

1. Title: paper and why it matters
2. One-sentence contribution
3. Problem setting
4. Method overview
5. Key technical idea
6. Main experiments
7. Strengths
8. Weaknesses / assumptions
9. Relevance to the user's project
10. Discussion questions

Conference-style talk:

1. Title
2. Motivation
3. Problem
4. Gap in prior work
5. Method intuition
6. Method details
7. Experimental setup
8. Main result
9. Analysis / ablation
10. Limitations
11. Takeaway

### 3. Produce a Slide Plan Before Heavy Editing

For each slide, write:

- slide number
- slide type
- takeaway title
- visual/evidence needed
- bullets or diagram content
- speaker note
- risk: what may confuse the audience

If a slide has no takeaway, merge it, cut it, or move it to backup.

Apply a capacity budget before editing source:

- A normal slide should have at most one H1, one primary visual region, and one takeaway.
- Do not combine a question box, long bullets, a code block, and a takeaway on the same normal slide.
- Code blocks on normal slides should usually be at most 3 lines; longer code belongs in backup.
- Tables should fit within 16:9 without shrinking text below readable size.
- Three-column layouts should keep each column to about 3 bullets unless the visual design clearly supports more.
- Backup slides may be dense, but each backup slide still needs a purpose: reference links, asset paths, implementation detail, or extra evidence.

### 4. Write Template-Compatible Source

After inspecting `progress-slides`, write in the format the template already uses. For Slidev-style Markdown, prefer this pattern:

```markdown
---
theme: default
title: Project Progress Update
---

# Specific Takeaway Title

- Evidence or status point
- Decision or implication

<!--
Speaker note: what to say in 20-40 seconds.
-->

---

# Main Result Supports the Current Claim

<figure-or-table-placeholder>

- Setup:
- Metric:
- Interpretation:
```

Keep speaker notes close to the slide source when the template supports notes. Keep image paths relative to the slide deck so the deck can be moved or shared.

Slidev source guardrails:

- Put deck-level frontmatter only at the top of the deck.
- Per-slide frontmatter must be a valid frontmatter block by itself:

```markdown
---
layout: center
class: text-center
---
```

- If a page does not need per-slide frontmatter, omit it. Do not leave `layout:` or `class:` lines in normal Markdown body text.
- After editing, search for `^layout:` and `^class:` outside frontmatter blocks if the source was heavily modified.
- Title metadata should include the project name so exported PDF/browser titles are recognizable.
- When the deck source is under `decks/`, run Slidev against that file, such as `npx slidev decks/2026-05-02-advisor-plan.md`, instead of assuming the default `slides.md` is the target.

Slidev root, assets, and styling guardrails:

- Identify the active Slidev root from the entry file before writing paths. For `slides/decks/<deck-id>.md`, the root may be `slides/decks/`, not `slides/`.
- Keep standalone meeting assets deck-local under the active root, such as `slides/decks/assets/<deck-id>/figure.png`, and reference them as `./assets/<deck-id>/figure.png` from `slides/decks/<deck-id>.md`.
- Do not depend on live code-worktree paths for meeting decks. Copy stable, presentation-ready figures into the deck-local asset directory.
- Put deck-wide CSS under the active Slidev root, such as `slides/decks/styles/index.css`, and load it from `slides/decks/setup/main.ts` with `import '../styles/index.css'`.
- Do not rely on one large Markdown `<style>` block for deck-wide styling; it can fail to apply consistently across slides.
- For code or pipeline slides, check Shiki-highlighted nested spans. If local styles become unreadable, override the specific slide block's `pre`, `code`, and `code span` colors.
- For result figures, inspect real image dimensions before choosing layout:

```bash
sips -g pixelWidth -g pixelHeight <figure>.png
```

- Size figure-pair slides separately from ordinary image grids. Two scientific plots often need a larger vertical budget than generic card images.

### 5. Use Project Evidence Correctly

- Pull stable figures from `code/docs/results/`, `code/docs/reports/`, paper figures, or user-provided assets.
- Do not copy raw logs, huge outputs, checkpoints, or wandb/tensorboard caches into the slides repo.
- If a figure is stale, unclear, or too dense, use `figure-results-review` before finalizing the deck.
- If slide claims diverge from the paper or project status, update `memory/` or `slides/.agent/` with the risk.

### 6. Validate Narrative and Terms

Before build or export:

- confirm the first slide title, browser/PDF title metadata, and main H1 include the project name
- confirm every normal slide has one primary takeaway
- search for `banned_terms`, stale project names, and internal implementation names in audience-facing headings and takeaways
- check that the final slide does not introduce a new unmotivated direction unless the deck scope explicitly allows it
- prefer presentation terms in takeaways, such as "isometric conditional model"; keep implementation terms, such as `model_D`, only in implementation-detail slides

### 7. Validate the Deck

Before finishing:

- run the template's preview/build command when dependencies are available
- confirm the deck opens locally; do not treat `npm run build` alone as proof that the slides are visually usable
- check that all image paths resolve in browser preview, not only in the Markdown source
- confirm global CSS is loaded from the active Slidev root
- check that text is readable in 16:9 presentation view
- check that each result slide explains setup, metric, and interpretation
- visually inspect the first slide, second slide, and final three slides because title, framing, and closeout mistakes are high impact
- screenshot representative slides at 16:9: one text-heavy/context slide, one table or metric slide, one two-figure slide, one code or pipeline slide, and one backup slide if backup uses a different layout
- when possible, export PNG/PDF through the template's export command, Slidev browser export UI, or `slidev export --format png`; Slidev CLI export requires Playwright/`playwright-chromium`
- if PNG/PDF export is blocked by missing Playwright or Chromium, record the missing dependency and use browser preview screenshots or manual browser inspection instead
- check tables, code blocks, three-column layouts, question boxes, and takeaway boxes for overflow
- treat excessive top-heavy whitespace as a layout bug even when nothing overflows; redistribute content with slide-specific classes instead of stacking every element near the top
- verify scientific figures are large enough for visual inspection, especially side-by-side plots
- update `slides/.agent/slides-status.md` and `slides/.agent/deck-index.md` with deck path, purpose, audience, source evidence, build status, visual validation status, stale evidence risks, known unchecked risks, and follow-up actions when using a project-control-root layout
- for important or reusable decks, also write `slides/.agent/decks/<deck-id>.md`

Final checklist:

```markdown
- [ ] Deck source lives in `decks/<deck-id>.md` unless this is a temporary/default `slides.md` deck.
- [ ] `slides.md` was not used to overwrite a previous real meeting deck.
- [ ] Title includes project name.
- [ ] Deck has one explicit narrative scope.
- [ ] Banned or stale terms checked with search.
- [ ] No normal slide has H1 + question box + code block + takeaway together.
- [ ] Code blocks are <= 3 lines unless in backup.
- [ ] Tables fit within 16:9 width.
- [ ] No literal `layout:` or `class:` frontmatter is rendered as body text.
- [ ] Deck-local assets resolve from the active Slidev root.
- [ ] Global CSS is imported from the active Slidev root, not only embedded in Markdown.
- [ ] Result figure dimensions were inspected before final sizing.
- [ ] Internal code names are replaced in audience-facing text where appropriate.
- [ ] Preview/build passes, or missing dependency is recorded.
- [ ] Representative 16:9 screenshots, PNG/PDF export, or browser visual inspection completed.
- [ ] Code blocks remain readable after syntax highlighting.
- [ ] Figure slides are readable and not undersized.
- [ ] `slides/.agent/slides-status.md` and `slides/.agent/deck-index.md` updated when project memory is present.
```

## Output Shape

For a planning-only request, produce:

```markdown
# Research Slide Deck Plan - [Deck Name]

## Context
- Audience:
- Time limit:
- Goal:
- One takeaway:
- Template: progress-slides
- Deck id:
- Deck path:
- Deck scope:
- Allowed terms:
- Banned terms:

## Slide Plan
| # | Type | Takeaway title | Visual/evidence | Speaker note | Risk |
|---:|---|---|---|---|---|

## Required Assets
- [ ] [figure/table/diagram]

## Decision Points
1. [Decision/question]

## Backup Slides
- [Backup topic]
```

For an implementation request, edit the actual `slides/` source files in the cloned `progress-slides` repo and report the changed paths plus the preview/build command used.

When creating a new deck in an existing slides component, default to:

```text
slides/decks/<YYYY-MM-DD>-<audience-or-purpose>-<slug>.md
slides/decks/assets/<deck-id>/...
slides/.agent/deck-index.md
slides/.agent/decks/<deck-id>.md
```

Use `slides/slides.md` only when the user explicitly wants the current default deck or the template tooling requires a temporary staging file.

## Do Not

- Do not create a separate in-skill slide template.
- Do not redesign the external template unless the user asks to modify the template itself.
- Do not make a deck of status bullets without evidence or decisions.
- Do not force a conference-talk narrative onto an advisor update.
- Do not overpack slides because the user is afraid to leave things out.
- Do not stop at Markdown correctness or build success when the user expects a deck they can open and present.
- Do not leave backup slides as unexplained asset dumps.
- Do not treat `slides/slides.md` as the only deck file for a project lifecycle.
- Do not lose old decks by reusing the same file for every meeting.
