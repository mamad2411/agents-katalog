---
name: check-progress
description: >
  Display current completion state for one or all active courses.
  Runs collect-progress.js to parse journals and extract completion
  percentages with git timestamps. Use when the learner asks about
  their progress or at the start of a session.
metadata:
  version: '1.0'
---

## Purpose

Shows the learner where they stand: which assignments are done, which
remain, and when completed ones were finished. Reads directly from
the journal and git history — no separate state file to maintain.

---

## Before You Start

No files need to be pre-read. This skill runs a script and presents
the output.

---

## Procedure

### Step 1 — Determine scope

- **Specific course requested** — use `--course <slug>`:
  ```
  node .agents/skills/core/check-progress/scripts/collect-progress.js --course <slug> --output text
  ```
- **All active courses** — omit `--course`:
  ```
  node .agents/skills/core/check-progress/scripts/collect-progress.js --output text
  ```

If the learner didn't specify, check the Active Course section in
`AGENTS-CUSTOM.md`. If a course is active, scope to that course. If no
course is active, run for all.

### Step 2 — Run the script

Run the command from Step 1. The script walks `progress/`, parses
each `journal.md`, and prints a human-readable summary.

### Step 3 — Present the result

Display the output to the learner as-is.

If the output is empty (no `progress/` directory or no journals
found), tell the learner: "No progress found. Start a course with
`/start-course` to begin tracking."

---

## Notes

- **Script requires Node.js.** If `node` is not available, read
  `progress/<slug>/journal.md` directly and report the Progress
  Tracker section manually.
- **Git timestamps** are enriched by the script from git log. If
  the repo has no commits yet (e.g., fresh clone not committed),
  completed dates will show as null — this is expected.

---

## Reference

- Script source: `.agents/skills/core/check-progress/scripts/collect-progress.js`
- Journal parser: `scripts/utils/parse-journal.js`
- Git utilities: `scripts/utils/git-utils.js`
- Tech spec §6.3.3: full skill specification
