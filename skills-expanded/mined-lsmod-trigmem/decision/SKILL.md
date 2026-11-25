---
name: decision
description: |
  Core decision logic for TrigMem method. Determines the best storage
  location for information in Claude Code memory (CLAUDE.md, Rules,
  Skills, Commands, or Agents). Internal use only.
  Use when another skill or command needs to classify content and
  decide where it should be stored in Claude Code's memory system.
user-invocable: false
allowed-tools: Read, Grep, Glob, AskUserQuestion
---

# TrigMem Decision Skill

Classify input content against the 6 information categories, map to a destination, and return a structured decision.

## Input

You receive a content description (text the user wants to store in Claude Code memory).

## Decision Logic

### Step 1: Classify Against the 6 Categories

Match the input to one category. If it clearly spans multiple, go to Step 4 (this is common — not an edge case).

| Cat | Name | Identifying Signal |
|-----|------|--------------------|
| 1 | Project Identity | What the project IS: name, purpose, tech stack. Unique, rarely changes. |
| 2 | Codebase Structure | Where things LIVE: directory layout, file locations. Navigation-oriented. |
| 3 | Operational Commands | How to DO something: build, test, deploy. Procedural with side effects. |
| 4 | Reusable Patterns | Universal HOW-TO knowledge: portable across projects using same tech. |
| 5 | Architectural Guidance | How WE do it HERE: project-specific application of patterns. |
| 6 | Iterative Corrections | DON'T do that AGAIN: reactive fixes for repeated mistakes. |

If classification is unclear, Read `ref-categories.md` for self-assessment questions, Cat 4 vs 5 distinction, and ambiguous case resolution.

### Step 2: Map Category to Destination

| Cat | Primary Destination | Refinement Needed? |
|-----|--------------------|--------------------|
| 1 | CLAUDE.md | No |
| 2 | CLAUDE.md / Rules | **Yes** — high-level map -> CLAUDE.md; directory-specific conventions -> Rules (needs file-pattern globs) |
| 3 | Commands | No — but extract reusable knowledge to Skills if present |
| 4 | Skills | No — check portability; consider configurable skill pattern |
| 5 | Rules / CLAUDE.md | **Yes** — directory-specific with globs -> Rules; project-wide + brief -> CLAUDE.md; detailed -> External + pointer |
| 6 | Rules / CLAUDE.md | **Yes** — file-type-specific -> Rules (with globs); project-wide critical -> CLAUDE.md |

For categories that map to a single destination (1, 3, 4): return immediately.

For categories requiring refinement (2, 5, 6), apply these rules:
- **Rules** require specific file-pattern globs (e.g., `*.ts`, `src/api/**`). Rules with broad patterns (`**/*`) provide no token savings over CLAUDE.md.
- **CLAUDE.md** is for brief, always-needed context. If content is too long: when a Skill exists for the same topic, prefer a skill companion (`.claude/skills/{name}/reference.md`); otherwise use the pointer pattern (brief reference in CLAUDE.md, full content in `docs/`).
- Use `AskUserQuestion` to resolve ambiguity when classification depends on user intent:
  - Rules vs CLAUDE.md destination unclear
  - Cat 4 vs Cat 5 and portability depends on user intent ("Is this meant to be portable across projects?")
  - Content description too vague to classify ("Can you be more specific about what you want to store?")
  - Decomposition boundaries unclear ("Should X and Y be stored together or separately?")
- When uncertainty is between destinations with similar trade-offs (not intent-dependent), make a best-guess decision and return `ambiguous` output with a recommendation.

### Step 2.5: Check Existing State

Before validating, scan all destination types for existing files that overlap with the proposed content.

| Destination | Scan Method | Match Criteria |
|-------------|-------------|----------------|
| CLAUDE.md | `Read CLAUDE.md` | If exists → Read `ref-claudemd-sections.md` to identify target section by content category |
| Rules | `Glob .claude/rules/*.md` | Compare topic keywords AND glob patterns. Same globs + same topic = update; same globs + different topic = create |
| Skills | `Glob .claude/skills/*/SKILL.md` | Compare proposed skill name against existing directory names (exact and substring) |
| Commands | `Glob .claude/commands/*.md` | Compare proposed command name against existing filenames |
| Agents | `Glob .claude/agents/*.md` | Compare proposed agent name against existing filenames |
| Linked docs | `Glob docs/*.md` | Compare proposed doc name against existing filenames |
| Skill companions | `Glob .claude/skills/*/reference.md` | Compare proposed companion topic against existing reference files in skill directories |

- If existing file found: set `Operation: update`, populate `Existing file:` field, and (for CLAUDE.md) `Section:` field, and (for overlaps) `Existing match rationale:`
- If no existing file found: set `Operation: create` (default, backward compatible)

### Step 3: Validate with Mechanism x Dimension Matrix (Tiebreaker)

If category classification alone does not resolve the destination, consult the matrix:

| Mechanism | Portability | Loading | Invocation | Isolation | Composability |
|-----------|-------------|---------|------------|-----------|---------------|
| CLAUDE.md | Project-bound | Always | Always active | Main | Low |
| Rules | Mixed | Pattern-matched | Automatic | Main | Medium |
| Skills | Universal | On-demand | Auto or User | Main | High |
| Commands | Universal | On-demand | User-explicit | Main | Low |
| Sub-agents | Universal | On-demand | Explicit or Auto | Isolated | Medium |

Ask: Does the content need to be always-loaded? Pattern-triggered? On-demand? User-controlled? Isolated? The mechanism whose dimension profile best matches the content's needs is the destination.

If the matrix alone doesn't resolve, Read `ref-decision-support.md` for dimension definitions, need→mechanism lookup, and trade-off comparisons.

### Step 4: Check for Decomposition

If the content spans multiple categories, recommend decomposition. Common patterns:

| Input Pattern | Decomposition |
|--------------|---------------|
| "We use X technology" | CLAUDE.md (identity) + Skill (how-to) + Rules (conventions) |
| "Run/Build/Deploy something" | Command (action) + Skill (knowledge) + CLAUDE.md (prereqs) |
| "Follow this coding standard" | Skill (universal) + Rules (specific rules) + Skill companion (reference) |
| "Enforce an architectural standard" | Skill (pattern) + Rule (conventions) + Sub-agent (applies it) |

Each component results in a separate file. Re-apply Steps 1-3 to each component individually to determine its specific destination. Split when aspects have different loading or invocation needs (e.g., always-loaded identity vs on-demand how-to).

#### Step 4b: Scan for Rule Candidates in Skill Components

After producing decomposition components, scan each **Skill component's** source content for enforceable constraints that should be extracted as separate Rules:

- **Keyword constraints:** Sentences containing NEVER, ALWAYS, ZERO, DO NOT, MUST NOT, MUST, or REQUIRED that state short enforceable rules scopeable to file globs
- **File extension patterns:** Paths like `*.repository.ts`, `*.use-case.ts`, `*.controller.ts`, or directory-scoped patterns from code blocks and file path comments

If any matches are found, append a `Rule candidates detected` section after the numbered components in the decomposition output (see Output Format below). Each candidate includes the constraint text and a suggested glob pattern.

If no matches are found, omit the section entirely (backward compatible — no extra output).

#### Step 4c: Route Reference Material to Skill Companion

After decomposition, check if a component pair exists: a Skill component AND a large reference/explanation component for the **same topic**.

If both exist:
- Route the reference component to `.claude/skills/{name}/reference.md` (a "Skill companion")
- The Skill's SKILL.md should reference the companion: "See `reference.md` in this directory for detailed documentation"
- CLAUDE.md should point to the skill path (`.claude/skills/{name}/SKILL.md`), not a separate `docs/` subfile
- Companion files have **NO frontmatter** — plain markdown only

This replaces the External Docs + Pointer pattern when a Skill exists for the same topic.

### Step 5: Fallback

If classification is uncertain after Steps 1-4, or when iterating on decomposed components, Read `ref-decision-support.md` for Phase 1 triage questions and Phase 2 per-destination refinement. This is an alternative classification path, not only a last resort.

If no category matches at all and no Skill exists for the same topic, recommend: External Docs + Pointer Pattern (store in `docs/`, add pointer in CLAUDE.md). When a Skill exists, prefer Skill companion (`.claude/skills/{name}/reference.md`).

## Output Format

**CRITICAL:** Your output MUST be exactly one of the three structured variants below. Do NOT produce prose summaries, markdown tables, bullet-point recaps, or any other format. A downstream parser depends on the `Decision:` field appearing on its own line. If the output is not in the structured format below, the system will fail.

Produce exactly one of these three variants:

### Clear Case (single destination, high confidence)

```
Decision: [CLAUDE.md | Rules | Skills | Commands | Sub-agents]
Operation: create | update
Existing file: [path or "none"]
Section: [section name]              ← CLAUDE.md only, omit otherwise
Existing match rationale: [reason]   ← only when Operation is update
Sub-destination: [if applicable, e.g., "pointer pattern" or "configurable skill"]
File path: [target path pattern]
Confidence: clear
Rationale: [1-2 sentences referencing the category and why this destination fits]
```

### Ambiguous Case (multiple plausible destinations)

```
Decision: ambiguous
Options:
1. [destination A] — Operation: [create|update], Existing file: [path] — [rationale]
2. [destination B] — Operation: [create|update], Existing file: [path] — [rationale]
Recommended: [best guess if any]
```

If invoking interactively and user intent would resolve the ambiguity, use `AskUserQuestion` before returning output. Only return `ambiguous` when the choice is genuinely a preference between valid options.

### Decomposition Case (content spans multiple categories)

```
Decision: decompose
Components:
1. [aspect] → [destination] ([file path]) — Operation: [create|update], Existing file: [path] — [rationale]
2. [aspect] → [destination] ([file path]) — Operation: [create|update], Existing file: [path] — [rationale]

Rule candidates detected in component N:
- "[constraint text]" → candidate glob: [pattern]
- "[constraint text]" → candidate glob: [pattern]
```

The `Rule candidates detected` section is **optional** — include it only when Step 4b found keyword constraints or file extension patterns in Skill component bodies. If nothing was detected, omit the section entirely.

## Destination to File Path Mapping

| Destination | File Path Pattern |
|-------------|-------------------|
| CLAUDE.md (direct) | `CLAUDE.md` |
| CLAUDE.md (pointer) | `docs/{name}.md` + pointer in `CLAUDE.md` |
| Rules | `.claude/rules/{name}.md` (with `globs:` frontmatter) |
| Commands | `.claude/commands/{name}.md` |
| Skills | `.claude/skills/{name}/SKILL.md` |
| Sub-agents | N/A (guidance only — recommend agent configuration) |
| Skill companion | `.claude/skills/{name}/reference.md` |

## Notes

- Placement is iterative. Initial placement can be refined later based on real usage.
- When recommending Skills for Cat 4 content that mixes universal pattern + project-specific paths:
  - Recommend the **configurable skill pattern**: separate pattern from config
  - Skill instructions reference config by name ("the domain directory"), not by path
  - Project-specific values go in a YAML `# Configuration` block in SKILL.md
  - The same skill works across projects — only the config block changes
  - Alternative: decompose into Skill (universal) + Rule/CLAUDE.md (project paths)
- Always include rationale referencing the decision framework.
