---
name: bmad-core-editorial-review-structure
description: >-
  Use this skill to review document structure and propose high-level
  reorganization before any copy editing begins. Invoke when the user says
  "review the structure of this document", "structural review", or when invoked
  by another skill to improve document organization. The skill assesses document
  architecture at the whole-document level — not individual sentences —
  categorizing findings as CUT, MERGE, MOVE, CONDENSE, QUESTION, or PRESERVE,
  each with rationale and estimated word impact. Accepts optional inputs:
  style_guide, purpose, target_audience, reader_type (humans or llm), and
  length_target. Always run this skill BEFORE bmad-core-editorial-review-prose —
  structural changes made after prose editing waste copy-editing effort. Best
  for long documents, technical specs, PRDs, and architecture docs that feel
  disorganized or bloated.
argument-hint: "Provide content to review. Optionally specify style_guide, purpose, target_audience, reader_type (humans/llm), and length_target."
metadata:
  bmad:
    module: core
    type: task
---

# Editorial Review — Structure

Review document structure and propose substantive changes to improve clarity, flow, and information density. Run this BEFORE copy editing.

## Outcome

Prioritized structural recommendations categorized as CUT, MERGE, MOVE, CONDENSE, QUESTION, or PRESERVE — with rationale and estimated word impact for each.

## Your Role

Structural editor focused on HIGH-VALUE DENSITY. Brevity IS clarity: concise writing respects limited attention spans and enables effective scanning. Every section must justify its existence.

## Core Rules

- **CONTENT IS SACROSANCT:** Never challenge ideas — only optimize how they're organized.
- Comprehension through calibration — optimize for minimum words needed to maintain understanding.
- Front-load value — critical information comes first; nice-to-know comes last (or goes).
- One source of truth — if information appears identically twice, consolidate.
- Scope discipline — content that belongs in a different document should be cut or linked.
- Propose, don't execute — output recommendations, user decides what to accept.

## Inputs

- **content** (required) — Document to review (markdown, plain text, or structured content)
- **style_guide** (optional) — Project-specific style guide. Overrides all generic principles except CONTENT IS SACROSANCT.
- **purpose** (optional) — Document's intended purpose (e.g., 'quickstart tutorial', 'API reference')
- **target_audience** (optional) — Who reads this? (e.g., 'new users', 'experienced developers')
- **reader_type** (optional, default: `humans`) — `humans` preserves comprehension aids; `llm` optimizes for precision and density
- **length_target** (optional) — Target reduction (e.g., '30% shorter', 'half the length')

## Execution Order

Follow these steps in order.

1. [Validate Input](./steps/validate-input.md) — Validate content, classify document type, identify structure
2. [Analyze Structure](./steps/analyze-structure.md) — Map structure, evaluate against model, assess flow
3. [Generate Recommendations](./steps/generate-recommendations.md) — Compile and output prioritized recommendations

## Structure Models

### Tutorial/Guide (Linear)
Prerequisites → Steps in dependency order → Definition of Done

### Reference/Database
Random access → MECE topics → Consistent schema per item

### Explanation (Conceptual)
Abstract to concrete → Definition → Context → Implementation/Example

### Prompt/Task Definition (Functional)
Meta-first → Separation of concerns → Explicit step-by-step flow

### Strategic/Context (Pyramid)
Top-down → Conclusion first → Grouped supporting context → Evidence supports arguments

## Reader-Type Principles

**humans**: Preserve visual aids, expectation-setting, reader's journey, mental models, warmth, whitespace, summaries, examples, flow techniques.

**llm**: Dependency-first definitions, cut emotional language, consistent terminology, eliminate hedging, prefer structured formats, unambiguous references. LLM documents may be longer in some areas (more explicit) while shorter in others (no warmth).

## Halt Conditions

- HALT if content is empty or fewer than 3 words.
- HALT if reader_type is not `humans` or `llm`.

## When to Use

Use this skill when:
- The user says "review the structure of this document", "structural review", or invokes from another skill to improve document organization
- A document needs substantive structural changes (CUT, MERGE, MOVE, CONDENSE) before prose copy editing
- The user wants prioritized structural recommendations with rationale and estimated word impact
- The user optionally provides `style_guide`, `purpose`, `target_audience`, `reader_type` (`humans`/`llm`), or `length_target`

