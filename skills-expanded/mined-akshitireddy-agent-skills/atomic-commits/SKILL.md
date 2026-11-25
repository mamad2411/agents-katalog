---
name: atomic-commits
description: Create focused, working Git commits with Conventional Commits messages.
---

# Atomic commits

Follow the repository's contribution policy and the user's instructions.
Otherwise use Conventional Commits with an imperative, specific summary:

```text
<type>(<optional scope>): <summary>
```

Common types include feat, fix, refactor, docs, test, build, ci, and chore.
Keep the summary concise; use a body for the problem, behavior, or trade-off
that the diff cannot explain. Mark actual compatibility breaks according to
the repository's release convention.

Each commit should contain one coherent concern and leave a usable state.
Stage only the intended files or hunks and preserve unrelated user changes.
Combine dependent edits when splitting would create a broken intermediate
state. Choose reviewable units rather than a target number of commits.

Run relevant checks before committing. Inspect the staged diff for accidental
files and sensitive content. Include generated files or configuration only
when they are deliberately tracked and required by the repository; exclude
temporary artifacts, credentials, and private machine state.

Committing, pushing, and contacting reviewers have separate side effects.
Carry out each only within the authorization provided for the task.
