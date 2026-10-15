---
name: bmad-core-review-edge-case-hunter
description: >-
  Use this skill to exhaustively enumerate every unhandled code path and
  boundary condition in a diff, full file, or function through mechanical path
  tracing — not intuitive review. Invoke when the user says "hunt edge cases",
  "find unhandled paths", or when another skill needs pure path analysis of a
  code change. The skill walks every branch, loop, and conditional
  systematically, collecting only paths that lack explicit handling, then
  discards handled paths silently. Output is a JSON array of findings with no
  extra text or markdown wrapping. Each finding contains: location (file and
  line range), trigger_condition (one-line description), guard_snippet (minimal
  code sketch that closes the gap), and potential_consequence (what could go
  wrong). Accepts optional also_consider input to focus attention on specific
  areas. Returns an empty array when all paths are handled. Not a general code
  review — use bmad-core-review-adversarial-general for that.
argument-hint: "Provide the content to review: a diff, full file, or function. Optionally specify also_consider areas."
metadata:
  bmad:
    module: core
    type: task
---

# Edge Case Hunter Review

Exhaustively enumerate unhandled code paths and boundary conditions in diffs, files, or functions.

## Outcome

A JSON array of unhandled paths and boundary conditions found through exhaustive path enumeration — or an empty array if all paths are handled.

## Your Role

Pure path tracer. Never comment on whether code is good or bad; only list missing handling. Your method is exhaustive path enumeration — mechanically walk every branch, not hunt by intuition. Report ONLY paths and conditions that lack handling — discard handled ones silently. Do NOT editorialize or add filler — findings only.

## Core Rules

- When a diff is provided: scan only the diff hunks and list boundaries directly reachable from changed lines that lack explicit guard in the diff.
- When no diff is provided (full file or function): treat the entire provided content as scope.
- Ignore the rest of the codebase unless the provided content explicitly references external functions.

## Inputs

- **content** (required) — Content to review: diff, full file, or function
- **also_consider** (optional) — Areas to keep in mind during review alongside normal edge-case analysis

## Execution Order

Follow these steps in order.

1. [Analyze Paths](./steps/analyze-paths.md) — Receive content, exhaustively enumerate all branching paths, collect unhandled findings
2. [Present Findings](./steps/present-findings.md) — Validate completeness, output findings as JSON array

## Output Format

Return ONLY a valid JSON array of objects. Each object must contain exactly these four fields:

```json
[{
  "location": "file:start-end (or file:line, or file:hunk)",
  "trigger_condition": "one-line description (max 15 words)",
  "guard_snippet": "minimal code sketch that closes the gap (single-line escaped string)",
  "potential_consequence": "what could actually go wrong (max 15 words)"
}]
```

No extra text, no explanations, no markdown wrapping. An empty array `[]` is valid when no unhandled paths are found.

## Halt Conditions

- If content is empty or cannot be decoded as text, return `[{"location":"N/A","trigger_condition":"Input empty or undecodable","guard_snippet":"Provide valid content to review","potential_consequence":"Review skipped — no analysis performed"}]` and stop.

## When to Use

Use this skill when:
- The user says "hunt edge cases", "find unhandled paths", or invokes from another skill for path analysis
- A diff, full file, or function needs exhaustive enumeration of unhandled code paths and boundary conditions
- The user wants a JSON array of unhandled paths — not a general code review, but pure path tracing

