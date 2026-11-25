---
name: browser-experiment-recovery
description: Use after Browser Action errors involving stale contracts, unknown outcomes, busy ownership, stale sessions, interrupted jobs, cancellation, or close ordering. Do not use to bypass validation or retry consequential operations blindly.
---

# Browser experiment recovery

Load `browser-action-protocol` with this Skill. Recovery is state inspection followed
by the smallest safe action, not generic retry.

## Required reading order

1. Read `docs/retry-matrix.md` for the error class.
2. Read `docs/stale-contract.md` for Skill or operation hash mismatches.
3. Read `docs/busy-and-stale.md` for browser/session ownership problems.
4. Read `docs/cancel-close-order.md` for interrupted work.
5. Read the exact protocol error recovery and operation contracts involved.

## Invariants

- Retry only when `dispatch_started=false` and the correction is deterministic.
- For `outcome=unknown`, inspect session, experiment, stream, and persistent state first.
- Reload exact Skill/docs after stale contract errors; never substitute guessed hashes.
- Busy errors require owner/state resolution, not parallel work.
- Cancel, inspect terminal state, then close.

## Completion standard

State the observed error class, dispatch state, inspected handles, current terminal or
ownership state, safe next action, and whether a retry remains prohibited.
