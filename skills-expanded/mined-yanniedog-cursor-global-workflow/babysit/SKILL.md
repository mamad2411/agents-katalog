---
name: babysit
description: >-
  Keep one open PR merge-ready: triage CI, conflicts, and review comments.
  babysit skill etc must always address PR bot feedback where appropriate.
---

# Babysit

Own **one open PR** until it is squash-merged (or the user waives in writing).
Use with `pr-fix-agent` for the full ship bar (`WORKFLOW.md` steps 4–7).

## Non-negotiable

**babysit skill etc must always address PR bot feedback where appropriate.**

That means every babysit / pr-fix / ship-bar loop:

1. Fetches bot and human review threads (not only CI status).
2. Treats substantive findings as merge-blocking until dispositioned.
3. Posts a `## Feedback plan` (implement / defer / decline) when any substantive threads exist.
4. Replies in-thread with `implemented in <sha>` / `deferred — <reason>` / `declined — <reason>`.
5. Resolves threads after the reply.
6. Re-runs `npm run pr:bot-feedback-check -- --pr <n>` until exit 0 (unless the repo gate explicitly skips that PR class — e.g. mobile-auto-release — **and** there are still no substantive threads left open).

Green CI alone is never enough. Do not enable auto-merge and walk away while substantive bot threads remain unanswered.

## What is “appropriate”

| Handle (required disposition + resolve) | Resolve without disposition text |
|-----------------------------------------|----------------------------------|
| Inline file comments proposing a code/doc/test change | Pure walkthrough / summary-only bot posts (still resolve) |
| P1/P2 / “actionable” / “potential issue” findings | Quota / rate-limit / “react with thumbs” noise — omit disposition reply only after resolve; unresolved still fails the gate |
| CI failures tied to the PR head | Duplicate threads already answered on the same finding — still resolve each thread (and reply if that thread lacks a closure) |
| Human review requests | |

When unsure, disposition the thread (`declined — <reason>` is valid) rather than ignoring it. Do not leave duplicates or low-signal threads unresolved unless the feedback gate explicitly implements a skip for that class.

## Loop

```sh
gh pr view <n> --json title,state,headRefName,statusCheckRollup
gh pr checks <n>
npm run wait-for-bots -- --pr <n>          # re-run while exit 2
# After exit 0: read ALL threads → Feedback plan → implement push → in-thread replies → resolve
npm run pr:bot-feedback-check -- --pr <n>  # must exit 0 before merge
npm run pr:merge -- --pr <n>               # or repo arm-and-park wrapper
```

After later pushes, re-scan for **new** bot threads and repeat disposition before merge.

## Anti-patterns

- Merging or arming auto-merge on “CI green” with open substantive bot threads.
- Skipping the Feedback plan because bots are “advisory”.
- Closing unresolved threads without an in-thread disposition.
- Treating auto-release / generated PR skip of `wait-for-bots` as a waiver of **open** substantive threads.

## Related

- Shared contract: `WORKFLOW.md` step 6, `rules/respond-to-each-review-comment.mdc`, `rules/pr-review-bot-replies.mdc`
- Peer role (by name only): pr-fix-agent — full ship-bar owner for one PR
