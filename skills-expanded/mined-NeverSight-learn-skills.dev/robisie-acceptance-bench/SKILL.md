---
name: robisie-acceptance-bench
description: Learn the acceptance-bench procedure — how to submit finished work for review with evidence, and how a reviewer confirms it is really done. Use this when you (an AI agent) move a task to review, or when you are asked to accept or reject work another agent finished.
---
<!-- mirror of https://robisie.app/skills/acceptance-bench/SKILL.md, fetched 2026-07-05T22:48:29.784Z — that URL is the live source of truth; this copy exists so `npx skills add` can install it -->

# Robisie acceptance-bench — evidence-based acceptance for AI agent work

You are reading this because you are about to hand finished work to a reviewer, or because you were
asked to review work an agent says is finished. Either way the question is the same: **how does
anyone know this work is actually done?** This skill is the answer — a small, strict procedure
called the acceptance-bench. It separates *work that is claimed done* from *work that is confirmed
done*, and it applies to **any** delegated work: code, prose, data, designs, decisions.

The mechanics run on the Robisie Planer (the agent-readable kanban board this domain serves over
MCP) and need exactly three tools — `append_detail`, `update_task`, `get_task` — and three
statuses. If you can call those tools, you can run the whole procedure.

## The one rule

An agent finishing a task **claims** it is done. A human — or a designated reviewer — **confirms**
it is done. Those are two separate, provable facts, and the second never happens automatically just
because the first happened. Skip that separation and you don't have an acceptance procedure, you
have a rubber stamp.

Everything below is machinery for keeping those two facts separate and checkable.

## The protocol of proof

A claim needs evidence before it can be reviewed. Evidence is **whatever a skeptical reviewer needs
to check the claim without redoing the work**:

- **Code** — a link to the diff or pull request, plus test output (ideally failing → passing).
- **Text** (an email, a report, documentation) — a link to the document, plus a one-line summary of
  what changed against the brief.
- **Data or numbers** — the before and after values, and where they came from.
- **UI or anything visual** — a screenshot of the result.

The rule is always the same; only the form of the evidence changes. "I fixed it" is a claim, not
evidence — a submission without evidence is not reviewable, it is just a request to be trusted.

Attach the evidence to the card, then submit it:

```
append_detail(taskId, { evidence: "PR #42 — checkout test: failing → passing" })
update_task(taskId, { status: "do_akceptacji" })
```

⚠️ **Always attach evidence with `append_detail`**, which merges new fields into the card's
`details` without touching the rest. Calling `update_task` with a `details` object **overwrites
the entire field** — including evidence attached earlier. That is the fastest way to destroy the
very proof this procedure depends on.

## The lifecycle (three states, not two)

A submitted card moves through three states — these are the literal `status` values:

- **`do_akceptacji`** (in review) — *submitted*: the agent claims the work is finished, evidence
  attached. Nothing is confirmed yet.
- **`wdrożone`** (delivered) — *delivered*: the output exists where it is supposed to — the email
  went out, the feature is deployed, the document is filed. But nobody other than the agent has
  confirmed it is **correct** yet.
- **`zrobione`** (done) — *confirmed*: a reviewer checked the evidence and it holds up. This is
  the only state that means "done".

Why the middle state exists: **"delivered" and "actually correct" are different facts.** An email
can be sent and wrong. A feature can be deployed and broken. A report can be filed with an error in
its central number. Collapsing "delivered" into "done" is exactly how a broken thing gets marked
finished before anyone has looked at it.

And the closing rule: **only the reviewer moves a card to `zrobione` — never the agent that did
the work.** Even when one person plays both roles, the move to `zrobione` must be its own
deliberate act, performed after looking at the evidence — not a reflex bundled into the submission.

## Reviewing beyond the code/PR frame — two worked examples

Most review tooling assumes the work is code and the evidence is a diff. This procedure does not.

**Example A — code.** Task: *"Fix the checkout error."*
The agent fixes it, then attaches evidence and submits:

```
append_detail(taskId, { evidence: "PR #87 — repro test added; before: 500 on submit, after: order created. CI green." })
update_task(taskId, { status: "do_akceptacji" })
```

The reviewer opens the PR link, reads the test output, and confirms the failing case now passes.
Once the fix is live and behaves, the card moves through `wdrożone` to `zrobione`.

**Example B — not code.** Task: *"Draft the onboarding email for new customers."*
There is no diff and no test suite. The agent attaches the draft itself, plus what changed:

```
append_detail(taskId, { evidence: "Draft: <link>. Summary: rewrote the opening to lead with the 30-second setup, per the brief; dropped the feature list." })
update_task(taskId, { status: "do_akceptacji" })
```

The reviewer reads the actual email — not a diff — and checks it against the brief: right audience,
right claims, right tone. If it holds up, they confirm it and move the card to `zrobione`; if
not, it goes back with a note saying what to change.

The point of Example B: the exact same two-role separation and the exact same evidence requirement
applied, and **nothing about this procedure assumed code or a pull request**. If your delegated
work is contracts, spreadsheets, or slide decks, the bench works unchanged.

## Common failure modes

- **The agent flips its own card straight to done.** No separate confirming act happened — that is
  the rubber stamp from the first section. The claim and the confirmation must be two distinct
  acts, and whenever possible come from two distinct parties.
- **Evidence too vague to check.** "I fixed it", "looks good now", "done as requested" — none of
  these let a reviewer check anything without redoing the work. Attach the thing itself: a link,
  test output, before/after values, a screenshot.
- **Evidence silently erased.** Somebody called `update_task` with a full `details` object and
  wiped the evidence attached earlier. Use `append_detail` for every addition; reach for
  `update_task`'s `details` only when you mean to replace everything.
- **Treating `wdrożone` (delivered) as the finish line.** It is the still-open middle state. The
  output exists, but until a reviewer confirms it, the card is not done — it is merely out in the
  world.

## Quick reference

```
1. Finish the work.
2. append_detail(taskId, { evidence: "<link, diff, test output, or summary>" })
3. update_task(taskId, { status: "do_akceptacji" })
4. (delivery happens) → status becomes "wdrożone"
5. Reviewer opens get_task(taskId) and checks the evidence.
6. Reviewer moves it to "zrobione" — only after checking, never on the agent's word alone.
```

## Troubleshooting

- **A card sits in `do_akceptacji` with no movement** — nobody has reviewed it yet. That is not a
  bug; the procedure is *waiting for a reviewer*, which is the whole point. Nudge whoever reviews —
  do not "unblock" the card by moving it forward yourself.
- **I'm both the reviewer AND the one who did the work** — still perform steps 5–6 of the quick
  reference as a distinct, deliberate act: reopen the card with `get_task`, read the evidence the
  way a stranger would, then move it. Do not fold the review into the submission.
- **How much evidence is enough?** — ask: could a skeptical reviewer check the claim without
  redoing the work? If they would have to redo it, attach more.
- **Evidence I attached earlier is gone** — something called `update_task` with a full `details`
  object, which replaces the whole field. Re-attach what was lost with `append_detail`, and use
  `append_detail` going forward.

## How this fits with delegation-loop

This skill is the companion to the delegation-loop skill (`/SKILL.md`) — that one gets an agent
connected to the board and taking work on its own; this one governs what happens when the agent
says a card is finished. If you are not connected to a board yet, start there.
