---
name: s7-explain-with-diagrams
description: Explain code using visual ASCII diagrams and analogies
disable-model-invocation: true
argument-hint: "<file-or-concept>"
---

# S7 — Explain with Diagrams: `$ARGUMENTS`

Explain the code or concept specified by `$ARGUMENTS` using the structured
template in `templates/explanation-template.md`.

## Instructions

1. **Read the target** — if it's a file path, read the file. If it's a concept,
   find the relevant code in the project.

2. **Follow the template** in the `templates/` subdirectory of this skill.
   Read `templates/explanation-template.md` and fill in each section.

3. **Key requirements**:
   - The analogy must be relatable (kitchen, library, post office, etc.)
   - The ASCII diagram must show data flow or structure
   - The walkthrough must reference specific line numbers
   - The gotcha must be a real pitfall, not a generic warning
