---
name: squad-review
description: Request repository-approved independent review with a self-contained briefing. Includes premise-validation latitude and working-tree hygiene clauses.
argument-hint: "<ITEM-ID>"
allowed-tools:
  - Bash
  - Read
  - Task
paths:
  - ".squad/items/**"
disable-model-invocation: true
---

You are requesting code review for item `$ARGS`. Invoke the `squad-code-review-mandatory` skill to construct the briefing correctly, use the repository-approved mechanism available in the selected runtime.
Optional `superpowers` helpers are not a universal client prerequisite; preserve
any required managed model/Check and the existing single-flight review.

First, post the request to the item thread:

```bash
squad review-request $ARGS
```

Then spawn the reviewer with a self-contained briefing. The reviewer does not see this conversation; the prompt must include:

- **Item file path:** `.squad/items/$ARGS-*.md` — the `## Acceptance criteria` is the contract.
- **The diff:** paste `git diff main...HEAD` inline if small, otherwise give the command.
- **Specific concerns:** any area you want them to focus on.
- **Output format:** prioritized findings (Critical / High / Medium / Low) with file:line and suggested fix per finding.
- **Premise-validation latitude:** "If the claimed failure seems dubious, verify it against pre-fix code in an isolated disposable checkout when the review contract permits execution. Never revert or patch the author's checkout or frozen input. Report non-reproduction or an unverified premise with evidence; a snapshot-only review stays within its supplied bundle."
- **Working-tree hygiene:** "The author's checkout and review tuple are read-only. Keep permitted experiments in an isolated disposable checkout; clean up only your own test artifacts. A client that shares the working directory does not grant shared-file mutation authority."

When the reviewer returns, evaluate each finding against evidence (the `superpowers` receiving helper is optional). Do not perform-agree. Verify each one, push back on the wrong ones with evidence, file out-of-scope findings as fresh items.
