---
name: ares-pr-gate
description: Gate commits, PR approvals, and merges on ARES. Reviews all pending changes against the repo's learned conventions and BLOCKS committing/approving/merging until conflicts are resolved or a human explicitly approves. Use before any git commit, git push, PR approval, or merge performed by an agent.
---

# ARES PR gate

No agent may commit, approve, or merge code until it has passed ARES review.
This is a hard gate, not a suggestion.

## When this applies
Before any of: `git commit`, `git push`, approving a PR, or merging.

## Review workflow

```
- [ ] 1. Resolve repo_id (owner/repo, lowercase) from `git remote get-url origin`
- [ ] 2. ares.ensure_repo_memory({ repo })
- [ ] 3. Collect the diff: `git diff --staged` (or the PR diff)
- [ ] 4. For each changed file, ares.check_conflict({ repo, intent, snippet })
        where snippet = the added/changed lines and intent = one line on what it does
- [ ] 5. Aggregate conflicts and decide the verdict
```

## Verdict

- **APPROVED** — no conflicts (or all below 0.6 confidence): proceed.
- **CHANGES REQUESTED** — any conflict: **STOP. Do not commit, push, approve, or
  merge.** Present each conflict:

  ```
  🔴 BLOCKED by ARES
  - <decision statement>  [decision_id]
    reason: <conflict reasoning>  (confidence X.XX)
    source: <decision source_url>
  ```

  Then either fix the code and re-run, or ask the user to explicitly approve the
  override. Only after approval, record it via `ares.record_decision` and proceed.

## Hard rules
- Never finalize a commit/approval/merge with unresolved conflicts and without
  explicit human approval.
- If ARES is unreachable, report it and ask the user; do not silently bypass.
