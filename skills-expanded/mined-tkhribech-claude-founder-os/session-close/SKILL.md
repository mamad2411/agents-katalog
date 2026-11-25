---
name: session-close
description: Use at the end of any substantial working session — when the founder says "done for the day", "wrapping up", "let's close out", or when a long session ends with work in flight. Captures this session's corrections and decisions into the memory tree, writes the handoff file, updates pending tasks, and leaves the workspace clean for the next session's cold start.
---

# Session Close — write the baton

The read-back half of this is the session-start block in `START-HERE.md`; this skill is the write half. Its one job: make the next session start from *knowledge*, not from zero. Run the steps in order.

## Hard rules (apply to every step)

- **Memory-only.** No live-system changes at close — read, capture, organize, write files. Nothing outward-facing.
- **Capture durable signal only.** A one-off ask (a quick draft, a single lookup) stays chat-only — no memory file for it or for the people/tools it mentioned once. Persist only reusable knowledge and things the founder will reference again. Unsure → skip; over-capturing creates orphans.
- **Delete, don't archive.** Superseded or empty files go to the system trash — no `-old` copies, no archive folders in the workspace; stale archives are how dead rules get trusted as current. Merge nuance into the survivor first.
- **Verify, don't assert.** Any "clean/confirmed" claim in the close summary must be backed by a command actually run this session.
- **Date-stamp** everything touched (first line = today, absolute date).

## Steps

1. **Inventory today's touches.** List the files created or edited this session (from the session itself, not just filesystem timestamps).
2. **Capture the signal — THE anti-repeat step.** Extract from this conversation: (a) every correction the founder made or better-way that got confirmed → a dated file in `memory/feedback/` (body: the incident, **Why:**, **How to apply:**); (b) every durable decision or ruling → update the matching file in `memory/RULES.md` / `memory/project/`, dated. Search for an existing file first — update it rather than spawning a near-duplicate.
3. **Consolidate duplicates.** If today produced two files covering one fact, merge into the canonical one (full-read both first), fix inbound links, trash the loser.
4. **Index for next session.** Add one-line pointers for today's new items to `memory/MEMORY.md` (rolling headline + the relevant anchor), and bump its date. If the index is over its size cap, compress the oldest entries into their linked files — the index stays pointers-only.
5. **Update the open loops.** `memory/status/PENDING-TASKS.md`: add new items, mark done ones, re-date deferred ones.
6. **Write the handoff.** `memory/status/session-handoff-<today>.md` per the template: what shipped (verified, with evidence), what's in flight with its *exact* next step, decisions made, landmines, open questions for the founder. Written for a reader with zero context — include full paths and absolute dates.
7. **Hygiene sweep.** Trash today's scratch/zero-byte/untitled files — never files another session may own (when in doubt, leave it); date-stamp anything missing it.
8. **Verified close summary.** Print: files touched/created/merged/trashed · corrections + decisions captured (by name) · index updates · warnings (conflicts, skips, failures) — each "clean" claim paired with the command that proved it.

## The mid-session habit this skill assumes

Don't save all capture for close: after every completed task, update the affected tracker or project file while context is fresh. Close then becomes a sweep, not an excavation — if closing regularly takes more than a few minutes, capture is happening too late.

## Failure mode to avoid

Fail soft: if any step errors, log the warning and continue — never let one failed command halt the close. An imperfect handoff beats no handoff; the next session's cold start is the one reader you must not leave empty-handed.
