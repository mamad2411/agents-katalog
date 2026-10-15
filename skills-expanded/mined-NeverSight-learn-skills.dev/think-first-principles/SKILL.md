---
name: think-first-principles
description: Rebuild a decision from what must be true instead of from precedent. Recover the real objective, label every assumption, compute the theoretical floor and compare the current system against it, delete before optimizing, then propose the cheapest test that would settle the remaining doubt. Use this whenever the user is choosing an architecture, sizing a system, cutting cost or latency, questioning a requirement, evaluating feasibility, redesigning a process, or saying things like "why is this so expensive", "is there a better way", "everyone does X but", or "challenge my assumptions". Reach for it any time a decision is expensive to reverse or the obvious answer is inherited rather than derived, even when the user never uses the phrase.
---

# Think from first principles

Most answers are copied. Someone picked a number, a tool, or a process step under constraints that no longer hold, and everyone downstream inherited it as fact. The discipline here is separating what must be true from what merely happens to be true, then rebuilding from the first group.

This is not contrarianism. Convention is often right, and the point is to know why you believe it.

## When to spend the effort

Run the full workflow when the decision is expensive to reverse, when the gap between options is large, or when the user asks for it. Otherwise take thirty seconds to ask what you are treating as given, and proceed normally if nothing interesting falls out. Grinding a full teardown through routine work buries the answer.

## The workflow

### 1. Recover the real objective

Write down the outcome the user actually wants and the metric that would prove it. The requested method is not the objective: "add a caching layer" is a proposed means, "p99 read latency under 100 ms at 10k requests per second" is an objective.

Watch for two objectives fused into one request. "Cut the queue backlog because the bill is too high" contains a throughput goal and a cost goal, and they often have opposite solutions, since buying throughput usually raises the bill. Separate them and ask which one the user is judged on.

**In a single response, do not stall on questions.** State the assumption you are proceeding on, label it, and carry the open questions into the final section as the cheapest test.

### 2. Label the assumptions, keep what survives

List every input that materially changes the answer and label each one: **hard constraint** (physics, mathematics, law, a stated user requirement), **verified fact** (measured or read from a named current source), **estimate** (reasoned, with a range), **inherited convention** (this is how it is done here), or **unknown** (load-bearing and unmeasured).

Then the rule is one line: keep hard constraints and verified facts, and treat everything else as provisional until it earns its way back.

The labels do the work. An assumption you cannot classify is usually an inherited convention wearing a lab coat. For each constraint, ask whether it follows from the nature of the problem or from someone's earlier decision, and watch for constraints that are actually someone else's solution: a schema shape, a vendor's page size, a framework's lifecycle, a team boundary.

### 3. Compute the floor

Estimate the least cost, time, energy, bytes, or work the problem requires under idealized conditions, and show the arithmetic so someone can check it.

**When the load-bearing numbers are unavailable, bracket them and compute both ends.** Take the plausible best and worst case, run the arithmetic on each, and check whether the conclusion flips. If an image resize costs somewhere between 30 ms and 400 ms of CPU, compute both ends, and if the answer lands far below the current bill either way, the conclusion is robust to your ignorance and you can state it plainly. If the conclusion does flip, you have identified the one number worth measuring first.

Label estimates as estimates. Invented figures dressed in units and arithmetic are more dangerous than an honest gap, because they survive review.

**When the observed number is a bill, decompose it before comparing.** The floor tells you the total is wrong; the itemization tells you where. Ask for the cost breakdown by line item, because the dominant line is frequently not the one everyone is arguing about, and the fix is often a configuration change rather than a redesign.

**When the complaint is a queue or a backlog, compare arrival rate against service rate.** Twelve million items a month is 4.6 per second, and knowing that reframes "we need a bigger machine" into "why is 4.6 per second backing up".

When no numeric floor is meaningful, name the irreducible steps instead: the information that must be gathered, the round trips that must happen, the state that must persist.

Comparing the current system against its floor tells you where to look. Within a small multiple, the system is close to done and further optimization is misspent. An order of magnitude or more says something structural is wrong. Treat the ratio as a pointer to a question, never as proof the gap is waste, since real systems pay for reliability, safety margin, and human time that no idealized floor accounts for.

### 4. Rebuild, deleting first

Construct the answer from the surviving constraints, smallest thing first.

Work the ladder in order: remove the requirement, then remove the step, then simplify what remains, then speed it up, then automate it. Deletion is the only optimization that cannot regress, and automating a step that should have been deleted is the most common way effort disappears.

Then attack the boundaries. Ask what changes if the work runs somewhere else, at a different time, batched differently, precomputed, derived instead of stored, or done once instead of per request. Most large wins come from moving a boundary rather than improving the code inside one.

On whether to reuse the conventional component: let the size of the gap decide. When the current system is within a small multiple of its floor, the boring dependency that a thousand teams have debugged is almost always right, and building your own is the error. When the gap is an order of magnitude or more, the boring thing is usually being misconfigured or misused, and the fix is configuration, a different call path, or deleting work, still rarely a rewrite.

### 5. Attack it, then give the cheapest test

Push the variables to their extremes: ten times the load, one tenth, the second year of operation, every dependency failing. Steel-man the conventional alternative and compare it on the same metrics, because that is the difference between analysis and advocacy.

Count what idealized reasoning omits: migration, operational burden, on-call load, unfamiliarity, integration surface, and the time cost of being novel. These are the usual reason a clever rebuild loses, and naming them yourself is more credible than having them pointed out.

Then give a recommendation with its uncertainty attached, and name the smallest thing that would settle it. Order the options by cost:

1. **Read the telemetry you already collect.** Cost breakdowns, dashboards, existing logs, a config or route table. Minutes, no code, and it frequently ends the debate.
2. **Measure the one thing nobody measured.** A timing run over a representative sample.
3. **Build a spike or benchmark** only when the first two cannot answer it.

Say which uncertain input would most change the conclusion, and put it first.

## How this fails

**Reinventing a solved thing.** First-principles reasoning is a strong argument for building it yourself, and that argument is usually wrong. If the rebuild saves less than the cost of owning it forever, use the boring thing.

**Confident numbers with no source.** Bracket and label instead, or say you do not know.

**Mistaking the floor for a forecast.** The theoretical minimum is a reference point, not a delivery target.

**Performing the ritual.** If the reasoning did not change the recommendation, compress it to a line. Structure that outruns the insight buries the answer.

**Ignoring people.** Team familiarity, hiring, and maintenance are real constraints. A design nobody can operate has failed.

## Reporting it

Lead with the recommendation and the one-line reason, then the arithmetic, then what you are still unsure about and what to check first. Keep the write-up proportional: a three-line teardown that changes the plan beats a two-page one that confirms it.

Use headings only when the work justifies them, and merge any that would repeat each other: objective and constraints, assumptions and what survives, the floor, the rebuilt approach, the stress test, then the recommendation with its next test.
