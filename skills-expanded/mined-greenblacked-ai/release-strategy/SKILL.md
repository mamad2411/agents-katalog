---
name: release-strategy
description: "Get a change into production gradually, so that being wrong costs a fraction of users rather than all of them — separate deploy from release, choose the mechanism (feature flag, percentage or ring rollout, blue/green, shadow traffic) from how the change fails, design rings and bake times that cross a full traffic cycle, write promotion gates and guardrails as numbers agreed before it starts, automate the rollback signal, and give every flag a removal date and an owner. Use this skill whenever someone is planning a canary, a staged, ring or percentage rollout, a feature flag or dark launch, a kill switch, or an experiment's guardrails — including phrasings like \"how do we ship this safely\", \"what percent should we start at\", \"how long do we bake before promoting\", or \"can we flag this off\". Not for a hard-to-reverse one-off switchover, a multi-phase platform migration, a red pipeline, a live incident, or a shipped mobile binary (mobile-release)."
allowed-tools: "Read, Write, Edit, Grep, Glob, Bash(kubectl:*), Bash(gh:*), Bash(git:*)"
---

# Release Strategy

A rollout is designed well when the worst plausible outcome is a small, named group of users having a bad few minutes, and the response to it is one person flipping one switch without a build.

The thing teams get wrong is treating deploy and release as one event. Code reaches production and is simultaneously live for everyone, so the only recovery is another deploy, which takes as long as the pipeline takes, and the decision to start it is made while the graph is still ambiguous. From there the failures are predictable. A canary gets 5% of traffic for five minutes, which is not long enough to cross a cache warm-up let alone a daily cycle, and the promotion happens because nothing obviously broke. The rollout is judged on the metric that motivated the change — conversion is up, latency is down — with no guardrail watching the things the change was never meant to touch. And the flags accumulate: dozens of them, each a permanent untested branch in production, until people stop trusting the system that was supposed to make releases safe. The procedure below is built to make each of those hard to do by accident.

## Scope

Use for: choosing between a feature flag, a percentage or ring rollout, blue/green and shadow traffic for a specific change; designing the rings, bake times and promotion gates; picking guardrail metrics and the automated rollback signal; adding a kill switch to a risky dependency or an expensive path; auditing a flag estate and removing what should have gone months ago; deciding what result would stop a rollout, before it starts.

Do not use for: a hard-to-reverse one-off switchover with a point of no return — a DNS flip, a region move, a provider swap — which is `cutover`; planning a multi-phase platform or tooling migration, which is `plan-platform-migration`; the schema change underneath a feature, which is `db-migration`; a broken pipeline, which is `ci-triage`; an incident happening now, which is `incident-response`, or `k8s-triage` for a Kubernetes workload; or a shipped iOS or Android binary, which cannot be recalled the way a flag or percentage can — that is `mobile-release`, which owns the app store's own rollout and a rejection.

## Deploy is not release

Separating them is the whole idea. Deploying puts the artefact on the machines; releasing decides who executes the new path. Once they are separate:

- Rollback is a runtime decision measured in seconds, not a pipeline run measured in minutes. That difference is the entire value proposition, and it is what lets a team act on an ambiguous signal early instead of waiting for certainty.
- The person who decides to release does not need to be the person who can deploy, so the decision can happen at a sensible hour with the right people watching.
- Code can ship dark for days, merged and exercised in production paths, which removes the long-lived branch that would otherwise be the actual risk.

The cost is real: two code paths exist at once, both have to work, and the number of live combinations grows with the number of flags. That cost is why the removal date in step 7 is not optional bookkeeping.

## Choosing the mechanism

Pick from how the change fails, not from what the team used last time.

| Mechanism | Fits a change whose | What it costs | Rollback |
| --- | --- | --- | --- |
| **Feature flag** | behaviour you want to toggle per user, tenant or plan, or turn off independently of deploys | Branching complexity in the code, and cleanup debt if the removal date is not enforced | Flip, seconds |
| **Percentage or ring rollout** | failure is statistical — a latency regression, an error-rate rise, a small fraction of requests hitting a new path | Needs enough traffic per ring for the metrics to mean anything, and a promotion process someone runs | Reduce the percentage, seconds to minutes |
| **Blue/green** | failure is all-or-nothing at the infrastructure level: a runtime upgrade, a base image change, a config-shaped rewrite | Double capacity for the overlap, and a plan for state that both sides share | Swap back, minutes, provided the old side is still warm |
| **Shadow or mirrored traffic** | correctness you want to compare rather than trust — a rewrite of a pricing engine, a search ranker, a parser | A plan for side effects: shadow requests must not write, charge, email or emit. This is the part people get wrong | Nothing to roll back; the shadow never served a user |

They combine. A common shape is blue/green for the platform underneath, with flags and percentage rollouts for behaviour above it. A rewrite often runs shadow first to establish correctness, then a ring rollout to establish performance under real load.

## Workflow

### 1. State what would make you stop, before you start

Write the stopping condition down first, while the change is still hypothetical and nobody is invested in it. "We roll back if checkout error rate exceeds 0.5% in the canary cohort for two consecutive minutes, or if p99 latency in the cohort is more than 20% above control." Decided during the rollout, with a partial graph and the author in the room, that number is always more generous than it should be.

The same applies to the success side: name the result that justifies promotion, so that promoting is an observation rather than a mood.

### 2. Design the rings

Order the population by how fast it tells you and how much it forgives.

| Ring | Population | What it catches | Typical bake |
| --- | --- | --- | --- |
| 0 | The team, internal staff, synthetic traffic | Crashes, obvious breakage, missing config | Hours, or one working day |
| 1 | A low-risk tenant cohort: free tier, internal customers, a single small region | Real-user behaviour the team does not exhibit, integration surprises | One full traffic cycle, usually 24 hours |
| 2 | 1-5% of general traffic | Statistical regressions: error rate, latency tail, resource use | 24 hours, crossing a peak |
| 3 | 25%, then 50% | Capacity and contention effects that only appear at scale — connection pools, cache hit rates, downstream quota | 24 hours minimum |
| 4 | 100% | Nothing new. This ring is the decision to stop watching | Watch through one more cycle before removing the flag |

Two things decide whether the rings are real:

**The bake time has to cross a full cycle.** Traffic, cache state, cron jobs, batch runs, the daily peak and the weekly one all change what the code does. Five minutes at 3% catches only the failures that would have been caught by a smoke test. If the change touches anything with a daily rhythm, the minimum useful bake is 24 hours; if it touches a weekly batch, the bake spans that batch or the batch is a separate ring.

**Ring assignment must be sticky.** Hash the user, tenant or session id, not the request, so a given user sees one consistent behaviour. A user flipping between old and new on every request produces broken sessions, unusable metrics, and support tickets nobody can reproduce.

Where the rings are also regions, remember that a ring boundary that follows a failure domain gives you a second benefit: a bad release cannot take out more than one domain at a time.

### 3. Write the promotion gate as a metric

A gate is a comparison against a number, evaluated on the cohort, over the bake window. Anything else is a feeling.

```text
Promote ring 2 -> ring 3 when, over the trailing 24h and at least 50k canary requests:
  canary 5xx rate            <= control 5xx rate + 0.1pp
  canary p99 latency         <= control p99 * 1.10
  canary checkout completion >= control completion - 0.5pp
  no new error signature in the canary above 10 events/hour
Otherwise: hold, or roll back if any guardrail is breached for 10 minutes.
```

Compare against a concurrent control, not against yesterday. Yesterday differs from today for a dozen reasons that have nothing to do with the release, and half of a bad rollout's early ambiguity comes from arguing about which of them it was.

State the minimum sample too. At 3% of a low-traffic service, a 24-hour window may still contain too few events to distinguish a 0.5pp regression from noise — in which case increase the percentage rather than pretending the gate passed.

### 4. Wire the guardrails, not just the headline metric

The metric that motivated the change will improve; that is why someone built it. The rollout is judged on what it was not supposed to touch.

- **Service guardrails**: error rate, latency tail, saturation, dependency error rates, queue depth downstream.
- **Business guardrails**: the conversion or completion step immediately downstream of the change, revenue per session, support contact rate.
- **Cost guardrails**: request volume to metered dependencies, egress, per-request compute. A change that improves latency by calling a paid API three times per request is a regression somebody else will find.
- **Per-cohort, always.** A guardrail computed over all traffic is diluted by the 97% not in the canary, and a real regression in the canary will hide inside it until it is far too late.

### 5. Automate the rollback, and be honest about the signal

Automating the rollback removes the worst variable, which is a human deciding whether a graph is bad enough while under pressure. Tie it to an SLO burn-rate or error-budget signal and let it act without asking.

The caveat is that an automated rollback is only as good as its signal. A signal that is slow (a 30-minute window) rolls back long after the damage; a signal that is not specific (overall error rate, all traffic) fires on unrelated incidents and flaps, and a rollback that flaps trains people to disable it. Requirements for a signal worth automating on:

- Fast: a window measured in minutes, with a short confirmation window so it clears on recovery.
- Cohort-scoped: computed on the canary population, compared with control.
- Specific: attributable to this change rather than to any bad thing happening anywhere.
- Tested: trigger it deliberately once, in a low ring, and confirm the rollback executes.

`alert-design` has the multiwindow multi-burn-rate construction that gives a signal both speed and stability; use the same shape here rather than inventing a threshold.

If no signal meets those requirements, say so and use a human gate with a named watcher and an explicit watch period. A human gate honestly labelled beats an automated one that nobody trusts.

### 6. Know what progressive delivery does not cover

Some changes cannot be made safe by fractioning traffic, and pretending otherwise is where the outages come from.

- **Schema changes.** A flag does not roll back a migration. The change is expand, backfill, migrate reads, migrate writes, contract, each step independently revertible — that is `db-migration`. A read-path flag can sit inside the expand phase, but the flag must not outlive the contract, or you have a flag whose off-path references a dropped column.
- **Irreversible side effects.** A payment taken, an email or push sent, a webhook delivered, a record deleted, a message published to a topic others consume. Fractioning traffic changes how many of these you cannot undo, not whether you can undo them. Guard them with idempotency keys, a dry-run mode, and a small explicit cohort — never a percentage nobody is counting.
- **Changes to the flag system itself.** The rollout mechanism cannot roll out its own change, and a flag service failing closed while a critical flag defaults off is a self-inflicted outage. Define the default value for every flag as the safe behaviour when the flag service is unreachable, and test that path.
- **Changes that are only safe as a set.** Two flags that must flip together are one flag with two effects. Split them and you get a production state nobody designed.

### 7. Give every flag a removal date and an owner

A flag is a branch in production. Both sides are live, only one is exercised by most traffic, and after a few weeks nobody tests the other. Left alone, flags accumulate until the combination space is untestable and the codebase has an invisible second architecture inside it.

The rule that works: every flag is created with a type, an owner and a removal date, and the removal is a ticket that exists from day one rather than one someone remembers to file.

| Flag type | Expected lifetime | Removal |
| --- | --- | --- |
| Release flag (rolling a change out) | Days to weeks | Removed as soon as the change is at 100% and has baked. This is the majority |
| Experiment flag | The length of the experiment | Removed when the experiment concludes, whichever way it concluded |
| Operational flag or kill switch | Long-lived by design | Kept, but reviewed and exercised on a schedule (step 8) |
| Permission or entitlement flag | Permanent | Not a feature flag. Move it into the authorisation model where it belongs |

Enforce it visibly: a stale-flag report in the sprint, a linter or scheduled job that opens a ticket when a release flag passes its date, and a removal step in the rollout's own definition of done. Skipping this is not free — the cost lands as a production incident caused by the untested side of a two-year-old flag that somebody finally flipped, and after that the team's answer to "should we flag this" becomes no.

`references/flag-hygiene.md` has the flag naming convention, the default-value rules for a flag service outage, the audit procedure for an existing estate, and the removal pull-request shape. Read it when adding flags to a codebase that already has many.

### 8. Kill switches are a different thing

A kill switch is not an experiment flag. It exists to shed a dependency, a feature or an expensive path during an incident, and its requirements are different:

- **Few, and well known.** A handful across the whole system, listed where on-call can find them in seconds. Fifty kill switches is zero kill switches, because nobody can pick one under pressure.
- **Reachable when the thing they protect is down.** A switch stored in the database it protects, or served by the service it disables, is not a switch. Config in a separate control plane, cached locally, failing to the safe value.
- **Exercised.** A switch that has never been pulled is a hypothesis. Pull each one in a low ring or a game day at least once, and record how long it took to take effect — propagation delay is the number on-call needs and the one nobody measures.
- **Owned, with a documented blast radius**: what stops working when it is pulled, and what the user sees.

### 9. Measure the rollout, then close it out

Watching a dashboard is not measurement. Record the comparison at each promotion — cohort, sample size, each gate metric against control, and the decision — so the rollout has a record that survives the people who ran it.

Closing out means: at 100%, flag removed by its date, dead code path deleted, the record attached to the change, and the guardrail dashboards either retired or promoted into permanent monitoring.

## Output format

```markdown
## Change
[What is changing, and how it fails — which decides the mechanism.]

## Mechanism
[Flag / percentage / ring / blue-green / shadow, and why this one for this failure mode.]

## Rings and bake times
| Ring | Population | Bake | Promotion gate |
[Sticky assignment key named. Bake times crossing a full traffic cycle.]

## Guardrails
[Per-cohort service, business and cost metrics, each with the threshold that holds them.]

## Rollback
Trigger:   [signal, window, threshold — or the named human gate and watcher]
Mechanism: [flag flip / percentage reduction / swap back]
Tested:    [when the rollback was last exercised, and how long it took]

## Stop condition
[The result agreed in advance that ends the rollout, written before it started.]

## Flag lifecycle
Name / type / owner / removal date / removal ticket.

## Out of scope
[Schema changes, irreversible side effects and anything else this rollout does not make
safe — named, so nobody assumes coverage that does not exist.]
```

## Anti-patterns

**Deploying to everyone and watching a dashboard.** The blast radius is every user, the recovery is a full pipeline run, and the decision to start it is taken while the graph is still ambiguous. Every minute of that ambiguity is a minute of full-population impact, which is exactly the cost that a 1% ring removes for almost nothing.

**A canary with no promotion gate.** Traffic goes to 5%, somebody glances at a graph, and it goes to 100% because nothing obviously broke. Absence of an obvious break is not evidence: it is what a 0.3pp conversion regression looks like on a chart with the wrong y-axis. Write the comparison against control, with a minimum sample, before the canary starts.

**Bake times measured in minutes.** Five minutes at 3% crosses no cache warm-up, no cron run, no daily peak. It catches the failures a smoke test already catches, and the ones it misses are precisely the ones that make a rollout worth doing. Cross a cycle or admit the rollout is ceremonial.

**Flags with no removal date.** Each one is a permanent untested branch in production. The estate compounds silently until the combination space is beyond testing, and the eventual incident — caused by the off-path of a flag nobody has exercised since it was written — is what convinces the organisation that flags are dangerous, which loses you the mechanism entirely.

**A flag wrapped around a migration.** The flag flips back; the dropped column does not come back. Reversibility for schema lives in the expand/contract sequence, one revertible deploy per phase. A flag may sit inside a phase, never across one.

**A kill switch that has never been pulled.** Discovering during an incident that the switch requires a deploy, or reads its state from the database that is currently down, converts your mitigation into a second incident. Pull each switch on purpose, on a schedule, and record the propagation delay.

**Judging a rollout on the metric that motivated it and no guardrail.** The metric someone built the change to improve will improve. The rollout's real question is what else moved — the checkout step downstream, the dependency's error rate, the per-request cost — and without per-cohort guardrails that answer arrives weeks later, from someone else, as a mystery.

**One rollout, several unrelated changes.** When the guardrail moves, nothing identifies which change moved it, so the response is to roll back everything and re-derive from scratch. Ship one behavioural change per rollout, even when they share a deploy.

## Reference files

- `references/rollout-mechanics.md` — read when implementing the mechanism: sticky bucketing and the hash key that makes it stable, traffic splitting on a load balancer, ingress and service mesh, blue/green with warm capacity and shared state, shadow traffic and side-effect suppression, and the automated analysis shape used by Argo Rollouts and Flagger.
- `references/flag-hygiene.md` — read when adding flags to a codebase that already has many, or auditing an estate: naming and typing conventions, default values for a flag-service outage, the stale-flag audit and its queries, the removal pull request, and how kill switches are stored and exercised.
