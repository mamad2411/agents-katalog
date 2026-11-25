---
name: pull-request-prep
description: "Prepares a review-ready pull request by checking scope, diff quality, tests, documentation, and risk, then drafting an evidence-based title and description. Use before opening or updating a PR."
license: MIT
metadata:
  author: OpenSelfHosting
  version: "1.0.0"
---

# Pull Request Preparation

## Goal
Make a change easy to review, test, and merge without hiding uncertainty or making unsupported claims.

## Workflow
1. Read repository contribution instructions, PR template, and applicable branch/release conventions.
2. Inspect the working tree, staged and unstaged changes, and intended base. Preserve user changes and include only changes in scope.
3. Summarize the purpose in one sentence. Group implementation changes into logical units and check for generated files, debug output, secrets, unrelated formatting, temporary artifacts, and accidental binary changes.
4. Verify behavior and appropriate quality checks. Run commands selected from the repository docs. Record actual results; do not infer that checks pass because they are configured in CI.
5. Confirm test coverage for the behavior, error cases, backward compatibility, migration, and security implications as relevant.
6. Update docs, changelog, screenshots, API/schema references, or migration notes where the project expects them.
7. Check whether the change alters deployment behavior, environment variables, permissions, data storage, external services, or public contracts. State rollout and rollback notes where needed.
8. Draft a concise title in the project's style and a description that covers context, solution, alternatives/tradeoffs if important, tests, and risks.
9. Add explicit unresolved questions and mark checks not run with reasons. Do not invent issue numbers, approvals, links, benchmark data, or CI outcomes.
10. If tools can open/create a PR, do so only when the user requested that action and the base/head/repository are unambiguous. Otherwise provide the draft only.

## Suggested PR description
- **Why:** problem and user impact.
- **What changed:** key implementation decisions.
- **Validation:** commands run and actual results.
- **Risk / rollout:** compatibility, migration, flags, deployment, or rollback notes.
- **Follow-up:** known limitation or deferred work, if any.

## Final checklist
The diff is scoped, tests exercise behavior, docs match implementation, secrets are absent, breaking changes are disclosed, and the description does not overclaim.
