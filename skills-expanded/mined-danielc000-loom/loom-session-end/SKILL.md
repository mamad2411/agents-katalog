---
name: loom-session-end
description: Use when wrapping up work — "done for now", "wrapping up", "end session", "log this", "save progress". Records progress + decisions on the board task and leaves the work clean and resumable by the next session.
---

# Session End (Loom)

Leave the work picked-up-able by the next session. The board is the source of truth; the vault holds
prose. The daemon auto-commits the vault — never run manual vault git.

## Steps

1. **Update the board task** (`tasks_update`): note what was completed in the body, record decisions +
   their rationale, and add items for what remains. Move the task to its correct column by ROLE
   (review / terminal / parked). Only move to a **terminal** column if it's actually true — scoped work
   outstanding means it isn't done.
2. **Code state** — pushing and merging is the **human-driven/lead path only**. **A worker never pushes
   and never merges** — finish via `/worker` (`worker_report`) instead; see "By role" below. For the
   human/lead path: ensure the build/gate passes; commit only if asked. Report any uncommitted changes
   plainly. When you *do* commit, stage an **explicit list of the paths this session touched**
   (`git add <path> …`) — **never `git add -A` or `git add .`** in a shared workspace: other unrelated
   in-flight work may be present and a blanket stage would sweep it into your commit. Its subject
   follows the card's Conventional-Commits title (`type(scope): summary`). Push with plain `git push`
   (it already refuses a non-fast-forward — there is no valid `--ff-only` push flag); reach for
   `--force-with-lease` only as a deliberate guard when a force is genuinely intended.
3. **Prose** — if you changed design/architecture notes in the project's vault, apply `/loom-doc-hygiene`
   (rewrite in place, no contradictions, bounded).
4. **Living resume doc** (leads) — if you keep one, make sure it's current: what's merged, the
   prioritized backlog, key decisions, where things stand. A successor should be able to read it cold.
5. **Summary** — a short, factual wrap-up: what shipped, what's verified, what's left.

## By role

- **Worker:** finish with `worker_report` — `done` (one-line summary + key decisions) or `blocked`
  (with `needs`). Don't merge; your manager reviews and gates. See `/worker`.
- **Manager near your context window:** hand OFF YOURSELF via `recycle_me`, seeding the successor from
  your living resume doc (`worker_recycle` is for recycling a *subordinate* worker, not yourself). See
  `/orchestrate`.

## Lifecycle close-out

Once the board and code are clean, park the session honestly:

- **Genuinely complete, session should stop:** end it with `end_me` (self-terminal).
- **More to do later, should resume:** `wake_me` (a delay + a note) to park it for a later wake rather
  than leaving it idle.
