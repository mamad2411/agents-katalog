---
name: context-engineering
description: Sets up what an agent knows about a repository - operating contract, conventions, session hygiene, compaction. Triggers - set up CLAUDE.md, AGENTS.md or GEMINI.md, agent keeps ignoring our conventions, output quality dropped in a long session, context window full, when to compact, repo rules.
---

# Context Engineering

An agent's output quality is bounded by what it knows and how cleanly it knows
it. Two failure modes dominate: **starvation** (the agent invents conventions
because none are written down) and **pollution** (so much stale, contradictory
context that the relevant part is drowned). Both look like "the model got worse".

## The context layers

| Layer | Contains | Lifetime |
|---|---|---|
| Operating contract (`CLAUDE.md` / `AGENTS.md`) | Invariants, sequence, bar protection | Months |
| Project profile | Stack, commands, layout, conventions | Changes with the stack |
| Decision record (`docs/adr/`) | Why things are the way they are | Permanent, append-only |
| Quality bar (`CONSTRAINTS.md`) | The numbers | Changes deliberately |
| Task context | The current spec, plan, diff | This task |
| Session scratch | What you just learned by reading code | This session |

Each layer has a home. Facts in the wrong layer rot: a stack detail written
into the operating contract survives its own truth.

## Where each agent reads instructions

| Agent | Loads | See what loaded |
|---|---|---|
| Claude Code | `CLAUDE.md` from the working directory upward, subdirectory files on demand, `@path` imports; by default `AGENTS.md` only when no `CLAUDE.md` exists | `/context` |
| Codex | `AGENTS.md` (or `AGENTS.override.md`) from `~/.codex`, then one per directory from the project root down to the working directory, up to 32 KiB by default | `/status` |
| Gemini CLI | `GEMINI.md` by default; `context.fileName` in `settings.json` can list `AGENTS.md`; an extension loads the file its manifest names | `/memory show` |

Keep one contract: `AGENTS.md`, with `CLAUDE.md` either identical or importing
it (`@AGENTS.md`), and Gemini pointed at `AGENTS.md` through `context.fileName`.
Hand-maintained copies drift apart. Confirm with the
command in the last column — a file that does not load does not exist.

## Writing the project profile

Keep it under ~200 lines. It answers what a new engineer asks on day one:

```markdown
## Stack
Language/runtime + versions. Package manager. Framework. Datastore.

## Commands
Install · run · test (fast) · test (full) · lint · typecheck · build · migrate
Use the checked-in wrapper, not a global tool.

## Layout
Which directory holds what, and the dependency direction between them.

## Conventions
Naming, error handling, logging, config, test placement — as they ARE,
with one pointer to an exemplary file per convention.

## Landmines
Things that look wrong but are deliberate. The one test that must run alone.
The module nobody touches without asking X.
```

Rules that keep it useful:

1. **Describe reality, not aspiration.** If the codebase uses two patterns, say
   which one new code follows and that the other is legacy.
2. **Point, don't paste.** "Follow the error handling in `internal/http/errors`"
   beats reproducing the pattern, which will drift.
3. **Every claim must be checkable.** A wrong command is worse than no command:
   the agent will run it, fail, and improvise.
4. **Prune on contact.** Any time a line turns out to be stale, fix it in the
   same session. Stale context compounds.

## Session hygiene

Degrading output inside a long session is usually pollution, not fatigue:

| Symptom | Cause | Fix |
|---|---|---|
| Re-explains things it already established | Key facts buried | Restate the current goal and constraints in one short message |
| Reintroduces a bug just fixed | Contradictory versions of the same file in context | Start a fresh session; carry over a written summary |
| Ignores a convention it followed earlier | Convention only ever mentioned in passing | Write it into the project profile |
| Drifts to an adjacent problem | Task boundary never stated | State what is out of scope explicitly |
| Confidently wrong about a file | Reasoning from an old read | Re-read before editing |

**Hand off in writing.** Ending a session: write what was decided, what remains,
and what was learned about the codebase into the plan or the profile. A session
that leaves knowledge only in the transcript loses it.

## Handoffs that survive compaction

Compaction and restarts are where sessions lose work: the summary keeps the
gist and drops the half-finished state, the approach already rejected, the
reason a test is red. Keystone makes the handoff a file and loads it for you:

| Piece | Written by | Holds |
|---|---|---|
| `.keystone/handoff.md` | the agent, via `/handoff` | goal, done with evidence, in progress, next step, decisions, rejected approaches, open questions |
| `.keystone/state/session.json` | the `session.handoff-save` hook, before compaction | branch, head, changed files, last `/verify` result |
| `LESSONS.md` | `/retro`, after review | lessons that outlive the task |

The `session.handoff-load` hook puts the note and the recorded state into the
next session's context, capped near 1,000 tokens and marked as a note to check
against the repository. Write the note before a long task is interrupted and
before you expect compaction, not after: the hook can record mechanics, only
the agent knows which approach already failed.

Compact at boundaries, not mid-change: after research and before
implementation, after an abandoned approach, between unrelated tasks — each
time after writing the handoff. (`/compact` in Claude Code and Codex,
`/compress` in Gemini CLI.)

Three rules keep handoffs honest:

1. **Evidence or it is "in progress".** "Done" without a command, test or
   commit behind it is a guess the next session will trust.
2. **Replace, don't append.** A handoff is the current state, not a diary.
3. **Promote what lasts.** Stack facts go to the profile, decisions to an ADR,
   lessons through `/retro` into `LESSONS.md`, rules into a check.

## Context and cost budget

Every token loaded at session start is paid on every turn and competes with
the task for attention. Budget it like any other resource:

| Context | Budget | Why |
|---|---|---|
| Always loaded: contract + profile + skill catalog | ≤ ~6,000 tokens | It rides along on every request; Codex drops all skill descriptions past its catalog budget |
| Handoff note | ≤ ~1,000 tokens | Enough for state; more is a transcript |
| A single tool result carried forward | Summarize past ~200 lines | Raw dumps crowd out the task |

Cost controls that do not trade away quality:

- **Fresh context for broad searches.** Delegate a wide sweep to a subagent and
  keep its conclusion, not its file reads.
- **Match the model to the step.** A cheaper model for mechanical edits and
  searches; the strongest model for design, debugging and review.
- **Stop loops early.** An agent that fails the same check three times needs a
  different approach or a human, not a fourth attempt.
- **Measure, then budget.** Read the harness's own meter (`/context`,
  `/status`, `/stats model`) per task for a week before setting a number;
  record it in `CONSTRAINTS.md` (§4 has a row for agent cost) so it is
  defended like any other budget. An estimate is not a measurement.

## Retrieval discipline

- Read before you edit — every time, not once per session.
- Prefer targeted reads (grep, symbol search) to whole-file loads.
- Summarize large outputs into conclusions; do not carry raw dumps forward.
- When the agent must know something to proceed, put it in a file, not a
  message. Files survive; messages scroll away.

## When not to use this

Don't restructure context as a response to one bad answer. Fix the answer, note
the cause, and change the context only for a pattern you have seen more than once.

## Exit checklist

- [ ] `CLAUDE.md` exists and states invariants only
- [ ] `AGENTS.md` exists for non-Claude agents and matches; each agent in use
      was shown to load the contract with its own command
- [ ] Project profile lists commands that were actually run and verified
- [ ] Conventions point at exemplary files rather than restating them
- [ ] `CONSTRAINTS.md` exists with real numbers
- [ ] Landmines section names the non-obvious hazards
- [ ] Nothing in the profile duplicates or contradicts the operating contract
