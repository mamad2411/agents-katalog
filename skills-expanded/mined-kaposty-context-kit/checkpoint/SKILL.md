---
name: checkpoint
description: |
  Prepare for context compaction by hand, with care, before you run /compact.
  A deliberate, model-driven pass that brings ALL durable context up to date so
  nothing is left stale anywhere: flushes the Session Ledger, syncs the plan file,
  carries what outlives the task into the project state file, graduates
  cross-project lessons into the memory store, reconciles project knowledge docs, refreshes the current situation (a /update-style "where we are, what's
  next"), guards against context bloat, and only then gives a green light to
  compact. It never compacts by itself. It exists because
  automatic compaction gives the model no turn to prepare, so quality
  preparation has to be a deliberate step. Complements the Session
  Ledger; does not replace it.
  TRIGGERS: "/checkpoint", "checkpoint", "prepare compact", "prepare for compaction",
  "before the compact", "save the context", "compact vorbereiten", "kontext sichern",
  and the same intent in any other language. Fire it right before every manual
  /compact. Two other things can ask for it: the UserPromptSubmit hook
  prompt-checkpoint.sh recognises those same phrases and keeps working after a
  compaction has dropped this description, and the Stop hook can ask by name once
  enough work has piled up, which is opt-in and ships off.
  Project-agnostic: no assumptions about language, stack, or repository layout.
---

# Checkpoint: prepare for compaction, deliberately

A compaction nobody prepared flattens the reasoning into a summary that keeps roughly
what happened and loses why. This skill is the answer: **fire this checkpoint by hand
whenever the window is getting full, right before you run `/compact` yourself.**

The whole point is that a prepared pass HAS a turn. So unlike a hook, it can actually
think: read the session, decide what matters, write it down well, and hand you a clean
state to compact from. Quality preparation is only possible when something fires it.

This does two things a raw `/compact` cannot: it makes the durable context **complete
and current** before the summary is taken, and it keeps the **red thread** (where we
are, what is next) explicit on disk so nothing depends on the summary being good.

## What it is not

- It does **not** run `/compact`. It prepares; you compact. The last line it prints is
  the go-signal, then you type `/compact`.
- It is **fired by hand**, by you, before every manual `/compact`. The `Stop` hook can fire
  it once enough work has piled up, but that is opt-in and ships off, because a pass that
  starts on its own interrupts work nobody asked to interrupt. Where it is switched on, the
  phases are the same with one difference: an auto-fired pass is housekeeping nobody asked
  for, so it reports **one sentence** (it ran, `/compact` is due) instead of the four-line
  hand-off below.
- It does **not** replace the Session Ledger. The ledger is the always-on discipline;
  this is the periodic deep pass that brings the ledger (and everything else) fully
  up to date before a compaction.

## Before you start: can this session write at all

Every phase below ends in a file write, so one check comes first. If the session is in plan
mode, `Write` and `Edit` are refused, the ledger included, and the refusal names no cause
(`Permission to use Write has been denied`). Measured on 2026-08-22, inside a checkpoint
pass: two refusals on the ledger before the third attempt landed. The gate can also outlast
an approved plan for the rest of that turn.

Retry the same write once, and do not work around it: no second path, no shell heredoc. If
it stays refused, say in one sentence that the pass cannot write while the plan is in
flight, hand back what you would have written, and end the turn. The next turn runs the
phases. A checkpoint that reports green without having written is worse than one that says
it could not run.

## The process

Run these in order. Each phase is a quality gate, not a checkbox.

### 1. Sweep the session
Look back over everything since the last checkpoint. Extract, honestly and completely:
- **Decisions** that got locked, and what each beat.
- **Facts** that got verified, each with the exact command or probe that proved it.
- **Questions** that opened, and what would settle them; and questions that got answered.
- **Paths** that were abandoned, and why (so they are never retried).
- **Task** shifts: is the goal still what the ledger says?

Do not summarise from memory of the summary. Read the actual work. A decision you fail
to capture here is a decision the compaction will erase.

### 2. Flush the ledger
Write everything from the sweep into `.claude/session-ledger.md`, in its sections
(`TASK`, `NEXT`, `OPEN`, `DECIDED`, `VERIFIED`, `DROPPED`, `PLAN`). Resolve items **in place**:
an answered `OPEN` becomes a `DECIDED` or `VERIFIED` and leaves `OPEN`. The ledger is a
working set, not a log. Keep it thin: no bulk data, no re-derivable status.

### 3. Sync the plan, and keep it cheap to read
If a plan file exists (the ledger's `PLAN` pointer), bring it current: mark done
endpoints done, add endpoints that emerged, append one dated decision-log line per real
change, and record any dropped approach with its reason. The plan is the long-form red
thread; the ledger points at it.

**A plan is the most expensive file this pass touches, so it gets a size discipline the
other stores do not need.** Measured in one real project: a single plan document had grown
to 116,000 characters, roughly 29,000 tokens, and there were fourteen of them. Reading one
to sync it costs more window than everything else in this kit combined. Nothing warns you,
because a plan grows one honest paragraph at a time.

Split it by how often it has to be read, and let each part live where its reading frequency
puts it:

- **The spine** is the part you sync: the endpoints, their status, the open questions, the
  decision log. This is what a checkpoint reads, so it stays small enough to read in full.
- **The evidence** is what made those endpoints right: sources, measurements, transcripts,
  the reasoning behind a call. Written once, read rarely, and it belongs in its own file
  next to the plan or in a clearly marked section below the spine. Never between endpoints.
- **The archive** is finished work. **Carried out means gone from the spine**, exactly as in
  the ledger: a done endpoint moves to a `done` or `archive` file with its date and its
  outcome, and nothing reads that file again. Deleting is wrong, it is the record of why the
  thing looks the way it does; leaving it in the spine is also wrong, it is paid for on
  every future read.

So this phase has a second half: after syncing, look at what the spine now costs. If it has
outgrown a comfortable read, move the finished endpoints out and say in one line that you
did. If the project keeps no plan file, there is nothing to do here and nothing to report.

### 4. Refresh the situation (the /update part)
Produce a concise, current picture:
- **Where we are**: the one-line state of the work right now.
- **What is next**: the single most valuable next action, with its lever and rough effort.
- **Open risks or blockers**: anything that would derail the next step.

Most of this is freshly derived and stays unstored, because it is re-derivable. Recompute
mechanical state here (branch, open work, test state) rather than carrying it.

**One exception, and it matters: write the "what is next" line into the ledger's `NEXT`
section.** It is a judgement, not a lookup, and after a compaction it is the very first
thing anyone needs. Spoken only in the hand-off, it dies with the summary; written to
`NEXT`, it comes back with the restore. Keep it to one line and keep it current.

### 5. Guard against bloat
Before compacting, catch context that must **not** survive:
- Large files or pasted bulk data (CSVs, logs, dumps) sitting in context. These belong
  in code-processed form, not the window. Name them and say: re-derive via a script, do
  not carry.
- Anything already on disk that is being duplicated in context.
A compaction that carries a 5 MB CSV forward is a compaction that failed. Flag it so the
post-compact window stays lean.

### 6. Bring all durable context current (not only the ledger)
The ledger is this session's working set. But durable knowledge that outlives the
session lives in other stores too, and a checkpoint's job is that **nothing durable is
left stale, anywhere**. Walk each durable store this project keeps and reconcile it
against what this session actually established.

**Which stores those are is not hardcoded, it comes from the context manifest**, the file
`context-manifest.yaml` in the project root (`context-manifest.example.yaml` in this kit is
the template). Read it before this phase. The fields that matter here are the `memory`
block plus `compaction.checkpoint.durable_context.project_state`, `.knowledge_docs` and
`.curated_ssot`.
That is what keeps this generic: the logic is the same everywhere, the manifest names the
paths per project. With no manifest, fall back to finding them by convention (a memory
index, a project state file, a plan file, the project's top-level knowledge docs) and say
which you reconciled,
so the softer discovery is visible. Then:

**The rule that governs this whole phase: reconcile, never append.** A durable store is
edited the way you would edit a wrong sentence, not the way you would add a log line. If
this session made an entry false, correct that entry or delete it; if it refined one, rewrite
it; only genuinely new knowledge becomes a new entry. Appending is what turns a memory store
into a pile where the newest and the outdated sit side by side and the reader cannot tell
which is which. In Claude Code the memory store is the auto-memory directory with its
`MEMORY.md` index (the manifest's `memory` block names it if the project puts it elsewhere).

Three stores, and what separates them is **reach**, not form. The test is one sentence:
*would this be useful in a different project?*

| Store | Reaches across | Carries |
|---|---|---|
| the ledger | one task, across compactions | the working set of the task in hand |
| the project state | every task in this project | where it stands, next steps, decisions, dropped paths, open questions |
| memory | every project | techniques, platform traps, how the user wants to work |

- **Project state** (`.claude/project-state.md`, or the path the manifest's
  `durable_context.project_state` names). The ledger is deliberately mortal: a new task
  archives it, and `DECIDED` and `DROPPED` go with it. That is the gap this file closes, so
  reconcile it every pass. What belongs here is what a later task would otherwise re-open:
  the decision and what it beat, the abandoned path and why, where the work stands, the next
  step. Keep it the same shape as the ledger, at project scope, and hold the same size
  discipline: correct and delete, never let it become a log.
- **Memory store** (long-term, cross-**project** facts). If this session produced something
  that would help in a **different** project, a reusable technique, a platform trap, a
  correction to how the user wants to work, write it into memory **now**. A fact that only
  matters here belongs in the project state instead, or it will sit in memory as noise for
  every other project. Discipline so memory stays signal, not a dump:
  - one fact per entry;
  - before adding, look for an existing entry that already covers it and **update that**
    instead of creating a duplicate;
  - **delete** an entry this session proved wrong;
  - keep the memory **index** in sync (a one-line pointer for each new entry);
  - only genuinely durable, cross-session facts, **never** this session's volatile state.
- **Project knowledge docs** (the domain notes, data dictionaries, methodology, status
  files this project maintains). If this session changed what is true, bring the affected
  doc current **in place**. A statement that is now wrong is worse than no statement.
  Reconcile, never append blindly.
- **What NOT to touch**: a manually curated single-source-of-truth file stays the human's,
  flag it as stale if it is, but do not clobber the curated part. And never write
  re-derivable or volatile state (branch, open reviews, build status) into any durable store.

The test for this phase: after it, is there any durable file in the project whose content
this session made **false or incomplete**? If yes, the phase is not done. "Context must
never be stale, anywhere" is the bar.

### 7. Put what is blocked on you to you

A checkpoint that carries a user dependent blockage into the compaction makes the exact
mistake this step exists against: after the compaction the blockage is still there, one
window later, and nobody was asked. So before the green light, whatever in `OPEN` stands in
the way of `NEXT` and only the user can settle goes to them in one `AskUserQuestion` call,
at most four, the recommendation as the first option with its reason in the description.
Only what blocks `NEXT`, never the whole section, and no call at all when nothing is
blocked on them. Where the tool does not exist, the same questions are the last lines of
the reply, numbered.

### 8. Green light (content check, then write the marker)
**First, a content check.** The marker asserts "the context is prepared", so it must not
sit on top of an empty ledger. If this session genuinely had reasoning (decisions,
verified facts, dropped paths) but the ledger is still empty after phases 1 to 7, the
checkpoint did not do its job: go back and flush it. A fresh marker over a hollow ledger
is a false "preserved" signal, and it is exactly what the freshness guardrail cannot catch
on its own, because the guardrail checks recency, not content. The only legitimate empty
ledger is a session that truly had nothing worth carrying; if that is the case, say so
explicitly rather than leaving it implied.

Then **write the freshness marker** so the guardrail knows a checkpoint just ran. **The
marker is per session**, and the session-start block named the exact path: look for the line
`Checkpoint marker for this session:` and write that file.

```bash
mkdir -p .claude && touch .claude/.checkpoint-ready.<the id from that line>
```

If you genuinely cannot find the path (no session-start block in context and none in the
transcript), write your session id into `.claude/.checkpoint-ready` instead
(`echo <id> > .claude/.checkpoint-ready`, and if you do not have an id either, an empty
`touch` still counts) and say so in the hand-off. That is
the shared fallback the guardrail still honours; it is only worse in a directory where
several sessions run at once, and there it is worse for a measured reason. A single shared
file made the guardrail test freshness rather than authorship, so a session that had never
checkpointed was waved through as soon as any other session set the marker.

Do not invent an id, and do not reuse one from a restored ledger: it belongs to the session
that wrote it, not to this one. A marker under a foreign id counts for nobody.

This is the one side-effect the skill leaves on disk. A companion `PreCompact` guardrail
hook blocks `/compact` unless this marker is fresh. The guardrail is idle-aware: if the
ledger has not changed since the marker, `/compact` passes regardless of clock age (prepare
at night, compact in the morning); the time window (default 8h,
`SESSION_LEDGER_CHECKPOINT_MAX_AGE_MIN`) only bites when work happened since. Write the
marker only after phases 1 to 7 are genuinely done, never as the first step.

Then finish with a hand-off of **at most four lines**:
- one line on what was persisted (ledger updated, plan synced, N decisions / M verified
  captured),
- the "what is next" line, so it survives verbatim,
- any bloat warning from phase 5,
- then: **"Checkpoint saved. Safe to run /compact now."**

This is a hard ceiling, not a style preference. Everything the checkpoint touched is on
disk and readable; repeating it in prose makes the user read the bookkeeping instead of
benefiting from it. So: no inventory of what was moved where, no per-section character
counts, no explanation of which entries were collapsed and why, no note that the size
limit was involved. The checkpoint is the one moment where a few lines are earned,
because the user asked for it. Everything around it stays silent.

Then stop. The user runs `/compact`. Getting the flushed reasoning back afterwards leans on
the ledger FILE plus a re-read line in the instruction file: the `compact`-matcher reinject
hook fires only late (best-effort) and there is no reliable PostCompact restore, so the
durable carrier is the file on disk. The restore output carries a canary line; if a later
turn is missing this reasoning and the canary is absent, read `.claude/session-ledger.md`.

## Relationship to the guardrail

The harness shows a compact affordance as the window fills (around 50%), your cue to run
this skill then `/compact`. The `PreCompact` guardrail (`precompact-guard.sh`) holds that
order: it blocks `/compact` when no checkpoint has run, and also when a marker sits over
a ledger that is still an empty skeleton, so a checkpoint that captured nothing does not
buy a green light. It cannot see whether this pass wrote down everything worth keeping,
that part is on this skill. **You fire the checkpoint, it prepares and marks; the
guardrail refuses the compaction until something is actually there.**

## Quality bars (what "maximal sauber" means here)

- Every verified fact carries its command. A claim without provenance is a belief.
- Every dropped path carries its reason. Otherwise it gets proposed again.
- Nothing important is left only in volatile context. If it matters, it is on disk.
- The ledger stays thin and re-derivable status stays out. Preparation is curation, not
  hoarding.
- The red thread is a single clear "next action", not a wall of state.

## Why manual, and why now

A hook cannot do this: it has no model turn and cannot judge what matters. Neither can a
compaction that nobody prepared, because by then there is no turn left. Only a fired pass
can read the session and curate it. So: **make firing this checkpoint the habit before
every compaction.** The context system carries the state; this pass makes sure the state
is worth carrying.
