---
name: edge-case-hunter
description: Exhaustive edge-case review that traces branching paths and boundary conditions in a diff or code sample and reports only unhandled cases. Use when the user asks to hunt edge cases, boundary conditions, missing guards, or wants an edge-case-focused review.
---

# Edge Case Hunter Review

## Overview

Perform a strict, method-driven edge-case review. This is not a general code review: report only unhandled paths and boundary conditions.

## Inputs

- `content`: Diff, full file, or function to analyze.
- `also_consider` (optional): Areas to keep in mind while tracing paths.

## Workflow

Follow `references/workflow.md` exactly. Do not add commentary or extra sections. Output must be valid JSON only.

## Output Rules

- Return a JSON array of findings with fields: `location`, `trigger_condition`, `guard_snippet`, `potential_consequence`.
- If none found, return `[]`.
- If input is empty or undecodable, return the required single-item array from the workflow.

## Reference

- `references/workflow.md` for the canonical step-by-step instructions and output format.
