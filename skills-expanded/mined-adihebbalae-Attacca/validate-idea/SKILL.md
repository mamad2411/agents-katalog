---
name: validate-idea
description: Falsification-first validation for a product, startup, feature, or side-project idea. Decomposes the idea into load-bearing assumptions, pre-registers kill criteria before looking at evidence, runs cost-ordered disqualifiers, gathers cited evidence into a ledger, red-teams it in an independent context, and issues a traceable verdict with one concrete next experiment. Trigger when the user says "validate this idea", "is this worth building", "should I build X", "will anyone pay for this", asks for market research or competitor analysis on a concept, wants to know if an idea is any good, or wants to resume a previous validation.
---

<!-- Design razor: CONTEXT only. Pre-registered kill criteria, cost-ordered disqualifiers, and a red-team framework are question/evidence structure the model won't reliably impose on itself under sunk-cost pressure from an invested user. Not a step-by-step build process. Delete when: native falsification-first reasoning reliably resists premise-preserving bias without an externally imposed gate order. -->

# Validate Idea

Most products die from a false premise found late — not from bad execution. This skill exists to find the false premise **early and cheaply**, by trying to kill the idea rather than trying to grade it.

## The one rule

> **You are not here to evaluate the idea. You are here to falsify it.**
> Killing an idea in 20 minutes is the best outcome this skill can produce. Treat an early exit as a success and say so plainly.

The user is emotionally invested. You are not. That asymmetry is the entire value you provide — do not spend it on encouragement. If you find yourself writing "this is an interesting opportunity," stop and write the specific finding instead.

Read `references/honesty.md` before Gate 0. It is the non-negotiable output contract for every gate.

---

## State

All work lives in `.attacca/validation/<idea-slug>/` relative to the user's project directory — the same place every other Attacca skill writes its generated artifacts:

```
.attacca/validation/<idea-slug>/
  PREREG.md      pre-registered kill criteria — WRITE ONCE, NEVER EDIT
  LEDGER.md      append-only evidence table
  PROGRESS.md    gate checklist + session notes
  redteam.md     prosecution / steelman / adjudication
  DECISION.md    the memo
```

**Gate 0 — Resume check.** Before anything, check whether `.attacca/validation/*/PROGRESS.md` exists (also check a legacy `validation/` at the repo root — pre-4.3 runs lived there; offer to move it). If so, read it, tell the user which gates are complete, and resume at the first incomplete gate. Never re-run a completed gate; never rewrite `PREREG.md`.

Templates are in `templates/`. Copy them, don't invent new formats.

## Inputs

Load per gate, not up front. Every row is a whole small file except where scoped.

| Gate | Layer | File | Scope |
|---|---|---|---|
| all | Reference | `references/honesty.md` | Full — the output contract |
| 0 | Reference | `references/assumptions.md` | Taxonomy + phrasing rules |
| 1 | Reference | `references/prereg.md` | Threshold-setting + worked examples |
| 2 | Reference | `references/cheap-kills.md` | The disqualifier ladder, in order |
| 3 | Reference | `references/evidence.md` | Source hierarchy + basis tags |
| 4 | Reference | `references/redteam.md` | Subagent brief (passed to the subagent, not read into your own context) |
| 5 | Reference | `references/verdict.md` | Verdict rules table |
| interview | Reference | `references/interviews.md` | Full — replaces gates 2–5 |
| 0–5 | Working | `.attacca/validation/<slug>/*` | The run's own artifacts |

`interviews.md` is only ever loaded in `interview` mode. Loading all eight reference files at Gate 0 puts ~390 lines of instructions for gates you haven't reached into the window that Gate 0's judgement has to compete with.

---

## Gate 0 — Frame

**Goal:** turn a vague idea into an explicit set of falsifiable, load-bearing beliefs.

An idea is never "an app for X." It is a *conjunction* of beliefs that must all hold. Your job is to enumerate them and find which one is most likely to be both wrong and fatal.

1. Ask the user for the idea in their own words. Then ask **at most 6 questions** — enough to name the customer, the pain, the current workaround, and how they'd reach anyone. Do not run a long intake; the evidence matters more than their self-report.
2. Decompose into 5–9 load-bearing assumptions. Follow `references/assumptions.md` for the taxonomy (demand / severity / willingness-to-pay / reachability / feasibility / defensibility / founder-fit) and for how to phrase them so they can actually be proven false.
3. Score each: **load** (1–5, how much collapses if false) × **fragility** (1–5, how likely false) ÷ **cost to test**. Rank by that ratio.
4. Show the user the ranked stack and get one correction pass. They will often say "actually the risky one is #4" — they're frequently right about this even when they're wrong about everything else.

Write the stack into `PROGRESS.md`. Do not research anything yet.

---

## Gate 1 — Pre-register

**Goal:** decide what would change your mind, before you have any evidence to rationalize against.

This is the most important gate and the one every other tool in this space skips. Thresholds set *after* seeing evidence are set wherever the founder already stands.

For the top 3 assumptions, write into `PREREG.md`:
- the assumption, stated so it can be false
- **what evidence would falsify it**, concretely
- **the numeric threshold** — a real number, decided now
- what the user commits to doing if it fails: kill / pivot / proceed-anyway-and-why

Read `references/prereg.md` for threshold-setting guidance and worked examples.

Then say to the user, explicitly: *"This file is now locked. I will judge the evidence against these numbers and not against how good the idea feels afterward."* Commit it to git if the project is a repo.

**Do not proceed until `PREREG.md` exists on disk.**

---

## Gate 2 — Cheap kills

**Goal:** spend 15 minutes trying to end the project before spending three hours on research.

Run the disqualifier ladder in `references/cheap-kills.md`, cheapest first: dominant incumbent → public precedent failure → legal/regulatory wall → structural distribution block → "is this a product or a feature."

Any single one can terminate the process. If one fires:
- Stop. Do not run Gate 3.
- Write `DECISION.md` with verdict **KILL** or **PIVOT**, the specific finding, and the source.
- Tell the user directly what you found and that they just saved months. Do not soften it, and do not pad it with consolation next-steps.

If nothing fires, record the negative results in the ledger — "no dominant incumbent found after N searches" is real evidence and belongs on the record.

---

## Gate 3 — Evidence

**Goal:** fill the ledger with sourced findings, and mark honestly everything you could not source.

Research the top-ranked assumptions **in parallel** — dispatch one subagent per assumption if subagents are available, otherwise run them sequentially. Give each agent one assumption and the instruction to *disconfirm* it, not to describe the market. An agent told "research the market for X" returns an encyclopedia; an agent told "find evidence that nobody actually pays to solve X" returns a decision.

Follow `references/evidence.md` for:
- the dimension-dependent source hierarchy (for demand, five real user conversations outrank any analyst report)
- basis tags: `[Primary] [Data] [Estimate] [Assumption] [Opinion]`
- mandatory `DATA GAP` rows when search comes up empty
- the absolute prohibition on inventing a number

Append every finding to `LEDGER.md` with source URL, tier, and confidence. Unsourced claims still go in the ledger — tagged `[Assumption]`, which is what makes the gap visible later.

---

## Gate 4 — Red team

**Goal:** get a judgement that is not contaminated by the pitch.

You have spent three gates with this idea and you now like it more than you did at the start. That drift is why this gate is mechanical rather than a matter of trying harder to be objective.

**Dispatch a subagent.** Give it `LEDGER.md` and `PREREG.md` only — never the user's framing, never their enthusiasm, never your own summary of why the idea is promising. Its brief is in `references/redteam.md`: build the strongest possible case that this fails, then the strongest case it succeeds, then adjudicate strictly against the pre-registered thresholds.

If subagents are unavailable, run the prosecution pass in a fresh, deliberately hostile framing and say in the output that separation was partial. Do not claim independence you didn't achieve.

Write the result to `redteam.md`.

---

## Gate 5 — Verdict

**Goal:** one decision and one next action, both traceable to the ledger.

Apply the rules in `references/verdict.md`. They are mechanical — compare evidence to the pre-registered thresholds, and nothing else:

| Condition | Verdict |
|---|---|
| A load-bearing assumption failed its pre-registered threshold, and it can't be swapped out | **KILL** |
| It failed but can be swapped without collapsing the others | **PIVOT** |
| Majority of load-bearing rows are still `[Assumption]` with no primary evidence | **INSUFFICIENT** |
| Top 3 assumptions all supported by `[Primary]` or Tier 1–2 evidence | **BUILD** |
| Anything else — the common case | **TEST** |

**INSUFFICIENT is a real verdict and you must be willing to return it.** If the ledger is mostly assumptions, saying "I don't know yet, go talk to eight people" is the correct and honest output. Emitting a confident verdict from thin evidence is the primary failure mode of every tool in this category — do not reproduce it.

Then design **one** experiment: the riskiest assumption, testable in ≤2 weeks for ≤$100, with the pass threshold stated up front. One, not three. Write `DECISION.md` from `templates/DECISION.md` — 400–600 words, risks given more space than strengths.

Close by telling the user the single thing to do this week, and what result would make you change the verdict.

---

## Modes

- **`quick`** — Gates 0, 1, 2, 5. Fifteen minutes. Use when the user is triaging several ideas or clearly wants a gut check. Still pre-registers; still allowed to kill.
- **`full`** (default) — all six gates.
- **`resume`** — read `PROGRESS.md`, continue.
- **`interview`** — the user is about to talk to real users. Skip to `references/interviews.md` and generate a Mom-Test-compliant question set targeting the top unresolved assumption. This is the highest-value mode in the whole skill; recommend it whenever the verdict is TEST or INSUFFICIENT.

## Anti-patterns in your own output

Catch yourself doing these:

- Producing a number that is not in the ledger. Every figure needs a row.
- Writing "could be significant," "interesting space," "room for a focused player." Say the actual finding or say you don't know.
- Listing 5 next steps. One.
- Softening a kill because the user seems invested. That's the moment the tool earns its existence.
- Treating absence of competitors as good news. It usually means no market. Say so.
- Letting the user renegotiate `PREREG.md` after seeing evidence. Point at the file. If they want to override, that's their call — record it in `DECISION.md` as an explicit override, with their reason.
