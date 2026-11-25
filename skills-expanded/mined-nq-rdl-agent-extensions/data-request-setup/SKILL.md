---
name: data-request-setup
license: CC-BY-4.0
description: >-
  Initialise project scope and review records for the Data Request workflow: create the .sqlreview/ directory with
  config.json (settings + the shared assumption/limitation definitions) and the scope/review
  report templates, from the bundled default or from answers to a few questions. Safe to re-run —
  an existing setup is diffed file by file and nothing is overwritten without confirmation. Use
  once per project before /data-request:bootstrap, :analyse or :explain, or whenever one of them
  reports "not initialised".
argument-hint: '[--default|--custom] [--check] [--yes] (non-interactive: --default --yes)'
user-invocable: true
compatibility: >-
  .sqlreview schema 2 (schema 1 remains readable) (docs/specs/2026-09-15-sql-review-plugin-design.md); bash 3.2+, jq >= 1.6,
  git optional. macOS and Linux.
allowed-tools: Bash, Read, Glob, Grep, Write, AskUserQuestion
metadata:
  repo: https://github.com/nq-rdl/agent-extensions
---

# Data Request — setup

The **Data Engineer** runs setup once per project. The **Data Analyst** fills
`answers.yaml` and its optional `answers.intake.json` sidecar in one pass, guided by
`/data-request:intake` (the analyst's interview, which needs no setup), then hands the
research decisions to the engineer for bootstrap (the engineer's interview) and draft.
See [analyst intake contract](references/analyst-intake.rst). The shared list's recorded
TUH facility house default is imported by bootstrap without a fresh question;
read [recurring decisions](references/recurring-decisions.rst) for its upstream marker,
original confirmation, exceptions and normal carry rules. Setup does not copy that list into projects.

Creates the `.sqlreview/` contract used by bootstrap, analyse, explain and lift.
Ordinary composition can run without setup; recording a hand-SQL candidate silently
initialises the default store when absent. **Among the record stages, setup alone accepts an
uninitialised project**: `sqlreview.sh status` exiting 3 means "proceed to init".
Arguments: `$ARGUMENTS`. `--default --yes` is the non-interactive form: take defaults, do not ask.
Treat free-text such as "take defaults, do not ask" or "non-interactive" as `--default --yes`.

```bash
S="${CLAUDE_PLUGIN_ROOT}/skills/setup/scripts"
bash "$S/sqlreview.sh" init --diff        # exit 0: all files match the bundled default
                                          # exit 10: lists new / same / differs per file (with a diff)
```

The root is the git top-level (or the cwd outside git); it is not configurable — hooks, helpers
and the other stages all resolve the same `.sqlreview/` by walking up from the cwd.

## 1. Fresh project (every file reported `new`)

`--check`: report and stop. Otherwise, unless `--default`/`--custom` was given, ask **once**
(AskUserQuestion), options in this order:

- **Default (Recommended)** — the bundled template as-is: the shared definitions
  (`references/definitions.rst`), roles "Data Engineer (RDL)" / "Data Analyst", all
  report sections.
- **Custom** — ask, in one AskUserQuestion call: the two role names as the team calls them. **The definitions are not customised here** — they are the workflow's shared vocabulary;
  point at `references/definitions.rst` if asked, and say a change belongs in that file.

Then confirm before writing (AskUserQuestion, skipped only with `--yes`): the target path and
the file list — `config.json`, `templates/scope.md`, `templates/review.md`, `templates/lifts.md`,
`reviews/.gitkeep` (an empty placeholder, so git keeps `reviews/` in a committed `.sqlreview/`).

```bash
bash "$S/sqlreview.sh" init                # copies the bundled default; never touches existing files
```

Custom answers: after `init`, show the two role names and confirm them with AskUserQuestion
(skipped only with `--yes`). Then run the helper with those answers as shell-quoted arguments:

```bash
bash "$S/sqlreview.sh" roles "<confirmed engineer role>" "<confirmed analyst role>"
```

The helper atomically updates only the two role names. It preserves `schemaVersion`, `definitions`
and all other settings. Stop on failure; do not patch or overwrite `config.json` directly.

### Requests that forbid hand-written SQL

On a fresh project or a re-run, when the request forbids hand-written SQL, tell the engineer about
`guard.require_lift_for_string_sql` in `config.json` (default `false`). When `true`, the guard hook
denies a Python or SQL write that passes a same-line f-string or concatenation to `execute`,
`executemany`, `query` or `read_sql`, unless a lift ledger entry names the file. It is experimental
and a reminder, not a sandbox: read `references/lifts.rst` (*Experimental write guard*) first, and
measure false positives on three backlog enquiries before enabling it. Enable it only after the
engineer confirms (AskUserQuestion; with `--yes`, report it and leave it off), through the helper:

```bash
bash "$S/sqlreview.sh" guard string-sql on     # off to disable; updates only that key
```

## 2. Already initialised (re-run — #126 §2)

Never clobber. For each file `init --diff` reports as `differs`, show the diff and ask
(AskUserQuestion): **Keep mine** / **Replace with the bundled default**. Apply only the replaced
ones:

```bash
bash "$S/sqlreview.sh" init --apply templates/review.md     # only the files the human chose
```

A `new` file (added by a newer plugin version) is applied after a single confirmation. `same`
files need nothing. Report what changed and what was kept.

### Migrating from SQL Review or SQL Code

Before removing the old plugin, inspect both project templates for `/sql-review:` or `/sql-code:`
invocations. For unchanged defaults, confirm and apply each replacement with
`init --apply templates/scope.md templates/review.md`. For customised templates,
show a targeted diff changing only `/sql-review:` or `/sql-code:` to `/data-request:` and apply the
confirmed edits, preserving custom sections and placeholders. `--check` reports
these pending changes without writing. Keeping an old invocation leaves migration
incomplete; report that explicitly.

For each existing `reviews/<slug>/scope.md` or `review.md` containing an old
invocation, rerender from its corresponding JSON after updating the template:

```bash
bash "$S/sqlreview.sh" render "<slug>" scope    # or review, for each affected report
```

Inspect any report customisations before rerendering and preserve them with the
user's chosen template edits. Verify no `/sql-review:` or `/sql-code:` invocations remain in the
active templates and reports. Do not rewrite JSON, snapshots or history; report
missing source JSON or any retained old invocations as incomplete migration.

## 3. Verify and hand over

```bash
bash "$S/sqlreview.sh" status          # exit 0 now; lists reviews (none yet on a fresh project)
```

For any `invalid` review, run `status --verbose` to name the reason. A legacy review whose slug is
not derived from any current path (a schema-1 hand-chosen slug) reports a binding mismatch; after
confirming the SQL it now describes, rebind it with `sqlreview.sh move --slug <old slug> <sql path>`.
`status --verbose` also prints `migrate=sqlreview.sh move '<path>' '<path>'` for a review under a
legacy-encoded slug (`sql__cohort%5Fpipeline__x`). It keeps working as is; the command renames it to
the readable slug (`sql__cohort_pipeline__x`) without marking it stale, then re-render its reports.

Tell the user the next stage: `/data-request:bootstrap <intended sql path>` before the SQL is
written, or `/data-request:analyse <sql path>` for SQL that already exists. Suggest committing
`.sqlreview/` — the reviews inside it are the handoff record.

Triage session state uses separate schema-1 `.sqlreview/ledger.json`, not a SQL review or
lift record. `sqlreview.sh ledger get|set` validates per-ticket entries; `ledger check FILE`
validates a stored ledger. `ledger --session get|set` uses durable local user state instead,
without initialising or writing a child. `/data-request:triage` owns its schema and resume
instructions. Roles in config remain display labels, never ledger owner/decider handles.

SQL paths are supplied explicitly to bootstrap/analyse. To customise report sections, edit the
project templates; SQL glob filtering and section flags are not configuration options.

Questions have an independent per-slug `questions.json` store: stable IDs, scope/review
applicability, owner and answered closure provenance, with no SQL revision. Read
[shared questions](references/questions.rst) before authoring/migrating or closing questions.
`questions` is read-only; `migrate-questions` retains scope/review bytes; `publish-questions`
updates only the store. Reports and release evidence use it rather than obsolete embedded
strings. Closing alone requires no carry-forward or new scope/review revision.

`fingerprint` records both `sql_sha256` (original full-file provenance) and `sql_body_sha256`
(exact body bytes after conservative leading comments). `header-only` and `scoped-header-only`
remain body-bound; `publish` records helper-owned full header hashes and timestamps in
`header_revisions`, and `render` notes them even with customised templates. Keep original
snapshots. Legacy records use their full hash or an authenticated snapshot for header comparison.
Hints, executable/nested comments, `@extract:` markers and code after a block close remain in
the body; malformed headers have no body hash. Any body edit, including whitespace or comments,
unbinds the record. Body equality never confirms changed assumptions, rationale or decisions.

`sqlreview.sh notes SQL --against SCOPE_DRAFT [--questions QUESTIONS_DRAFT]` adds `scope_check`:
exact unmatched header items, rationale differences, and all open scope-question/header pairs.
Bootstrap checks these before publish, warning with both identities on semantic settlement.
Pairs are review inputs, not inferred conflicts. Fresh scopes supply a staged question store;
resume defaults to sibling `questions.json` (legacy strings only when no store exists).
Missing declared/invalid stores fail visibly. Staged questions must preserve sibling published
IDs, text/applicability and closed rows; newly added questions must be open, as at publication.
Reconcile wording or explicitly confirm provisional
implementation use while retaining the unanswered Q ID; an engineer choice is not an analyst answer.

`sqlreview.sh notes SQL --against REVIEW_DRAFT --confirmed-by HANDLE` additionally reports
`header_carry_over` and `header_walk` for explicitly named, dated engineer header decisions.
HANDLE is the explicitly intended human confirmer, not config role labels or `recorded_by`.
Read-only rows preserve date-only `decided.at` and show the separate observed source-commit
time; they never fill `confirmed_*`. Same-day sources are eligible from that displayed time;
precise UTC ISO cutoffs reject later sources. Analyse asks ONE answered Carry over all
question listing items and governed locations, then records `carried_basis: header-decision`.
Publish re-proves source bytes and all subsequent relevant path revisions plus working SQL.
Shallow/missing history, repeated/relocated ranges, body-prefix changes and relevant merge/
rename ambiguity are walked; unrelated PR merges with identical SQL path blobs are allowed.
Git attribution is not human authentication. Retain independent origins; no answer means
no publication. Later carryforward keeps `decided` and uses its normal confirmation fields.

`remap SLUG [DRAFT]` uses `diff -U 0` against an authenticated same-kind snapshot to update only
unchanged `location.lines` and `logic[].lines` in a draft. It reports `{document, prior_revision,
remapped, walk}`; changed or ambiguous ranges remain untouched for reassessment. Default:
`review.draft.json` when a review exists, otherwise `scope.draft.json`; absent default drafts are
seeded from the published record, existing drafts are preserved. An explicit draft must be a
JSON file directly inside that slug's directory, never `scope.json`, `review.json` or `lifts.json`.
It is retry-safe and atomic on failure. Missing baseline exits 6; corrupt evidence exits 2;
invalid draft ranges/binding exit 4. It never publishes, confirms, increments revisions, refreshes
fingerprints or advances snapshots. See analyse/bootstrap's update paths before carryforward.
