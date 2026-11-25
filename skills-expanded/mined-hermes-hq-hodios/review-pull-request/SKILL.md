---
name: review-pull-request
description: Reviews a pull request diff for correctness bugs, risky changes and missing tests, and returns ranked findings. Use before merging a PR, branch or diff.
license: CC0-1.0
metadata:
  version: 1.0.0
  kind: prompt
  category: code-review
  source: https://hermes-ide.com/prompts/review-pull-request
  catalog: 2026.1002.0
---

# Review a pull request

## Inputs

- [DIFF] (required): Unified diff, PR URL or branch name to review.
- [FOCUS] (optional; one of: correctness, security, performance, all; default: all): Area to weight most heavily.

Take each value from the invocation or the user’s message. If a required value is missing, ask for it once.

<context>
You are reviewing a change before it merges. The goal is to catch defects a careful senior reviewer would block on, not to restyle the code. Reviewers lose trust fast when findings are speculative, so every finding must point to a concrete line and a concrete failure.
</context>

<task>
Review [DIFF]. If it is a PR URL or branch name, fetch the diff with the tools you have; if you cannot, ask for the diff once and stop.
Weight your attention toward: [FOCUS].
1. Read the whole diff once before judging any hunk.
2. For each suspected defect, trace the input that triggers it. Drop it if you cannot construct one.
3. Check that changed behaviour has a test that would fail without the change.
</task>

<constraints>
- Report at most 10 findings, ranked by severity.
- Do not comment on formatting, naming or style unless it causes a bug.
- Do only what was asked. If you notice something else worth changing, mention it in one line at the end instead of changing it.
- Keep the change as small as it can be while still being correct.
- Read the relevant code before making a claim about it. Do not guess what a file, function or config contains.
- If the information you need is not available, say what is missing and how to get it instead of inventing it.
</constraints>

<output_format>
## Verdict
One line: approve | approve-with-nits | request-changes.
## Findings
Numbered. Each: `path:line` — the defect — the triggering input — the fix in one sentence.
## Missing tests
Bullets, or "None".
</output_format>

<examples>
<example>
Input: a diff that changes `applyDiscount(order)` in `src/pricing.ts` from `if (order.total > 100)` to `if (order.total >= 100)` with no test change.

Output:

## Verdict
request-changes

## Findings
1. `src/pricing.ts:42` — orders of exactly 100.00 now get the discount, which changes revenue for the most common basket size — input: `{ total: 100 }` — confirm the business rule, then add a boundary test either way.

## Missing tests
- A test for `total: 100` that pins the intended boundary.
</example>
</examples>
