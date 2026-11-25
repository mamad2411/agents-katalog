---
name: scriptorium-workflow
description: >-
  Step-by-step execution guide for the scriptorium 5-phase book production pipeline.
  Use when: running any phase (1 through 5), orchestrating chapter production, managing parallel
  review steps (R1+R2+R3 simultaneous), handling recovery after interruption, understanding 
  completion markers, debugging a stalled pipeline, or knowing the exact file inputs and outputs
  for each step. Covers DAG dependency management and the chapter batch parallelization strategy.
license: MIT
---

# Tech-Editorial: 5-Phase Workflow Execution Guide

## How to Start

**One-sentence startup** — say this to your AI tool:

```
The source code for [project name] is in [directory path].
Please read QUICK_START.md, then ask me any questions.
If you have no questions, start your work.
```

**Resume after interruption:**
```
Please read checkpoint.md and continue where we left off.
```

The AI reads `QUICK_START.md` and runs the full pipeline autonomously.
The sections below are the detailed reference for each phase.

---

## Phase 1 — Outline Finalization

### Step 1.1 — Architect Analyzes Source Code
**Agent**: #1 Architect (general-purpose)  
**File Pointers IN**: source code root, `templates/source-map.md`, `templates/outline.md`  
**Output**: `outline-draft.md`, `source-map.md`  
**Completion**: `<!-- ARCHITECT_DRAFT_COMPLETE -->` in `outline-draft.md`

### Step 1.2 — Reader Advocate Reviews
**Agent**: #2 Reader Advocate (general-purpose)  
**File Pointers IN**: `outline-draft.md` only  
**Output**: `outline-reader-feedback.md`

### Step 1.3 — Content Reviewer Initial Check
**Agent**: R3 Content Reviewer (general-purpose)  
**File Pointers IN**: `outline-draft.md`, `templates/style-guide.md`  
**Output**: `outline-r3-review.md`

### Step 1.4 — Human Decision Gate
Human reviews all three files → produces `outline-final.md`. This is a hard checkpoint — do NOT proceed to Phase 2 without human sign-off.

---

## Phase 2 — Shared Resources Build

**Agent**: #0 Orchestrator (direct execution)  
Creates the `meta/` directory with 5 files:

| File | Purpose | Type |
|------|---------|------|
| `meta/glossary.md` | Full-book term definitions | Append-only |
| `meta/style-guide.md` | Writing voice, format rules | Static |
| `meta/metaphor-registry.md` | Used analogies/metaphors log | Append-only |
| `meta/chapter-summaries.md` | Per-chapter summaries (grows as chapters complete) | Append-only |
| `meta/cross-references.md` | Inter-chapter reference table | Append-only |

---

## Phase 3 — Per-Chapter Pipeline (Repeat × N chapters)

### Step 3.1 — Research
**Agent**: #3 Researcher (explore — read-only)  
**File Pointers IN**: chapter spec from `outline-final.md`, source code files for this chapter, `meta/glossary.md`  
**Output**: `research/chXX-research.md`  
**Completion**: `<!-- RESEARCH_COMPLETE -->`  
**Constraint**: Every claim must cite exact source file + line number. No fabrication.

### Step 3.2 — Writing
**Agent**: #4 Writer (general-purpose)  
**File Pointers IN**: `research/chXX-research.md`, chapter spec from `outline-final.md`, `meta/style-guide.md`, `meta/chapter-summaries.md`, `meta/glossary.md`, `meta/metaphor-registry.md`  
**Output**: `drafts/chXX-draft.md`  
**Completion**: `<!-- DRAFT_COMPLETE -->`  
**Word count target**: {{每章目标字数}} ± 20%

### Step 3.3 — Three-Way Parallel Review
Run R1, R2, R3 **simultaneously in separate agent contexts**:

| Reviewer | Context Budget | File Pointers IN | Output |
|----------|---------------|-----------------|--------|
| R1 Code | ~37K tokens | draft + source files + source-map | `reviews/chXX-r1-code.md` |
| R2 Consistency | ~30K tokens | draft + glossary + chapter-summaries + metaphor-registry + cross-refs | `reviews/chXX-r2-consistency.md` |
| R3 Content | ~18K tokens | draft + style-guide only | `reviews/chXX-r3-content.md` |

After all 3 complete, Orchestrator merges into `reviews/chXX-review.md` + `<!-- REVIEW_COMPLETE -->`  
**Merge priority**: R1 ❌ > R3 ❌ > R2 ⚠️ > others

### Step 3.4 — Three-Way Parallel Reader Panel
Run RS, RE, RH **simultaneously**:

| Reader | Persona | File Pointers IN |
|--------|---------|-----------------|
| RS | CS Junior student | draft only |
| RE | 8yr engineer | draft + source-map |
| RH | Tech hobbyist | draft only |

Orchestrator merges → `reader-feedback/chXX-panel.md` + `<!-- READER_PANEL_COMPLETE -->`

### Step 3.5 — Post-Chapter Long-Memory Update
Orchestrator executes directly (do NOT delegate):
```
meta/chapter-summaries.md  ← append 200-300 word summary
meta/glossary.md           ← append new terms from R2 report
meta/metaphor-registry.md  ← append new metaphors from R2 report
meta/cross-references.md   ← append new inter-chapter references
```

---

## Phase 4 — Final Audit

Invoke R1 + R2 + R3 in parallel across the full book:
- R1: validates all code snippets are still accurate against current source
- R2: checks global term/metaphor consistency across all chapters  
- R3: final readability and sensitivity scan

**Output**: `final-audit-report.md` + revised `chapters/chXX.md` files with `<!-- CHAPTER_FINAL -->`

---

## Phase 5 — HTML Publishing

**Agent**: #11 Bookbinder (general-purpose)  
**File Pointers IN**: all `chapters/chXX.md`, `meta/style-guide.md`  
**Output**: `publish/` directory (index.html + ch*.html + style.css + assets/)  
**Completion**: `<!-- HTML_COMPLETE -->` in each HTML file

---

## Recovery Protocol

State is always recoverable from files alone:
1. Scan for `<!-- *_COMPLETE -->` markers: `grep -r "_COMPLETE" . --include="*.md"`
2. Cross-check with SQL todos table if used
3. Resume from the last incomplete step — files without completion markers are safe to regenerate
4. Partially written files (no marker) = treat as not started

## Parallelization Rules

**Within a chapter batch**: chapters in the same batch can run Steps 3.1→3.4 simultaneously  
**Between batches**: strictly serial — batch N+1 must wait for all long-memory updates from batch N  
**Recommended batch size**: 2-3 chapters (balance parallelism vs. context coherence)

## Failure Handling

| Scenario | Action |
|----------|--------|
| Review returns ❌ CRITICAL | Re-invoke Writer with specific ❌ items, then re-run only the reviewer who flagged it |
| Word count off by >20% | Re-invoke Writer with explicit section expansion/trimming instructions |
| Agent crashes without completion marker | Re-invoke with same file pointers — safe to overwrite |
| 3+ consecutive failures on same chapter | Mark as `blocked` in todos, skip chapter, continue; human review after all others complete |
