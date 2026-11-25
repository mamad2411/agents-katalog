---
name: lore
description: "Persistent project knowledge base so a new session resumes from recorded state instead of re-reading the whole codebase. Sets up and maintains docs/lore/ (STATE, ROADMAP, DECISIONS, LEARNINGS, JOURNAL): current status, phased progress path, why decisions were made, what was tried and failed, and dead ends not to retry. Use when: starting a new project or scaffolding its docs; beginning a session on a project that has docs/lore/ and you need context; finishing a task, fixing a bug, or making an architectural choice and the outcome should be recorded; the user says continue/resume, asks what the state is, asks to record a decision or lesson, or asks why something was done a certain way."
---

# Lore

A project's real knowledge is not in its code. Code shows *what* exists; it never shows what was tried and abandoned, why one approach beat another, or which trap costs an hour every time someone forgets it. Without that record, every new session re-derives it — usually by re-reading the whole repo, sometimes by repeating a mistake that was already paid for once.

This skill maintains that record as five files under `docs/lore/`, and defines when to read each and when to write to it.

## The files

| File | Holds | Read when |
|---|---|---|
| `STATE.md` | Current status: what works, what's mid-flight, active blockers, next steps. **The entry point.** | Every session start — always, fully |
| `ROADMAP.md` | Phased progress path with checkboxes. Where the project is going. | Session start; when picking the next task |
| `DECISIONS.md` | Dated decisions: what was chosen, why, what was rejected. | Before changing anything architectural; when asked "why is it like this?" |
| `LEARNINGS.md` | Traps, failed approaches, dead ends. Each entry has a `Trigger:` line. | Grep before touching an area — see below |
| `JOURNAL.md` | Append-only dated work log. Raw history. | Rarely — only to reconstruct a specific past session |

**Size discipline:** `STATE.md` stays under ~150 lines. It is the only file read in full every session, so it must describe the present, not accumulate history. When something in it becomes past tense, move it: a finished task → `JOURNAL.md`, a resolved choice → `DECISIONS.md`, a paid-for mistake → `LEARNINGS.md`. `STATE.md` is a dashboard, not an archive.

## Mode 1 — Session start (resume)

Trigger: a session begins on a project containing `docs/lore/`, or the user says continue / resume / "where were we".

1. Read `docs/lore/STATE.md` and `docs/lore/ROADMAP.md` in full. That is the context load — **do not fan out and read the codebase to rebuild context.** The point of the lore is to make that unnecessary.
2. Grep `LEARNINGS.md` for the area about to be touched:
   ```bash
   grep -i -A6 "<area keyword>" docs/lore/LEARNINGS.md
   ```
   Every entry carries a `Trigger:` line naming the files or subsystems it applies to, so grep against a filename, module, or tool name.
3. Open only the specific files the task needs.
4. Tell the user briefly, in their language, where things stand and what the next step is per `STATE.md` — then wait or proceed as they asked.

Steps in `STATE.md` are marked `▶️` (actionable now) or `⛔ [needs user]` (blocked on a credential, a decision, or something only the user can run or see). **Start the first `▶️` step rather than asking which to do** — mention the `⛔` ones once as reminders and move on. Asking the user to choose when the file already answers it defeats the point of having written it down.

If `STATE.md` claims something is done, treat that as a claim to verify cheaply (run the test, check the file exists), not as ground truth. Records go stale; say so when one is wrong and fix it.

## Mode 2 — New project (init)

Trigger: starting a new project, or an existing project with no `docs/lore/`.

1. **Check for an existing knowledge file first** — `docs/STATUS.md`, `NOTES.md`, `CHANGELOG.md`, a `## Status` section in the README. If one exists, **adopt and migrate it; never create a parallel second source of truth.** Ask before restructuring a file the user already maintains.
2. Copy the five templates from this skill's `templates/` directory into `docs/lore/`.
3. Fill them from what is actually known now — project goal, stack, constraints. Leave a section empty rather than inventing content for it.
4. Build `ROADMAP.md` as phases with checkboxes, each phase a shippable slice with a stated "done when" condition. This is the progress path.
5. Append the protocol block from `references/protocol-block.md` to the project's `CLAUDE.md` (create it if absent). Without that block, a future session has no instruction to read the lore at all — **this step is what makes the whole thing work.**
6. Show the user what was created and how to keep it alive.

## Mode 3 — Recording (log)

Trigger: a task finished, a bug was fixed, an approach failed, a design choice was made, or the user asks to record something.

Do this **at the end of a task, before reporting completion** — not batched at session end, where a context cutoff loses it.

1. Update `STATE.md`: refresh the status section and its date, move finished items out, and mark each next step `▶️` or `⛔ [needs user]`.
2. Append to `JOURNAL.md`: one dated entry, what was done and what changed.
3. If a choice was made between real alternatives → append to `DECISIONS.md` with the rejected option and the reason.
4. If time was lost to something → append to `LEARNINGS.md` with a `Trigger:` line.
5. If a phase advanced → tick the checkbox in `ROADMAP.md`.

Steps 3–5 are conditional; 1–2 are not.

## What is worth recording

The test: **would a competent developer with full repo access still not know this?** If they'd learn it by reading the code or `git log`, it does not belong in the lore.

Record:
- A failed approach and the reason it failed — the highest-value entry type, because it is exactly what a fresh session would otherwise retry.
- A non-obvious constraint discovered by hitting it (version incompatibility, API quirk, an ordering that matters).
- Why the rejected alternative was rejected.
- A measured fact that contradicts an intuition — "X was expected to be faster; it wasn't, by 3x."
- An external dependency's real behavior, when it differs from its docs.

Do not record:
- What the code structure already says, or what `git log` already says.
- Restatements of the task the user just gave.
- Speculation, or a plan not yet acted on. Record outcomes.
- Anything that only matters inside the current conversation.

## Writing rules

- **Dates absolute.** "2026-07-19", never "yesterday" or "last session" — relative time is meaningless when read months later.
- **Language:** write entries in the language the user communicates in; keep headings and field keys (`Trigger:`, `Why:`, `Rejected:`) in English so grep works across languages.
- **Every learning gets a `Trigger:`** naming the file, module, or tool it fires on. An entry nobody can find is an entry that does not exist.
- **State the negative plainly.** "This did not work" is the useful part; hedging destroys the value of the record.
- **Update in place, don't append duplicates.** Before adding an entry, check whether an existing one covers it and revise that instead. When a recorded fact turns out to be wrong, correct or delete it — a stale lore is worse than none, because it is trusted.
