---
name: code-review-rubric
description: Severity-tagged code review format used by the MortgageCheck pipeline. Defines [blocker]/[important]/[suggestion]/[nit] tags and the CODE-REVIEW.md structure (Summary, Acceptance-Criteria checklist, Findings grouped by severity). Use when writing or grading a code review report for this codebase.
metadata:
  version: "1.0"
---

# Code review rubric

This skill defines the format every `CODE-REVIEW.md` in this repo must follow. It is consumed by the `code-reviewer` sub-agent and can also be used to grade a review written by a human or another agent.

## Severity tags

Every finding is tagged with exactly one of these. The tag goes in square brackets at the start of the finding line.

- **`[blocker]`** — must fix before merge. Use for: correctness bugs, security issues, broken acceptance criteria, anything that would cause a regression in production. If you tag something `[blocker]`, you are saying the merge should not happen until it is resolved.
- **`[important]`** — should fix before merge. Use for: significant maintainability concerns, missing test coverage on a critical path, API design issues that will be costly to change later. Not a hard stop, but worth holding the merge for.
- **`[suggestion]`** — worth considering. Use for: refactoring ideas, naming improvements, alternative approaches that are arguably better but not clearly so. The author may take it or leave it.
- **`[nit]`** — purely stylistic, optional. Use for: whitespace, comment wording, trivial preferences. The author can ignore these without explanation.

Calibration rule of thumb: if you cannot articulate what would break if the finding is ignored, it is not a `[blocker]`. If you find yourself tagging more than two things `[blocker]` in a small change, re-read each one and downgrade where the failure mode is speculative.

## CODE-REVIEW.md structure

Every review file has these three sections in this order. No others, no preamble.

### 1. Summary

One to three sentences. State the overall assessment ("ship it", "ship with the two blockers fixed", "needs rework") and the single most important reason. This is the only part many readers will read; make it count.

### 2. Acceptance Criteria

A checklist mirrored from `FEATURE-REQUEST.md`. For each acceptance criterion, one of:

- `- [x] <criterion text> — <one-line evidence: file:line or test name>`
- `- [ ] <criterion text> — <one-line reason it is not met>`

If the feature request has no explicit acceptance criteria, derive them from the requirements and say so in the section opener.

### 3. Findings

Grouped by severity, in this order: Blockers, Important, Suggestions, Nits. Skip a group entirely if it has no entries (do not write "None"). Each finding is a single bullet:

```
- [<severity>] <file>:<line> — <what is wrong and the suggested fix>
```

Keep each finding to one or two sentences. If you need more, link out to an explanatory paragraph below the list rather than bloating the bullet.

## Example finding

```
- [important] lib/calculations.ts:142 — `evaluateStressTest` reuses `monthlyIncome` from the caller's scope but does not validate it is positive; a zero-income input would produce `Infinity` here. Suggest adding an early return or asserting `monthlyIncome > 0` at the top of the function.
```

## What this rubric does NOT cover

- It does not post the review to a forge (GitHub, GitLab). The output is a Markdown file the team — or a separate downstream agent — can act on.
- It does not run tests, lint, or any tool. It is a format spec for a human-readable artifact.
- It does not include line-by-line diff annotations. The granularity is one finding per concrete issue, with a `file:line` pointer.
