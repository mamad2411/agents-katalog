---
name: pr-triage
description: Triage a stack of open pull requests into review / merge / close buckets with a clear next action for each.
---

# PR Triage

> Unofficial, agentstack-authored. Not affiliated with or endorsed by GitHub.

Use this skill when there are more open pull requests than anyone can review at
once and you need to decide what to do with each.

## Workflow

1. List the open PRs with author, age, CI status, and review state.
2. Sort each into exactly one bucket:
   - **Merge** — approved, green CI, no unresolved threads. Ready now.
   - **Review** — needs a human pass; note who should look and why.
   - **Changes** — failing CI or open review comments; the ball is with the author.
   - **Close** — stale, superseded, or abandoned. Say what supersedes it.
3. For each PR, write one line: bucket, the single next action, and the owner.
4. Surface the critical few first: small approved PRs that can merge immediately,
   then anything blocking other work.

## Conventions

- Prefer unblocking small, ready PRs before starting large reviews.
- Do not merge or close anything automatically — produce the plan and let a human
  confirm.
- Flag PRs older than two weeks with no activity as close candidates, but verify
  before recommending closure.
