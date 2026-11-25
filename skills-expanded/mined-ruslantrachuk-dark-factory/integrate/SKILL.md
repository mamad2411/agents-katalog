---
name: integrate
description: >
  Use when built code is about to be committed — "commit it", "commit this slice", "run the gates", after each
  build-tdd slice — and as the rules of the feature pipeline's single writer. Runs the slice's tests and lint before
  the commit, one commit per slice, closes the bd subtask; after the last slice, the full gate once with root-cause
  fixes. Next: the reviewer role, then wrap.
---

# Skill `integrate` — commit what was built, keep the branch green

> Part of the dark-factory plugin. Gate commands: `testCmd` and `lintCmd` in `.claude/factory/feature-pipeline.json` (in the
> project's main checkout, the first path of `git worktree list`), or the
> project's pre-push hook (`.githooks/pre-push`); a frontend with its own lane (`frontendDir`) runs typecheck, lint and
> tests there when it was touched.

The integrator is the only writer to git and bd for the batch: one writer means no `index.lock` or database races and
no two hands on one file.

## After each slice (or each wave)

1. **Scoped tests** of the batch — the slices' own test files, by absolute path. db tests among them run with
   `-m db` when the machine has Docker.
2. **Lint** of the batch's files (the format fix may be applied to them).
3. **One commit per slice**: `git add <its files>` and `git commit`. Commit only code, tests, migrations and code
   docs; the project documents and the PR description belong to `wrap`.
4. **Close the subtask** (with a bd queue): `bd close <id> --reason "…"`. Never the phase task — `scripts/merge-feature.sh` closes it
   after the merge.
5. **Red** → fix the small thing and run again. What cannot be fixed stops the batch with the failing tests and why.

## After the last slice — the full gate, once

1. The fast suite and lint over the whole branch (`testCmd`, `lintCmd`), and the frontend lane if it was touched.
   The db lane runs here only when the run is told to; otherwise CI runs it and the PR description says so.
2. Red → `systematic-debugging`: the root cause, never an adjusted test. Commit the fix.
3. Long commands run synchronously; a background run returns before its outcome is known and counts as failed. One
   command is limited to 600 s — a longer lane runs in shards.

## Commit messages

For a reviewer and a future reader of the history, not for a machine. Subject: the essence of the change
(Conventional Commits, in the project language, ≤~70 characters). Body: plain prose — what changes and why. No chains
"A → B → C", no file paths or symbol names as the main text, no JSON, no telegraphic style; details (tests,
assumptions) as short bullet points.

Next: **the `reviewer` role** with a fresh context before merge (one combined lens for a small diff, separate lenses
for a large one), its findings fixed with this skill again, then **`wrap`**.
