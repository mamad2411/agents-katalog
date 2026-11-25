---
name: change-hygiene
description: Version-control and change-flow discipline — commits, branches, pull requests, code review flow, and history that stays useful. Use when committing, branching, opening or reviewing PRs, resolving merge conflicts, planning how a big change lands, or when the user says "commit", "PR", "pull request", "branch strategy", "git workflow", "merge", or "revert".
---

# Change Hygiene

Version control is not a backup system; it's your project's **memory and undo button**. Every discipline here serves two moments: the reviewer trying to verify your change today, and the debugger (human or AI) trying to understand it at 2 a.m. next year. Sloppy history taxes both, forever — and in AI-assisted development, where code volume is 10×, history hygiene is what keeps the firehose reviewable.

## Commits — the unit of undo

- **One logical change per commit**, and the build passes at every commit. This is what makes `git bisect` a superpower and `revert` a one-liner instead of surgery. "WIP", "fixes", "more changes" commits get squashed before they reach the shared branch.
- The message: subject line says *what* in imperative mood ("Reject payments exceeding invoice balance"), body says **why** and what alternative you rejected — the code already shows the what; only the message can carry the why (same rule as code comments, code-quality). A year later, `git log` on a file should read as the file's biography.
- **Never mix refactoring with behavior change in one commit** — the single most valuable habit in this skill. A reviewer can verify "no behavior change" or "this one behavior changed", never both in one diff (legacy-code-changes, code-quality).
- Commit generated files, lockfiles yes (dependency-discipline); build artifacts, secrets, `.env` no — and anything secret that ever touches history is burned: rotate it (threat-model-security), don't just delete the line.

## Branches — short-lived or they rot

- Branch per change, merged within days. A branch alive for weeks is a merge conflict with interest accruing — the cure is slicing the work smaller (requirements-to-spec Gate 3), not rebasing harder.
- The default branch is sacred: always deployable, protected (no direct pushes, CI required), and never force-pushed. Force-push on *your own unshared* branch is fine and good (clean up before review); on anything shared it's rewriting someone else's memory.
- Big features that can't merge in days: merge them anyway, dark — behind a feature flag, wired but off (deployment-safety). Long-lived feature branches are where integration bugs breed unseen.
- Merge conflicts are resolved by understanding *both* intents, not by picking a side that compiles. After any nontrivial resolution, run the tests for both features' paths — the conflict marker is where two authors' assumptions collided.

## Pull requests — sized for actual review

- **A PR must be reviewable in one sitting** (~400 lines of real diff is the ceiling where review quality collapses; less for dense logic). Bigger work lands as a stack of small PRs, each green and coherent: schema → service → API → UI (the same slicing as ai-build-quality Law 5, because reviewability is the constraint in both).
- The description answers three things before anyone reads the diff: **what** changes for users/callers, **why** now, and **how it was verified** — with evidence (test run output, screenshot, the command you ran), not assurances. "Tests pass" with no output shown is a claim, not evidence.
- Draft PRs for early direction-checks are cheaper than polished wrong PRs. Ask for the review you need ("logic check on the allocation math; skip style").
- Review discipline as the author: respond to every comment (fix, or argue — never silently ignore), and don't push unrelated new work onto a PR under review; that resets the reviewer's mental diff.
- Review discipline as the reviewer: correctness first (code-quality's 3 passes), blocking vs nitpick clearly labeled, and review *promptly* — a stalled review queue quietly sets the team's real velocity.

## Landing and history

- Squash-merge as the default (one PR = one clean commit on main, revertable atomically); preserve individual commits only when they're genuinely independent and each green.
- Tag releases; deploy from tags/SHAs so "what's in production" is a fact, not an investigation (deployment-safety's fingerprint rule).
- **Revert-first culture**: when a landed change breaks things, revert immediately and investigate calmly — a revert is not an insult, it's the undo button working as designed. Fix-forward only when the fix is truly one obvious line or rollback is impossible (root-cause-debugging's incident rule).

## AI-specific hygiene

AI-assisted work tempts two sins this skill exists to block: the **mega-commit** ("implemented the feature" — 40 files, one commit, unbisectable) and the **unread commit** (committing generated code the author never reviewed — the commit is your signature; you're asserting you read it). Slice AI output into logical commits as if a careful human had written it, and never let "the AI wrote it" appear as an implicit excuse anywhere in the history.
