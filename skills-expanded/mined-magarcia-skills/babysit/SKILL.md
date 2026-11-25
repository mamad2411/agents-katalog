---
name: babysit
description: Monitor an open pull request through CI, review feedback, conflicts, draft-to-ready transitions, and merge readiness. Use after opening a PR, when the user says "babysit this PR" or "CI is failing," or as the final stage of $ship.
---

# Babysit

Read the applicable `AGENTS.md` files and repository merge conventions first. Resolve the exact repository and PR before acting.

Loop: observe, classify, act within the user's authorization, wait, and repeat until the requested terminal condition is reached or human input is required. Use the product's wait or monitoring mechanism between polls; do not hold a shell open with long sleeps.

## Observe

- Use `$github:github` for PR metadata, patch context, approvals, and lightweight comment reads.
- Use `$github:gh-fix-ci` for GitHub Actions checks and logs. Do not infer a failure from its check name, and do not imply the GitHub connector exposes Actions logs.
- Use `$github:gh-address-comments` when unresolved thread state, inline anchors, or resolution status matters. Flat PR comments are not a complete view of review threads.
- Use local `git` and bounded `gh` commands only for capabilities the connector does not cover. Confirm `gh` authentication before networked CLI work.

## Act

**CI failures**

- Caused by the PR: reproduce locally, identify the root cause, propose a focused fix, and get approval before editing. Test the approved fix locally before pushing.
- Flaky or unrelated: retry once when reruns are within the requested babysitting scope. The same failure twice is evidence of a real problem.
- Pre-existing on the base branch: verify that claim, report it separately, and do not fix it in this PR.
- Stop after roughly three failed fix-and-push cycles for one root cause. Summarize the evidence instead of stacking speculative fixes.

**Review feedback**

- Classify unresolved threads as a clear change request, question, judgment call, scope change, disagreement, resolved, outdated, or duplicate.
- Use `$github:gh-address-comments` to present actionable threads and confirm which to address unless the user explicitly asked to fix all unresolved actionable feedback.
- Draft answers for questions. Do not post replies, resolve threads, or submit reviews unless the user authorized those GitHub writes.
- Re-request review only when repository convention and the user's requested scope support it.

**Conflicts**

- Follow the repository's merge or rebase convention. Default to merge when no convention exists because rebasing rewrites shared history.
- Use `$resolving-merge-conflicts`; read both sides' commits before resolving and ask when intent is ambiguous.
- Run relevant tests after resolution. A clean textual merge does not prove semantic correctness.

**Draft to ready**

- Mark ready only when required CI is green and no actionable review thread remains.
- Use the reviewer method established by `$pr` if the project assigns reviewers at ready time.
- A request limited to CI investigation does not authorize marking the PR ready.

**Merge**

- Enable auto-merge only when the user asked to get the PR merged, repository policy allows it, checks are green, approvals are complete, and no actionable threads remain.
- Merge directly only when the user explicitly asked for a direct merge. Otherwise report that the PR is ready to merge and stop.
- Run post-merge steps from the applicable `AGENTS.md` files.

Never retry a real failure until green or enable auto-merge with unanswered review feedback.
