---
name: verify-landing-queue
description: "Check the landing queue and its path leases against the TLA+ model in verification/landing-queue/. Use when a change touches t3/added/landing/scripts/landing_lib/, before you trust a claim about lease overlap, queue order, one trunk writer, what merges, or recovery after a crash."
---

# Verify the landing queue

`verification/landing-queue/LandingQueue.tla` and the sibling modules beside it are
a hand-written TLA+ model of the landing queue and its path leases. TLC checks the
model inside a stated bound.

TLA+ checks the model. It does not read the Python. A rerun of an unchanged model
passes after a real code regression, with the same state counts. A passing rerun
alone does not show the model matches the current code.

Before a passing run counts, and before `Verified at` moves, compare each affected
action and its helper assumptions with the changed code and update the model to
match. Start from the diff, not from the table. Run `git diff --stat <Verified at>
..HEAD -- t3/added/landing/scripts/landing_lib/` and read every changed function
against its action before you run anything. A function can change behaviour without
moving a transaction boundary and without appearing in the table's right column.

Read every result with the pstack `/statechart` skill. It turns an invariant
violation into the shortest path to it in plain words, and draws the state graph
when nothing breaks. Use it rather than reading `tlc.out` yourself.

## Does my change touch the verified code?

Compare the model and run the check when a change touches any of these, in
`t3/added/landing/scripts/landing_lib/`.

| Code | Actions in the model | Promises |
| --- | --- | --- |
| `leases.py`: `lease_claim`, `lease_renew`, `lease_release`, `lease_widen` | `Claim`, `Renew`, `Release`, `Widen` | P1, P2, P6 |
| `_leases/store.py`: `admission`, `in_flight` | `Clash`, `InFlight` inside every lease write | P1 |
| `_leases/owner.py`: `check_owner`, `raise_floor` | `Stale`, `OwnerAllowed`, `RaiseFloor` | P2 |
| `seam.now` and lease expiry | `ClockTick` | P1, P5b, P6 |
| `_queue/entries.py`: `submit` | `Submit`, `SubmitDuplicate` | P2, P5b |
| `drain.py`: `land` and the `.queue.lock` flock | `DrainStart`, `DrainEnd`, `Crash` | P3a |
| `_queue/entries.py`: `reconcile` | `ReconcileFetch`, `ReconcileAttempt`, `ReconcileLanding` | P3b, P5a, P5c |
| `_queue/entries.py`: `attempt`; `_queue/prs.py`: `build`, `build_line` | `IntegrationReset`, `SettleAlready`, `BounceApply`, `BounceCheck`, `RecordLanding`, `BeginPublish`, `AbandonAttempt`, `SettleLanded`, `RecordCandidate` | P3b, P4, P5 |
| `_queue/entries.py`: `publish` | `Publish`, `PublishRefused` | P3b, P3c |
| `_queue/entries.py`: `settle_landed`, `settle_bounced` | `Landed`, `Bounced` inside every settling action | P4, P5b |
| `_queue/integration.py`: `apply`, `check` | `ApplyRun`, `CheckRun` | P4, P5c |
| `_queue/prs.py`: `ensure_pr` | `OpenPr`, `StorePr` | P4 |
| `_merge/rollup.py`: `absent_since`, `absence_waits` | `AbsenceSeen`, `GraceEnds` | P4 |
| `_merge/required.py`: `request_merge` | `RequestMerge` | P4 |
| `_merge/settle.py`: `take_pr` | `SettleMerged` | P3b, P4 |
| `_merge/settle.py`: `bounce_open_pr` | `BounceOpenPr` | P4, P5b |

These actions stand for an actor and not for our code, so read them when an
assumption about that actor changes.

| Actor | Actions |
| --- | --- |
| The forge | `ChecksPost`, `ChecksFinish`, `HeadMoves`, `ForgeCompletes` |
| Another writer on trunk | `OutsiderPush` |

`ReleaseThenSettle` stands for no code. It is the broken order behind one variant.

The model also leans on helpers. These are `foundation.overlaps`,
`foundation.covered`, `foundation.fingerprint`, and `Store.tx`. It assumes overlap
is intersection over atomic paths, coverage is a subset test, a fingerprint is equal
exactly when a replay carries the same change, and a transaction is all or nothing.
A change to any of them can invalidate a promise without moving a transaction
boundary. So can a change to the values `land.py` passes to these functions.
Message-only changes do not need this comparison.

If the change moves a transaction boundary, adds or removes a `Store.tx()`, adds an
external call between two transactions, or changes when the queue lock is taken,
the model needs updating even when the table does not name the function. Say which
transaction moved.

## Run it

One command, from the repository root:

```sh
python3 skills/landing/scripts/land.py slot -- python3 verification/landing-queue/check.py --scratch-parent <parent>
```

`--scratch-parent` is required and has no default. It takes the machine's scratch
directory, the one a brief or the restaurant's `scratchDir` names. Any existing
writable directory works, so when neither names one, make one with `mktemp -d`
and delete it afterwards. `check.py` creates a new directory under the parent for
each config's TLC state and deletes that directory, by its exact path, when TLC
exits. With the argument missing it prints a usage error naming
`--scratch-parent` and runs nothing.

It runs five base configs and every config in `variants/`, and exits 0 only when
each answers what the model says it should. It prints one row per config with the
states generated, the distinct states found, the deepest level, and the wall time.

Bounds. TLC explores with one worker in breadth-first order. `Depth` is 12 in
`leases.cfg`, 30 in `publish-one.cfg`, 32 in `merge-one.cfg`, 24 in `publish.cfg`,
and 18 in `merge.cfg`. Each variant sets its own depth. The bound is enforced in
`Next`, and there is no `CONSTRAINT`, so no violation is reported past `Depth`.
`leases.cfg`, `publish-one.cfg`, and `merge-one.cfg` run out of new states before
`Depth`. `publish.cfg` and `merge.cfg` stop at it. What is left out is listed in
`verification/landing-queue/README.md` under "What the check does not cover".

A base config must report `holds`. A variant must report `breaks <invariant>` with
the invariant its `EXPECT:` line names. A variant's result counts only while every
base config holds. When a base config breaks, the variants that name the same
invariant may be breaking through that bug rather than through the rule they remove,
and `check.py` cannot tell the difference.

## Tell a real bug from a modelling error

The model is written by hand from the code, so it can describe the design and miss
the code. Before you report a bug, check these in order.

1. Does the model's action match the function the map in the model's header names,
   line for line? A missing guard, a guard in the wrong order, or two transactions
   folded with no reason in the map is a modelling error. Fix the model, then
   re-run.
2. Is the counterexample a sequence the code can really produce? Read each step
   against the function it names. A step the code cannot take is a modelling error.
3. Only then is it a bug in the code. Do not weaken the invariant to make it pass
   and do not change `landing_lib/` to match the model. Write the counterexample as
   a numbered list of steps in the code's words, reproduce it in a throwaway
   repository and store, and file it as `Correctness:` or `Safety:`.

A variant that reports `holds` is a modelling error in the variant. A base config
that reports `breaks` is a finding against the code, or a modelling error, decided
by steps 1 and 2.

## When the change is intended

1. Read the code at the new commit, the action that covers it, and the helper
   assumptions above.
2. Update the action so it still stands for one transaction or one external call,
   or say in the map why a fold cannot change a promise. If a guard moved, move it.
   Keep a check's pass or fail outcome in the model even when the code stops acting
   on it. The failure comes from outside the program, and dropping it deletes the
   case that proves the promise.
3. If a promise changed, update `verification/landing-queue/README.md` and the
   model's promises section together, and add or change a variant in
   `verification/landing-queue/variants/` that shows the new promise failing when
   its check is removed. A promise with no failing variant is unproven and belongs
   in the report as a gap.
4. Run the check. Every base config `holds` and every variant `breaks` its own
   invariant.
5. Move `Verified at` below to the new commit, and only after steps 1 to 4 pass.

## Coverage record

- Model: `verification/landing-queue/LandingQueue.tla` and its sibling modules,
  configs beside it and in `variants/`.
- Runner: `verification/landing-queue/check.py`.
- Verified at: `91251ca92`. Each action was compared with the code at that commit.
- Last full run: 21 runs, every base config held and every variant broke its named
  invariant, in 2m48s through the slot, with the config rows adding up to about
  168 seconds. States generated
  and distinct: leases
  133,513 and 7,714; merge-one 6,140,551 and 816,762; merge 4,570,849 and 898,400;
  publish-one 6,408,995 and 631,184; publish 2,668,895 and 633,592.

Before advancing `Verified at`, compare every affected action and helper assumption
with the changed code. Update the model to reflect changed guards, outcomes, and
transaction boundaries, then run the check. An unchanged model can pass after a code
regression. If the check fails, work through "Tell a real bug from a modelling
error".

For the reverse case, a change to verified code that never updated the model, see
the `/maintain-formal-verification-skill` skill.

## Known limits

The search is bounded, and a pass covers the modelled actions and nothing else. Git
and GitHub are modelled as external actors, along with the clock and other writers
on trunk, so the model holds only as far as those actors behave as its actions say.
The model drifts unless someone compares it with changed code and updates it.
`Verified at` records that comparison. Rerunning an unchanged model cannot detect
drift by itself.
