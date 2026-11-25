---
name: quizzing
description: >-
    Consolidated design questionnaire — get a design right on the first go by front-loading
    clarifying questions into one convenient web form instead of a long back-and-forth. The
    inverse (in cadence) of "grilling": first look up facts, ask 1-5 grilling-style "bearing"
    questions one at a time, then generate a capped (20 by default), paginated web questionnaire with
    recommended answers, ranges, examples, and custom input. Answers come back as JSON that this
    skill interprets to produce the design; the process loops for refinements. Use when the user
    says things like "quizzing", "run quizzing on this", "design questionnaire", "ask me
    everything up front", "let's scope this properly before you build", or wants a structured,
    low-friction way to align on a design before implementation.
user-invocable: true
---

# Quizzing

Quizzing front-loads an agent's clarifying questions into **one convenient, well-designed
questionnaire** so the design is right on the first go. It keeps the best principles of the
`grilling` skill but changes the interaction model from a relentless one-at-a-time interview to a
short **bearing phase** followed by a single **capped, paginated web form**. Answers return as a
JSON file that this skill reads to produce (or revise) the design.

## Principles (inherited from grilling)

1. **Look up facts, don't ask them.** Anything discoverable from the environment (filesystem,
   tools, git, docs) must be looked up — never put a discoverable fact to the user.
2. **Decisions are the user's.** Only ask about genuine decisions the user must own.
3. **Always recommend.** Every question carries the agent's recommended answer and a short
   rationale, so accepting the defaults is fast.
4. **Do not act until confirmed.** After answers return, summarize your interpretation and wait
   for explicit confirmation before building anything — on every loop.

## Prerequisites

- **Node.js ≥ 14** — required to run the web form tooling (`web/generate.js`, `web/serve.js`).
  These use only the Node standard library, so there is **no npm install and no `node_modules` at
  runtime** (`npm install` is only needed for the test suite, which additionally requires Node ≥ 18
  for jsdom). A **web browser** is needed to
  display the form.
- **Node.js and a browser are prerequisites, not options.** Every host CLI that can run this skill
  is itself a Node application, and Quizzing exists to put a human in the loop, so a human with a
  browser is the premise. There is no conversational or non-browser fallback — see step 4.
- This project's tooling: `web/serve.js`, `web/generate.js`, and the schemas in `schema/`.

## Lifecycle

```
facts → bearing (1-5, one at a time) → author form (≤20) → run form → answers JSON
      → summarize → confirm → [gaps/challenge? → follow-up form] → design
```

### 1. Discover facts

Investigate the repo and tools first. Record the relevant facts — you will embed them in the
questionnaire's `discoveredContext` so the user sees what you already know and isn't asked about it.

### 2. Bearing phase (grilling-seeded, always on)

Ask **1–5 main "bearing" questions**, grilling-style: **one at a time**, each with your recommended
answer, waiting for the reply before the next. Keep it short — these exist only to orient you so the
generated form is well-targeted. Capture the takeaways as the `bearingSummary`.

### 3. Author the questionnaire

Write a questionnaire JSON conforming to [`schema/questionnaire.schema.json`](schema/questionnaire.schema.json).
Rules:

- **Cap: 20 questions** (`questionCap`, default 20). The generator/server **rejects** forms that
  exceed the cap they declare. The point is speed — target minutes, not a 30-minute interview. If
  you have more candidate questions, prune low-impact ones, fold them into recommended defaults, or
  defer them to a later loop.
  - **Set a different `questionCap` only when the user explicitly asked for a different number**,
    and then set it to the number they asked for. Never raise it to make room for questions that
    did not fit — that is the pruning problem, not a cap problem. A non-default cap is reported on
    every build, so it is visible to the user either way.
- **Ask decisions, not facts.** If you can look it up, look it up.
- Give every question a **`recommended`** answer with a `rationale` (and `confidence`).
- Use the right **type**: `single-select`, `multi-select`, `boolean`, `range` (1–5 / 1–10 for
  calibration, with `scale.anchors`), `text`, `ranking`, or `decision-matrix` (see below).
- Provide concise **`options`** with descriptions; allow **`customInput`** where "other" is
  plausible; add an **`example`** or **`diagram`** (see below) when a question needs context.
- Use **`branching`** to reveal follow-up questions only when relevant (keeps the form short).
- Group into **`sections`**; set `order`.

**Visual aids — lean on diagrams.** A picture removes ambiguity faster than prose, so add a
`diagram` whenever a question is about a flow, an architecture, or a set of relationships. The form
renders every diagram inline with **no network calls** (self-contained), so prefer the declarative
formats — you describe the *structure* and the build step computes a deterministic, correctly
laid-out SVG (boxes sized to text, edges anchored to borders). Don't hand-place pixels.
- **`flow`** — a directed graph of steps. Give `nodes` (`{id,label,highlight?}`) and `edges`
  (`{from,to,label?,style?}`); set `direction` to `LR` (default) or `TB`. Ideal for
  request/approval flows, state machines, pipelines.
- **`layered`** — a tiered architecture. Give `tiers` (`{label,nodes}`) top-to-bottom and `edges`
  between any nodes. Use `style:"async"` on edges for dashed lines; a sync/async legend appears
  automatically when both are present.
- Escape hatches: `svg` (inline markup in `content`) or `image` (a base64 `data:` URI in `content`)
  — use only when the declarative formats can't express what you need. `image` content that is not
  a data URI is rejected by the schema and dropped by the form: a remote URL would make the
  questionnaire fetch over the network. Author-supplied `svg` is **sanitised at
  build time**: `<script>`, `<style>`, and `<foreignObject>` elements, `on*` handlers, any URL that
  isn't a `#fragment` or a `data:image/…`, and any attribute containing a `url()` that isn't a
  same-document `url(#id)` are stripped. Nothing is lost by preferring `flow` / `layered`.
- **Always** include `alt` text describing the diagram for accessibility and non-visual fallback.

**Weighted trade-offs — `decision-matrix`.** Reach for this when the choice between options turns on
several criteria pulling in different directions, and you want the user's *reasoning* rather than
just their pick. The user scores every option against every criterion; the form computes a weighted
total per option and highlights the winner live. Prefer `ranking` when you only need a preference
order over a single dimension, and `single-select` when one criterion dominates.
- Supply the candidates as normal **`options`** — they become the matrix rows.
- **`matrix.criteria`** — the scored columns. Each is `{id, label, weight?, description?}`. `weight`
  is relative importance (default `1`); totals are the weighted sum of scores. Use `description` to
  say what a *high* score means, so scoring is unambiguous.
- **`matrix.scale`** — the per-cell score range, `{min, max, step?}` (`step` defaults to `1`).
  Defaults to 1–5 when omitted. Keep it small; 1–5 is almost always right.
- **`matrix.seed`** — optional starting scores, `optionId → criterionId → number`, expressing your
  recommendation. Any cell you omit starts at the scale midpoint.
- Still give the question a **`recommended`** answer naming the option you'd pick and why — the
  matrix shows the working, `recommended` states the conclusion.
- You get back `matrixScores` (every cell the user set) plus `matrixResult` (`totals` and
  `winnerOptionId`). Read the scores, not just the winner: a narrow margin is itself a finding.
**Consistency checks** (optional, top-level `consistency`) — the form asks one question at a time, so
nothing otherwise stops a user assembling a set of answers that cannot all be true at once. A check
fires when *every* rule in its `when` array holds, using the same condition shape as `branching`
(`questionId` plus one of `equals`, `includes`, `gte`, `lte`).

- **`severity`** is the decision that matters. `error` blocks submission and should be reserved for
  combinations that genuinely cannot be built. `warning` (the default) is shown, can be accepted,
  and records that acceptance in the answers JSON — use it for anything that is merely expensive,
  risky, or unwise. Prefer `warning`: an over-eager `error` strands the user with no way forward.
- **`message`** must name *both* answers in tension, in plain language. The user cannot see your
  check ids, and "invalid combination" tells them nothing about what to change.
- **`explain`** says why it matters; **`evidence`** carries the environmental facts that make it so —
  this is where a fact you discovered in step 1 does its work.
- **`suggest`** offers one-click corrections. Each names a `questionId`, a button `label`, and the
  answer fields to set (`selectedOptionIds`, `rangeValue`, `booleanValue`, `customText`). A
  correction only sets what it names; it never clears anything else.
- A check is skipped while any question it references is hidden or unanswered, so half a
  contradiction never fires and a collapsed branch cannot complain about a question the user can no
  longer see.
- **Do not let your own recommendations trip a check.** The seeded defaults must be mutually
  coherent, or the form opens already complaining.

```json
{
  "id": "attach-after-absent-checks",
  "severity": "error",
  "when": [
    { "questionId": "virus-scan", "equals": false },
    { "questionId": "attach-timing", "equals": "after-checks" }
  ],
  "message": "Attachments are set to appear only after checks pass, but scanning is turned off, so there are no checks to wait for.",
  "explain": "With no scan step, \"after checks\" has nothing to gate on.",
  "suggest": [
    { "questionId": "virus-scan", "label": "Scan uploads after all", "booleanValue": true },
    { "questionId": "attach-timing", "label": "Attach immediately instead", "selectedOptionIds": ["immediate"] }
  ]
}
```

See [`examples/file-uploads.questionnaire.json`](examples/file-uploads.questionnaire.json) for a
complete, valid questionnaire, and
[`examples/file-uploads.answers.json`](examples/file-uploads.answers.json) for what comes back. It
is deliberately one worked example rather than several: every question type, both declarative
diagram formats, all three `required` modes, and `branching` appear exactly once, in the place each
is the natural way to ask. A test asserts that coverage, so a type added to the schema without an
example fails the build.

### 4. Run the form

**Preflight:** confirm the runtime with `node --version`. If Node ≥ 14 is present, use the web form
(connected mode preferred). If Node is missing, install it — see *Prerequisites* below; there is no
fallback path to take instead.

Prefer **connected mode** so answers return automatically:

```bash
node web/serve.js <questionnaire.json> --out <answers.json>
```

This serves the form on a loopback-only server, opens the browser, waits for the user to submit,
writes `<answers.json>`, prints the path, and exits 0. Run it as a **blocking foreground command**
and read the file when it returns.

Fallback — **static mode** (portable, manual return):

```bash
node web/generate.js <questionnaire.json> <form.html>
```

The user fills it and Downloads/Copies the answers JSON back to you.

**Prerequisites: Node.js and a browser.** Both are a given — every host CLI that can run this skill
is itself a Node application, and Quizzing exists to put a human in the loop, so a human with a
browser is the premise rather than a case to work around. There is no non-browser adapter; don't
improvise one.

The form presents **one question per screen** (Next/Prev, progress), pre-selects your recommended
answers, and offers two ways to pass on a question:

| Control | Shown on | Means | You should |
|---------|----------|-------|------------|
| **Skip** | optional questions only (`required` not `true`/`"conditional"`) | No opinion — don't ask again | Decide it yourself and state the assumption |
| **Defer to a later round** | every question | Matters — ask me next round | Re-ask it in the next quizzing loop |

Note that **Defer satisfies the `required` gate**, so a required question can always be passed on
deliberately; only Skip is withheld. Neither control leaves a value behind — the seeded
recommendation is cleared, so a skipped or deferred question never masquerades as an answer.

### 5. Read the answers JSON

Parse the answers file — it conforms to [`schema/answers.schema.json`](schema/answers.schema.json)
and is the **only authoritative input** to the design. For each response, honor:

- `selectedOptionIds` / `rangeValue` / `booleanValue` / `ranking` / `customText` — the actual choice
  (use stable ids, not labels).
- `recommendationDisposition` — `accepted` / `modified` / `overridden` tells you where the user
  diverged from your recommendation; pay closest attention to those.
- `skipped` / `deferred` — do not treat as answered; `deferred` items are candidates for a follow-up
  loop.
- `activeBranchIds` — which conditional paths were shown.
- `validation.warnings` and `validation.checks` — consistency findings the user was shown. A check
  with `acknowledged: true` is a trade-off the user saw explained and took deliberately: treat it as
  a decision to respect and restate in your summary, not a defect to fix. `status: "partial"` means
  warnings were present and nothing was blocking.

### 6. Summarize and confirm

Produce a concise summary of the design as you now understand it, calling out any overrides and open
items. **Wait for explicit confirmation before acting.**

### 7. Loop when needed

If the user challenges the direction, new questions arise, or items were deferred, run the follow-up
generator instead of authoring the next round from scratch:

```bash
node web/followup.js <questionnaire.json> <answers.json> [next.questionnaire.json]
```

It reads back what the last round left open and drafts the next questionnaire with lineage already
wired (`parentLoopId`, `parentSessionId`, a fresh `loopId`, `version` reset to 1, `bearingSummary`
carried). Three things are carried forward, each stamped with `provenance` so you can tell a
carried-over question from one you wrote:

- **`deferred` responses** — copied **verbatim**. The user asked to decide these later; re-wording
  makes them answer what looks like a different question.
- **`recommendationDisposition: "overridden"`** — a `text` question asking what made the chosen
  answer right, naming the labels involved. The reason was never captured, and it is what makes your
  next recommendation better.
- **Unacknowledged `warning` checks** — a `single-select` built from that check's own `suggest`
  corrections, plus "Keep it as it is". An *acknowledged* warning is a decision, not a loose end, and
  is deliberately not carried.

If nothing was deferred, overridden, or left unresolved, it writes no file and says so — author a
follow-up only if the user has raised something new.

**The tool drafts; you author.** It carries forward what the last round left open; you must review
every drafted question and add the questions this round is actually *for*. It invents no options and
no rationale. Keep the result within `questionCap` and one-at-a-time. Then repeat bearing (if needed) →
form → summarize → confirm until aligned. Then build.

## Authoring checklist

- [ ] Facts looked up and placed in `discoveredContext` (not asked).
- [ ] 1–5 bearing questions asked one at a time; `bearingSummary` captured.
- [ ] Within `questionCap` (20 unless the user asked for another number); each question is a genuine decision.
- [ ] Every question has a `recommended` answer + rationale.
- [ ] Ranges used for calibration with anchors; declarative `flow`/`layered` diagrams (with `alt`) where they clarify.
- [ ] `decision-matrix` used where a choice hinges on several weighted criteria (with `matrix.seed` carrying your recommendation).
- [ ] Branching used to keep the form short.
- [ ] `consistency` checks added for combinations that cannot both be true (`error`) or are expensive/risky (`warning`), each with a message naming both answers and a suggested correction.
- [ ] Your own recommended answers do not trip any check.
- [ ] Ran the form (connected mode preferred) and read the answers JSON.
- [ ] Summarized and got explicit confirmation before building.
- [ ] For a follow-up round: generated it with `web/followup.js` from the previous answers, reviewed
  every drafted question, confirmed the deferred items are present, and added the questions this
  round is for.

## Relationship to grilling

Quizzing is grilling's counterpart, not its replacement. Reach for **grilling** when decisions are
so entangled that each answer reshapes the next question. Reach for **Quizzing** when most decision
branches can be anticipated and you want a fast, low-friction, single-pass alignment.
