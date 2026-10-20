---
name: baton
description: Use when handing off an in-progress session to another agent or a future session — ending a session with unfinished work, "pick up where I left off", passing a task to a fresh agent/another window/codex, running low on context, or persisting intent + learnings before context is lost. Covers both dropping a baton (writing the handoff) and grabbing one (resuming from it).
---

# Baton

## Overview

A relay only works if the baton is passed cleanly. When you hand work to another
agent — a fresh window, a future session, a different model — that runner starts
with **zero of your context**. A baton is a single markdown file that lets them
grab the work and sprint, instead of re-deriving everything you already know.

**Core principle:** capture what the next runner can't reconstruct from the code
or git history — your *intent*, the *dead ends you already ruled out*, and the
*exact next step* — grounded in verified repo state, not your chat narrative.

Two sides to this skill: **Drop a baton** (you're handing off) and **Grab a
baton** (you're picking one up).

## When to Use

**Drop a baton when:**
- A session ends with work unfinished and someone/something will continue it.
- The user says "hand this off", "pick up later", "pass this to another agent".
- You're running low on context and want to checkpoint before it's summarized away.
- You're about to dispatch the rest of the work to a separate agent/session.

**Grab a baton when:**
- Starting work in a repo where a prior session may have left one (check first).

**Don't use for:** a finished task (no handoff needed), or durable architecture
rationale (that belongs in a long-lived design doc, not a baton).

## Where the Baton Lives

Default destination: **`.baton/`** at the repo root — a dedicated folder for
handoffs, created if it doesn't exist. It works in any repo, so there's no other
location to choose.

`.baton/` is local scratch, not committed. The first time you drop a baton,
ensure it's git-ignored — if `.gitignore` doesn't already cover it, add a
`.baton/` line.

Filename: **`<YYYY-MM-DD>-<short-slug>.md`**
(e.g. `.baton/2026-06-13-formula-eval-rounding.md`).

The next agent finds the latest with `ls -t .baton/`.

## The Iron Rule: Verify Before You Write

A baton built from the chat story instead of repo reality is worse than none —
it sends the next runner the wrong way with false confidence. Before writing,
run `git status` and `git branch --show-current` and confirm what is *actually*
committed vs. uncommitted. The "State of play" section must reflect runtime
truth. If reality contradicts the narrative, **the baton documents reality** and
flags the gap.

## Baton Format

Fill every section. If one is genuinely empty, write "none" — don't delete it
(the next runner relies on the shape being consistent).

```markdown
# Baton: <one-line title of the work>

**TL;DR:** <1–3 sentences: what this is, where it stands, the single next action.>

## Intent & Goal
Why this work exists and the desired end state. Include the acceptance
criteria — ideally the exact command/test that must go green.

## State of Play (verified against git)
- Branch: <branch> — confirmed via `git branch --show-current`
- Committed: <what's landed>
- Uncommitted / in flight: <what's in the working tree, from `git status`>
- Verified working: <what you've actually run and confirmed>
- Assumed / unverified: <what you believe but haven't proven>

## Learnings & Landmines
The highest-value section — what the next runner can't get from the code:
- Non-obvious discoveries.
- **Dead ends already ruled out** (so they don't repeat them) and *why*.
- **Do NOT touch** zones and the reason.

## Pointers
- Key anchors: `path/to/file.ts:123` — what's there.
- Relevant docs / prior batons / PRs.
- Commands to get oriented or reproduce: `<cmd>`.

## Next Steps
Ordered, concrete, immediate action first. Not "finish the feature" — the
literal next move.

## Open Questions
Unresolved decisions + your current lean (so they can proceed if no one answers).
```

## Grabbing a Baton (resuming)

1. **Find it:** `ls -t .baton/` — read the newest.
2. **Trust but verify:** re-check "State of play" against real `git status` before
   acting; the repo may have moved since the baton was dropped.
3. **Continue** from Next Steps.
4. **Retire it** when the work lands: delete it if it was only scratch, or fold
   durable learnings into a canonical doc and then delete. Don't let stale batons
   pile up in `.baton/`.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Baton restates the diff | The diff is already in git. Capture intent, dead ends, next step. |
| Built from chat, not `git status` | Verify first — a confidently-wrong baton is worse than none. |
| Vague next step ("continue the work") | Write the literal next action. |
| Dead ends omitted | Naming what *didn't* work is the highest-value content — it saves a full re-derivation. |
| Scattered handoff location | Always `.baton/` at repo root — never elsewhere, or the next agent can't find it. |
| Stale batons pile up | Retire it when the work lands: delete, or fold learnings into a canonical doc. |

## Response Behavior

After dropping a baton, state the exact path written and a one-line summary of
what's in it.
