---
name: play-mk-dump
version: 1.0.0
description: Executes issues from a kick spec step by step, tracking progress in the spec file across sessions. Use when user runs /play-mk-dump, wants to execute a spec from /kick-mk-dump, or wants to continue work on an in-progress spec.
user-invocable: true
---

# play-mk-dump

Executes a kick spec one issue per session. After each issue completes, you `/clear` and re-invoke to start the next — this keeps each issue's execution in a clean context window. Tracks state in the spec file so sessions resume from the right place.

Accepts an optional arg: `/play-mk-dump {filename}` — uses that spec directly.

## Flow

**Step 1: Load spec**

Read `docs/monkey-brain/spec-index.md`. Auto-create if missing — see [REFERENCE.md](REFERENCE.md) for schema.

- Filter rows where status = `remaining`
- No remaining → tell user: "No remaining specs. Run `/kick-mk-dump` first." → stop
- One remaining → use it automatically. Multiple → show list, ask user to pick.
- Arg provided → use that spec filename directly.

**Step 2: Resume or start**

Read the selected spec file. Scan all issues for sub-step state:

- Issue has `[~]` sub-step → resume from first `[ ]` sub-step inside it
- No `[~]` found → find first issue with any `[ ]` → start it
- All sub-steps `[x]` → spec complete → go to Step 5

Read "Done when:" of the current issue before doing anything — this is the exit condition.

**Step 3: Execute sub-steps**

> Spec file content is already in context from Step 2 — do not re-read it. Use the content already loaded.

Before starting the first sub-step: mark it `[~]` in spec file, write `## Current Issue` block (see [REFERENCE.md](REFERENCE.md)).

Work through sub-steps one at a time:
- After each sub-step completes: mark it `[x]`, mark next sub-step `[~]`, update `## Current Issue` block
- If blocked or uncertain: stop, state what's unclear, ask user — do not assume, do not skip

**Step 4: Issue complete**

> spec-index.md content is already in context from Step 1 — do not re-read before updating.

- Verify "Done when:" is fully met — if not, keep working
- Mark all sub-steps `[x]`, remove `## Current Issue` block
- Write `## Resume` block immediately — write after EVERY issue, not just at session end
- Update `docs/monkey-brain/spec-index.md` row: status → `done`, date → today, note → one sentence describing what was built
- Check for next issue:
  - Next issue exists → output "✅ Issue N done. Type `/clear` then `/play-mk-dump` to start Issue N+1." → stop
  - No next issue → go to Step 5

**Step 5: Spec complete**

All issues are `[x]`:
- Remove `## Current Issue` and `## Resume` blocks from spec file
- Update `docs/monkey-brain/spec-index.md` row: status → `done`, date → today, note → one sentence summary of entire spec
- Create `docs/monkey-brain/specs/{yyyy}/{mm}/done/` if it doesn't exist
- Move the spec file to `docs/monkey-brain/specs/{yyyy}/{mm}/done/{filename}`
- Update the spec file's path in `spec-index.md` to include `done/` (e.g. `2026/05/done/filename.md`)
- Tell user: "Spec complete. All issues done."

## Execution Principles

- **Think first:** Read "Done when:" before every issue. State assumptions explicitly.
- **Simplicity:** Minimum changes that satisfy the criteria — no extras.
- **Surgical:** Touch only what the issue requires. Nothing adjacent.
- **Verify:** Check "Done when:" before marking complete — don't assume it's done.
