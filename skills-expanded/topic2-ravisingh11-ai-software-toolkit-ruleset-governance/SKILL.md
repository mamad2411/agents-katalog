---
name: ruleset-governance
description: "Design, review, and apply GitHub rulesets for branch and tag protection, required checks, signed commits, force-push blocking, file restrictions, and configurable approval policy. Use when asked to harden merge rules, protect main, or standardize rulesets across repositories."
---

# Ruleset Governance

Use this skill for GitHub branch, tag, and push ruleset design.

## Workflow

1. Inspect current branch protection, rulesets, default branch, required checks, bypass actors, and repository risk tier.
2. Choose the lightest rule that protects the repo without slowing solo development.
3. Prefer evaluate or warn-first rollout for broad org changes unless the user explicitly asks for enforcement.
4. Apply strict rules only where checks are stable and recovery paths are clear.
5. Re-read ruleset state after changes.

## Recommended Solo-Developer Baseline

- Block force pushes and branch deletion on `main`.
- Require pull requests for changes to `main`.
- Require status checks only when validation is stable and available to the repository.
- Require zero approving reviews by default so a single developer can merge a
  PR without self-approval.
- Raise the approval count to `1` or more when multiple engineers or higher-risk
  review requires it.
- Do not configure a standing owner/admin bypass. Any emergency exception must
  be narrowly scoped, auditable, and documented.
- Do not require checks from a CI system that the repository has not adopted.

## Decision Rules

- Do not require signed commits org-wide without confirming the user's signing setup.
- Do not require a check that is flaky, missing, or named inconsistently.
- Do not require runner-backed checks if the repo does not have reliable runner capacity.
- Do not apply release/tag restrictions to repos that do not publish releases.
- Keep ruleset names explicit: `main-safety`, `release-tags`, `push-hygiene`.

## References

- GitHub ruleset rule types: `references/ruleset-baseline.md`
