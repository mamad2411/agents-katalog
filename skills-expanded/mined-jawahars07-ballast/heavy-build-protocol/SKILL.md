---
name: heavy-build-protocol
description: The working discipline for heavy tasks - building agents or systems, multi-hour features, large refactors, complex debugging. An eight-phase loop numbered from zero, with a verification requirement in every phase and a single approval gate before anything irreversible. Load it BEFORE starting any task expected to take more than about ten tool calls.
---

# Heavy Build Protocol

Capability differs between models. Discipline transfers.

Follow this loop and you get work that is evidence-grounded, verified, and honestly reported.
Skip phases and you reproduce the failures that made each phase necessary.

## The loop — eight phases, never skip one

Numbered from zero, because phase 0 happens **before the first tool call**. If you find yourself
already running commands, you skipped it.

### 0. FRAME — before any tool call

Write three lines:

- **(a)** the goal, in one sentence
- **(b)** the definition of done
- **(c)** **how done will be verified** — a named, observable check

**If you cannot name the verification, you do not understand the task yet.** That is the whole
point of this phase. "I'll know it works when I see it" is not a check.

Reframe a messy or voice-dictated prompt into a clean interpretation and state it. Do not bounce
back a menu of options at this stage.

### 1. RECON — read reality before planning

Never plan from how things "usually work". In order:

1. Recent change logs — what actually moved lately
2. The actual files and configs involved
3. The actual runtime state. Run it. Read the real error.

**Cheapest evidence first:** `ls` and logs before code reads, code reads before web research.
Batch independent reads in parallel.

*The failure this prevents:* a stored note said a scheduled job had been fixed. The log said
UNRESOLVED. The log was right. Notes describe what was true when written; reality is what runs.

### 2. PLAN — decompose into verifiable stages

Every stage gets an observable exit check: a test count, a clean build, an HTTP 200, a
screenshot.

Identify every irreversible or outward-facing action — deploy, submit, publish, spend, delete —
and place a gate in front of it.

**If the build will generate a lot of code, write a `CONVENTIONS.md` first.** Exact function
signatures, the data shapes, and an explicit "never invent an API" rule. That file exists in one
project specifically because a model hallucinated APIs mid-build; the constraints file fixed it.

### 3. GATE — one approval checkpoint, not many

Batch every question and decision into a **single** checkpoint before anything live or
irreversible. Interrupting six times is worse than interrupting once with six things.

For genuine forks, present options **with a recommendation**. The human decides.

For autonomous-agent builds specifically: a full **dry run** is mandatory before enabling live
execution.

### 4. BUILD — smallest verifiable increment

Fan out independent modules in parallel, with **one central integrator** holding architectural
and design direction. Serialise what genuinely depends.

**One source of truth per fact.** A single config file others read, never the same constant
written in two places.

Match the surrounding code style. Comments only for constraints the code cannot show.

### 5. VERIFY — observe behaviour, do not infer it

**Compiling is not working.** Run the real flow and watch it.

Name the check in your report: "35/35 pass", "build clean, 1909 modules, zero console errors",
"asset returns HTTP 200".

If you cannot see the output, build yourself a feedback loop — a headless screenshot loop, a log
tail, a test harness. Being unable to observe your own work is a problem to solve, not a reason
to guess.

**Kill stale state before trusting results.** A stale dev server holding a port once served an
old build and burned an hour of debugging a bug that was already fixed.

### 6. REPORT — outcome first, failures verbatim

Lead with what happened.

Paste real error output. Never paraphrase it into "there was an issue" — the exact string is the
thing a person can search for.

Mark unfinished work **UNRESOLVED, needs user**. Never round "mostly works" up to done. State
what was verified and what was not.

### 7. LOG — record the lesson, not just the change

Write down *why*, not only *what*. "Moved the UI out of the 3D scene because that overlay
component is unreliable at depth" is worth keeping. "Updated UI" is not.

A session that is not logged did not happen, as far as the next session is concerned.

## Hard rules

Each one traces to a real correction.

1. **Two failed attempts on the same approach means stop.** Change approach, or go research the
   established pattern. One UI element was rejected twice; the fix was not a third variation, it
   was reading how a well-regarded open-source project solved the same problem and replicating
   that. **Research beats thrashing.**
2. **Never invent an API, a flag, or a file path.** Verify it exists — `grep`, docs, `--help` —
   before calling it. If you cannot verify it, say so.
3. **Never fabricate data.** No invented metrics, companies, or usage numbers, anywhere. Seed and
   example figures must be labelled as such.
4. **Ambiguous intent defaults to the safe interpretation.** Destructive verbs — delete, deploy,
   push, submit, uninstall — require explicit confirmation.
5. **Vet third-party code before installing it.** No exceptions, including mid-build when it is
   inconvenient. See the `security-vet` skill.
6. **Scope stays lean.** Ship the smallest thing that proves the point. List the gold-plating as
   "next"; do not build it.

## What a finished heavy task looks like

A real trace worth matching:

> Problem stated with symptoms → root cause traced to specific code (an energy-threshold voice
> detector plus loose substring matching) → three dependency-free fixes, each explained →
> **18/18 tests pass, compilation verified** → tunables documented with their environment
> variable names → a future upgrade noted but deliberately not built, because it needs a new
> dependency → logged with the code paths.

Cause, fix, named verification, documented knobs, an honest scope line, logged. Every heavy task
should end shaped like that.
