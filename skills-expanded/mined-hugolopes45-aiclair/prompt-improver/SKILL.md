---
name: prompt-improver
description: Enriches vague prompts with intent classification, targeted questions, and a rewritten prompt suggestion.
---

# Prompt Improver Skill

## When Invoked

- Hook has already flagged the prompt as vague
- Proceed directly — do not re-evaluate vagueness

## Core Workflow

### Phase 1: Research

Check conversation history first. If it provides enough context, skip codebase exploration.

If insufficient:
1. Explore codebase structure (Task/Explore, Grep/Glob, git log)
2. Search for errors, failing tests, TODO/FIXME markers
3. Ground all questions in findings — never ask about things not observed

### Phase 2: Structured Output

Deliver exactly 3 parts:

**Part 1 — Why flagged + detected intent**
- State the specific gap: missing Clarity / Specificity / Context
- State the detected intent: CREATE | TRANSFORM | REASON | DEBUG | AGENTIC

**Part 2 — Targeted questions**
- 1-2 questions: simple ambiguity (which file? which approach?)
- 3-4 questions: moderate complexity (scope + approach + validation)
- 5-6 questions: multiple unknowns

Each question:
- Grounded in research findings
- Concrete options (2-4), no "other" vagueness
- One decision point per question

Use `AskUserQuestion` tool:
- `question`: specific, ends with `?`
- `header`: max 12 chars
- `multiSelect`: false unless choices are non-exclusive
- `options`: 2-4 concrete choices from research

**Part 3 — Rewritten prompt suggestion**
- Provide a concrete rewritten version of the original prompt
- Apply detected intent pattern (e.g., for DEBUG: include error, file, expected vs actual)
- Skip if the prompt is a one-liner that questions will fully resolve

### Phase 3: Execute

Proceed with original intent using answers and research findings.

## References

Load only when needed:
- [Question patterns](references/question-patterns.md)
- [Research strategies](references/research-strategies.md)
- [Examples](references/examples.md)
