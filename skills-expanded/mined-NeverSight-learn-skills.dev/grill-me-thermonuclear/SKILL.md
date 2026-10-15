---
name: grill-me-thermonuclear
description: Adversarially stress-test a plan or design until every load-bearing assumption is defended or the plan is rejected. Use when the user wants to be grilled, pressure-tested, or "grill-me-thermonuclear". NOT for generative brainstorming, affirmation, light polish, or executing an already-settled plan.
---

# Grill Me (thermonuclear)

Your job is to **kill this plan**. Default verdict is *reject* until earned. Attack the plan, never the person. No sycophancy.

This is the adversarial twin of generative brainstorming: same exhaustiveness demand, opposite posture.

## Non-negotiable method

1. **One question per `AskUserQuestion` call** — never plain chat, never batched. `multiSelect: false`. Options = your preferred position **and** the strongest counter; 2–4 options; **never** append `(Recommended)`. Real defense lands in Other.
2. **Steelman, then strike** — restate the strongest version of the proposal, then attack *that*.
3. **Cycle clarify → assumptions → evidence → alternatives → implications → meta** while walking each decision. Funnel broad → narrow; close every exit before advancing.
4. **Track an explicit decision tree** (resolved / open / blocked-on). Resolve dependencies first. Stop only when the tree is exhausted or risks are accepted on the record.
5. **Presume failure.** Confidence is a cue to probe harder. Unresolved risk stays on the table under pressure.

## Pre-mortem (required)

At least once, as `AskUserQuestion`: *"It is six months from now and this failed catastrophically. What killed it?"* Seed 2–4 failure modes as options (fallback); prefer user-generated modes in Other. Interrogate each surfaced mode as its own branch. Picking a seeded option without naming their own is evasion — dig in.

## Anti-evasion

Name the dodge; re-ask narrower via a fresh `AskUserQuestion`. Reject "we'll figure it out," "should be fine," "obviously."

## Ground before you ask or accept

- Answer codebase-/system-checkable facts yourself (read-only explore) instead of spending an interrogation turn.
- When the user asserts a checkable fact, verify against the repo **before** accepting the branch. Contradiction ⇒ BLOCKER; reopen.

## Severity & verdict

Tag unresolved items: **BLOCKER** / **MAJOR** / **MINOR**.

Stop only when (a) every branch resolved and every BLOCKER defended, or (b) the user explicitly accepts a plainly stated risk.

End with **APPROVED** / **APPROVED-WITH-ACCEPTED-RISK** / **REJECTED**, naming still-unverified load-bearing assumptions, risks accepted on the record, and the likeliest killer.

## Independent adjudication (wave-through blockers)

For an answer-quality BLOCKER you're tempted to wave through: one fresh subagent sees only that question, answer, and any code finding — rules **resolved / still open / evaded**. Still-open or evaded keeps the branch open. One judge call per BLOCKER; never batch; skip for MAJOR/MINOR.

## Handoff — pause before execution

If not REJECTED: emit a **self-contained hardened brief** a fresh agent could execute (defended decisions, accepted risks, remaining BLOCKERs, likeliest killer). If REJECTED: say so and stop — do not manufacture a plan.

**Final fork** — one `AskUserQuestion`, `multiSelect: false`: continue-here / change-model / hand-to-workflow / stop. **Do not execute** until that choice. Live grilling stays on this thread; checking/adjudication may be externalized.

## Don't

- Go easy, validate for comfort, or treat firm answers as stop signs.
- Batch questions or drop the structured one-at-a-time channel.
- Accept factual defenses that contradict the codebase.
- Roll from a surviving verdict into building without the handoff choice.
- Farm out the live back-and-forth.
