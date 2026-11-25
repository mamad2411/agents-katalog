---
name: yolo-next
description: Use when the user asks what to work on next, what to pick up, or what to prioritize in a YOLO repo. Ranks the backlog from derived status, dependencies, stalled work, open issues and code TODOs, and recommends the top 3 with reasons. Read-only. Triggers on "what next", "what should I work on", "what should I pick up", "yolo next".
---

# yolo-next

Recommend what to do next. Read-only: it never writes briefs, branches or commits. Status
rules: `../../yolo/conventions.md`.

## Gather
1. Derive every feature's status exactly as `yolo-status` does (landed, verified,
   in-progress, planned, cancelled, untracked-branch). Read each active brief's `goal`,
   `milestone` and `depends_on`.
2. For in-progress branches, note the last commit date: `git log -1 --format=%cr feature/<slug>`.
3. Count dependents: how many planned or in-progress briefs list each slug in `depends_on`.
4. Open issues, if a forge CLI is available and authenticated:
   `gh issue list --limit 20` or `glab issue list --per-page 20`. Skip quietly otherwise.
5. Code markers: `git grep -nE 'TODO|FIXME|HACK'` on base, counted per file. Mention only
   clusters, not every line.

## Rank
Apply these in order. Each rule only reorders within what the earlier rules left open.
1. **Finish before starting.** A `verified` feature is one merge from done; it goes first.
2. **Continue live work.** An in-progress branch touched in the last 7 days beats starting
   something new. With 3 or more in progress, recommend only finishing or cancelling, not
   starting.
3. **Decide on stalled work.** In-progress with no commits for 7+ days: recommend
   continuing it or cancelling it (`yolo-brief` cancel). Don't let it sit silently.
4. **Unblock others.** Among unblocked planned briefs, prefer the one with the most
   dependents, then the current milestone (the one with the most features already landed),
   then the oldest `created_at`.
5. **Outside signals.** Bug issues and TODO clusters are candidates for non-feature work.
   Suggest them as plain fixes, not briefs, unless one is clearly a feature.
6. **Untracked branches.** Flag them: brief them or delete them.

## Output
The top 3, each with:
- what: slug or issue, and one line on what it is
- why now: the rule that ranked it, in plain words
- unblocks: dependents, if any
- next step: the exact command or prompt, e.g. `git switch feature/<slug>`,
  "verify <slug>", "merge feature/<slug>", "brainstorm <slug>", "cancel <slug>"

If the backlog is empty, say so, and suggest asking for candidate features based on the
project, its issues and its TODOs.

## Constraints
- Read-only. Recommend; never act.
- Don't invent priorities the data doesn't support. If two options are a coin flip, say so.
