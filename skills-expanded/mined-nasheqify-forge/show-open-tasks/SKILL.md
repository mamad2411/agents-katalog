---
name: show-open-tasks
description: >
  Fast terminal overview of the OPEN tasks in a docs/tasks/ tree, grouped by
  priority, newest first. Triggers when the user wants a task list / overview /
  status table ("liste aller tasks", "zeig offene tasks", "task overview"); NOT
  for changing a task's status (use task_status_update) or creating one (use
  task_creation).
status: active
relevant_for: ["buddy"]
invocation:
  primary: user-facing
  secondary: [orchestrator]
disable-model-invocation: false
uses: []
---

Read and follow `framework/work-principle.md` before taking up work.
Resolve this reference against the framework root; retain the consumer CWD.


# Skill: show-open-tasks

## Purpose

A read-only, at-a-glance overview of the open work in a project:
*what is still on the list, how urgent, how old, what depends on
what, when last touched.* One compact terminal table per priority
group, **sorted by created date descending (newest first)** within
each group — no file-by-file hand-reading.

Project-neutral: works in any repo following the
`docs/tasks/<NNN>.yaml` convention. Read-only — never edits task
files. Status changes go through `task-status-update`; creation
through `task-creation`.

## Script-less

This skill carries **no `.py` script**. The procedure below is run
directly with standard shell tools. The data extraction is one shell
loop; the table is rendered from the resulting rows.

## Definition of "open"

Open = `status` NOT in the terminal set. Per the schema SoT
(`framework/task-schema.yaml` → `terminal_status`): terminal =
`done, superseded, wontfix, absorbed`. Everything else (`pending,
in_progress, blocked`, any unknown/in-flight label) is **open** —
unknown values are read tolerantly as open, never silently terminal.
Default tasks dir: `docs/tasks` (override per the active project's
docs routing).

## Priority normalization

`priority` is read tolerantly per the schema SoT
(`framework/task-schema.yaml` → `fields.priority.read_aliases`): first
word, lowercased; the alias map (`mid|med|normal → medium`,
`hi → high`, `lo → low`) is **defined there, not here** — this skill
applies it, the schema owns it. Trailing notes (e.g.
`high (YYYY-MM-DD)`) stripped. Missing/unrecognized → `unknown`.

## Columns

| Column  | Source field        | Format                          |
|---------|---------------------|---------------------------------|
| ID      | filename `NNN.yaml` | numeric, left-aligned, width 5  |
| TITLE   | `title:`            | dynamic width, clipped + `…`    |
| DEP     | `blocked_by:`       | comma-joined IDs, `—` if empty  |
| STATUS  | `status:`           | identifier (no prose), width 12 |
| CREATED | `created:`          | YYYY-MM-DD, width 10            |
| TOUCHED | `updated:`          | YYYY-MM-DD, width 10            |

**Inline-comment-strip rule** (applies to all parsed fields):
everything from the first `#` to end-of-line is dropped before
further parsing — so `blocked_by: []  # note text` reads as `[]`.

**`blocked_by` parsing:** inline list form only — `[]`, `[123]`,
`[123, 456]`. Block-style YAML lists (`blocked_by:\n  - 123`) are
**not** parsed. Convert to inline form if needed.

## Sort

Two-key sort, with implicit ID tie-breaker:
1. Priority rank ascending: `high < medium < low < unknown`
2. Created date **descending** within each priority group (newest
   first)

## Width

Dynamic via the `COLS` env var (default **140**, fallback
`$COLUMNS`, minimum 30). Fixed column widths: ID=5, DEP=10,
STATUS=12, CREATED=10, TOUCHED=10. TITLE absorbs the remainder:
`COLS − 58`. Group bars and dashed sub-header rows use the same
total width.

## Procedure

One self-contained pipeline. `TASKS` = the active project's tasks
dir (per docs routing — e.g. `docs/tasks`, or an absolute path).
`COLS` = terminal width (default 140 when unset/undetectable; in
Claude Code the env is typically empty, so the default applies).

```bash
TASKS=docs/tasks
COLS=${COLS:-${COLUMNS:-140}}
TWIDTH=$((COLS - 58))
[ $TWIDTH -lt 30 ] && TWIDTH=30
{
for f in "$TASKS"/[0-9]*.yaml; do
  [ -e "$f" ] || continue
  id=$(basename "$f" .yaml)
  case "$id" in *[!0-9]*) continue;; esac          # pure-numeric task files only
  val() { v=$(sed -n "s/^$1:[[:space:]]*//p" "$f" | head -1); \
          v=${v%%#*}; \
          v="${v%"${v##*[![:space:]]}"}"; \
          v=${v%$'\r'}; v=${v#[\"\']}; v=${v%[\"\']}; \
          printf '%s' "$v"; }
  st=$(val status | tr '[:upper:]' '[:lower:]')
  case "$st" in done|superseded|wontfix|absorbed) continue;; esac
  pr=$(val priority | tr '[:upper:]' '[:lower:]'); pr=${pr%% *}
  case "$pr" in mid|med|normal) pr=medium;; hi) pr=high;; lo) pr=low;; high|medium|low) ;; *) pr=unknown;; esac
  case "$pr" in high) pk=0;; medium) pk=1;; low) pk=2;; *) pk=3;; esac
  cr=$(val created); up=$(val updated)
  dep=$(val blocked_by); dep=${dep#[}; dep=${dep%]}; dep=$(printf '%s' "$dep" | tr -d ' "'"'")
  [ -z "$dep" ] && dep="—"
  ti=$(val title)
  printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' \
    "$pk" "${cr:-9999-99-99}" "$pr" "$id" "$ti" "$dep" "${st:-?}" "${up:-—}"
done
} | sort -t$'\t' -k1,1n -k2,2r | awk -F'\t' -v tw=$TWIDTH -v cw=$COLS '
  BEGIN {
    fmt = sprintf(" %%-5s  %%-%ds  %%-10s  %%-12s  %%-10s  %%-10s\n", tw)
    bar = ""; for (i=0; i<cw; i++) bar = bar "━"
    dashtitle = ""; for (i=0; i<tw; i++) dashtitle = dashtitle "─"
  }
  $3 != g {
    if (g != "") print ""
    g = $3
    pad = cw - length(g) - 4
    if (pad < 4) pad = 4
    printf "━━ %s %s\n", toupper(g), substr(bar, 1, pad)
    printf fmt, "ID", "TITLE", "DEP", "STATUS", "CREATED", "TOUCHED"
    printf fmt, "─────", dashtitle, "──────────", "────────────", "──────────", "──────────"
  }
  {
    n++
    t = $5
    if (length(t) > tw) t = substr(t, 1, tw-1) "…"
    printf fmt, $4, t, $6, $7, $2, $8
  }
  END { printf "\n%d open\n", n }
'
```

**What it does, by stage:**

1. **Extract** — per pure-numeric task YAML, read `status`,
   `priority`, `blocked_by`, `created`, `updated`, `title` with a
   quote-and-comment-safe `val()` helper (strips inline `# …`
   comment, trailing whitespace, one layer of surrounding `"`/`'`,
   `\r`). Terminal statuses skipped. `priority` normalized per the
   rules above. `blocked_by` brackets + spaces stripped → CSV IDs or
   `—`. Emits a sort-key prefix (priority-rank · `created`) followed
   by the row data.

2. **Sort** — `sort` on priority-rank ascending (`-k1,1n`), then
   `created` **descending** (`-k2,2r`, reverse) → newest task on top
   within each priority group.

3. **Render** — `awk` prints a full-width `━━ PRIORITY ━━━…` bar at
   each group boundary, then a column-header row + dashed
   sub-header, then one data row per task (title clipped to
   `TWIDTH−1` with `…`). Footer = total open count.

Adjust column widths or default `COLS` to taste; the pipeline is the
contract, the awk formatting is cosmetic. Keep it scannable — this
is a fast glance, not a detail dump.

### Optional: last git change

When the user asks for the factual trail beyond `updated:`, add a
`LAST CHANGE` column: `git -C <repo> log -1 --date=short
--format='%ad — %s' -- "$TASKS/$id.yaml" "$TASKS/$id.md"` (→
`uncommitted` if empty, `—` if not in git). Off by default — costs
one git call per task. The `updated:` field captures the intended-
state signal; the git column is the factual-trail.

## CC-Rendering (Claude Code orchestrator path)

When the skill is invoked by Buddy in a Claude Code session
(orchestrator, not direct terminal use), long bash stdout gets
folded by the CC UI with a `Ctrl+O to expand` marker. That blocks
side-by-side typing and breaks the at-a-glance purpose.

**Mitigation:** Buddy runs the pipeline with output captured (via
tmpfile redirect, e.g. `bash … > /tmp/sot-$$.txt`) and **inlines
the rendered table verbatim into the assistant message as a fenced
code block**. Assistant-message text is not subject to the bash-
output fold. The user reads the table in the reply, no Ctrl+O
dance.

When the user runs the pipeline directly in their own shell (no
orchestrator in the loop): the fold does not apply; output goes to
stdout as usual. No special handling needed.

## Boundaries

- Read-only. No status mutation, no file writes (except the optional
  tmpfile for CC-rendering), no commits.
- Not a backlog renderer — reads task YAMLs, not `backlog.md`.
- Not a plan/critical-path tool — that is `plan_engine`. This skill
  is the fast human glance, deliberately decoupled from plan_engine.
  **No commentary, no "what to do next", no observations layer.**
  Render the table, stop. Footer line `N open` is the end.
- The YAML `updated:`/`created:` dates are the intended-state
  signal; the optional git line is the factual-trail signal.
- Multi-line block-style `blocked_by:` lists are not parsed — use
  inline form.
