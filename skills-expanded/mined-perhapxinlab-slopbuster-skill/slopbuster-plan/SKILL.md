---
name: slopbuster-plan
license: Apache-2.0
description: Research-first upfront planning at the start of a new project or major feature, when little is settled. Use when asked to plan, design, or architect a system before implementation, to study a market or landscape, to size an opportunity, or to produce a project plan / architecture decision record / frontend design docs. Searches the live web for competitors, prior art, and commercial signals, grades the opportunity across dimensions, and grounds every decision in real products and real constraints instead of inventing from imagination.
---

# SlopBuster — Plan

This is the **upfront** phase — the start of a project, when little is known and the
expensive mistakes are still cheap to avoid. You are not designing a system from
imagination. You are **synthesizing a system from existing reality** — real products you
went and found, real open-source implementations you read, real commercial and market
signals you searched for. Originality comes from combination and refinement, not invention
from zero. This is the phase that stops slop from being born on day one.

Two jobs, both upfront: **read the opportunity honestly** (is this worth building, against
whom, how hard), and **lay out the plan** to pursue it. You grade the first the way the audit
grades code — dimension by dimension, with a headline verdict — and you write the second as a
multi-document plan, one md per facet.

Do not write code in this skill. The deliverable is a graded, researched, multi-document plan.

## Lead with research — actually search the web

Planning from memory is how slop is born. Before you grade or decide anything, go and look.
Use **WebSearch** and **WebFetch** to study the live landscape, not your recollection of it:

- **Direct competitors** — who already does this, what they charge, what they do well and badly.
- **Adjacent products** — neighbours solving a related problem whose UX or architecture transfers.
- **Prior art & real code** — comparable open-source repos, including at least one over-engineered
  one (to learn what *not* to do). Look past the README at structure, boundaries, async design.
- **Commercial signals** — pricing pages, funding, job posts, changelogs, reviews, what users
  complain about. The market tells you whether the opportunity is real.

Capture every source you actually consulted with its **real URL**, a `kind`, and a one-line
takeaway. The desktop app renders these as **clickable links**, so the URLs must be real strings
(use `null` only for a genuinely offline/internal source). Do not cite from memory and do not invent
URLs — if you did not open it, it is not a source. If you can't explain why a finding matters, it
isn't one.

If the user gives too little to plan against, make explicit **Assumptions**, label them, and list
what needs confirming — but don't block on it. Research narrows the unknowns; it doesn't have to
eliminate them before you can grade.

## Detect what's being planned, load the right pack

- **Backend / service / general system** → [references/backend-planning.md](references/backend-planning.md)
- **Frontend app architecture** → [references/frontend-planning.md](references/frontend-planning.md)
  (routing, client/server boundary, state model, data layer — produces `frontend.md`)
- **Design system & visual/content design** → [references/design.md](references/design.md)
  (style direction, design tokens, components, the Design Page, accessibility, and content —
  produces `style.md` + `design.md`). Load alongside the frontend pack for any UI work.
- **Agent / LLM-heavy system** → also load [references/agent-system-planning.md](references/agent-system-planning.md)
  (token discipline, context engineering, long-chain process design)

## The flow (order matters)

1. **Frame the problem & scope.** What's solved, who's the user, who isn't, what's out of
   scope. If a script / single service / existing SaaS would do, say why it won't.
2. **Search the landscape.** Several serious references, not one or two: direct competitors,
   adjacent products, best-in-class UX, the cautionary failures, and the commercial signals
   above. For each: what it does well, what it does badly, what architecture is visible, what
   it costs. Record the source with its URL as you go.
3. **Read real code.** Find comparable repos — production-grade, experimental, and at least
   one over-engineered one. Look past the README at structure, entry points, boundaries,
   async design, infra choices.
4. **Extract patterns.** What did multiple teams independently converge on, and *why*?
   Where do they diverge, and why? **If you can't explain why a pattern exists, don't adopt it.**
5. **Grade the opportunity.** Score it dimension by dimension (below) — an honest read of whether
   this is worth building, against whom, and how hard. Order the dimensions worst/most-uncertain
   first; the headline grade is a considered judgement, not an average.
6. **Debate, then decide.** Argue real alternatives (centralized vs modular, sync vs async,
   in-process vs worker vs external) with pros, cons, failure modes, scaling cost. Write down
   what you chose, what you rejected, and when the rejected option would become right.
7. **Map constraints.** Technical, infra, human (team size/skill/maintenance), time. When
   constraints conflict, prioritize and justify.
8. **Plan & milestones.** Incremental, testable, deployable, reversible. No "build it all at
   once," no "optimize later" without a boundary.

## Grade the opportunity (like the audit grades code)

The audit grades a codebase across categories with a capped headline; planning grades the
**opportunity** across dimensions the same way. Pick the dimensions that fit the project — a
flexible set, not a fixed enum. Typical ones:

- **Market & Competition** — is there demand, how crowded, how defensible.
- **Commercial Viability** — willingness to pay, pricing headroom, cost to serve, path to revenue.
- **Feature Scope** — how large the surface is, how much is table-stakes vs differentiating.
- **Build Difficulty** — technical risk, infra, team fit, time to a usable slice.

Add or drop dimensions to fit (distribution, regulation, data moat, timing…). Each dimension gets
a **grade** (`A+ A B C D F`), a **0..100 numeric**, and a **1–2 line summary** of why. Then a single
**overall grade** + **overall numeric** — the headline read of the opportunity, capped by the
weakest load-bearing dimension, not an arithmetic mean. A great market with an impossible build is
not a B. State the recommendation in plain words: pursue, narrow, or walk away.

## Deliverables

- **Research summary** — products and repos studied, what was learned, with sources.
- **Opportunity scorecard** — the graded dimensions + headline verdict and recommendation.
- **Architecture Decision Record** — key decisions + rationale.
- **Explicit non-goals.**
- **Project plan** — phases, milestones, risk points (incl. the data-model & concurrency/async
  sections from the backend pack, and the design docs from the design/frontend packs).
- **Open questions** — what still needs validation.

## Persist the plan (automatic)

Always write the deliverables to files — don't just print them. The plan is **one md file per
facet plus a `plan.json` manifest** (master-detail), not one combined document — write each facet
file separately so no single document holds everything. Default location, at the repo root, in a
version dir (create it if missing): `.slopbuster/plan/<version>/`.

- One md per facet — write only what you produced. Typical facets: `overview.md` (always),
  `competitors.md`, `market.md`, `features.md`, `architecture.md` (or `adr.md`), `roadmap.md`,
  `risks.md`, plus `frontend.md`, `backend.md`, `design.md`, `style.md`, `non-goals.md`,
  `open-questions.md` when the work calls for them. Facets are flexible per project — add/drop to
  fit. Filename = the `doc` field in `plan.json`.
- Each facet md is the **depth**. It must **cite its sources as clickable markdown links** —
  `[title](https://…)` — so a reader can follow every claim back to where you found it. The
  `scorecard` and `sources` in `plan.json` are the structured *surface* for the app; the md bodies
  carry the argument. Do not inline full md bodies into the JSON, and do not leave the md
  uncited.
- `plan.json` beside them (below).

If the user named a different location (e.g. the repo's `docs/` or `.ai/`), use that. These are
durable team artifacts — tell the user the paths when finished, and note they can be promoted
into `docs/`/`.ai/`. The build phase (`slopbuster-rules`) and audit read them back.

### Plan manifest (required — drives the desktop app's dashboard + facet tabs)

Alongside the md files, write a `plan.json` manifest the SlopBuster Desktop app reads to build the
master-detail UI: a **dashboard gauge** from the headline grade, a **scorecard** of the graded
dimensions, a **clickable source list**, and one editable Monaco tab per facet (each facet maps to
exactly one `.md` file in the same version dir). The app may pass a versioned target dir (e.g.
`.slopbuster/plan/v3-<date>/`); when it does, write the facet md files **and** `plan.json` into that
dir. Otherwise default to `.slopbuster/plan/`.

Write `plan.json` as (camelCase, no renames, no extra fields):

```json
{
  "overall": "<one-paragraph summary of the opportunity + recommendation>",
  "overallGrade": "A+|A|B|C|D|F",
  "numeric": 72,
  "meta": {
    "generatedBy": "<tool + model, e.g. 'claude-code / claude-opus-4-8' — never blank>",
    "author": "<git log -1 --format=%an>", "email": "<git log -1 --format=%ae>",
    "commit": "<git rev-parse HEAD>", "branch": "<current branch>",
    "generatedAt": "<ISO-8601 — date>"
  },
  "scorecard": [
    { "key": "market", "label": "Market & Competition", "grade": "B", "numeric": 74, "summary": "<1-2 lines>" },
    { "key": "commercial", "label": "Commercial Viability", "grade": "B", "numeric": 70, "summary": "<1-2 lines>" },
    { "key": "feature-scope", "label": "Feature Scope", "grade": "C", "numeric": 65, "summary": "<1-2 lines>" },
    { "key": "difficulty", "label": "Build Difficulty", "grade": "C", "numeric": 60, "summary": "<1-2 lines>" }
  ],
  "sources": [
    { "title": "Vendor X", "url": "https://…", "kind": "product|repo|paper|article", "takeaway": "<why it matters>" }
  ],
  "docs": [
    { "key": "overview", "label": "Overview", "doc": "overview.md", "summary": "<1-2 lines>" },
    { "key": "competitors", "label": "Competitors", "doc": "competitors.md", "summary": "<1-2 lines>" }
  ]
}
```

- **`overall`** — one-paragraph read of the opportunity plus the recommendation, shown above the
  scorecard.
- **`overallGrade`** / **`numeric`** — the headline opportunity grade (`A+ A B C D F`) and a 0..100
  score that drives the dashboard gauge. The `numeric` is a **considered read**, capped by the
  weakest load-bearing dimension — not an average of the scorecard.
- **`scorecard[]`** — the graded dimensions, a flexible set. Each: `key` (stable slug),
  `label`, `grade` (`A+ A B C D F`), `numeric` (0..100), `summary` (1–2 lines). **Order
  worst/most-uncertain first.**
- **`sources[]`** — the research sources you actually consulted. `kind` ∈ `product | repo | paper |
  article`; `url` is a real string (or `null` only for a genuinely offline source); `takeaway` is
  why it matters. These render as **clickable links** in the app — never fabricate a URL.
- **`docs[]`** — one entry per md facet actually written, **`overview` first**. `key` stable slug,
  `label` tab title, `doc` md filename relative to the dir, `summary` 1–2 lines. No stubs — only
  facets you wrote.

The contract is documented in [references/output-contract.md](references/output-contract.md).

The plan is ready only when you can answer truthfully: *if we pursue this and it fails, will we
understand why, and know what we'd have changed?* If not "yes," it's not ready.
