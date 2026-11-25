---
name: spec
description: Interrogate a vague ask into a precise, backlog-ready WHAT spec — five-Why, scope/MVP lock, failure-mode enumeration, read-code-first, quantify-everything. Convergent and relentless on one decided direction. Triggers on "spec this out", "turn this into a spec", "what exactly are we building", "sharpen this ask before handoff", and when /office-hours or /brainstorm have settled the WHY but the WHAT is still fuzzy.
argument-hint: "[vague ask | issue# | rough doc path]"
---

# Spec

Ported from gstack `spec` — the WHAT-interrogation half (five-Why, scope/MVP lock, failure-mode
enumeration, read-code-first, quantify-everything). It is the sibling of /plan's HOW-interrogation
(both from gstack `spec`, split WHAT vs HOW). No CE spec engine exists; the CE flavor reaches the
lifecycle second-hand via the already-shipped /plan.

`/spec` interrogates a vague request — round by round — until the WHAT is precise enough that an
unfamiliar implementer (or an AI agent) could build it without a single follow-up question. It is
friendly but relentless: ambiguity is a bug and it finds it. It quantifies everything, thinks in
failure modes, and reads the code before it asks. Its only durable output is a sharp `docs/specs/`
artifact that routes onward — it never owns the issue and never enters the work thread.

## Position in the lifecycle

`/spec` is **OFF-CHAIN, saga-UNTOUCHED, and routed** — it sits between exploration and execution. It
never enters the work thread and never writes the saga. Its lane, vs its neighbors:

- **vs `/brainstorm`** — `/brainstorm` is divergent exploration that produces a requirements doc across
  candidate directions. `/spec` is **convergent and relentless on the ONE decided direction**: the
  WHAT is chosen; `/spec` makes it precise.
- **vs `/plan`** — `/plan` settles the HOW (architecture, approach, KTDs, the implementation register).
  `/spec` pins the precise **WHAT** (who, current behavior, target, scope boundaries, acceptance,
  failure modes) and stops at the water's edge of design.
- **vs filing the card** — filing routes an artifact to `mission-control`.
  `/spec` produces the sharp **source** that envelope points at.

**Routes IN:** `/office-hours` frame-diagnostic (a settled "what exactly are we building" question),
`/brainstorm` (a convergent ask emerging from divergent exploration), or direct invocation.

**Routes OUT:** `mission-control` (-> issue -> `/plan`); `/plan` (when the WHAT is locked
but a HOW must still be settled); an **optional `/doc-review`** readiness pass before filing.

Resolve any cross-command route through the lifecycle routing reference at
the routing each command's own skill states (do not copy the
routing table here).

## Core principles

1. **Refuse ambiguity — the HARD GATE.** Do NOT produce a spec artifact after message 1. Interrogate
   first. The user's opening message is their initial request; begin Phase 1 immediately — do not ask
   them to repeat themselves, and do not skip ahead to a draft.
2. **Lock what + why before how.** Run the five-Why, then lock scope. Push back on premature solutions
   ("before we talk about *how*, let's lock *what* and *why*") and on scope creep ("that's a separate
   issue — let's finish this one"). Two rounds of pushback per question, then capture and move on.
3. **Read code before asking — cite `path:line`.** Before ANY Phase-3 question you MUST have read real
   evidence from the codebase (Grep/Glob/Read) and cite `path:line`. This is the magical moment: the
   operator sees you grounded in their actual repo, not a generic checklist. The **non-code escape**:
   if you searched and found nothing related, say so explicitly ("no code surface — treating as
   greenfield / non-code") and proceed.
4. **Quantify everything.** "Several files" is not acceptable — find the exact count. "Improves
   performance" is not acceptable — state the metric and the target. Think in failure modes: what
   happens when the input is empty, null, enormous, duplicated, called by the wrong role, or called
   twice? Enumerate them; an unenumerated failure mode is an unwritten test scenario.
5. **Sharpen, don't own the issue.** `/spec` writes a `docs/specs/` artifact and routes it; it does
   not file the SDLC issue — `mission-control` owns the issue body. It reads the repo but does not mutate
   it, and it is saga-untouched: no `saga.py`, no work-thread write.
6. **Leave a clean handoff.** End on a sharp artifact and a named next command — never a half-locked
   spec dressed up as ready.

## Interaction method

Use `AskUserQuestion` for **routing** decisions only — where to route next, which open question to
resolve first (call `ToolSearch` with `select:AskUserQuestion` first if its schema is not loaded). Use
**free-form** for the substantive interrogation (the five-Why, scope, technical categories): those
answers are inherently narrative and menu options would nudge them. Ask in tight rounds; never silently
skip a question.

In a channel session (`redis-channel` active), `AskUserQuestion` cannot be called — inline the choices
in your reply text instead, following the canonical channel-inline convention in
`saga/skills/brainstorm/SKILL.md` (do not duplicate its wording here).

Use repo-relative paths in everything you write — absolute paths break portability across worktrees.

---

## Phase 0 — Parse the ask, set origin

Parse `$ARGUMENTS` and set `origin` for the artifact frontmatter:

- **Vague ask (free text)** -> `origin: direct`. Treat the text as the initial request.
- **Issue ref (`#N` or a URL)** -> read it read-only with `gh issue view <N>` and set `origin: issue:#N`.
- **Rough doc path** (an upstream `docs/brainstorms/*-requirements.md`, a `docs/ideation/` survivor, or
  the root `STRATEGY.md`) -> read it as grounding, set `origin: <repo-relative path>`. The upstream doc
  is starting context, not a settled spec — `/spec` still interrogates the WHAT.

Then begin Phase 1 immediately. Do not draft an artifact in Phase 0.

## Phase 1 — Five-Why (the WHAT/WHY lock)

Load `references/interrogation.md`. **This load is non-optional** — the anti-hand-waving bar per
question lives there. Ask until you can crisply answer all five, and do NOT proceed until all five are
answered without hand-waving:

1. **Who** is affected? (end-user role, automated system, internal team — "just me, solo dev" is fine.)
2. **What is the current behavior?** (what IS happening — verified, not assumed.)
3. **What should the behavior be instead?**
4. **Why now?** (blocking other work? costing money? correctness bug? compliance risk?)
5. **How will we know it's done?** (an observable, measurable done-signal — not vibes.)

## Phase 2 — Scope lock + failure-mode register

Lock the boundary early; it prevents creep later. Answer all five:

1. **What is explicitly out of scope?** Lock this first.
2. **What existing systems does this touch?** Files, tables, services, endpoints.
3. **Ordering constraints?** Must A happen before B?
4. **The MVP cut** — the smallest version that delivers the value (surface it even if you don't take it).
5. **Failure modes + rollback** — the native gstack failure-mode register: enumerate what breaks if
   shipped wrong, and how to undo. Do not proceed until scope is locked.

## Phase 3 — Technical interrogation (HARD: read code first)

**Mandatory:** before asking ANY Phase-3 question, read at least one piece of real-code evidence and
cite `path:line`. Map the request to evidence yourself — do not ask "what file should I look at?"
first. The **non-code escape** applies when there genuinely is no code surface ("no code surface —
treating as greenfield / non-code") — then proceed. Then ask about whichever of the six categories
apply (skip ones that clearly don't): **data model · API · background processing · UI · infrastructure
· testing**. Don't ask what the code already answers.

## Phase 4 — Draft review

Present a full draft and ask: **"Does this accurately capture what you want? What did I get wrong?"**
Iterate until the user confirms.

## Phase 5 — Write, optional readiness pass, route

Read `references/spec-template.md` and write the artifact to
`docs/specs/<YYYY-MM-DD>-<slug>-spec.md`. Run the post-write checklist in the template before
confirming. Then:

- **OFFER an optional readiness pass** on the spec before handoff (do not auto-run it). Two
  complementary options, offer either or both:
  - **Spec-phase rubric pass** — run the SPEC-phase rubrics against the draft via the engine at
    `../../scripts/lifecycle_review.py` (rubrics under `saga/references/rubrics/spec/`). List with
    `python3 ../../scripts/lifecycle_review.py rubrics list-cores --phase spec` (+ `list-extras`),
    read each with `rubrics read --phase spec --slug <slug>`, apply every `core` rubric and the
    fitting `extras` by judgment. This is the WHAT-rigor readiness check; do not add a new command.
  - **`/doc-review` pass** — hand the spec to `/doc-review` for the broader readiness-skeptic review.
- **Route onward:** `mission-control` (-> issue -> `/work`) when the WHAT is locked and ready
  for the backlog; `/plan` when a HOW must still be settled; or stop if the user is done.
- **No saga write.** `/spec` is off-chain; it does not advance or mint any work thread.

## Hard boundary

`/spec` interrogates and sharpens the WHAT. It never commits, pushes, opens or merges PRs, or
deploys. It does **NOT** file an SDLC issue (`mission-control` owns issue creation) — it produces the
source artifact only. It does **NOT** write or advance the saga (no `saga.py`, no `--lifecycle-phase`)
— it runs off-chain. It does **NOT** do `/plan`'s HOW job (architecture, KTDs, the implementation
register) nor `/brainstorm`'s divergent exploration job. It reads the repo but does not mutate it.

## Reference files

- `references/interrogation.md` — the WHAT-altitude procedure: the five-Why with an anti-hand-waving
  bar per question; the scope-lock five; read-code-first (mandatory-evidence rule, request->evidence
  mapping, cite `path:line`, the six categories, the non-code escape); the native failure-mode
  register; quantify-everything; and the anti-patterns catalog. The HOW-altitude sibling lives in
  `saga/skills/plan/references/interrogation.md` and is deliberately not duplicated
  here.
- `references/spec-template.md` — the locked `docs/specs/` artifact: frontmatter + sections, the
  post-write checklist, and the `mission-control` routing note (the artifact is a `mission-control` source mapping to
  `requirements-ready`; `mission-control` owns the issue body).
- `saga/references/formatting-style.md` — the shared formatting contract the written spec follows
  (one-line section summaries, short blank-separated paragraphs, comparative data as tables/bullets).

## Learn more

The WHAT-interrogation rigor — five-Why, quantify-everything, lock scope before solution — comes from
gstack `spec`, itself informed by Garry Tan's "boil the lake" discipline: get the problem exhaustively
right before touching the solution.
