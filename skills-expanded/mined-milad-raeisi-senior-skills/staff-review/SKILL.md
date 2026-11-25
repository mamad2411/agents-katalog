---
name: staff-review
description: Review code like a staff engineer. Use when asked to review, check, critique, or approve a diff, PR, branch, or file, before opening or merging a PR, when self-reviewing your own changes before declaring them done, and when responding to review comments you received. Prioritizes correctness, security, and data integrity over style; every finding is verified and has a location, a concrete failure scenario, and a severity; feedback received is evaluated on its merits rather than accepted blindly.
license: MIT
metadata:
  category: craft
  version: "1.2.0"
---

# Staff Review

A review's value is the bugs it prevents and the understanding it spreads, not the number of comments. Ten style nits bury the one comment that matters. Review in order of what is most expensive to get wrong, verify each finding before you report it, and be specific enough that the author can act without a follow-up question.

## Before reading the diff

- Understand the intent: the PR description, linked issue, or the user's request. A diff can only be correct *relative to a goal*.
- Get the full diff (`git diff <base>...HEAD`, `gh pr diff <n>`) and the list of touched files. Read the surrounding code too; bugs live where changed code meets unchanged code.

## Review in priority order

1. **Does it do what it set out to do?** Check each requirement against the change. Look for missing pieces: an updated API without updated callers, a new field never written.
2. **Correctness.** Edge cases (empty, null, zero, max, Unicode, time zones), error paths, off-by-one, concurrency and ordering, state transitions (see `state-machine-hunter`), resource cleanup, idempotency of retried operations.
3. **Security and data integrity.** Untrusted input reaching queries, shells, templates, or file paths; missing authorization checks; secrets in code or logs; migrations that can lose data or lock tables (see `security-audit`).
4. **Design.** Does the change fit the codebase's structure? Shallow wrappers, leaky abstractions, duplicated logic, and coupling across modules (see `deep-modules`).
5. **Tests.** Do they test behavior, and would they fail if the change were broken? Are the risky paths covered?
6. **Readability.** Names, comments explaining *why*, unnecessary complexity.
7. **Style.** Only what the linter or formatter doesn't already enforce, and only if it matters.

## Verify every finding

Before reporting a problem, try to prove yourself wrong: read the caller, check whether the edge case is handled elsewhere, and run the code or a test if you can. An unverified "possible issue" costs the author time to disprove. Report things you couldn't confirm as questions, not findings.

## Finding format

```markdown
**[blocker] Refund can be applied twice on retry**: `billing/refund.ts:88`
`processRefund` isn't idempotent: if the HTTP call times out after Stripe accepted it, the job retries and refunds again.
Scenario: Stripe responds slowly (>10s) -> job times out -> retry -> customer refunded twice.
Suggestion: pass the refund ID as Stripe's `Idempotency-Key`.
```

| Severity | Meaning |
|---|---|
| **blocker** | Bug, security hole, or data risk; must be fixed before merge |
| **major** | Likely problem or significant design issue; should be fixed or explicitly accepted |
| **minor** | Real but small improvement |
| **nit** | Optional polish; batch these or skip them |

End with a verdict and summary: approve, approve with nits, or request changes, plus the one or two things that matter most. Mention what's done well when it's genuinely notable; it tells the author what to keep doing.

When many findings appear, prioritize them with `bug-triage` instead of demanding everything. A review reports findings; it doesn't edit the code unless the user asked you to fix it.

## Self-review before declaring done

Read your own diff top to bottom as if a stranger wrote it:

- Debug output, commented-out code, stray files, or unrelated changes?
- Did you update the docs, types, callers, and tests affected by the change?
- Are errors handled and surfaced honestly?
- Would the next person, or agent, understand *why* from the code and commit message?

## Receiving review feedback

- **Evaluate each comment on its merits.** Reviewers can be wrong too. Check the claim against the code before changing anything.
- **Agree when it's right, with no theatre.** Fix it and say what changed. Skip the effusive thanks.
- **Push back with evidence when it's wrong.** "This is handled in `validate()` at line 40; here's the test covering it." Disagreement backed by facts is respectful; silent compliance with a wrong suggestion is not.
- **Clarify ambiguous comments** before implementing a guess.
- Re-run the verification after addressing feedback (see `evidence-before-claims`).
