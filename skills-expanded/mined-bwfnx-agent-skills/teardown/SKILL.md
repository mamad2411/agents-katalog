---
name: teardown
description: Tear down a workflow, process, or business plan before improving it — using ESIA (Eliminate, Simplify, Integrate, Automate) for processes and Discovery-Driven Planning for plans, run strictly in order with gates between steps. Built for consultants and advisors working through a client's operations, and for tearing down their own internal workflows. Use this whenever the user wants to streamline, fix, tighten, audit, re-engineer, or rethink a process or plan — theirs or a client's; whenever they ask "how do I automate this," "how do I speed this up," "where is this bleeding money," or "is this worth doing"; whenever they mention business process re-engineering, process mapping, waste, margin, or cutting steps; and whenever a plan rests on untested assumptions. Use it even if they only ask about the automation or speed part — that is exactly the case this skill exists to catch.
---

# Teardown

Two established engines, one ordering rule.

- **Process mode → ESIA.** Eliminate, Simplify, Integrate, Automate. Peppard &
  Rowland, *The Essence of Business Process Re-Engineering* (1995).
- **Plan mode → Discovery-Driven Planning.** McGrath & MacMillan (1995):
  reverse income statement, deliverables spec, key assumptions checklist,
  milestone chart.

**The ordering rule** predates both: Hammer's *Don't Automate, Obliterate*
(HBR, 1990). Automating a process you haven't questioned encases the waste in
software. Every step below exists to stop that.

Run **one step per turn.** Do not preview later steps. Do not produce a
four-section report — that's a listicle, not a teardown.

## Pick two things at the start

**Engine:** process (ESIA) or plan (DDP). If the object is a plan for a process
that doesn't exist yet, it's plan mode.

**Standing:** operator or advisory.

- **Operator** — it's yours to change. You can cut and see what happens.
- **Advisory** — it's a client's, or another team's. You have no authority to
  cut, and you shouldn't want it. The deliverable is a ranked set of questions
  and candidate cuts *they* decide on, plus the reasoning that got you there,
  in a form they own after you leave.

Say both out loud before step 0. Standing changes what step 2 is allowed to do,
so guessing it is not an option — ask if it's unclear.

---

## Step 0 — Get the object (both modes)

**Process mode:** map the as-is. A numbered list of every step, handoff,
approval, and wait. Ten to forty items is typical.

**Plan mode:** build the key assumptions checklist. Every belief the plan
requires to be true. Include the boring ones — staffing, channel access,
payment timing — those are where DDP says the fatal ones hide.

If the user hasn't given you enough to enumerate, ask. No inventory, no run.

**Who builds the inventory matters.** Ask whether the list came from someone
who actually performs the work, or from someone who manages it. A manager's map
of a process is a wish list — it omits the workarounds, the second spreadsheet,
and the phone call that makes the official step function. If the answer is
"manager," say so and treat the inventory as provisional until a practitioner
reviews it.

**Step 0 is not skippable.** The skip-ahead rule below lets the user jump to a
later *step*; never past the inventory. "Just automate it" still gets
"automate what, exactly — list the steps."

Record the count as **N**. If N < 8, say so and run conversationally — the
scoreboard math below is noise at that size.

---

## Step 1 — Question the requirements

Not part of ESIA. It comes from **Value Analysis** (Miles, GE, 1947): for each
item ask *what function does this perform*, then *what else would perform that
function*. Pair it with **5 Whys** when the answer is circular.

For each item, get:

- **Owner** — a named human. Not "compliance," not "the client," not "policy."
  A department can't be argued with; a person can.
- **Function** — what it produces that something downstream consumes.

Tag each item:

- `ORPHAN` — no owner nameable. First to go.
- `INHERITED` — it's there because it's always been there. Second to go.
- `IMMOVABLE` — a statute, contract, or funder condition compels it.
  **Requires a citation** — the clause, named. "It's required" without a source
  is an ORPHAN wearing a badge. And note what's actually mandated: rules
  specify an *outcome*, almost never your implementation of it. The outcome
  survives; the implementation goes to Simplify.

If more than half the inventory returns IMMOVABLE, stop. That's the finding —
most of those are inherited belief. Restart step 1 demanding citations.

**Gate:** every item has an owner or a tag before advancing.

---

## Step 2 — Eliminate

ESIA's first move, and the one with the most leverage. Non-value-adding
activity goes — but not in arbitrary order.

### The materials ratio — where to start

ESIA tells you what to cut but not what to cut *first*. This does, and it's
arithmetic rather than opinion.

**Materials ratio = fully-loaded cost of the thing ÷ irreducible cost of what
it's actually made of.**

- **Process:** cost of running the step (time × loaded rate, plus tooling and
  licenses) ÷ the cost of the smallest defensible version of the output. A
  four-hour report assembled from data that takes twenty minutes to pull has a
  ratio near 12.
- **Plan:** price ÷ true input cost. Delivered cost of a service ÷ the cost of
  the labor and materials actually consumed. Note that a healthy service
  business is *supposed* to score high here — read this one against the gap
  test below before drawing any conclusion, or you'll flag an 80% gross margin
  as a defect.

A high ratio means the design is too complex, the process is too inefficient,
someone in the chain is taking a margin you haven't noticed — **or the gap is
the value.** Expertise, judgment, IP, brand, and relationship all produce high
ratios by design, and the framework this borrows from assumes manufacturing,
where value roughly equals material transformation. That assumption does not
hold for advisory, creative, or licensed work.

So the ratio never says *cut*. It says *look here, and name what's in the gap.*
Write the gap out loud in one sentence before deciding anything:

- "The gap is four hours of reformatting." → eliminate.
- "The gap is fifteen years of knowing which question to ask." → that's the
  product. Leave it alone and check whether you're charging for it.

If you can't name what's in the gap, that's the finding. Investigate before
cutting.

### Computing it without fooling yourself

- **Write the denominator first**, before you compute anything. Describe it as
  a concrete artifact — "a one-page memo with these three numbers" — not an
  abstraction like "the insight." Abstractions can be resized after the fact to
  produce whatever ratio you wanted.
- **Only avoidable cost counts** in the numerator. A platform license you're
  locked into for eighteen months doesn't vanish when you cut the step, so it
  doesn't inflate that step's ratio. Count what actually stops being spent.
- **State the basis** — per run, per month, per client. A step shared across
  twelve processes has a wildly different ratio depending on whether you charge
  it whole or allocated. Compute at the level you can act on, and say which.
- **Near-zero denominator?** Don't divide. A step whose output is an approval,
  a signature, or a status update has no irreducible input cost. Those don't
  enter the ranking — they go straight onto the elimination candidate list,
  which is usually where they belonged.
- **Skip where the denominator is guesswork.** A fabricated ratio is worse than
  none, because a number ends the argument.

Rank what remains. Report the top three and start Pass A there — except where
the top item is tagged IMMOVABLE with a valid citation. Those can't be
eliminated, so route them to step 3 with priority: a high-ratio immovable is
the four-page compliance form that could be one page and satisfy the same
clause. That's the single best use of this screen.

### The passes

Peppard & Rowland's elimination targets: over-production, waiting time,
transport, over-processing, inventory, defects and failures, duplication,
reformatting, inspection, reconciling. Walk the inventory against that list —
reformatting and reconciling in particular hide in plain sight because someone
built a job title around them.

**Pass A — cut.** ORPHAN and INHERITED first, then anything matching a target
above, working down the materials-ratio ranking. Record the count deleted, **D**.

**Cut to the point of failure.** ESIA is conservative — it removes what's
provably non-value-adding. The sharper posture is to keep cutting until
something actually breaks, then restore. That's what makes the add-back test
below mean anything: without it you'll stop at comfortable.

Three hard limits on that posture, no exceptions:

- Never in **advisory mode** — you don't get to break someone else's process to
  learn where its edges are.
- Never on an **IMMOVABLE** item with a valid citation.
- Never where failure has a cost that can't be undone — safety, legal exposure,
  a client relationship, data you can't get back. Cut to failure is for things
  you can restore on Monday.

Where those limits bite, say so and cut conservatively instead.

**Advisory substitute — the reversible trial.** You can't cut to failure in
someone else's shop, but the client can, and finding the edge is still the
point. So convert each candidate cut into a trial they can run:

- What stops happening, starting when.
- What you expect to break, named specifically. A prediction they can check.
- How long it runs before you both look — a week, a billing cycle, ten
  transactions.
- What restores it, and who can trigger that without asking permission.

A cut with no named reversal isn't a trial, it's a change order. The
add-back count comes from what the trials actually forced back, not from
argument at a whiteboard — which makes advisory mode slower and the evidence
considerably better.

**Pass B — add back.** Restore only what genuinely fails without it. Record the
count restored, **R**.

The forcing function differs by mode:

- **Process:** walk the shortened version end to end. What actually breaks?
  Reality does the arguing.
- **Plan:** nothing is real yet, so nothing "breaks." Substitute a person — for
  each cut, name who would object and what they'd say. Restore only if the
  objection survives one round of pushback.

**The add-back test** (a heuristic, not from the literature — treat it as a
smell, not a law): if you were forced to restore nothing, you were timid, and
Pass A should run again. If you restored more than half of what you cut, you
were reckless. Report D, R, and the ratio either way.

---

## Step 3 — Simplify

For what survived. Peppard & Rowland's simplification targets: forms,
procedures, communication, technology, flows, problem areas. IMMOVABLE items
get their *implementation* simplified here — this is where the four-page
compliance form becomes one page that satisfies the same clause.

---

## Step 4 — Integrate

The step most people skip, and the one that actually buys speed. Integration
targets: jobs, teams, customers, suppliers. Collapse handoffs into single
owners; pull the customer or supplier inside the process rather than
corresponding with them across a wall.

**Note on cycle time:** ESIA has no separate "accelerate" step, and that's
deliberate. Cycle time is the *measure*, not a move — it falls out of
eliminate and integrate. If you're looking for a speed lever that isn't one of
those two, you're usually looking at asking people to hurry. Measure cycle
time at step 0 and again at the end; don't chase it as its own step.

---

## Step 5 — Automate

Last. Automation targets from the framework: work that is dirty, difficult,
dangerous, or boring, plus data capture, data transfer, and data analysis.

Only for steps that survived 1–4 and are now stable. Anything still changing
shape shouldn't be automated — you'd be casting concrete around a moving part.

---

## Plan mode: what replaces steps 2–5

ESIA is process-native. Don't force a plan through it. After step 1, switch to
the DDP sequence:

1. **Reverse income statement** — start from the profit the venture must earn
   to be worth doing, work backward to required revenue, then to allowable
   cost. This is the constraint everything else answers to.
2. **Deliverables spec** — what the operation must actually be able to do to
   hit those numbers.
3. **Rank the assumptions** by uncertainty × consequence. The riskiest belief
   with the biggest downside goes first, regardless of how uncomfortable it is.
4. **Milestone chart** — for each top assumption, the cheapest test that could
   disprove it, and when. DDP's whole point: convert assumptions to knowledge
   at the lowest possible cost, and treat milestones as decision points, not
   dates on a calendar.

The reverse income statement is the plan-mode equivalent of the elimination
pass. It kills more ideas than any amount of critique, because it's arithmetic.

---

## Advisory mode reminders

The owner should be in the room. Step 0's authorship rule matters most here —
if you're mapping a client's process from what the founder told you, you have
the official version, not the real one. Ask to hear it from whoever runs it
daily before you rank anything.

Keep the scoreboard and the materials ratio. Both are good conversation
openers precisely because they're arithmetic — a number moves a discussion
that an opinion about someone's process will not.

---

## When the user skips ahead

They will. Warn **once**, specifically, then comply.

> "You're asking me to automate the intake form. Nobody has established the
> intake form should exist. Proceeding anyway — flagging it."

Name the actual thing and the actual unearned step. Don't lecture, don't
repeat, don't refuse. Log it.

---

## Close-out

```
Object: <name>   Engine: process (ESIA) | plan (DDP)   Standing: operator | advisory
N: __  D: __  R: __  ratio: __%
Highest materials ratio: <item, value>  Gap is: <one line>  → cut? y/n
Cycle time: before __ / after __        [process mode]
Top untested assumption: <one line>     [plan mode]
Survived: <count> items
Unearned steps taken: <list, or none>
```

## Legitimate null results

Sometimes the honest answer is "eliminate nothing." Say it. A run that cuts
zero items but produces three named owners and one ORPHAN nobody knew about is
a successful run. Don't manufacture deletions to make the scoreboard look good.

## When not to use this

These frameworks optimize for value-added throughput. Some processes are
load-bearing for reasons throughput can't see — trust-building, learning,
relationship, ceremony, deliberate redundancy in safety-critical work. If the
object's purpose is relational rather than operational, say so up front and
offer to run it with that flag raised, rather than quietly cutting the human
parts.

## Sources

- Peppard, J. & Rowland, P. (1995). *The Essence of Business Process
  Re-Engineering.* Prentice Hall. — ESIA
- Hammer, M. (1990). "Reengineering Work: Don't Automate, Obliterate." *HBR.*
- McGrath, R. G. & MacMillan, I. C. (1995). "Discovery-Driven Planning." *HBR.*
- Miles, L. D. (1947, GE). Value Analysis / Value Engineering — function test
- The materials ratio, the cut-to-failure posture, and the add-back test are
  adapted from the process algorithm described in Walter Isaacson's *Elon Musk*
  (2023), where the ratio appears under a different and less useful name.
