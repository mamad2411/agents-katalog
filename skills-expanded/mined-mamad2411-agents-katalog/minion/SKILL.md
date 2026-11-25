---
name: minion
description: "Delegate a tracked task (or whole milestone) to a headless sub-agent so the main conversation stays small. Activate on 'minion <task>', 'delegate <task>', 'run <task> in a subagent', or any ask to execute tracked work without burning main-window context. The sub-agent runs the spec end-to-end and reports a compact summary back."
license: MIT
---

# Minion

Your delegate. Run one tracked task — or a milestone of tasks — in a headless
`Agent` sub-agent. Heavy work (reads, edits, test output) stays in the sub-agent's
context; the main window sees only a small summary.

You are the orchestrator. Do NOT do the task work yourself. Resolve, gate,
dispatch, relay, pause.

## Task source

Minion needs three task ops: **RESOLVE** (name → spec path), **GATE** (dependencies
+ status), **EXPAND** (milestone → ordered task list). Bind a source, in priority:

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

Dispatch template: `references/dispatch.md`.

## Flow — execute in order

1. RESOLVE. Use the bound task source to map the user's name to its spec path;
   echo the resolution in one line. WHEN the user gives a direct spec path → DO:
   use it as-is, no resolution. WHEN the name is ambiguous (matches more than one
   slug) → DO: ask which; never guess.
2. GATE. Use the task source to read the task's `Dependencies:` + status; confirm
   each is `DONE`. WHEN the source can't supply deps (e.g. a raw path) → DO: read
   them from the spec/repo, or note none are declared.
3. SELF-CONTAINED CHECK. Read the spec. Confirm every decision it needs is in the
   file or the repo — the sub-agent cannot see this chat.
4. PRE-FLIGHT (optional). See the WHEN/DO rules below.
5. DISPATCH. Resolve the sequence first — the project override's `Default:` when
   `.agents/seq/sequences.md` sets one, else `standard`; `as <name>` overrides
   per run. Spawn `Agent` (`subagent_type: general-purpose`) with the prompt from
   `references/dispatch.md`, spec path injected; a non-standard sequence replaces
   the dispatch's baked steps (`references/dispatch.md` → Sequence). Foreground
   by default.
6. RELAY + PAUSE. Branch on the returned `STATUS` (rules below).

## Rules — WHEN / DO

WHEN the user names a milestone, not a single task →
DO: use the task source to expand it into an ordered task list (dep order). Run
one sub-agent per task. PAUSE after each report. Never chain straight through.

WHEN a dependency is not `DONE` →
DO: STOP. Name the blocker. Do not dispatch.

WHEN the spec needs a decision that exists only in this conversation and is NOT
written in the file →
DO: STOP. Tell the user the spec needs that line. Offer to add it (you author
specs in main). Do not dispatch an under-specified task.

WHEN the task is architectural, uncertain, or the user says "preflight" /
"audit first" →
DO: read the spec HERE in main, then audit narrow — LOCATE before READ (grep the
symbols/anchors the spec names, open those regions), READ NARROW (map / signatures
or a line range, full read only what you'll edit). The spec's referenced files +
Criteria bound the surface; no bulk dir reads. This runs in MAIN — keep it tight.
Surface concerns. PAUSE for spec edits. On the user's go, dispatch with
`PREFLIGHT: done` appended so the sub skips its step 1.

WHEN the task is routine grind with no flagged uncertainty →
DO: skip pre-flight. Dispatch directly. The abort contract in the dispatch
template is the safety net.

WHEN an audit was JUST run this session — a prior task's pre-flight or
audit-after — and it covers THIS task's surface (files ⊆ audited set OR
same-milestone continuation) AND nothing mutated that surface since (beyond the
audited task's own validated edits) AND same session →
DO: reuse it. State the call out loud ("reusing audit from <task>"). Dispatch with
`PREFLIGHT: done` AND inject its `PRIOR AUDIT: <the carried LEDGER line>`. Do not
re-audit.

WHEN scope differs, the surface changed, or you are unsure the prior audit covers
this task →
DO: run a fresh audit. When unsure, always fresh.

WHEN the user says `--no-audit` →
DO: skip the main pre-flight ONLY. Send `PREFLIGHT: done` only when a reusable
audit actually covers the task; otherwise dispatch plain — the sub-agent's own
audit-before still runs (it is the safety net). WHEN the user says `--audit` /
`--preflight` → DO: force a fresh audit.

WHEN a project override `.agents/seq/sequences.md` sets a non-standard `Default:`,
or the user passes `as <name>` →
DO: resolve that sequence and inject its ordered steps into the dispatch in place
of the baked standard (`references/dispatch.md` → Sequence; the override format is
in the seq skill's `references/sequences.md` → Project override). Pull each step's
definition, in order: the override's own Step Library → the seq skill's built-in
Step Library (`references/sequences.md`) → the four core steps the dispatch
already bakes (audit-before, work, audit-after, report). WHEN a step's definition
can't be sourced from any of those, or its primary path needs a capability the
headless sub lacks (e.g. spawning sub-agents) with no stated fallback → DO: don't
dispatch blind; tell the user, run `standard`, or ask which to use.

WHEN the sub-agent returns `STATUS: DONE` →
DO: relay the OUTPUT block terse, substance unchanged. PAUSE for review/compact.

WHEN the sub-agent returns `STATUS: ABORTED` →
DO: relay it through the clarifier block (Surfacing a decision below) — the sub is
headless and reports in spec terms, so TRANSLATE its BLOCKER/NEED into plain words
the user can act on; never paste its raw block. Do NOT proceed. Do NOT re-dispatch
blindly. WHEN the sub made partial edits → flag them for revert. Re-dispatch only
after the blocker is resolved — minion is spec-driven, so a re-run after the fix
is clean.

WHEN in a milestone batch and a task returns `ABORTED` or fails a Criteria →
DO: STOP the batch. Surface it. Do not run a task that depends on the stalled one.

WHEN running a milestone batch →
DO: audit the FIRST task fresh (pre-flight or in-sub). For each later task that
continues the same surface, carry the prior task's `AUDIT` ledger forward as its
`PRIOR AUDIT` (dispatch `PREFLIGHT: done`). Re-audit only a task that opens a new
surface. State each reuse.

## Surfacing a decision (clarifier) — WHEN / DO

<!-- Mirror of seq/SKILL.md "Surfacing a decision (clarifier)". Same block, same
     rules — edit BOTH or neither. -->

WHEN minion pauses and puts a choice to the user — a blocked GATE, a spec that
needs a decision, a sub-agent's `ABORTED` finding you relay, a milestone stall, or
a poor-delegation call → DO: lead with this four-line block, in this order, BEFORE
any reasoning:

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
- Translate the sub-agent. It is headless and reports in spec terms — its
  `BLOCKER`/`NEED` name files, symbols, ticket refs the user can't see. Your relay
  IS the clarifier, not a paste of the sub's block; the raw `OUTPUT` goes below,
  if at all.
- No bare references. A spec section, a ticket number, a symbol name — never cite
  what the reader can't see; say what it IS and why it matters, inline, same
  sentence (a short parenthetical is fine).
- Consequences, not labels. "A → re-dispatch now" is a label; "A → re-dispatch now
  (fast, but repeats the abort if that reading is wrong)" is what lets a
  non-expert actually decide.
- It comes FIRST. Evidence and detail go BELOW the block, and only when they'd
  change the call — never as preamble above it.
- The Answer line is the exact action, replyable in one word or one letter. This
  line IS the message; everything else is optional reading.

The format above is universal. The block below is ONLY an illustration of its
SHAPE — a generic scenario, not part of this skill's domain. Your real situation
will differ; never reuse its wording, terms, or subject.

Example (illustration only):

> - **Problem:** The task you asked for depends on another unfinished task — setting up the login service — so running it now would build on a piece that could still change underneath it.
> - **Choices:** A → wait until the login task is done, then run this one (safe, but blocked until that lands) / B → run now against the half-built version and redo the affected parts if it changes later (unblocks you today, risks rework).
> - **Rec:** A — the login task is nearly done, so waiting likely costs less than B's rework.
> - **Answer:** yes → I wait for the login task, then run this · no → run now and accept possible rework.

## Audit ledger

The reuse rules above need a record of what was audited — keep one in context.

WHEN any audit completes — a main pre-flight, or a sub-agent that returned an
`AUDIT` field — DO: record one ledger line, fixed format:
`LEDGER: task=<name> | surface=<globs> | approach=<one line> | proofs=<n/m met> | validated=<yes|no>`.
This is the artifact the reuse rules match against; the fixed format survives
compaction, and the sub-agent's `AUDIT` output is how a headless audit reaches
main.

WHEN a task's `audit-after` validated its surface (tests green, premise holds) →
DO: treat that surface as a reusable `PRIOR AUDIT` for any continuation task — its
own expected edits are already accounted for.

- The ledger is in-context only (this session). New session → no ledger → audit
  fresh. This is why reuse requires "same session".
- Works across skills: a `/seq` audit in main, or a `/minion` `AUDIT` output, both
  populate the same ledger — so you can `/seq` task 1 then `/minion` task 2 and
  reuse.

## Hard rules

- DO NOT commit, bump version, or edit ChangeLog — the user's, always.
- DO NOT create, rename, or resequence tasks — that's the task source's job, in main.
- DO one task per sub-agent.
- DO NOT echo raw sub-agent tool output — relay its OUTPUT block.

WHEN the task spans 3+ unrelated subsystems or is exploratory →
DO: tell the user it's a poor delegation candidate. Recommend running it in main.
