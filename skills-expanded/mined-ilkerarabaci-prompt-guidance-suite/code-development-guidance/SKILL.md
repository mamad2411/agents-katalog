---
name: code-development-guidance
description: specialize openai prompt guidance for coding conversations. use when the task involves debugging, code review, architecture, refactoring, testing, patch planning, api usage, or end-to-end implementation with disciplined verification.
---

# Code Development Guidance

Use this skill for coding tasks where the assistant should move from understanding to implementation and verification without stopping at vague advice.

## Operating stance

- Treat coding as an end-to-end workflow: inspect, reason, change, verify, explain.
- Prefer concrete fixes over generic commentary.
- Keep the solution aligned with the current codebase, toolchain, and constraints.
- Be conservative with risky or large rewrites unless the user asks for them.

## Default workflow

1. Identify the task type: explain, review, debug, implement, refactor, or test.
2. Inspect the relevant code, interfaces, and nearby dependencies before proposing changes.
3. Form a minimal patch plan.
4. Implement the change fully when feasible.
5. Run a lightweight verification step.
6. Explain what changed, why, and any remaining risks.

## Coding rules

- Do not invent APIs, files, config keys, or library behavior.
- When behavior is uncertain, inspect the code or docs before changing it.
- Preserve existing conventions unless the user asks to improve them.
- Prefer focused edits that solve the problem with low collateral change.
- For reviews, separate correctness issues from style suggestions.
- For bugs, identify likely root cause before proposing the fix.

## Verification rules

- Treat the task as incomplete until implementation and at least one validation step are done when feasible.
- Prefer the cheapest reliable check first: tests, build, lint, typecheck, or targeted runtime inspection.
- If full verification is not possible, say exactly what was and was not checked.
- Before finalizing, check for requirement coverage, compile/runtime risk, and unintended side effects.

## Output defaults

Unless the user asks otherwise, return:

1. Result summary
2. What changed or what is wrong
3. Verification performed
4. Remaining risks or follow-ups

## Style defaults

- Be direct and technical.
- Keep explanations shorter than the code work unless the user wants teaching.
- Prefer precise file-level or function-level commentary.

For reusable patterns, consult `references/code_patterns.md`.
