---
name: buchbinder
description: "Professional book writing workflow for OpenCode — fiction, non-fiction, and mixed projects. Provides the complete /buchbinder methodology with a TUI menu system for research, drafting, critique, revision, citation management, editing, review, and publishing. Use when starting a book project, organizing writing, managing research, handling citations, or navigating any phase of a long-form writing project."
---

# Buchbinder — Professional Book Writing Methodology

This skill contains the complete Buchbinder methodology for producing long-form written work with AI assistance. It covers three workflow tracks (fiction, non-fiction, mixed), the full command architecture, project file conventions, and how companion sub-skills activate per-phase.

## Core Principles

1. **Phase separation** — Each phase of writing has a distinct goal, output, and quality gate. Never conflate drafting with editing, or research with revision.
2. **Progressive elaboration** — Start lean and add detail only when needed. No document exceeds ~500 lines without splitting.
3. **Externalised knowledge** — Character profiles, research notes, citations, and tracking data live in dedicated files, not in the AI's context window.
4. **Structured iteration** — Critique and revision are formal phases with defined inputs and outputs, not informal back-and-forth.
5. **Track-appropriate rigour** — Fiction and non-fiction share the same architectural principles but differ in their quality gates (consistency vs. factual accuracy).

---

## The Three Tracks

| Track | When to Use | Core Phases |
|-------|-------------|-------------|
| **Fiction** | Novels, short stories, serials, narrative non-fiction with creative elements | Constitute → Specify → Clarify → Research → Outline → Task → Draft → Critique → Revise → Edit → Review → Publish |
| **Non-fiction** | Academic works, journalism, biography, technical books, essays, reports | Constitute → Research → Annotate → Outline → Draft (with citations) → Critique → Fact-check → Revise → Review → Publish |
| **Mixed** | Creative non-fiction, memoir with research, narrative journalism | Constitute → Specify + Research → Clarify → Outline → Draft with citation markers → Critique → Revise → Edit → Fact-check → Review → Publish |

---

## Command Architecture

Buchbinder exposes a single hub command `/buchbinder` with a TUI menu system for each workflow phase. When invoked without a subcommand, `/buchbinder` presents a menu of available phases. The "Guided" option runs automatic state detection and presents a contextualised roadmap.

### Phase Commands

| Subcommand | Alias | Phase | Track | Purpose |
|-----------|-------|-------|-------|---------|
| `constitute` | `const` | 1 | All | Define creative or intellectual principles, quality baseline, and non-negotiables |
| `specify` | `spec` | 2 | Fiction, Mixed | Build a lean story specification and knowledge map |
| `clarify` | `clar` | 3 | Fiction, Mixed | Resolve ambiguities in the specification |
| `research` | `rsrc` | 2/4 | All | Active research: web search, source ingestion, annotation, literature review |
| `outline` | `plan` | 4/5 | All | Chapter structure, pacing, argument arc, foreshadowing, or thesis progression |
| `task-manager` | `tasks` | 5/6 | All | Break outline into tracked, dependency-ordered tasks |
| `draft` | `write` | 6/7 | All | Write chapters or sections with pre-draft checklist |
| `critique` | `alpha` | 7/8 | All | Structured external-feedback simulation: alpha, beta, peer, sensitivity |
| `revise` | `revision` | 8/9 | All | Plan revisions, categorise feedback, track changes |
| `edit` | `editor` | 9/10 | All | Line-level editing with suggestion tracking and approved-edit application |
| `review` | `qa` | 10/11 | All | Broad project QA: continuity, consistency, factual accuracy, readiness |
| `cite` | `citation` | 3 | Non-fiction | Citation ingestion, formatting, bibliography generation, validation |
| `publish` | `pub` | 11/12 | All | Format export, submission preparation, metadata packaging |
| `track` | — | Utility | All | Unified tracking: characters, plots, timelines, sources, themes |
| `timeline` | — | Utility | All | Chronological consistency verification |
| `meta` | — | Utility | All | Bibliographic metadata management |
| `drafter` | — | Utility | All | Loose draft jumpstart from raw ideas |

### Shorthand Aliases

The `/buchbinder` command uses the hubMenu tool for routing. Subcommands are selected via the TUI menu; direct dispatch works by appending the subcommand label (e.g. `/buchbinder draft`).

---

## Project File Structure

```
project-root/
├── .opencode/                    # Per-project OpenCode configuration
│   ├── commands/
│   │   └── buchbinder.md               # Hub command (installed by buchbinder)
│   ├── skills/                   # Sub-skills (installed by buchbinder)
│   └── tools/                    # TypeScript tools (installed by buchbinder)
├── book/                         # All book content (rename as needed)
│   ├── track.json                # Track selection: fiction | non-fiction | mixed
│   ├── meta.json                 # Bibliographic metadata
│   ├── constitution.md           # Phase 1 output
│   ├── specification.md          # Phase 2 output (fiction/mixed)
│   ├── research/                 # Research artifacts
│   │   ├── research-plan.md
│   │   ├── sources/              # Source notes, annotations
│   │   ├── bibliography/         # Formatted citations
│   │   └── interviews/           # Interview transcripts, field notes
│   ├── outline/                  # Phase 4/5 output
│   │   ├── _main.md              # Index + shard map
│   │   ├── part-1.md
│   │   └── ...
│   ├── tasks.md                  # Phase 5/6 output
│   ├── content/                  # Draft chapters
│   │   ├── chapter_00001.md
│   │   └── ...
│   ├── critique/                 # Critique artifacts
│   │   ├── round-1/              # Per-round feedback
│   │   └── ...
│   ├── revisions/                # Revision tracking
│   │   ├── revision-log.md
│   │   └── ...
│   ├── knowledge/                # Fiction: character profiles, world-building
│   │   ├── character-profiles.md
│   │   ├── locations.md
│   │   ├── glossary.md
│   │   └── ...
│   ├── tracking/                 # State tracking
│   │   ├── character-state.json
│   │   ├── plot-tracker.json
│   │   ├── timeline.json
│   │   └── ...
│   └── drafts/                   # Loose draft material
│       └── chapter_00001.md
├── memory/                       # Durable reference
│   ├── constitution.md           # (linked from book/)
│   ├── personal-voice.md         # Fiction voice reference
│   └── research-methodology.md   # Non-fiction methodology reference
└── output/                       # Published exports
    ├── manuscript/               # Compiled manuscript
    ├── epub/
    ├── docx/
    └── latex/
```

### Split Mode

When any document exceeds ~500 lines, split into a folder with `_main.md` as the index:

- `specification.md` → `specification/_main.md` + shards (`core.md`, `world.md`, `cast.md`, `plot.md`)
- `outline.md` → `outline/_main.md` + shards per part or arc
- `tasks.md` → `tasks/_main.md` + shards per phase

---

## Plugin Maintenance: Refresh & Index

The buchbinder plugin evolves. To sync an installed project with the latest plugin source without overwriting your project work, use:

```bash
npx buchbinder-refresh        # idempotent: syncs plugin assets, rebuilds index, preserves local edits
npx buchbinder-index          # rebuild only the lore semantic index
```

`buchbinder-refresh` writes a manifest at `.opencode/.buchbinder-install-manifest.json` that records every file it installed (with per-file SHA256) so subsequent refreshes are diff-based — your HTML-comment overrides in phase specs are preserved across refreshes. Run `--force` to overwrite them (destructive).

The semantic lore index lives at `.opencode/cache/lore-index/index.json` and is consulted on every phase invocation. The index is built incrementally — re-running on an up-to-date index is a no-op. Index coverage includes: series lorebook, series outline, per-book knowledge, constitution, specification, book outline (whole + per-chapter), and XML drafts (chunked by `<metadata>`, `<awareness-map>`, and per-`<scene>`). See the README for full details.

Phase specs that need continuity (`draft`, `critique`, `revise`) use `--pin-chapter N --pin-side previous|both` to include the entire adjacent chapter(s) verbatim in the context, regardless of semantic score.

---

## Phase Detail Summary

### Phase 1: Constitute (all tracks)
Establish the governing principles for the entire work. Output: `constitution.md`

| Section | Fiction | Non-fiction |
|---------|---------|-------------|
| Core Values | Theme, message, emotional intent | Thesis, argument, purpose |
| Quality Baseline | Prose standards, pacing preference | Rigour standards, evidence requirements |
| Style Principles | Language register, atmosphere | Tone, accessibility level, disciplinary conventions |
| Content Principles | Character, plot, worldbuilding norms | Chapter structure, argument flow, citation density |
| Reader Contract | Genre expectations, content warnings | Audience level, assumed knowledge |
| Revision Procedures | How revision decisions are made | How factual corrections are handled |

### Phase 2-3: Specify & Clarify (fiction/mixed)
Create the story's blueprint and resolve ambiguities. Output: `specification.md` + `knowledge/`

### Phase 2: Research (non-fiction/mixed)
Active research phase: gather sources, evaluate credibility, extract annotations, build bibliography. Output: `research/` directory

### Phase 4: Outline (all tracks)
Convert specification or research into a structured chapter-by-chapter or section-by-section plan. Output: `outline.md` or `outline/`

### Phase 5: Task Manager (all tracks)
Break the outline into tracked, dependency-ordered tasks. Output: `tasks.md` or `tasks/`

### Phase 6: Draft (all tracks)
Write chapters one at a time with the pre-draft checklist ensuring full context is loaded. Output: `content/chapter_NNNNN.md`

### Phase 7: Critique (all tracks)
Simulate structured external feedback. Modes: alpha reader (structural), beta reader (experience), peer review (field-appropriate), sensitivity reader. Output: `critique/round-N/`

### Phase 8: Revise (all tracks)
Categorise critique feedback, plan revisions, apply changes with tracking. Output: `revisions/revision-log.md`

### Phase 9: Edit (all tracks)
Line-level pass: suggest changes, track approvals, apply confirmed edits. Output: updated chapters

### Phase 10: Review (all tracks)
Broad project QA: continuity, tracking accuracy, factual verification (non-fiction), final readiness assessment. Output: review report

### Phase 11: Publish (all tracks)
Format export, metadata packaging, submission preparation. Output: `output/`

---

## Companion Sub-Skills

These skills activate automatically based on context when installed:

### Writing Techniques (`skills/fiction/writing-techniques/`)

| Skill | Activates When | Purpose |
|-------|---------------|---------|
| `dialogue-techniques` | Writing dialogue | Subtext-heavy, distinctive, character-driven dialogue |
| `character-depth` | Developing characters | Psychological backstory, Wound/Ghost, internal contradictions |
| `scene-structure` | Drafting scenes | Goal/Conflict/Disaster/Reaction/Dilemma/Decision framework |
| `pacing-rhythm` | Managing pace | Pacing archetypes, sentence-level rhythm, fragment detection |
| `emotional-interiority` | Writing POV | Internal reactions, sensory-emotional responses |
| `strategic-reversal` | Writing contests/tactics | Bluffs, hidden rules, clever reversals |
| `comedic-banter-rhythm` | Writing banter | Comedic escalation, argument exposition, humour under pressure |
| `punctuation-emotional-effect` | Editing prose | Punctuation for rhythm, silence, hesitation, emphasis |
| `namecraft` | Naming entities | Names for characters, factions, places, abilities, systems |

### Genre Knowledge (`skills/fiction/genre-knowledge/`)

| Skill | Purpose |
|-------|---------|
| `genre-fantasy` | Magic systems, worldbuilding, fantasy tropes |
| `genre-romance` | Romance arcs, emotional beats, HEA/HFN structures |
| `genre-thriller` | Suspense mechanics, pacing, stakes escalation |
| `genre-horror` | Dread, atmosphere, fear mechanics |
| `genre-mystery` | Clue planting, red herrings, fair-play rules |
| `genre-scifi` | Speculative worldbuilding, technology consistency |

### Quality Assurance (`skills/quality-assurance/`)

| Skill | Purpose |
|-------|---------|
| `pre-draft-checklist` | Ensures full context is loaded before drafting |
| `consistency-checker` | Catches plot holes, character inconsistencies, timeline errors |
| `forgotten-elements` | Identifies dropped threads and forgotten entities |
| `style-enforcer` | Enforces chosen prose style |
| `citation-validator` | Validates citation format and cross-references |
| `fact-checker` | Flags factual claims for verification |

### Research (`skills/research/`)

| Skill | Purpose |
|-------|---------|
| `web-research` | Search strategies, source credibility assessment |
| `interview-methods` | Interview design, transcription, synthesis |
| `field-notes` | Observation recording, annotation standards |
| `source-annotation` | Active reading, marginalia, extraction |

### Non-Fiction (`skills/non-fiction/`)

| Skill | Purpose |
|-------|---------|
| `academic-writing` | Thesis statements, argument structure, academic register |
| `citation-styles` | APA 7th, Chicago 17th, MLA 9th, IEEE, and custom styles |
| `argument-structure` | Claim/evidence/warrant, counter-argument, synthesis |
| `source-evaluation` | CRAAP test, bias detection, source triangulation |

### Critique (`skills/critique/`)

| Skill | Purpose |
|-------|---------|
| `alpha-reader` | Structural critique: pacing, plot holes, character arcs |
| `beta-reader` | Experience critique: engagement, confusion, investment |
| `peer-review` | Field-appropriate peer review simulation (academic/professional) |
| `sensitivity-reader` | Representation and authenticity assessment |

---

## Task Markers

| Marker | Meaning |
|--------|---------|
| `[P]` | Can be done in parallel |
| `[Dep:N]` | Depends on task N |
| `[High]` | Critical path |
| `[ForReview]` | Draft complete, awaiting critique |
| `[Revised]` | Revision applied |
| `[Done]` | Complete and approved |

## Citation Markers (Non-Fiction)

| Marker | Meaning |
|--------|---------|
| `[Source: key]` | Claim backed by source `key` |
| `[CitationNeeded]` | Claim requires a source |
| `[Verify: key]` | Source `key`'s claim needs cross-verification |
| `[Disputed: key1 vs key2]` | Sources disagree on this point |

---

## Conventions

- **Phase-gate discipline**: Complete each phase's output before starting the next. The `/buchbinder guided` subcommand enforces this.
- **One chapter per file**: `content/chapter_NNNNN.md` with zero-padded numbering.
- **Context reload**: The pre-draft checklist ensures constitution, specification, outline, knowledge, tracking, and previous chapter are loaded before every new chapter.
- **Split at 500 lines**: Any file approaching 500 lines should be split into a directory with `_main.md` as index.
- **Serious tone**: All command output uses professional register. No emoji in generated content.
