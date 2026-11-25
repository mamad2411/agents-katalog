---
name: tw-number-vet
description: "a speedup, a regression, a throughput, a latency or an eval result is about to be reported, recorded in a decision, or used to justify a change"
kind: workflow
---

# tw-number-vet

Owner role: **reviewer** (created by CEO on 2026-11-18).

Related: [tw-decision-first](../tw-decision-first/SKILL.md) - that skill produces
the number, this one vets it before it leaves the machine.

Use this skill when: a measured number is about to leave the machine - a
before/after in a self-check note, a regression in a review finding, a baseline in
`docs/Team/Throughput.md`, a speedup in a PR body, or an eval result that decides
which variant ships. It is the working form of R13 in `docs/Team/Research.md` 6.4,
taken from pstack's benchmark checklist.

## Why this exists

The cheapest false claim the team can record is a number. A warm cache, a debug
build on one side, or work that never ran inside the timed region each produce a
convincing speedup, and none of them fails a gate: the record looks like evidence
(`strong`, a digest, a range) and a reviewer who re-runs it reproduces the same
wrong number. The vet is what turns a measurement into a claim.

## Budget

- 5 minutes for a ballpark the user asked for: one run, questions 4 and 7 only,
  and say that it is one run.
- 20 minutes for a number that lands in a record, a finding or a decision.
- 45 minutes for a harness that will be frozen, or a choice between options.
- Stop when the run-to-run spread is larger than the effect: the verdict is then
  `no measurable difference`, and more runs do not help.

## Steps

1. **Write the claim first, in the words it would ship.** "export is 30% faster at
   p50 on the 60k-row fixture". The questions below test that sentence, so a claim
   that cannot be written down is not ready to measure.
2. **Read the harness.** What does it time, count and ignore? Check the machine
   with `uptime` and `nproc`. If it is busy and cannot be quiet, interleave the
   sides so both see the same noise, and say so.
3. **Answer the seven, each from a run, never from reading the code.**
   1. *Why not double?* Name the limiter from a profile taken in a run you do not
      report. If a change did not move the number, the limiter explains why.
   2. *Was every side tuned?* Release build, production flags, same data, as warm
      or cold as production sees it. One side left on defaults compares
      configurations, not implementations.
   3. *Does it break a physical limit?* Do the arithmetic against bandwidth, cores
      or the time the changed piece took. Past a limit means the run measured a
      cache, a no-op or a bug.
   4. *Did it error?* Count failures and check the output is correct, not merely
      present. Rejections are fast; timeouts and retries are slow.
   5. *Does it reproduce?* At least five runs per side, alternating, then median and
      range. A gap smaller than the spread is no measurable difference.
   6. *Does it matter?* Measure the end-to-end path a user waits on, and report the
      micro result as a share of it.
   7. *Did it even happen?* Confirm the work ran inside the timed region: the rows
      were written, the bytes read, the result used.
4. **Report the verdict first.** `faster`, `slower`, `no measurable difference` or
   `inconclusive`, then the number with its unit, the run count, the range and the
   limiter. One primary number per PR body; the runs and the limiter evidence go in
   a linked artifact.
5. **Record it where the gate reads it.** A number in a self-check, a review or a
   `decision add` carries the verdict, the run count, the range and the limiter on
   the same line as the command. A claim that cannot name its limiter is
   `inconclusive`, and an inconclusive number never justifies a change.

## Stop condition

The verdict is one of the four, the limiter is named, and the record carries the
run count and the range - or the verdict is `inconclusive` with the missing
evidence named. A number reported without those is noise, not evidence, and the
reviewer refuses it the same way it refuses "looks good".

## Verdict on this skill

verdict: no observed effect

- Created 2026-11-18 from R13 of the pstack deep read, before any number has been
  vetted with it. Nothing measured yet.
- What would make it `helped`: the next five recorded numbers each carry a verdict,
  a run count, a range and a limiter, and no reviewer finding repeats a claim the
  vet would have refused.
- What would make it `confounded`: a milestone where the numbers are vetted *and*
  the harness or the review profile changed in the same cut.
