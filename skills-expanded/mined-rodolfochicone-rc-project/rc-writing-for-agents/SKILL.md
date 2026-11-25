---
name: rc-writing-for-agents
description: "Writes what agents read — skills, AGENTS.md, hooks — and audits context cost. Use when authoring or trimming one. Not for READMEs."
model: sonnet
effort: medium
metadata:
  credits: Doctrine adapted from writing-great-skills (mattpocock/skills)
  adapted-by: RC — merges the former rc-skill-best-practices, rc-agents-md, rc-context-budget and rc-hookify
---

# Writing for Agents

Every artifact an agent reads — a skill, a resident instruction file, a hook, a pointer doc — is the
same object under different loading rules. They shared four skills and one doctrine; now they share
one skill, because the doctrine is the part that matters and it was written four times.

The goal is **predictability**: the agent taking the same *process* every run, not producing the same
output. Every lever below serves it.

**Bold terms** are defined in [`references/glossary.md`](references/glossary.md).

## Branches

| The artifact | Read |
| --- | --- |
| A skill — new, bloated, or with triggers that don't fire | [`references/authoring-procedure.md`](references/authoring-procedure.md), then audit with [`references/checklist.md`](references/checklist.md) |
| A skill whose `references/` the agent ignores | [`references/loading-diagnosis.md`](references/loading-diagnosis.md) in full, before proposing a fix |
| `AGENTS.md` / `CLAUDE.md` — resident context | [`references/resident-files.md`](references/resident-files.md) |
| A hook — a rule that must hold every time | [`references/hooks.md`](references/hooks.md) |
| "Where is my context window going?" | [`references/context-audit.md`](references/context-audit.md) |

Every branch ends in a written audit, item by item — fix each Fail and re-audit. A document that
reads well but fails its audit is not done. The doctrine below governs every line you write in any
branch, not just the ones a procedure file mentions.

## The two budgets

Every authoring decision trades these against each other:

- **Context load** — material present in the window regardless of use: a skill's `description`, every
  line of a resident file, an MCP tool schema. Paid every turn, on every task, whether or not it
  applies.
- **Cognitive load** — the human cost of knowing what exists and when to reach for it. A user-invoked
  skill has zero context load and spends this instead: *you* become the index.

Neither is free, so "just add it" is never the answer. A rule bearing on 5% of sessions taxes the
other 95%, and rules **dilute each other** — instruction-following is a budget, so a bloated file
enforces *less*, with the critical rule drowning in the noise.

And the reader is a frontier model. It knows git, testing, the language's idioms and general best
practice, and it can read the codebase. It needs **decisions, not knowledge**, and it parses a crisp
rule without an example. What survives is the **delta**: the difference between stock behavior and
what this project needs.

## The no-op test

The central method, and the reason this doctrine shortens documents rather than improving them:

> Delete the line. Ask whether the agent's behaviour changed. If it didn't, the line was waste.

Run it **sentence by sentence**, not line by line. When a sentence fails, delete the whole sentence —
do not trim words from it. Be aggressive: most prose that fails should go, not be rewritten. A weak
directive is a no-op (*be thorough*, when the agent is already thorough-ish); the fix is a stronger
word (*relentless*), not a longer explanation.

## Information hierarchy

Content sits on a ladder ranked by how immediately the agent needs it:

1. **In-file step** — an ordered action. Each ends on a **completion criterion**: the condition that
   says the work is done. Make it *checkable* (can the agent tell done from not-done?) and, where it
   matters, *exhaustive* ("every modified model accounted for", not "produce a change list"). A vague
   criterion invites **premature completion**; a demanding one drives the **legwork** that makes the
   output worth having.
2. **In-file reference** — a definition, rule or fact consulted on demand. Often a legitimately flat
   peer-set (every rule of a review on one rung) — an arrangement, not a smell.
3. **External reference** — pushed into a separate file and reached by a **context pointer**, loaded
   only when the pointer fires.

**Progressive disclosure** is the move down that ladder. **Branching** is its cleanest test: inline
what every branch needs, push behind a pointer what only some branches reach. A pointer's *wording*,
not its target, decides whether the agent actually reaches the material. Where the ladder decides how
far down a piece sits, **co-location** decides what sits beside it: keep a concept's definition, rules
and caveats under one heading, so reading one part brings its neighbours along.

Push too little down and the top bloats; push too much and you hide what the agent needs. That
tension is the whole decision.

## Leading words

A **leading word** is a compact concept already in the model's pretraining that the agent thinks
*with* while running — *seam*, *tracer bullet*, *red*, *tight*, *lesson*. Repeated across a document it
accumulates a distributed definition and anchors a whole region of behaviour in the fewest tokens, by
recruiting priors the model already holds.

It pays twice. In the body it anchors **execution** — the agent reaches for the same behaviour every
time the word appears. In a description it anchors **invocation** — when the same word lives in your
prompts, docs and code, the agent links that shared language to the skill and fires it more reliably.

Hunt for the collapse. A triad spelled out at three sites, a description spending a sentence to
gesture at one idea — each is begging to become one token:

- "fast, deterministic, low-overhead" → *tight* (a **tight** loop).
- "a loop you believe in" → *red* — a fuzzy gate becomes a binary observable state.

Assume every document you touch is carrying restatements that a leading word retires.

## Pruning

Keep each meaning in a **single source of truth** — one authoritative place, so changing the behaviour
is a one-place edit. Then check every line for **relevance** (does it still bear on what this does?)
and run the no-op test on what remains. Nothing should appear twice in any form; duplication is the
reliable sign of a document nobody tested.

When you abstract from a specific run, strip what belonged to that repo and write for the *class* of
task. A document improves by getting shorter.

## Failure modes

Use these to diagnose a document that isn't working:

- **Premature completion** — a step ends before it is genuinely done, attention slipping to *being
  done*. Sharpen the completion criterion first (cheap, local); only if it is irreducibly fuzzy *and*
  you observe the rush, hide the later steps by splitting.
- **Duplication** — the same meaning in more than one place. Costs tokens and maintenance, and
  inflates that meaning's rank on the ladder past its real one.
- **Sediment** — stale layers that settle because adding feels safe and removing feels risky. The
  default fate of any document without a pruning discipline.
- **Sprawl** — simply too long, even with every line live and unique. The cure is the ladder:
  disclose reference behind pointers, split by branch.
- **No-op** — a line the model already obeys by default, so you pay load to say nothing.
- **Negation** — steering by prohibition backfires: *don't think of an elephant* names the elephant.
  Prompt the **positive** so the banned behaviour is never spoken; keep a prohibition only as a hard
  guardrail you cannot phrase positively, and pair it with what to do instead.
- **Scar tissue** — a rule added after one incident, resident forever.
- **Example creep** — good/bad code blocks multiplying under each rule. Cut the blocks, sharpen the
  rules: an example pays double rent and pins the rule to one surface form.
- **Emphasis inflation** — the caps arms race. Emphasis on everything is emphasis on nothing.

## Invocation

Two choices with different costs:

- **Model-invoked** keeps a description, so the agent fires it autonomously and other skills can
  reach it. Pays **context load** every turn. Write the description as a routing rule, not a summary:
  front-load the leading word, one trigger per genuine **branch** (synonyms renaming one branch are
  duplication), and cut identity that is already in the body. Cap it at ~150 characters — the host
  charges every shipped description against a listing budget, and past that budget it drops
  descriptions entirely, leaving the skill present by name with nothing to match against.
- **User-invoked** (`disable-model-invocation: true`) strips the description from the agent's reach:
  only a human typing its name invokes it. Zero context load, paid in **cognitive load**.

Choose model-invocation only when the agent or another skill must reach it on its own. When
user-invoked skills multiply past what you can remember, the cure is a **router**: one user-invoked
skill that names the others and when to reach for each.

## When to split

Each cut spends one of the two budgets, so split only when the cut earns it:

- **By invocation** — split off a model-invoked skill when it has a distinct leading word that should
  trigger it on its own, or another skill must reach it. You pay a new always-loaded description, so
  that independent reach has to be worth it.
- **By sequence** — split a run of steps when the steps still ahead tempt the agent to rush the one in
  front of it.

Neither justifies a split whose only argument is that the topics feel separate. Two artifacts that
need each other's vocabulary to explain themselves — where each description spends words saying what
it is *not* — are one artifact that was cut in the wrong place.

## Bundled files

- `references/glossary.md` — full definition of every bold term.
- `references/authoring-procedure.md` — spec mechanics for a new skill: metadata rules, directory
  layout, script conventions, validation.
- `references/checklist.md` — the exit audit: doctrine (Part A) plus spec compliance (Part B).
- `references/loading-diagnosis.md` — ignored references: symptoms, the pointer-strength ladder,
  fixes in order.
- `references/resident-files.md` — `AGENTS.md`/`CLAUDE.md`: the rent test, the scope ladder, form.
- `references/hooks.md` — authoring a RC hook in the house style, wiring and verifying it.
- `references/hook-events.md` — the per-event I/O contract (which events reach the model, which can
  block).
- `references/context-audit.md` — inventory and rank what consumes the window.
- `scripts/validate-metadata.py` — read-only; validates a `name`/`description` pair against the spec:
  `python3 <skill-dir>/scripts/validate-metadata.py --name "[name]" --description "[description]"`.
- `assets/SKILL.template.md` — skeleton for a new SKILL.md.
