---
name: security-review-before-commit
description: Run a security compliance review on code changes before commit by evaluating the diff against the security rules. Use when the user asks for a security review before commit or when preparing to commit code.
---

# Security review before commit

## Mandatory for deploy workflow

This skill is part of the mandatory deploy workflow. When the user says "deploy" or "deploy all", run this skill (and the architecture review per `.cursor/references/beacon-architecture-rules.md` for Beacon-based apps, or project-specific architecture doc) before every commit and deploy. All code must pass security and architecture reviews before the deploy script is run.

## When to use

- User asks to "run security review on my changes" or "check security before commit."
- You are about to recommend committing or to run commit; run this skill first.

## Steps (execute in order; do not skip or substitute)

1. **Get the current code changes.** Run `git diff` for unstaged changes and `git diff --staged` for staged changes. Include both if relevant.
2. **Evaluate the diff against the security rules.** Read `.cursor/references/security-rules.md` and, for Beacon/Beacon-based apps, `.cursor/references/beacon-architecture-rules.md`. For each rule that applies to the changed code, check the diff for compliance. Note any violations (rule + location + finding).
3. **Produce a compliance report.** Set result to **PASS** if there are no violations, **FAIL** if there are one or more violations. The report must include: Result (PASS/FAIL), Rules checked, Violations (if any), Recommendation (OK to commit / do not commit and list issues to fix).
4. **Apply the report result.** If PASS: you may recommend commit; optionally summarize. If FAIL: do not recommend commit; list violations and remediation; offer to fix or note user-approved exceptions.

## Output to user

Show the compliance report: Result (PASS/FAIL), number of findings, and either "OK to commit" or the list of issues to fix. Do not recommend commit until the report is shown.
