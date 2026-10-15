---
name: commandments
description:
  Audit the current branch, PR, or uncommitted changes against the project's
  COMMANDMENTS.md, the code-style and human+agent readability conventions. Use
  when asked to "check the commandments", "commandments review", "readability
  review", "do my changes follow our conventions", or to gate a diff on code
  cleanliness and readability before merge. Surfaces a worked checklist; does
  not auto-fix unless asked.
disable-model-invocation: true
allowed-tools: Bash, Read, Grep, Glob, Edit, Agent
argument-hint: "[pr-url|owner/repo#number] [--full] [--fix]"
---

# Commandments Review

Audit changed code against the project's commandments (code style + human/agent
readability). The output is a **worked checklist**: every applicable commandment
is listed with a status, and every violation cites `file:line` with a concrete
fix. A clean diff is a valid result; do not manufacture findings.

This skill checks only what a linter cannot. It never re-flags anything oxlint /
oxfmt / knip already enforce, and it never proposes formatting churn.

## Step 1: Load the commandments

Find the rules, in this order:

1. `COMMANDMENTS.md` at the repo root (project-specific; preferred).
2. `docs/COMMANDMENTS.md` (project-specific, docs-folder convention).
3. `~/.agents/docs/commandments.md` (the shared fallback copy, if present).

Read the whole file. The review covers the numbered commandments. **Skip the
"Beyond style" section** (those are architectural requirements enforced
elsewhere, not readability conventions) and skip anything the intro lists as
linter-enforced.

If none of these exist, stop and tell the user there are no commandments to
check against.

## Step 2: Determine scope

Parse `$ARGUMENTS`:

- **A PR reference** (`https://github.com/owner/repo/pull/N` or `owner/repo#N`):
  review that PR. Get the diff with `gh pr diff N -R owner/repo` and metadata
  with `gh pr view N -R owner/repo --json title,body,headRefName,files`.
- **No PR reference (default): review the current local work.** This is the
  union of:
  - uncommitted changes: `git diff` and `git diff --staged`, plus untracked
    files from `git status --porcelain`,
  - committed-but-unmerged work on the branch: determine the base with
    `git merge-base HEAD origin/HEAD` (fall back to `origin/main`, then `main`),
    then `git diff <base>...HEAD`.
- `--full`: review the full content of every changed file, not just the changed
  hunks (use when a hunk's correctness depends on the rest of the file). Default
  is diff-scoped.

Collect the changed files and their hunks. If there are no changes, say so and
stop.

Always confirm the resolved scope to the user in one line before reviewing (e.g.
"Reviewing 7 changed files on `branch` vs `origin/main`, diff-scoped").

## Step 3: Walk each commandment against the changes

This is LLM-guided, not a scanner. For each applicable commandment, read the
rule and its self-check, look at the changed code, and classify. Use `Grep` /
`Read` to pull the surrounding context you need.

For a large diff (more than ~15 changed files), fan out with the `Agent` tool:
one subagent per group of files, each handed the commandments text and its slice
of the diff, returning findings as structured `file:line` + commandment + fix.
The subagents research only; they do not edit.

Rules of engagement:

- **Scope to the diff.** Every finding must cite a line the change adds or
  modifies. A pre-existing problem in an untouched sibling is a follow-up note
  at most, never a blocking finding on this diff.
- **Calibrate severity** as probability x consequence. Most readability findings
  are LOW or MEDIUM. Reserve HIGH for a real correctness or maintainability
  trap.
- **Weight commandment 1 (readability) highest.** It is the point of the review.
- **Hold comments to commandments 13-14 strictly** (run the comment sweep below
  — comments are the easiest violation to miss reading file-by-file). A comment
  can carry a real "why" and still be a violation when it is verbose: trim
  multi-sentence narration, restated code, and PR-level rationale down to the
  single non-obvious constraint. "Dense but every sentence is justified" is NOT
  a pass; recommend the tighter rewrite. **Any comment added inside a `*.test.*`
  file is a violation** (14: none in tests) — fold the intent into the `it(...)`
  / `describe(...)` title and delete it; the only survivor is a note about a
  non-obvious test-harness mechanism the test code alone can't explain (a jsdom
  quirk, a fixture's seeded state). Also flag a comment that prefixes the
  current feature ticket (`TICKET-123: ...`): the commit and PR already carry
  it, and 13 reserves ticket references for linking the specific bug a
  workaround addresses, not for labelling the feature's own work.
- **Recommend, don't reshape.** Layering and single-responsibility findings
  (commandments 2 and 3, e.g. a raw query in a route, business logic in a route)
  are recommendations with a suggested target location. Do not silently
  restructure routes, services, or repos.
- **No nitpicking the formatter.** If oxfmt/oxlint would fix or catch it, drop
  it.

### Comment sweep (every added comment, no exceptions)

Reading file-by-file misses comments, so enumerate them mechanically. List every
comment line the diff ADDS, across all files including tests:

```sh
git diff <base>...HEAD | awk '
  /^\+\+\+ b\// { f=$2; sub(/^b\//,"",f) }
  /^\+/ && !/^\+\+\+/ {
    if ($0 ~ /\/\// || $0 ~ /\/\*/ || $0 ~ /^\+[[:space:]]*\*/) print f": "substr($0,2)
  }'
```

Give every line a verdict against 13-14; do not let an added comment reach the
report as an unexamined PASS. Apply the test-file rule (any comment in a
`*.test.*` file is a violation) and the strict verbosity test from the comments
bullet above to each one.

## Step 4: Report

Render a worked checklist. Every applicable commandment appears with a status,
so the reader sees what passed, not only what failed:

- `PASS` — the diff honors it (or had no relevant code).
- `VIOLATION` — cite `file:line`, state the issue in one line, give the concrete
  fix.
- `NEEDS REVIEW` — a judgment call worth a human's eyes; explain the tension.
- `N/A` — not exercised by this diff.

Group by commandment number. Then a short verdict: `CLEAN`, `MINOR` (only LOW
findings), or `NEEDS WORK` (any MEDIUM+), with a one-line rationale.

Format each violation as:

```
[VIOLATION] #1 Readability — apps/web/src/components/QueryErrorBanner.tsx:38
  A `styles` object drives static inline styles; a reader can't see the design
  intent from the markup.
  Fix: move to Tailwind utility classes with theme tokens; use <Button> for Retry.
```

## Step 5: Optional fixes

Only if the user passed `--fix` or asks after seeing the report. Apply the fixes
you proposed, smallest first, and keep the diff minimal (commandment 12). Do
**not** auto-apply layering/route-shape changes (commandments 2 and 3); list
those as recommendations and let the user decide. After fixing, run
`pnpm run check` and report the result.
