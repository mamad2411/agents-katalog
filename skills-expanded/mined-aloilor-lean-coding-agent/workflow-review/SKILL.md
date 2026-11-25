---
name: workflow-review
description: Orchestration workflow for code reviews, audits, or risk assessments.
disable-model-invocation: true
---

# Code Review Workflow

Orchestrated by the main agent. Follow the shared scaffolding in `AGENTS.md` — **Workflow Delegation**, **Standard Artifacts**, and **Shared Stop Conditions** — and never run this workflow from a subagent.

This is a review-only workflow. It does not draft a plan or run `$lean-grill-with-docs`; the mandatory grill gate applies to the planning, feature, refactor, and bug-fixing workflows.

Every review run produces a durable pass artifact at `.agents/code-reviews/review_YYYYMMDD_<name>_pass_N.md`.

## Steps

1. Spawn `code-reviewer` to review the requested scope and record the pass at `.agents/code-reviews/review_YYYYMMDD_<name>_pass_N.md`.
2. Report findings first, ordered by severity, with file/line references when available.
3. Do not make edits, run `implementer`, or enter a fix loop unless the user explicitly asks to fix the findings.

In the final response, link the review artifact and state the verdict, coverage, residual risks, and omissions.
