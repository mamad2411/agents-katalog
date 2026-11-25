---
name: "Handover"
description: "Capture the current coding session's state into durable in-repo artifacts (PROGRESS.md + a self-contained HANDOVER.md) at a milestone or phase change, so a fresh session can resume without the transcript."
alwaysAllow: ["Bash", "Write", "Edit", "Read"]
---

# Handover — Capture Session State

You are closing out a coding work session by writing durable state, not a chat summary.
The next session will read your artifacts COLD and must be able to resume without this transcript.

## When to use this skill

Invoke at a boundary, not mid-thought:

- A milestone finished (a feature or layer is stable).
- A phase change (planning → building, or building → polish).
- The conversation has drifted or accumulated noise.
- The user says "wrap up", "hand off", "save state", or "we'll continue later".

Compaction is for staying in ONE thread. Handover is for crossing a boundary. If the user just
wants to keep going in the same thread, do NOT write a handover — say so.

## Before you write

1. Find the project root (the repo or working directory being built). If it's ambiguous, ASK —
   do not guess.
2. Read the project's existing docs: spec / README, PROGRESS.md, and any prior HANDOVER.md.
   Detect where docs live (root vs a docs/ folder) and follow that convention.
3. **Verify, don't assume.** Establish current state from reality, not memory:
   - Check git: `git status` and `git log --oneline -5`.
   - If there's a build, a running app, or tests, note whether they were actually run this session.
   - Re-read the key source files you're about to describe.
   Anything you did NOT verify goes in `<unknowns_and_do_not_assume>`, not `<current_state>`.

## What to write

1. **Append to PROGRESS.md** — a dated milestone block (see format). Never wipe this file.
2. **Overwrite HANDOVER.md** — the full XML-sectioned brief (see format). Fill EVERY section.
   Empty sections are a smell; if a section is truly N/A, write "none" with one line of why.
3. **Archive a copy** to `handover/HANDOVER-YYYY-MM-DD-HHMM.md`. Get the timestamp from
   `date '+%Y-%m-%d-%H%M'` so it matches the user's clock. Keep this folder visible (not hidden) —
   the growing trail of snapshots is part of the practice.
4. If `init.sh` does not exist and the project needs a non-obvious startup, write one.

## HANDOVER.md format

```markdown
---
title: Handover — {project-name}
project: {project-name}
date: YYYY-MM-DD
time: HH:MM
phase: planning | building | testing | polish | shipped
---

<mission>
One or two sentences. What is this project trying to be, and what does "done" mean
for the CURRENT phase (not the whole project)?
</mission>

<current_state>
What works right now (verified, not assumed). What is half-built. What is broken.
Be concrete: "Add-item works in the browser; delete button throws on an empty list."
</current_state>

<artifacts>
- repo / branch: {repo} @ {branch} — last commit {sha or 'uncommitted changes'}
- key files: path — one-line role
- spec / docs: which file holds the source spec, and which sections are now stale
- running app: how it's started (e.g. `npm run dev`, `python3 -m http.server 8000`)
- tests: where they are, how to run them
</artifacts>

<decisions>
Settled choices the next session must NOT reopen, with the why in one clause.
- Chose vanilla JS over a framework — keep it readable, no build step.
- Dropped offline mode — out of scope for v1 (non-goal).
</decisions>

<constraints>
Hard limits and forbidden moves for THIS project (read from the repo, not assumed).
- Stack and tooling as established in the repo.
- Don't force-push; open a PR instead.
- Any conventions the project's docs/README require.
</constraints>

<verification>
Evidence level for the claims above. What was actually run vs assumed.
- Ran: `npm test` — 12 pass / 1 fail (delete-empty case).
- Manually checked: golden path in browser — PASS.
- NOT verified: mobile layout, error states.
</verification>

<next_steps>
Exact next actions, in order. The next session executes these, not re-plans them.
1. Fix the delete-on-empty-list crash (app.js around line 42).
2. Add an empty-state message to the list view.
3. Re-run tests + golden path, then commit.
</next_steps>

<unknowns_and_do_not_assume>
Explicit gaps. The next session MUST verify these before acting on them.
- Unsure whether the storage key changed — check the code before assuming the schema.
- Don't assume the spec's data model section is current; it predates the latest redesign.
</unknowns_and_do_not_assume>

<source_of_truth_rank>
When this brief disagrees with reality, trust in this order:
running code > tests > spec / docs > PROGRESS.md > this HANDOVER > older handovers.
</source_of_truth_rank>

<startup_protocol>
What the next session must read and run BEFORE answering or editing. Prescriptive.
1. Read: the spec/README, PROGRESS.md, this file, then the key source files.
2. Run: `bash init.sh` (or the documented start command) and exercise the app/tests.
3. Confirm current_state matches what you see; note any drift out loud.
4. Only then start next_steps[1].
</startup_protocol>
```

## PROGRESS.md format

Append a dated block at every milestone — this is the chronological spine the HANDOVER snapshots from.

```markdown
## 2026-06-13 14:20 — Add/list complete
- Done: add and list items, local persistence.
- Verified: browser golden path PASS.
- Next: delete + edit.
- Risk: no input validation yet.
```

## Quality bar

- **Concrete over vague.** "Fix the delete crash near app.js:42" beats "continue work".
- **Decisions are closed doors.** Anything in `<decisions>` must not be re-litigated next session.
- **Separate verified from assumed.** This is the single most important anti-hallucination move.
- **Self-contained.** No section may say "see our earlier conversation".
- **Read constraints from the project**, not from assumptions — stack, conventions, and limits
  come from the repo's own docs and config.
- Target the HANDOVER at ~40–70 lines. Longer means it belongs in the spec or PROGRESS.md.

## After writing

1. Confirm in one line with the paths, e.g.:
   > Handover written to HANDOVER.md (archived as handover/HANDOVER-2026-06-13-1420.md),
   > PROGRESS.md updated.
2. **Recommend a fresh session.** The point of a handover is a clean context window. Tell the user
   to START A NEW SESSION and run the `resume` skill there — do not just continue in this one.
   Suggested wording:
   > To pick this up with a clean context, open a new session and run the `resume` skill. It will
   > read HANDOVER.md, verify it against the live files, and restate the plan before changing anything.

## Do not

- Do not invent test results or claim something works that you did not run.
- Do not overwrite PROGRESS.md (append only) or delete the handover/ archive.
- Do not write a handover for a trivial mid-thread save — recommend continuing instead.
- Do not run `resume` yourself in the same session right after writing — that defeats the purpose
  (the context is already polluted). Hand off to a fresh session.
