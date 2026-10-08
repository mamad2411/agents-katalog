---
name: log-triage-actions
description: Analyse a build/test/CI log — given either a path to a log file or log output pasted straight into the prompt — fix the root causes behind its failures, and record the whole triage as an evidence-backed ACTIONS.md under .ai/actions/<RepoName>/<UUID>/. Use when asked to "find any issue or error from this log", to triage logs/npm-test-all.log or any make/npm/vitest/jest/CI output, to triage a wall of pasted terminal/CI output, to fix what a log reports and write up the steps and tools used, or to re-open/append to a previous action log.
allowed-tools: Read, Glob, Grep, Bash, Write, Edit
argument-hint: "<path to the log | pasted log text> [--uuid <existing run UUID>] [--report-only]"
---

# log-triage-actions

Turn a failing log into (a) fixed root causes and (b) a durable report that
survives the session. The deliverable is one folder per triage run:

```
<repo>/.ai/actions/
└── <RepoName>/                 # from `git rev-parse --show-toplevel`, basename
    └── <UUID>/                 # minted by scripts/new-action-folder.sh
        ├── ACTIONS.md          # the report
        ├── input.log           # only when the log was pasted, not a file (AL-13)
        ├── input.clean.log     # optional, ANSI-stripped copy of the above
        └── .run-context        # repo/date/commit captured at mint time
```

The log reaches you one of two ways — **a path** to a file on disk, or **text
pasted into the prompt**. Everything after Step 1 is identical; the only
difference is that pasted text has to be given a path of its own first.

The rules live in [`references/conventions.md`](references/conventions.md)
(stable ids **AL-01…AL-13**) and the report shape in
[`references/ACTIONS.template.md`](references/ACTIONS.template.md). Cite rule
ids in your working notes; never re-derive the method from a past report.

## Mode dispatch

Decide from the argument alone — no judgment:

| Argument | Mode |
| --- | --- |
| a path to a log file | **Triage** (the default: analyse → fix → report) |
| pasted log text (multi-line output, no such file on disk) | **Triage**, after capturing it (Step 1b) |
| `--report-only` | **Report** — analyse and write up, change no source |
| `--uuid <UUID>` | **Resume** — append to that existing run folder |
| none | list candidate logs and ask |

Treat the argument as **pasted text** when it is multi-line, or when it is a
single line that does not resolve on disk (`test -f`) but does look like output
— a timestamp prefix, an `Error:`/`FAIL`/`npm ERR!` marker, a stack frame, an
ANSI escape. When it is genuinely ambiguous — one bare token that is neither an
existing file nor recognisable output — ask, do not guess.

Candidate listing for the no-argument case:

```bash
find . -name '*.log' -not -path '*/node_modules/*' -not -path '*/.git/*' \
  -newermt '-7 days' -size +0 2>/dev/null | head -20
```

Use **Report** mode when the log came from a system you do not own, when the
user only asked "what's wrong with this log", or when a fix would touch
anything outside this repo. Pasted output is *often* one of these — a CI job,
a colleague's terminal, another checkout — but not inherently: a paste whose
failures reproduce in this repo gets the full Triage flow like any other log.
Decide it by whether the causes live here, not by how the log arrived.

---

## Triage flow

### Step 1 — Mint the run folder first

Do this **before** analysis, so evidence has a home and the report survives an
interrupted session:

```bash
DIR="$(.claude/skills/log-triage-actions/scripts/new-action-folder.sh)"
cat "$DIR/.run-context"
```

Resume instead with `--uuid <UUID>`; list prior runs with `--list`, or get the
most recent with `--latest`.

### Step 1b — If the log was pasted, give it a path  (AL-13)

A pasted log has no `path:line` to cite, and AL-10 requires one for every
claim. So persist it **verbatim** before reading it — same bytes, no
reformatting, no trimming of noise, no "…" elision:

```
Write → <the path Step 1 printed>/input.log
```

(`Write` needs the literal absolute path — the shell's `$DIR` does not expand
for it.)

From here on `$DIR/input.log` **is** the log: cite it as
`.ai/actions/<RepoName>/<UUID>/input.log:<line>` exactly as you would a
committed log file, and read it back with Read/Grep rather than working from
the prompt text, so your line numbers are the file's line numbers.

Keep ANSI escapes and progress-bar carriage returns as pasted. If they make it
unreadable, strip them into a **second** file and cite that, leaving
`input.log` untouched as the original:

```bash
# strip ANSI colour, then collapse progress-bar redraws to their final state
sed -e 's/\x1b\[[0-9;]*[A-Za-z]//g' -e 's/.*\r//' \
  "$DIR/input.log" > "$DIR/input.clean.log"
```

Line numbers shift only if the strip drops whole lines, which this one does
not — but cite whichever file you actually read, and say which in the report.

Skip this step entirely when the argument was a path — an on-disk log is
already citable, and copying it would fork the evidence.

### Step 2 — Read the whole log, then find its producer

Read it end to end (`wc -l` first; page if huge). Then locate what generated
it — the report must name the producer, and Step 6 has to re-run it:

```bash
grep -rn "<log basename>" --include=Makefile --include='*.sh' --include='*.mjs' \
  --include='*.yml' --include='*.yaml' -l . 2>/dev/null | grep -v node_modules
```

Read the producer script. It tells you the intended pass criteria, whether the
log is truncated or appended per run, and which units are in scope.

A pasted log has no basename to grep for, so recover the producer from the
**content** instead — the echoed command line, an `npm run <script>` banner, a
`make[1]: Entering directory` line, a CI job name, the tool's own header — and
match that against `package.json` scripts, `Makefile` targets, or workflow
files. Confirm the candidate by checking that its output shape matches the
paste.

If no producer can be identified — output from another machine, another repo,
or a tool not wired into this one — say so in the report, and treat Step 6's
second verification as unavailable rather than inventing a substitute command.

### Step 3 — Collapse symptoms into root causes  (AL-01, AL-06)

List every failing unit, then group. Two failures sharing one constant, one
config gap, or one missing build step are **one** issue. State the collapse
explicitly: *"4 failing packages, 2 root causes."*

While grouping, separate units that **failed** from units that **never ran** —
a dormant suite is a silent coverage hole and the more serious finding.

### Step 4 — Disprove the log's framing  (AL-02, AL-03, AL-04, AL-05)

For each cause, run the check that could **falsify** the obvious reading
before accepting it. This is the step that earns the report:

- "missing file" → `find` it repo-wide; it may exist at another depth
- "no tests found" → do test files exist, and does the matcher match them?
- echoed config → is it the tool's **default**? diff against a working sibling
- any `../` chain → resolve it one segment per row in a table
- intent unclear → read the doc comment/type/test name as the oracle

Do not proceed to a fix until you can state the mechanism in one sentence.

### Step 5 — Fix causes, not symptoms  (AL-07, AL-08, AL-09)

Match the working sibling's pattern exactly. Verify the fix's preconditions
first. **Never green-wash** — no `--passWithNoTests`, `|| true`, `.skip`,
loosened thresholds, or deleted assertions to make the log quiet. Note in the
report each shortcut you rejected and what it would have hidden.

### Step 6 — Verify twice  (AL-11, AL-12)

1. Run each fixed unit **individually**.
2. Re-run **the exact producer from Step 2**.

When Step 2 could not identify a producer, step 1 still stands — run every unit
you touched, and say plainly in the report that the end-to-end re-run was not
possible and why. An unverifiable half is reported as unverified, never dropped
silently.

Then interrogate every surviving skip and warning: by design, or newly masked?
Decide it with a command, not an assumption. Report real numbers — never
"should now pass".

### Step 7 — Write `$DIR/ACTIONS.md`  (AL-10)

Fill [`references/ACTIONS.template.md`](references/ACTIONS.template.md) — all
five sections in order. Every claim carries an anchor: a `path:line`, a quoted
log line with its number, or verbatim command output; prefer a `diff` block
over prose for any edit. Section 4 (tools used) is written **from your actual
tool calls in execution order**, so keep track as you go rather than
reconstructing it at the end. Section 5 must name the check that would catch
this class of bug automatically, not just the instance you fixed.

### Step 8 — Report back

Tell the user the root causes, the before/after numbers, anything deliberately
left alone, and the `ACTIONS.md` path. If the log was pasted, mention that it
was saved to `input.log` beside the report — the user pasted it into a session
and may not expect it on disk. Note that `.ai/` and `.claude/` are git
submodules here — mention the write, and let the user decide about committing.

---

## Self-update

When a triage teaches something general — a new disproof pattern, a new
green-washing trap, a section the template lacked — add or amend a rule in
`references/conventions.md`:

1. Append the next free id — one past the highest in the file; never renumber
   or reuse a retired id.
2. Give the rule a one-line statement, then the concrete evidence that produced
   it. Rules without a real example get deleted at the next review.
3. If it changes the report shape, update `ACTIONS.template.md` in the same
   edit so the two never drift.
4. Retire a rule by marking it `**RETIRED**` with the reason. Do not delete.

Escalate into Self-update when a log's failure mode does not fit any existing
rule — that is the signal the rule set is short, not that the log is odd.

## Related

- `makefile-self-improve` — same repo-local skill conventions (rule ids,
  `references/` + `scripts/` layout, self-update mode).
- `findings` (global) — read-only investigation reports under `.ai/findings/`.
  Use that when nothing gets fixed; use this when the log gets **repaired**.
