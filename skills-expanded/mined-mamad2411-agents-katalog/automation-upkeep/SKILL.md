---
name: automation-upkeep
description: Implement deterministic, idempotent phase automation using Chainlink-style checkUpkeep/performUpkeep for updatePhase/requestDraw/openDay/closeDay, with safe retries and manual fallback.
---

# Automation Upkeep (Deterministic + Idempotent)

## When to use
- Adding/adjusting automated phase transitions, VRF request triggers, or scheduled open/close logic.
- Any time you touch `checkUpkeep`, `performUpkeep`, or “keeper/cron” responsibilities.

## Goal (Definition of Done)
- ✅ `checkUpkeep` is **read-only**, deterministic, and cheap.
- ✅ `performUpkeep` is **idempotent**: repeated calls never corrupt state.
- ✅ Automation is optional: manual public functions still allow progress.

## Canonical actions (encoded in performData)
Define a small action enum + payload:
- `ADVANCE_PHASE(dayId)`
- `REQUEST_DRAW(scope, id)`
- `OPEN_DAY(nextDayId)`
- `CLOSE_DAY(dayId)`

`checkUpkeep` returns:
- `upkeepNeeded` boolean
- `performData = abi.encode(action, params...)`

## Deterministic checks (checkUpkeep)
- Only use on-chain state + timestamps/deadlines stored on-chain.
- Never call external systems or random sources.
- Never depend on mempool, “latest blockhash”, off-chain price, etc.

## Idempotent execution (performUpkeep)
- Decode performData.
- Re-check preconditions:
  - correct phase
  - deadline passed
  - draw not already requested
  - day not already opened/closed
- Execute 1 action max per call (preferred), emit `UpkeepPerformed(action, id, ok)`.

## Failure behavior
- Fail closed with deterministic revert reasons:
  - `NOT_NEEDED`, `NOT_IN_PHASE`, `ALREADY_REQUESTED`, `ALREADY_OPEN`, etc.
- Never partially update state then revert.

## Security notes
- If keeper role exists, enforce AccessControl; otherwise keep public but safe via phase guards.
- Prefer pull-based payouts; upkeep should not “push funds” to users.

## Testing checklist
- Unit: checkUpkeep true/false on boundary conditions (before/after deadline).
- Integration: performUpkeep advances phase correctly.
- Idempotency: calling performUpkeep twice results in 2nd call being no-op/revert-safe.
- “Stuck” scenarios: VRF pending; ensure automation does not spam requests.
