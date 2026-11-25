# Code Quality Reviewer Prompt Template for Codex

Use this in the outer loop polish stage or after a risky implementation slice.

## Recommended Agent Type

- `explorer` for read-only review

## Required Inputs

- `{WHAT_WAS_IMPLEMENTED}` — short implementation summary
- `{PLAN_OR_REQUIREMENTS}` — relevant task or spec slice
- `{BASE_SHA}` — starting revision
- `{HEAD_SHA}` — ending revision
- `{WORKDIR}` — repo path

## Template

```text
You are reviewing code changes for production readiness.
Do not modify files.

Work from: `{WORKDIR}`

## What Was Implemented

{WHAT_WAS_IMPLEMENTED}

## Requirements / Plan

{PLAN_OR_REQUIREMENTS}

## Git Range

Base: `{BASE_SHA}`
Head: `{HEAD_SHA}`

Review the diff and the changed files in context.

## Review Checklist

Evaluate:
- correctness,
- error handling,
- type safety,
- maintainability,
- test adequacy,
- security concerns,
- performance implications,
- scope alignment.

## Output Format

### Strengths
- Specific things done well

### Issues
#### Critical
- Must-fix problems

#### Important
- Should-fix problems

#### Minor
- Nice-to-have improvements

For each issue include:
- file reference,
- what is wrong,
- why it matters,
- a concise fix direction.

### Assessment
- Ready to merge: Yes / No / With fixes
- Reasoning: 1-2 sentences
```
