---
model: opus
description: Rapid spec development for simpler tasks. Deep codebase analysis with opinionated recommendations and max 10 targeted questions. Use instead of spec-elicitation for straightforward features, refactors, and well-understood work.
argument-hint: <feature-description> [output-path.md]
allowed-tools: [Read, Write, Edit, Glob, Grep, AskUserQuestion, Task]
---

<objective>
Rapidly develop a focused specification for $1 by deeply understanding the codebase first, making informed assumptions, and asking only the most critical clarifying questions (max 10).

Output spec will be written to $2 (defaults to `spec.md` if not provided).

Unlike full spec-elicitation, this command is opinionated — it analyzes the codebase, infers conventions, and recommends approaches rather than asking about every dimension. Questions are reserved for genuinely ambiguous decisions where assumptions would be risky.
</objective>

<context>
Feature/task to specify: $1
Output file: $2 (default: `spec.md`)
Project root contents: !`ls -1 | head -30`
Package info: !`for f in package.json pyproject.toml Cargo.toml requirements.txt go.mod; do [ -f "$f" ] && echo "=== $f ===" && head -30 "$f"; done 2>/dev/null`
Existing spec check: !`[ -n "$2" ] && target="$2" || target="spec.md"; [ -f "$target" ] && echo "Existing spec found at $target:" && head -20 "$target" || echo "No existing spec at $target"`
</context>

<process>

## Phase 1: Deep Codebase Analysis (Silent)

Before asking ANY questions, thoroughly explore the codebase to understand:

1. **Project structure** — frameworks, languages, patterns, directory layout
2. **Existing conventions** — naming, architecture, state management, error handling
3. **Related features** — how similar functionality is already implemented
4. **Data models** — existing entities, schemas, relationships
5. **Integration patterns** — how services communicate, API patterns, auth flows
6. **Testing patterns** — what test frameworks are used, coverage expectations

Use Glob, Grep, and Read tools extensively. The goal is to answer as many spec questions yourself as possible through codebase analysis before involving the user.

## Phase 2: Form Opinionated Recommendations

Based on codebase analysis, draft recommendations for:

- **Architecture approach** — where new code should live, what patterns to follow
- **Data model changes** — new entities/fields needed, based on existing schema conventions
- **API design** — endpoints/interfaces following existing patterns
- **Error handling** — matching existing project error strategies
- **Testing approach** — matching existing test patterns and coverage levels

Document your assumptions. You will present these alongside your questions.

## Phase 3: Targeted Interview (Max 10 Questions)

Using AskUserQuestion, ask ONLY questions that meet this bar:

> "Would a wrong assumption here cause significant rework or a fundamentally broken design?"

**Question selection rules:**
- Ask about **intent and scope** — what exactly should this do and NOT do
- Ask about **ambiguous business logic** — rules that can't be inferred from code
- Ask about **user-facing decisions** — UX choices with multiple valid approaches
- **DO NOT ask about** technical implementation details you can infer from the codebase
- **DO NOT ask about** conventions already established in the project
- **DO NOT ask about** edge cases you can handle with sensible defaults

**Question format:**
- Lead with your recommendation: "I'd recommend X because [codebase evidence]. Sound good, or do you have a different preference?"
- Use multi-choice with your recommended option marked
- Batch related questions into a single AskUserQuestion call (up to 4 per call)
- State assumptions you're making so the user can correct any that are wrong

**Hard limit: 10 questions maximum across all rounds.** Budget them wisely:
- Round 1 (3-4 questions): Core scope and intent
- Round 2 (3-4 questions): Key design decisions informed by Round 1 answers
- Round 3 (2-3 questions): Final clarifications only if truly needed
- Stop early if you have enough clarity

## Phase 4: Spec Generation

Synthesize codebase analysis + user answers into a focused spec.

Determine the output path: if $2 was provided, use that; otherwise default to `spec.md` in the current directory. If an existing spec file is found at that path, update it rather than overwriting.

Write to the spec file:

```markdown
# [Feature/Product Name]

**Created:** [timestamp]
**Status:** Draft
**Type:** Quick Spec

---

## Summary

[2-3 sentences: what this is, why it matters, and the core approach]

---

## Scope

### In Scope
- [Specific deliverable 1]
- [Specific deliverable 2]

### Out of Scope
- [Explicit exclusion 1]
- [Explicit exclusion 2]

---

## Requirements

### Core Functionality
1. [Requirement with acceptance criteria]
2. [Requirement with acceptance criteria]

### Business Rules
| Rule | Description |
|------|-------------|
| [Name] | [What it does] |

---

## Technical Approach

### Architecture
[Where new code lives, what patterns to follow — based on codebase analysis]

### Data Model Changes
[New/modified entities, following existing schema conventions]

### Key Implementation Notes
- [Important technical decision and rationale]
- [Convention to follow from existing codebase]

---

## Edge Cases & Error Handling
| Scenario | Behavior |
|----------|----------|
| [Edge case] | [How to handle — following existing patterns] |

---

## Assumptions Made
1. [Assumption and reasoning — user can flag if wrong]
2. [Assumption and reasoning]

---

_Quick spec generated through rapid elicitation with codebase-informed recommendations._
```

Present a brief summary and ask if any section needs revision.
</process>

<success_criteria>
- Codebase deeply analyzed before any questions asked
- Maximum 10 questions asked total (fewer is better)
- Each question leads with a recommendation rather than being open-ended
- Assumptions clearly documented so user can correct any that are wrong
- Spec follows existing project conventions discovered during analysis
- Spec written to file, not just displayed
- Spec is focused and actionable — ready for implementation
</success_criteria>