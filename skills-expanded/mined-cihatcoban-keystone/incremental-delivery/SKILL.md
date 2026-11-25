---
name: incremental-delivery
description: Implements a planned task in thin vertical slices that each leave the system shippable, behind flags where needed. Triggers - implement the next task from the plan, start coding, how do I land this big change safely, should this go behind a feature flag, long-lived branch.
---

# Incremental Delivery

The failure this prevents: a three-week branch that touches 60 files, cannot be
reviewed meaningfully, conflicts with everything, and is discovered to be wrong
only at the end. Incremental delivery trades a small amount of scaffolding for
the ability to stop, redirect or ship at any moment.

## The loop

```text
pick slice → failing test → minimal code → green → clean up → full suite → commit
     ↑                                                                       │
     └───────────────────────────────────────────────────────────────────────┘
```

One behavior per pass. The system is releasable after every pass — incomplete
features are hidden behind a flag, not left half-wired.

## What a slice looks like

| Not a slice | A slice |
|---|---|
| "The persistence layer" | "Saving one entity, with its uniqueness rule, verified by a test" |
| "Error handling" | "Timeouts on the payment call return 503 and log once" |
| "The settings page" | "The one setting that matters, end to end, behind a flag" |

A slice crosses layers and produces observable behavior. If it produces only
structure, it is not a slice — and structure without a consumer is usually the
wrong structure.

## Rules

1. **See the test fail first.** A test that has never been red proves nothing;
   it may be asserting on the wrong thing entirely.
2. **Commit only green.** The mainline is always releasable. Work in progress
   lives behind a flag, not in a broken build.
3. **Resist scope.** A defect spotted outside the slice gets an issue, not a
   fix in this diff. Mixed-purpose diffs are the main cause of unreviewable PRs.
4. **Keep PRs under ~400 changed lines.** Review quality falls off a cliff past
   that; above it, reviewers approve rather than review.
5. **Structural and behavioral changes never share a commit.** Rename *or*
   change logic. A diff that does both is impossible to read — the reviewer
   cannot tell what moved from what changed.
6. **Integrate at least daily.** Long-lived branches are deferred integration
   risk, priced with interest.

## Feature flags

Anything user-visible or behavior-changing ships behind a flag, default off.

- Name it for the capability, not the ticket: `checkout.express_pay`.
- Check the flag in **one** place, as close to the entry point as possible.
  Flag checks sprinkled through the code are a combinatorial test problem.
- Record the removal condition when you create it: what makes it permanent,
  and who deletes it. **Flag removal is a task in the plan, not good intentions.**
- Flags are release toggles, not permanent configuration. A flag older than one
  or two release cycles is technical debt — an untested code path pretending to
  be a feature.

## Changing behavior that already exists

Never edit in place. Expand → migrate → contract:

1. **Expand** — add the new path alongside the old; nothing switches yet.
2. **Migrate** — route traffic to the new path progressively, ideally with
   **shadow comparison**: run both, serve the old, log the differences. The
   difference log is the evidence the new path is correct.
3. **Contract** — once the difference log is clean for a full cycle, delete
   the old path.

Each phase is its own deploy and its own PR. This applies to data, APIs and
internal logic alike.

## Stopping conditions

Stop and report rather than pushing through when:

- The slice turns out several times larger than planned — the decomposition was
  wrong; fix the plan, not the estimate
- The change requires an irreversible action (data deletion, destructive
  migration, external write)
- There is no way to test what you are about to write — usually a design
  problem, not a testing problem
- A `CONSTRAINTS.md` threshold blocks you — the threshold is not the obstacle,
  the change is

## Exit checklist

- [ ] Each commit is green, one logical change, with its test
- [ ] No structural and behavioral change mixed in the same commit
- [ ] Incomplete behavior sits behind a flag defaulting to off
- [ ] Flag has a named removal condition and a task
- [ ] Behavior changes use expand/migrate/contract, not in-place edits
- [ ] Full suite run before the final commit, not just the focused test
- [ ] Anything deferred is written down as an issue, not carried in your head
