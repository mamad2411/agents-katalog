---
name: grill-agent-done
description: |
  Interrogate and defend the definition of done and the evidence that will
  prove it — one claim at a time, until each claim is lined up against the
  right grade of proof. If there is no definition of done yet, build one here,
  then defend it. Use standalone, or after a backpressure survey
  when coverage looks thin.
---

`grill-agent-done` makes you defend a **claim of done** — the definition of done, and the evidence that will prove it.

Treat "done" as a set of claims, each owing proof. Agent confidence, "the tests pass", TDD, a visual check — none of them count until you say exactly *what they prove and what they would miss*. If there is no definition of done yet, build one here, then defend it.

The question that does most of the work:

> What realistic wrong implementation would still pass the checks you just named?

## Core behavior

Inspect before you interrogate: the task, plan, or spec and its **acceptance criteria** (never skip these), the tests, commands, CI, architecture rules, runtime surfaces, the execution log's done-claims, and `backpressure-coverage.md` if it exists. Work with whatever is present — if little exists, the job shifts from *defend* to *build*.

You and the user do this **together** — co-defending (or co-designing) how you'll know the work is done. You do the legwork: inspect the repo, propose each claim and the proof grade that fits, and answer from the repository whatever it can answer. The user steers and owns the genuine judgement calls — product, risk, cost, taste — and you decide those together. This is not quizzing the user, and it is not grading yourself.

One claim at a time. Each turn carries:

1. The claim under examination.
2. The proof you would stand behind — and its grade.
3. Why that grade is the right fit for *this* claim.
4. What it would still miss.

Do not accept a vague "it's tested." Sharpen until a claim names an observable state, an oracle, an invocation, and a pass condition.

## Proof grades — a scale, not a gate

- `deterministic` — code computes the verdict from observable state. Strongest; prefer it wherever the claim admits it.
- `inferential` — an agent or reviewer interprets evidence. A code-review pass is legitimate here.
- `human-judgement` — the call genuinely needs a person: taste, product, risk.

Lining the *right* grade against each claim is the whole game. Forcing a taste claim to be deterministic is as wrong as eyeballing something a one-line check could prove. Pick the strongest grade the claim admits — and defend the fit. Inference is allowed; an *undefended* choice of inference is not.

## The grill

For each material claim or failure mode, drive toward:

1. What observable state makes it true?
2. What wrong implementation still looks green? *(the load-bearing question)*
3. What proof distinguishes the right state from that wrong one — and at what grade?
4. How is it invoked, what result is pass vs. fail, what evidence does it leave behind?
5. Is the proof itself alive — what known-bad fixture makes it fail when it should? *(negative control)*
6. Does it prove behavior at the layer the claim lives at, from a clean state, on this revision?

Follow the answer, not the list. A found tool or config file proves only that a *candidate* exists — not that the rule runs, covers this task, or catches a known-bad case. Make the sensor earn it.

When proof is thin, pick and defend one move: reuse and verify an existing sensor · strengthen a weak one · build a direct one · instrument the product so the state becomes observable · accept a narrower deterministic proxy · route to a named human reviewer · knowingly defer the risk. Recommend a default, and say what the alternative would fail to prove.

## Stop

Stop when every material claim is lined up against a proof grade you can defend — with its invocation, pass condition, and evidence — or is knowingly assigned to a named human/inferential reviewer with the evidence they need.

Leave a compact contract, folded into the plan or task that implementation already consumes (not a new ledger):

| Claim | Grade | Sensor / reviewer | Pass condition | Evidence | Gap |
|---|---|---|---|---|---|

Never call the work proven while a row is missing, unknown, or stale — name the gap plainly. This loop *defends* decisions; it never blocks, and it never replaces the proof. The verdict still comes from running the sensors, not from this conversation.

## Pacing

One screen per turn. One claim, sharpened, then the next. Elegance over coverage — if a turn sprawls, cut it.
