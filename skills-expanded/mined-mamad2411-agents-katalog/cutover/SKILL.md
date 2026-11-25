---
name: cutover
description: "Plan and run a high-stakes, hard-to-reverse switchover to completion — a DNS or traffic switch to a new system, a datacentre or region move, a hosting or vendor swap, a monolith-to-service carve-out with a big-bang or gradual shift, a database failover or promotion. Produces the numbered runbook with owners and abort conditions, written go/no-go criteria, a timed rehearsal, a rollback plan with an explicit deadline, the data freeze and reconciliation steps, the comms cadence, and a bake-then-decommission plan. Use this skill for planning or running a migration weekend or switchover window, including phrasings like \"we're moving off Heroku on the 14th\", \"how do we cut DNS over without dropping requests\", or \"who decides to roll back\". Not for routine deploys, feature-flag rollouts, a live unplanned incident, or the multi-phase migration plan a cutover sits inside — that is plan-platform-migration."
allowed-tools: "Read, Write, Grep, Glob, Bash(dig:*), Bash(curl:*)"
---

# Cutover

A cutover goes well when the window is boring: every step was run before, in order, by the person named next to it, and the only thing anyone learns on the day is what the clock says.

The difficulty is not technical. It is that a cutover is an operation with a point of no return, a decision-maker, an audience and a clock, and teams keep running it as if it were a deploy — improvised, in a call with eleven people, with the rollback plan existing only as a shared belief that "we can just point DNS back". Three things then go wrong in the same order every time. The plan has never been timed, so the two-hour window becomes five and nobody can say when it will end. The rollback has no deadline, so at hour four the choice between reverting and pressing on is made by whoever is most tired. And the decommission gets folded into the same window to save a trip, which removes the only thing that made the change reversible. The procedure below exists to make each of those impossible before the window opens, because none of them can be fixed inside it.

## Scope

Use for: a planned switchover with a point of no return — traffic or DNS moved to a new system, a region or datacentre move, a hosting or payment or email provider swap, carving a service out of a monolith, a database promotion or failover, a system-of-record replacement.

Do not use for: routine deploys or a progressive feature-flag rollout, which are reversible by design; a live unplanned incident, which is `incident-response`, or `k8s-triage` for a Kubernetes workload; the writeup afterwards, which is `postmortem`; or the schema change and backfill mechanics themselves, which are `db-migration` and are usually finished well before the cutover window opens.

## What separates a cutover from a deploy

| | Deploy | Cutover |
| --- | --- | --- |
| Reversal | Redeploy the previous artefact, minutes | A separate procedure with its own duration, and a point after which it stops being available |
| Decision | Automated, or the author's | A named person, at a named time, against written criteria |
| Audience | The team | Stakeholders, support, and often customers |
| Time | Whenever CI is green | A window with a start, an end, and a rollback deadline inside it |
| Preparation | Tests | A timed rehearsal of the actual steps |

If the change has none of these properties, it is a deploy. Treat it as one and do not spend a week on ceremony.

## Workflow

Steps 1 to 5 all happen days before the window. If the window is tomorrow and none of them are done, say so plainly and move the date — that conversation is much cheaper before than after.

### 1. Name the roles and the point of no return

Three roles, three people. One person holds the keyboard and runs the steps. One holds the clock and the comms — announcing step numbers, tracking elapsed time against plan, posting updates. One decides: go, no-go, roll back. The decider does not type. A cutover where the person executing is also the person judging whether it is going well has no judgement in it, because they are busy.

Then write down the single sentence that names the point of no return: the step after which the old system can no longer serve correctly. Usually the first write that lands only on the new side. Everything before it is rehearsal with real traffic; everything after it is commitment.

### 2. Write the runbook

Numbered steps, in order, each with the same five fields. A step without an abort condition is a step nobody knows how to stop.

```markdown
### Step 7 — Shift 10% of traffic to the new stack
Owner:     @name (keyboard)
Duration:  5 min (rehearsed: 3m40s)
Command:   aws elbv2 modify-listener --listener-arn ... --default-actions file://weights-90-10.json
Expect:    new-stack RPS ≈ 10% of total within 60s; 5xx rate unchanged; p99 within 10% of baseline
Abort if:  5xx above 0.5% for 2 consecutive minutes, or p99 above 2x baseline → run rollback step R3
```

Rules that make a runbook usable at 03:00: exact commands, copy-pasteable, with the real ARNs and hostnames filled in — there is one marked place at the top of the document for environment-specific values, and nowhere else. Timestamps in UTC, because half the participants are not in your timezone and "2pm" is how two people join an hour apart. Every step has an expected observation, so "done" means the operator saw something, not that the command exited zero. Any step needing more than one person is split into two steps.

### 3. Rehearse it, and time it

Run the entire runbook against staging, a shadow copy, or a restored snapshot — with a stopwatch. Then use the measured durations in the plan, not the estimates.

An untimed cutover cannot have a window, because a window is a claim about duration and you have no data. The rehearsal also finds the two things that only a rehearsal finds: the step nobody owns because it sits between two teams, and the credential or firewall rule that exists in staging and not in production.

Rehearse the rollback too, from the far side of the point of no return. A rollback plan that has been read but never executed is a document, not a capability.

### 4. Write the rollback runbook and set its deadline

The rollback is its own numbered runbook with its own owners and its own measured durations. It is not "undo the steps above" — the reverse of a step is often a different operation with different risks, and the data written since the switch has to go somewhere.

Then set the **rollback deadline**: the clock time after which rolling back costs more than going forward. It follows from arithmetic you do beforehand — window end, minus rollback duration, minus a margin for the rollback going badly. Write it into the runbook and announce it at the start of the window.

Its purpose is to move the decision out of the moment. At hour four everyone is invested, tired, and sure the next step will be the last one; without a deadline the group discovers at hour six that rolling back now would overrun into Monday morning traffic. State it as: "If we have not completed step 14 by 04:30 UTC, we roll back. That decision is not reopened during the window."

### 5. Go/no-go

Entry criteria are written and agreed days ahead, then checked in a short call at T-0. Agreeing them on the day is how a criterion becomes whatever the room is already comfortable with.

Anything unchecked is a no-go. "We will fix it during the window" is the sentence that turns a two-hour window into a five-hour one, because the fix is unrehearsed work inserted into a plan whose timings assumed it was not there.

```markdown
## Go / no-go — [system], [date], T-0 [UTC time]
| # | Criterion | Owner | Status |
|---|-----------|-------|--------|
| 1 | Runbook rehearsed end to end; measured duration ≤ window | | |
| 2 | Rollback runbook rehearsed from past the point of no return | | |
| 3 | Rollback deadline agreed and written into the runbook | | |
| 4 | Data reconciliation green on the rehearsal (counts + checksums) | | |
| 5 | DNS TTLs lowered ≥ 48h ago and confirmed at the authoritative servers | | |
| 6 | New stack passing synthetic checks under production-shaped load | | |
| 7 | Monitoring and alerting live on the new stack, dashboards open | | |
| 8 | Support briefed; customer notice sent; status page prepared | | |
| 9 | Named keyboard / clock / decider present and available for the window | | |
| 10 | Change freeze on both systems in effect | | |
| 11 | Backups taken and a restore verified, not merely taken | | |
| 12 | No unrelated deploy, release or infrastructure change in the window | | |

Decision: GO / NO-GO — [decider name], [UTC timestamp]
```

### 6. Move traffic, not switches

Prefer a shift you can stop halfway. Weighted routing, a canary percentage, or a proxy that fans out — anything that lets you send 1%, look at it, then 10%, then 50% — converts a binary event into a series of small reversible ones, and it is available on nearly every load balancer, service mesh and CDN.

Where the platform only offers a flip, DNS mechanics decide the plan:

- Lower TTLs days ahead, not hours. The old TTL has to expire before the new one is honoured, so a change made at T-1h on a 24-hour record is still being served from caches tomorrow.
- Resolvers ignore TTLs. Some cap them low, some pin them high, some serve stale on failure. Java applications with the default `networkaddress.cache.ttl` cache a resolved address for the life of the JVM, so a long-lived client may never re-resolve at all.
- Therefore plan to serve correctly from both sides simultaneously for a stated period rather than relying on propagation. "DNS has propagated" is not an observable state.
- Verify at the authoritative servers rather than at your own resolver: `dig +norecurse @ns1.example.net api.example.com` tells you what was published; your laptop tells you what your ISP cached.
- Drain connections rather than cutting them. Keep-alive sockets survive a DNS change indefinitely; the old side has to stop accepting and let existing requests finish.

`references/traffic-switching.md` has the per-mechanism detail — weighted DNS, load balancer target groups, service mesh splits, CDN origin switches, and the health-check and draining settings that decide whether the shift is clean. Read it when designing the traffic step.

### 7. Data: freeze, sync, reconcile, release

The data half is where cutovers actually fail, and the order is fixed:

1. **Freeze writes** on the old system — read-only mode in the application, not a hopeful message to users. Note the UTC timestamp.
2. **Final delta sync.** Everything since the last bulk copy. Its duration is what sets the freeze length, so it is the number the rehearsal most needs to measure.
3. **Reconcile, before releasing traffic.** Row counts per table, checksums or hashes over the columns that matter, and a sampled record-by-record diff weighted towards the newest rows and the awkward types — money, timezone-sensitive timestamps, text encodings, nullable columns.
4. **Release writes** on the new system only when reconciliation is green. Publish the numbers into the channel; a reconciliation nobody saw is a reconciliation nobody did.

Decide in advance what a mismatch means. A handful of rows differing in a low-value audit table is a note; any difference in financial or identity records is a no-go and a rollback. Deciding that during the window, with the freeze running, produces the wrong answer.

### 8. Run the window

The clock owner posts on a fixed cadence — every 15 or 30 minutes — **including when nothing has changed**. Silence is read as failure by everyone not in the call, and it generates exactly the side-channel questions that distract the people executing.

```text
[UTC 02:15] Cutover step 7 of 19. On plan (+4 min). 10% traffic on new stack, error rate nominal.
            Next update 02:30. Point of no return is step 11, not yet passed.
```

The status channel is the record. Every command run, every observation, every decision, with timestamps — it is the raw material for the postmortem and for the next rehearsal, and it costs nothing while the operation is calm. One channel, not four; the decider and the keyboard are not answering DMs.

If something unplanned appears, the decider chooses one of three: continue, hold at this step, or roll back. "Investigate while continuing" is not one of them.

### 9. Bake, then decommission separately

Keep the old system running, in a state you could return to, for a stated period — days for most systems, a full billing or reporting cycle for anything financial. Write down what "reversible" requires during the bake, because it usually means continuing to replicate the new system's writes back to the old one, and that does not happen by itself.

Then schedule the decommission as its own change, with its own approval, after the bake. An old system left running indefinitely is both a cost and a split-brain risk: something will eventually route to it, write to it, and be believed. Put a date on it during the cutover planning, or it will still be running next year.

## During the window

| Signal | Class | Action |
| --- | --- | --- |
| Error rate up on the new stack right after a traffic increase | Capacity or config on the new side | Shift the traffic back to the last good weight. That is a step, not a rollback; take it immediately and diagnose at the lower weight. |
| Latency up but errors flat | Cold caches, cold connection pools, unwarmed JIT | Expected on a new stack. Hold at the current weight and watch it settle rather than shifting further or reverting. |
| Old system still receiving traffic long after the switch | Cached DNS, pinned resolvers, keep-alive connections | Expected. Keep serving both sides. Never "fix" it by turning the old side off. |
| Reconciliation counts disagree | Data integrity | Do not release writes. Apply the pre-agreed mismatch rule; if it is not clearly within the noted tolerance, roll back. |
| A step takes more than twice its rehearsed duration | Plan divergence | Hold. Recompute the finish time against the rollback deadline and have the decider re-confirm go or roll back with that number in hand. |
| An unrehearsed step is proposed mid-window | Scope creep | No. Note it, finish or roll back, do it as a separate change. Unrehearsed work is what the window's timings did not include. |
| Rollback deadline reached, cutover incomplete | Deadline | Roll back. The decision was made when everyone was rested; this is where that pays for itself. |

## Output format

```markdown
## Cutover: [system] → [system]
Window: [UTC start] – [UTC end] · Rollback deadline: [UTC] · Point of no return: step N

## Roles
Keyboard / Clock and comms / Decider — named.

## Go / no-go criteria
[The table above, filled in, with owners.]

## Runbook
[Numbered steps: owner, rehearsed duration, command, expected observation, abort condition.]

## Rollback runbook
[Same shape. Total measured duration. What it costs after the point of no return.]

## Data plan
[Freeze start, delta sync duration, reconciliation checks and their pass criteria, release gate.]

## Comms
[Channel, update cadence, stakeholder list, customer notice, status page.]

## Bake and decommission
[Bake period, what keeps the old system reversible during it, decommission date and owner.]
```

## Anti-patterns

**The cutover that has never been rehearsed.** Every estimate in the plan is a guess, so the window is a guess, and the first genuine surprise arrives at the least reversible moment. The rehearsal is also the only way to find the step that sits between two teams and is owned by neither.

**A rollback plan with no deadline.** Guarantees the decision gets made at the worst possible time by the most tired person in the call. The deadline exists precisely so the choice is made in advance, in daylight, by people who are not currently invested in it working.

**Decommissioning in the same window.** Removes the only thing that made the change reversible, in exchange for saving one scheduled change later. The old system is the rollback plan; keep it warm through the bake period.

**Silence between updates.** Everyone outside the call assumes failure and starts asking, which pulls the keyboard and the decider into answering instead of executing. A fixed cadence with "no change" updates costs one line every fifteen minutes and buys back the operators' attention.

**Everyone on the call has a keyboard.** Two people making changes to the same system without a shared order produces a state neither of them can describe, and no log that reconstructs it. One keyboard; anyone else who needs to act gets handed the step and announces before and after.

**Relying on DNS propagation.** There is no such event. Some clients honour the TTL, some cache for the life of the process, and some serve stale for hours. Plan to run both sides at once, and treat traffic still arriving at the old system as normal rather than as a problem to solve by shutting it off.

**Scope added inside the window.** "While we're in here" work is unrehearsed by definition, and its risk lands on a system that is already mid-change. Note it and do it as a separate change.

**Fixing a no-go item during the window.** Converts entry criteria into decoration. The next cutover's criteria will then be treated as advisory too, which is how the whole mechanism stops working.

## Reference files

- `references/runbook.md` — read while writing the plan: the full runbook and rollback templates, the go/no-go and comms templates, the T-minus schedule, and a worked example of a provider migration window.
- `references/traffic-switching.md` — read when designing the traffic step: DNS and TTL mechanics, resolver and client caching behaviour, weighted and canary shifting on load balancers, service meshes and CDNs, connection draining, and how to verify a shift rather than assume it.
