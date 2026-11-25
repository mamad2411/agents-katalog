---
name: seq
description: "Run a tracked task INLINE in the main conversation through a named step-sequence (default: audit→work→audit→report). Inline twin of /minion — same loop, but executed here (sees chat context) instead of delegated to a sub-agent. Activate on '/seq <task>', 'seq <task>', 'do <task> inline', 'run <task> here'. Sequences are named and editable, or ad-hoc via 'as <key,key,...>'; mix /seq and /minion per task."
license: MIT
---

# Seq

Inline executor. Run one tracked task through a named step-sequence, here in the
main window — no sub-agent. Twin of `/minion`: same sequences, different venue.
minion delegates (cheap context, headless); seq runs inline (costs main tokens,
but you see this chat and can course-correct).

Default sequence = `standard`: audit-before → work → audit-after → report.
Sequences, step definitions, Abort rule, Audit reuse: `references/sequences.md`.

## Task source

Seq needs three task ops: **RESOLVE** (name → spec path), **GATE** (dependencies +
status), **EXPAND** (milestone → ordered task list). Bind a source, in priority:

1. **Named inline** — user says e.g. "use tasky" / "resolve via <procedure>".
2. **Declared by the project** — a task procedure named in CLAUDE.md or a
   referenced process doc. Route all task ops through it automatically.
3. **Direct spec path** — skip RESOLVE; read GATE info from the spec/repo; EXPAND
   does not apply.

WHEN no source bound and no direct path → DO: STOP, ask which task (path or
procedure). Never invent a task layer.
WHEN the bound source can't supply an op (e.g. raw path, no dep metadata) →
DO: do that op manually from the spec/repo, or skip it with a stated assumption.
Never block on a missing tracker.

## Flow — execute in order

1. RESOLVE. Map name → spec path via the source; echo it in one line. Direct path
   → use as-is. Ambiguous name → ask; never guess.
2. GATE. Read `Dependencies:` + status; each must be `DONE`. Source can't supply
   → read from spec/repo, or note none declared.
3. PICK SEQUENCE. Default = the project override's `Default:` when
   `.agents/seq/sequences.md` sets one, else `standard`. Per-run `as ...`
   overrides below. (`references/sequences.md` → Project override.)
4. RUN INLINE. Execute the sequence's steps in order, each per its definition in
   `references/sequences.md`. A step is done when its EXIT ARTIFACTS were
   printed, not when its actions ran.
5. HAND BACK. Report, then end your turn for review.

## Rules — WHEN / DO

WHEN the user passes `as <seqName>` → DO: run that sequence from the registry.
Unknown name → STOP, list the available sequences.

WHEN the user passes `as <key>,<key>,...` (ordered step keys) → DO: run that
one-off sequence directly — no registry edit. Unknown key → STOP, list the step
library. After a successful run, offer to save it as a named row.

WHEN the user names a milestone, not a single task → DO: EXPAND into an ordered
task list (dep order). Run each inline, one at a time. PAUSE between tasks.

WHEN a dependency is not `DONE` → DO: STOP. Name the blocker. Never run blocked.

WHEN a step hits a blocker → DO: follow the Abort rule in
`references/sequences.md` — STOP inline, surface it, wait. Abort early (during
audit-before) before editing. Already edited → list the changes.

WHEN an audit JUST run this session covers this task's surface (Audit reuse rule,
`references/sequences.md`) → DO: reuse it; state the call. Scope differs or the
surface changed → fresh audit.

WHEN the user says `--no-audit` → DO: skip audit-before ONLY. audit-after always
runs — it is the safety net. Truly bare run = `as quick`.
WHEN the user says `--audit` → DO: force a fresh audit-before.

WHEN the task is well-defined routine grind with no need to watch →
DO: recommend `/minion` instead to save main context.

## Surfacing a decision (clarifier) — WHEN / DO

<!-- Mirror of minion/SKILL.md "Surfacing a decision (clarifier)". Same block, same
     rules — edit BOTH or neither. -->

WHEN seq pauses and puts a choice to the user — Abort rule, an ambiguous RESOLVE,
a blocked GATE, a sub-agent's finding you must relay, or any fork the spec/repo
can't settle → DO: lead with this four-line block, in this order, BEFORE any
reasoning:

- **Problem:** what is blocking AND why it matters, in plain words — define every
  term as you use it.
- **Choices:** `A → … / B → …`, each naming what HAPPENS if picked (the
  consequence or risk), not just a label.
- **Rec:** which option, why, and what the other option costs you.
- **Answer:** the reply the user sends verbatim —
  `yes → <recommended action> · no → <the alternative>` (or `A → … / B → …` when
  yes/no is ambiguous).

Write it for a COLD reader — someone who never saw this task. The test: could
they pick correctly from this block ALONE? If answering would make them ask "what
does X mean?", the block failed — expand X. This is the whole point; the rules
below serve it.
- No bare references. A spec section, a ticket number, a symbol name, "the sub
  said" — never cite what the reader can't see; say what it IS and why it matters,
  inline, same sentence (a short parenthetical is fine).
- Consequences, not labels. "A → re-run now" is a label; "A → re-run now (fast,
  but repeats the stall if that reading is wrong)" is what lets a non-expert
  actually decide.
- It comes FIRST. Evidence and detail go BELOW the block, and only when they'd
  change the call — never as preamble above it.
- The Answer line is the exact action, replyable in one word or one letter. This
  line IS the message; everything else is optional reading.
- Don't re-narrate the sub-agent's report — extract the decision; the report body,
  if kept at all, goes below.

The format above is universal. The block below is ONLY an illustration of its
SHAPE — a generic scenario, not part of this skill's domain. Your real situation
will differ; never reuse its wording, terms, or subject.

Example (illustration only):

> - **Problem:** The task you asked for depends on another unfinished task — setting up the login service — so running it now would build on a piece that could still change underneath it.
> - **Choices:** A → wait until the login task is done, then run this one (safe, but blocked until that lands) / B → run now against the half-built version and redo the affected parts if it changes later (unblocks you today, risks rework).
> - **Rec:** A — the login task is nearly done, so waiting likely costs less than B's rework.
> - **Answer:** yes → I wait for the login task, then run this · no → run now and accept possible rework.

## Changing sequences

WHEN the user gives ordered step keys + a name → DO: append a row to the registry
in `references/sequences.md`. Then it's runnable via `as <name>`. WHEN no
existing step key fits → DO: add a new `### <key>` to the step library first.

WHEN the user wants a different default for every run, or their own sequences
kept out of the skill → DO: put them in the project override
`.agents/seq/sequences.md` and set its `Default:` line — no edit to this skill;
delete the file to restore. (`references/sequences.md` → Project override.)

## Hard rules

- DO NOT commit, bump version, or edit ChangeLog — the user's.
- DO NOT create, rename, or resequence tasks — that's the task source's job.
- DO one task at a time; pause between in milestone mode.
