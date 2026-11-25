---
name: grill-me
description: Alias of grill-me: a relentless interview to sharpen a plan or design. Use when the user wants their plan stress-tested through questions. Not for implementation; it delegates to the grilling skill.
disable-model-invocation: true
---
Call the Skill tool with "grilling".

## Purpose
Alias skill. Sends the session to the `grilling` skill, which interviews the user until a plan or design is sharp.

## When to use
The user asks to be grilled, challenged, or interviewed about a plan or design.

## When NOT to use
- The user wants documents (ADRs, glossary) created as well -> use grill-with-docs.
- The plan is already final and only needs implementing.

## Core workflow
1. Call the Skill tool with "grilling".
2. Follow the grilling skill until the plan has no open questions.

## Validation
- Confirm the grilling skill was actually invoked and the user answered its questions before summarising.

## Output requirements
A sharpened plan or a list of resolved and still-open decisions, as returned by the grilling skill.

## Example
```text
User: "Grill me on this migration plan." -> invoke grilling -> ask one question at a time -> summarise decisions.
```

## Related skills
grilling, grill-with-docs, domain-modeling
