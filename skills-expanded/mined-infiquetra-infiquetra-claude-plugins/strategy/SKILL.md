---
name: strategy
description: Create or maintain the repository root STRATEGY.md — the durable direction anchor (target problem, approach, who it's for, key metrics, tracks). Interview-driven and rerunnable. Triggers on "write our strategy", "update the direction", "what are we working on", "set up the strategy doc", and when /ideate, /brainstorm, or /plan need upstream grounding and no STRATEGY.md exists yet.
argument-hint: "[optional: section to revisit, e.g. 'metrics' or 'approach']"
---

# Strategy

Ported from Compound-Engineering ce-strategy; CE downstream ce-ideate / ce-brainstorm / ce-plan map to infiquetra /ideate / /brainstorm / /plan.

`/strategy` produces and maintains the repository root `STRATEGY.md` — a short, durable anchor that
captures what the product is, who it serves, how it succeeds, and where the team is investing. It lives
at the repo root as a canonical well-known file (a peer of `README.md`). A handful of sharp questions,
answered well, produce a better strategy than any amount of prose; this skill asks them, pushes back on
weak answers, and writes the doc.

## Position in the lifecycle

`/strategy` is the **durable direction anchor** — top-of-funnel, off-chain, and **advisory**. It sits
upstream of execution: it never enters the work thread and never writes the saga. Its only durable
output is the root `STRATEGY.md`, which downstream skills read as grounding. It is the **records**
member of a record-vs-challenge-vs-readiness trio that can all touch direction:

- **`/strategy` RECORDS direction** — captures the chosen direction in `STRATEGY.md`.
- **`/founder-review` CHALLENGES it** — is the direction ambitious, coherent, and worth doing?
- **`/doc-review` checks `STRATEGY.md` READINESS** — can the doc safely drive implementation? (its path
  tie-breaker maps `STRATEGY.md -> strategy/scope`.)

The inbound edge: `/office-hours` is the frame-finding front door, and once a direction-ask settles into
a real "where are we pointed" question, it **routes that onward to `/strategy`** to record it.

## Core principles

1. **Anchor, not plan.** Strategy is what the product is and why. Features belong in `/brainstorm`;
   schedules belong in the issue tracker. Do not let either creep into the doc.
2. **Rigor in the questions, not the headings.** The headers are plain English; the interview questions
   in `references/interview.md` are what enforce strategy discipline.
3. **Short is a feature.** The template is constrained. Adding sections costs more than it looks like —
   push back on expansion.
4. **Durable across runs.** This skill is rerunnable: it updates in place, preserves what is working,
   and only challenges stale or weak sections. On a **material direction shift**, *suggest* a
   `docs/engineering-journal/DECISIONS.md` ADR to record why direction changed — offer it, do not
   auto-write it.

## Interaction method

Use `AskUserQuestion` for **routing** decisions only — which section to revisit (call `ToolSearch` with
`select:AskUserQuestion` first if its schema is not loaded). Use **free-form** responses for the
substantive sections (problem, approach, persona, metrics, tracks): they are inherently narrative and
menu options would nudge the answer. Ask one question at a time; never silently skip a question.

In a channel session (`redis-channel` active), `AskUserQuestion` cannot be called — inline the choices
in your reply text instead, following the canonical channel-inline convention in
`saga/skills/brainstorm/SKILL.md` (do not duplicate its wording here).

Use repo-relative paths in everything you write — absolute paths break portability across worktrees.

## Focus hint

Interpret any argument as an optional focus: a section name to revisit (`metrics`, `approach`,
`tracks`) or a scope hint. With no argument, proceed open-ended and let the file state decide the path.

---

## Phase 0 — Route by file state

Read the root `STRATEGY.md` using the native file-read tool, then route:

- **File does not exist** -> first run. Go to Phase 1. Announce: "Strategy doc not found — let's write
  it."
- **File exists AND the argument names a specific section** -> targeted update. Go to Phase 2.
- **File exists, no argument** -> ask which section(s) to revisit (`AskUserQuestion`), then Phase 2.

Announce the path in one line: "Found existing strategy — let's review and update."

## Phase 1 — First-run interview

Load `references/interview.md`. **This load is non-optional** — the pushback rules, anti-pattern
examples, and per-section quality bar live there. Improvising from memory produces a passive
transcription instead of a strategy doc.

Run the interview in the section order of the final document, with the opening question, the pushback
rules, and **two rounds of pushback per section maximum** (capture what the user gave after that and
note the section is worth revisiting next run):

1. Target problem
2. Our approach
3. Who it's for — **agent-as-customer adaptation:** for an agent-facing product the primary persona MAY
   be an AI-agent consumer (jobs-to-be-done framed, same rigor). This is a **light prompt, not forced**
   for human-facing products.
4. Key metrics
5. Tracks — **investment areas only, no actor-naming** (a track is a domain of work, not the agent that
   does it).
6. Milestones (optional)
7. Not working on (optional)
8. Marketing (optional)

When the 5 required sections (1-5) are captured, read `references/strategy-template.md`, fill it in,
present the full draft in chat, offer one round of edits, then write the root `STRATEGY.md`.

## Phase 2 — Update run

Read the existing root `STRATEGY.md` thoroughly and summarize current state in 3-5 lines. If the
argument named a section, jump to it in `references/interview.md`; otherwise ask which section to
revisit via `AskUserQuestion` (channel -> inline). For each revisited section, re-interview with **full
pushback as if this were a first run** — do not rubber-stamp existing weak content. **Preserve all
other sections exactly**, bump `last_updated` in the frontmatter to today's ISO date, then write back to
the root `STRATEGY.md`.

On a **material direction shift** (target problem, approach, or persona meaningfully changes — not a
wording tweak), *suggest* a `docs/engineering-journal/DECISIONS.md` ADR capturing why direction changed.
Offer it; do not auto-write it.

## Phase 3 — Downstream handoff

After writing, note in one line that the file lives at the repo root as `STRATEGY.md` and that
`/ideate`, `/brainstorm`, and `/plan` will pick it up as grounding on their next run.

If the strategy implies concrete implementation work, route it onward — to `/plan` (settle the HOW) or
`/plan` (route it through the lifecycle). Resolve any cross-command route through the lifecycle routing
routing each command's own skill states (do not
copy the routing table here). If no downstream skill has run yet on this repo, suggest `/ideate` or
`/brainstorm` as the next step.

## Hard boundary

`/strategy` **RECORDS** direction. It does **NOT** implement or make code changes; does **NOT** write
product requirements or implementation plans (`/brainstorm` and `/plan` do); does **NOT** prioritize
the backlog; does **NOT** compute metric values (it records *which* metrics matter and *where* they
live, not what they read today); does **NOT** file SDLC issues (`mission-control` does); does **NOT**
challenge ambition or scope (`/founder-review` does); does **NOT** check readiness (`/doc-review` does);
and does **NOT** commit, push, open PRs, merge, or deploy. It runs upstream of the work thread, so it
does **NOT** write the saga — no `saga.py` invocation, no `--review-paths`. Record the direction in
`STRATEGY.md`, name the next command, then stop.

## Reference files

- `references/interview.md` — the per-section pushback rulebook: Overall Rules; the 8 sections with
  opening question + quality bar + named anti-patterns + sharper correction questions + capture rule;
  the two-round pushback rule; and the Infiquetra agent-as-customer / tracks-are-not-actors deltas.
- `references/strategy-template.md` — the locked `STRATEGY.md` template: YAML frontmatter + the 8
  sections in locked order, the 3-5 metrics / 2-4 tracks constraints, delete-optional-if-unused, and
  the post-write checklist.
- `saga/references/formatting-style.md` — the shared formatting contract the written `STRATEGY.md`
  follows (short blank-separated sections leading with the point, comparative data as bullets/tables).

## Learn more

The "Target problem / Our approach / Tracks" structure is informed by Richard Rumelt's *Good Strategy
Bad Strategy* — his kernel of diagnosis, guiding policy, and coherent action. The interview questions
push past what he calls "bad strategy": fluff, goals dressed up as strategy, and feature lists in place
of a guiding choice.
