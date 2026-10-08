---
name: skill-reviewer
description: Critically analyzes an existing `SKILL.md` file against strict technical and instructional standards. Outputs a detailed critique and a letter grade (A-F). Use to audit skill quality.
---

# Skill Reviewer ("The Grader")

## Purpose
To provide an objective, rigorous assessment of an Agent Skill's quality. This ensures that all skills in the system are "Atomic", "Clear", and "Robust".

## When to use
*   When auditing an existing skill for improvements.
*   Before finalizing a new skill to ensure it meets standards.
*   When a skill is failing or producing poor results.

## Rubric (The Standard)

### 1. Atomic Modularity (20%)
*   **Fail:** The skill does two unrelated things (e.g., "Review Code AND Deploy App").
*   **Pass:** The skill does one thing well (e.g., "Review Code").

### 2. Clarity & Instruction (30%)
*   **Fail:** Returns vague instructions like "Do the needful" or "Write good code".
*   **Pass:** Returns specific steps: "1. Open file X. 2. Parse JSON. 3. Handle Error."
*   **Critical:** Must separate "What to do" from "How to do it".

### 3. Formatting & Metadata (20%)
*   **Fail:** Missing YAML frontmatter, broken links, no examples.
*   **Pass:** Valid YAML, `name` matches directory, clear headers, illustrative examples.

### 4. Technical Depth (30%)
*   **Fail:** Uses deprecated libraries, `print` debugging, or insecure patterns.
*   **Pass:** Uses modern libraries (e2.g. `pathlib`), proper logging, and error handling.

## Instructions

1.  **Read the Input:** Analyze the provided `SKILL.md` content.
2.  **Evaluate:** Go through the Rubric above for each section.
3.  **Grade:** Assign a Letter Grade (A, B, C, D, F).
    *   **A:** Perfect. No changes needed.
    *   **B:** Good. Minor tweaks (typos, formatting).
    *   **C:** Acceptable. Functional but lacks depth or clarity. Refactor recommended.
    *   **D:** Poor. confusing instructions, bad code practices. Immediate refactor required.
    *   **F:** Broken. Invalid YAML, missing sections, completely wrong.
4.  **Critique:** Write a structured report listing specific issues and *required fixes*.

## Output Format

```markdown
# Skill Audit: [Skill Name]

**Grade:** [A/B/C/D/F]

## Summary
Brief overview of quality.

## Issues (Must Fix)
1.  [Category] Description of issue 1.
2.  [Category] Description of issue 2.

## Suggestions (Nice to Have)
*   Suggestion 1...
```

