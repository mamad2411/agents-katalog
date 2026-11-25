---
name: review-spec
description: Review a spec file from a QA perspective: weak assertions, missing coverage, implementation-focused tests. Use when the user runs /review-spec or asks for a review of their tests.
---

# /review-spec — Review a Spec from a QA Perspective

**Type:** Quality
**Description:** Reviews a spec file from a QA perspective, flagging weak assertions, missing coverage, and implementation-focused tests. Built for Persona 2 and 3.

---

## Input Format

- A path to a spec file (or a pasted spec)

## Output Format

A structured review:
- **Strengths** — what the spec does well
- **Findings** — each issue with severity (blocker / major / minor), location, and a concrete fix
- **Missing coverage** — scenarios not yet tested (negative / edge)
- **Verdict** — ship / revise

## Step-by-Step Instructions

1. Read the spec and its Page Object(s).
2. Read the spec conventions in CLAUDE.md.
3. Evaluate against QA quality criteria:
   - **Assertion strength:** Are assertions meaningful, or just `toBeVisible()` everywhere? Do they verify the actual outcome?
   - **Behavior vs implementation:** Does it test what the user experiences, or internal/DOM details? (Common Persona 3 mistake.)
   - **Coverage:** Are Happy Path, Negative, and Edge cases all present and non-trivial?
   - **Structure:** AAA comments, plain-language names, fixture usage, no logic in `describe`.
   - **Isolation:** No order dependencies or shared mutable state.
4. List findings with severity, exact location, and a concrete fix each.
5. Call out missing scenarios explicitly and suggest `/new-spec` or `/tc-to-spec` to fill them.
6. Give a clear verdict.

## Rules

- Be specific — cite line locations and propose concrete fixes.
- Favor behavior-focused assertions over implementation checks.
- Do not rewrite the whole file unless asked; this skill reviews. Offer `/refactor` for big rewrites.
