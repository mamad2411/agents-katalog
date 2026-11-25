---
name: goal-writer
description: Drafts a goal+rider document pair that briefs an autonomous coding agent on one round of work — a goal file under 4,000 characters (sized to fit the /goal command in both Claude Code and Codex) plus an unbounded rider with phased plans and named depth tests. Use when the user says "draft a goal", "write a goal+rider", "new goal for the next round", "rider for X", "brief the next agent on X", or asks for a /goal condition or objective for Claude Code or Codex.
license: Apache-2.0
metadata:
  author: Nick Spisak
  version: "1.0.0"
  based-on: "goal-rider-author v1.0.0 by SpecStory, Inc. (Apache-2.0) — gregceccarelli.com/goal-engineering"
allowed-tools: Bash Read Write Edit Glob Grep
---

# Goal Writer

Two documents brief one round of autonomous agent work:

- **Goal** — the spine, hard-capped at 4,000 characters: what to do, what
  to read first, the posture, the verification, the stop condition. Small
  enough to paste directly into `/goal` in Claude Code or Codex.
- **Rider** — the prescriptive detail, unbounded (typically 10–35 KB):
  data schemas, phase plans, named depth tests, verb signatures, error
  footers, out-of-scope lists.

The pair is portable: the same two files brief Claude Code, Codex CLI,
Cursor, or a human reviewer without modification. The slash command is
the runtime; the pair is the spec. The pair compounds; the slash command
does not.

The pair is also **primitive-agnostic**. A loop is an agent repeating
cycles of work until a stop condition is met, and `/goal` is one of four
loop types (turn-based, goal-based, time-based, proactive). `/goal` is
this skill's primary runtime, but the same two files feed a turn-based
verification skill, a scheduled `/loop`, or a proactive routine without a
rewrite — see [references/harness-goal-commands.md](references/harness-goal-commands.md).
Start with the simplest loop that fits the task.

This skill is project-agnostic. Substitute the project's own toolchain
commands wherever the templates say `<project's ... command>`.

## When to use

- The user is starting a new round of agentic work and wants goal+rider
  files written into the project's `docs/goals/` (or equivalent).
- Right scope: **one feature, two to five files, half a day to a day of
  agent runtime**.

When NOT to use: fifteen minutes of polish, a hot-fix, or a tiny PR — a
five-line CSS tweak doesn't need eleven phases. The overhead only
amortizes against rounds that would otherwise run hours of agent time.

Soft prerequisites — check, and tell the user what's missing:

1. An architecture / AS-BUILT doc and a CHANGELOG. If absent, offer to
   write a minimal AS-BUILT first (one round, one rider, one phase).
2. A fast test lane (~30 seconds). If the suite takes 40 minutes, the
   phase loop breaks down.

## Pre-work — do not skip

Gather context before drafting. Read in this order, skipping items the
project doesn't have:

1. **Project architecture doc** — `AS-BUILT-ARCHITECTURE.md`,
   `ARCHITECTURE.md`, `docs/architecture.md`, or whatever the project
   uses. A "what's shipped vs thin" section, if present, grounds the
   goal in reality.
2. **Prior goal+rider pairs** in `docs/goals/`. Their invariants compose
   forward; do not duplicate verbatim. Skim the most recent two pairs to
   absorb voice and section conventions.
3. **Recent commits**: `git log --oneline -30 -- docs/goals/` and
   `git log --oneline -30`. Reveals delivery cadence and the
   conventional-commit format in use.
4. **Source code at HEAD** for any data structures, file paths, or
   function names you'll quote in the rider. Verify they match HEAD
   before citing.
5. **Research or pain-point reports** (unmet-needs docs, retros). They
   ground the ergonomics in real pain.

If you can't find prior pairs or an architecture doc, **ask the user**
for a pointer — don't invent one. If `docs/goals/` doesn't exist,
create it.

## Step 1 — Scope the round

Pick a **headline word**: one word naming the end-state after the round
(Liveness, Coherent, Friendliness, Hardening, Self-documenting). If you
cannot pick a single word, the scope is two rounds — split it.

Then state **one measurable end state**. Both harnesses' official
guidance converges here:

- Claude Code: a condition needs *one measurable end state*, *a stated
  check* ("`npm test` exits 0"), and *constraints that matter* ("no
  other test file is modified").
- Codex: "A good goal is bigger than one prompt but smaller than an
  open-ended backlog" — one objective, one stopping condition, files to
  read first, commands that prove progress.

## Step 2 — Draft the goal (≤ 4,000 characters)

**Path:** `<project>/docs/goals/<YYYY-MM-DD>-<HHMM>-<project-slug>-<topic>-goal.md`
where `<HHMM>` is the local 24-hour authoring time, so `ls docs/goals/`
sorts in true authoring order.

**Hard cap:** `wc -c` ≤ 4,000. Both harnesses cap `/goal` input at
4,000 characters; `wc -c` counts bytes, which is conservative
(bytes ≥ Unicode chars), so it is safe for both. The cap is the forcing
function: it makes you decide what the goal *is* before writing it.

Follow the full skeleton in [references/goal-template.md](references/goal-template.md).
Section order:

1. `GOAL:` line — starts with a verb, names the current pain with real
   file paths and function names, ends with the headline word.
2. `**Read first.**` — absolute paths: architecture doc, the rider,
   exemplars. Non-negotiable; if you can't point at grounding documents,
   the round isn't ready.
3. `**Posture.**` — what does NOT change this round. Mostly negations:
   "No schema changes. No new deps. No `git push`." Posture is the fence
   that keeps an agent under pressure from inventing solutions outside
   the round.
4. Domain body — modes, verbs, contracts; the what-to-build.
5. `**Phases.**` — one line pointing at the rider's phases and the loop:
   depth test → implement → green → commit.
6. `**Verification.**` — observable commands and assertions. Every
   bullet must be **transcript-provable**: a command the executing agent
   runs whose output lands in the conversation. Claude Code's goal
   evaluator never runs tools — it judges only what the agent surfaced.
7. `**Stop when**` — a single sentence tying verification to the final
   commit. Optionally add a bound: "or stop after 20 turns."

**Trim priority when over budget:** drop parenthetical detail already in
the rider → shorten Read-first entries to bare paths → compress Posture
→ cut verification smokes to two → drop cross-rider notes.

## Step 3 — Draft the rider (no cap)

**Path:** same directory, same `<YYYY-MM-DD>-<HHMM>` prefix as the goal,
suffix `-rider.md`. Author the goal first, then mirror its timestamp —
never split the pair across minutes.

Follow the full skeleton in [references/rider-template.md](references/rider-template.md).
Top-level sections, in order:

| Section | Carries |
|---|---|
| Posture (decided — do not redesign) | Maturity tier, no-schema-change, no-push, no-V1-invention |
| Data model (files, not fields) | JSON schema per new state file |
| Algorithms | Pseudocode for non-obvious logic — the rider IS the spec |
| Verb signatures | CLI verbs, flags, refusal-cases table per verb |
| Phases (eleven) | `### P1`–`### P11`, named depth tests per phase, written first |
| Integration matrix | Feature × mode table (when multi-mode) |
| Error-footer canonical pairs | `\| Error \| try: \|` table |
| Out of scope | One bullet per V1-candidate item |
| Dependencies | Tier 1 / 2 / 3 policy |
| Engineering invariants | Do-not-violate list |
| Process invariants | Commit cadence, CHANGELOG, demo capture |

The rider opens by citing the goal's absolute path and stating it
"supersedes nothing in prior riders — their invariants still apply."

**Every phase follows the same loop:** write the named depth tests
first and watch them fail → implement the slice → project's full
build+test+lint+fmt green → one conventional commit ending `(rider PN)`
→ one CHANGELOG line. **P11 is doc-only**: architecture-doc section +
CHANGELOG milestone block, no depth test. Eleven is a target, not a
rule — nine to twelve is fine when the structure earns it.

**Depth tests are named behavioral assertions**, listed in the rider
before any implementation exists:
`stallguard_sigterm_then_sigkill_after_grace_period`, not
`test_stallguard_5`. Each name should be defensible in code review.

## Step 4 — Validate

Run the bundled validator:

```bash
scripts/validate_pair.sh <goal-file> <rider-file>
```

Five mechanical checks: goal ≤ 4,000 bytes; rider has ~11 `### PN`
headers (9–12 warns, only a missing phase structure fails); rider has
the six standard `##` sections; the two files cite each other by
filename; both filenames share the same `<YYYY-MM-DD>-<HHMM>` timestamp
prefix. Fix and re-run until it exits 0. Then stage both files.

## Step 5 — Commit and hand off

Commit the pair:

```
docs(goals): add <topic> goal+rider (<one-line headline>)

<2–3 sentences: what the goal is for; what the rider prescribes; what's
explicitly out of scope. Mention named depth-test discipline,
files-not-fields posture (if applicable), and the V1 invention guard.>
```

Add the project's standard `Co-Authored-By:` footer if it uses one.

Then tell the user how to start the round — the goal file body pastes
directly into either harness's `/goal` because of the cap:

- **Claude Code:** `/goal <goal file body>` (or headless:
  `claude -p "/goal ..."`).
- **Codex CLI:** `/goal <goal file body>`.

**Model selection (recommendation).** Spend the sharpest, most limited
model on judgment — scoping the round and authoring this pair — and hand
the execution to a thorough builder. In practice that is often the
architect/builder split: the most capable model designs and writes the
goal+rider; Codex, which tends to be more exhaustive on implementation
detail, runs the phase loop. Route recurring or mechanical loops
(time-based, proactive) to smaller, faster models and reserve the
expensive model for the calls that actually need judgment. Choosing the
right model per task is as much a token-management lever as the turn cap.

Harness mechanics, evaluator limits, and per-harness tips:
[references/harness-goal-commands.md](references/harness-goal-commands.md).

## Discipline checklist

1. Two documents, two budgets — `wc -c` the goal before declaring done.
2. One shared timestamp per pair; filenames sort chronologically.
3. Phased local commits only; never instruct `git push`.
4. Files-not-fields: durable per-feature state lives in working-tree
   files (write `.tmp`, then atomic rename), not new struct/DB fields.
5. Depth tests first — a phase whose tests were never red is suspect.
6. P11 always updates the architecture doc + CHANGELOG; "shipped vs
   thin" lists stay honest.
7. Out-of-scope decisions go to `docs/V1-CANDIDATES.md`, never silently
   expand scope. Each round ends with next round's candidate list.
8. Conventional commits, scoped; execution commits end `(rider PN)`.
9. Frontmatter of human-readable artifacts mirrors the project's own
   convention — if prior impl docs exist, match their shape
   (Date / Status / Commit span / Owner); if not, propose a minimal
   frontmatter and keep it stable across riders.
10. Friendliness is verifiable: auto-detect don't ask; preflight +
    preview; refuse with `try: <command>` lines; one-command rollback;
    lifecycle hints. Each bullet gets a depth test.
11. Judgment in markdown, invariants in code: when the project has a
    skill / prompt-template / config-driven prompt mechanism, prefer
    it over a hardcoded const so users can tune voice or behavior
    without a rebuild (project-specific; skip if no such mechanism
    exists).
12. Verification must be provable from the executing agent's own
    transcript output — a tool-less evaluator can only judge what the
    agent surfaced.
13. Verification as a companion skill (recommended for user-facing
    rounds): encode "what good looks like" as a `SKILL.md` with
    quantitative checks and the tools/connectors to run them, and point
    the rider's Verification at it, so the agent self-verifies
    end-to-end instead of trusting a successful edit. Depth tests and a
    verify skill reinforce each other; the verify skill runs headless in
    both harnesses. See the rider template.
14. Loop hygiene (recommended): set an explicit turn cap in `Stop when`
    ("stop after N tries"); after the round, run a fresh-context
    reviewer (`/code-review` or a second agent); and when a result
    misses the bar, encode the fix as a durable invariant or named depth
    test so every future iteration inherits it — don't just patch the
    one issue.

## Anti-patterns

- Inventing V1 architecture inside an alpha rider.
- Schema changes without a stated strong reason.
- Backwards-compatibility shims for code no caller uses.
- Comments explaining WHAT the code does.
- Half-finished implementations ("we'll finish in P12").
- Duplicating prior riders' invariants verbatim — say "invariants hold."
- Depth tests written after implementation.
- Stop conditions that don't tie to verification ("stop when it feels
  done" is not a stop condition).
- Subjective end states ("cleaner", "better", "improved") — the
  evaluator can't judge them; use exit codes, counts, and diffs.
- Inventing CLI verbs not in the goal.
- Emojis in written artifacts.
- "TODO: maybe add X" — either it's P-numbered or it's a V1 candidate.

## Additional resources

- [references/goal-template.md](references/goal-template.md) — full
  goal skeleton with a worked example and trim rules. Read before
  drafting the goal.
- [references/rider-template.md](references/rider-template.md) — full
  rider skeleton, standard 11-phase shape, depth-test naming, threshold
  calibration notes. Read before drafting the rider.
- [references/harness-goal-commands.md](references/harness-goal-commands.md)
  — `/goal` mechanics in Claude Code and Codex (evaluator behavior,
  limits, budgets, resume semantics). Read when handing off or when the
  user asks how the round will run.
- [scripts/validate_pair.sh](scripts/validate_pair.sh) — run it; don't
  re-implement the checks by hand.
