---
name: a2-key-aggregation
description: Implement/review the A2 scalable winner model using canonical playerKey per WinMode + O(1) aggregated counters & winner counts (no loops over players) for daily/monthly commit→reveal→draw→claim.
---

# A2 Key Aggregation (O(1) Winners)

## When to use
- Touching **reveal**, **draw/VRF callback**, **claim**, **win modes**, or anything that might reintroduce loops over players.
- Adding new win conditions, “order ignored” variants, or changing how pot splits/winner counts are computed.

## Goal (Definition of Done)
- ✅ No unbounded loops over players in draw/claim paths.
- ✅ For every WinMode, contract stores:
  - `playerKey` per player
  - `countByKey` aggregated counter
  - `winningKey` and `winnersCount` computed in O(1)

## Canonical approach

### 1) Canonical keys per mode (computed on reveal)
- Compute `playerKey = keyFn(mode, revealedSequence)` for each supported WinMode.
- Persist:
  - `dailyPlayerKeyByMode[dayId][player][mode] = playerKey`
  - `dailyCountByModeKey[dayId][mode][playerKey]++`
- Emit `DailyKeyRevealed(dayId, player, mode, playerKey)` (or equivalent) for indexability.

### 2) Draw computes winningKey and winnerCount in O(1)
- Build draw result numbers (VRF).
- For each WinMode:
  - `winningKey = keyFn(mode, drawNumbers)`
  - `winnersCount = countByKey[...][winningKey]`
  - Persist `winningKey` and `winnersCount`
  - Emit `DailyWinnersCount(dayId, mode, winningKey, winnersCount)` (or equivalent)

### 3) Claim is a pure comparison + claimed flag
- Read:
  - `playerKey = playerKeyByMode[dayId][msg.sender][mode]`
  - `winningKey = winningKeyByMode[dayId][mode]`
- Require `playerKey == winningKey` else `NOT_WINNER`.
- Require `!claimed[dayId][msg.sender][mode]` else `ALREADY_CLAIMED`.
- Mark claimed then credit/payout (pull-based preferred).

## Key functions (must be canonical & deterministic)
- `MODE_*_EXACT_ORDER`: order matters → `_keyExactOrder(seq)`
- `MODE_*_SET_MATCH`: order ignored but full set match → `_keySetMatch(seq)` (canonical sorted/packed form)
- `MODE_*_K_VALUE_MATCH`: K computed from seq → `_calculateKValue(seq)` then `_keyKValueMatch(k)`

## Weight aggregation (no player loops)
- Any weight system must rely on **aggregates** (e.g., sums/counters by target number/clan), updated at reveal-time (when the revealed sequence is known).
- Never compute weights by iterating revealed players.

## Anti-patterns (forbidden)
- ❌ Reintroducing `revealedPlayers[dayId]` iteration in `draw`, `claim`, or VRF callback.
- ❌ Non-canonical key formats (different packing between reveal and draw).
- ❌ Updating aggregated weights in `applyRelics` when the effect depends on the revealed sequence.

## Testing checklist
- Unit: keyFn outputs stable bytes32 for same input; rejects invalid sequences.
- Unit: `countByKey` increments exactly once per reveal per mode.
- Integration: reveal N players → draw → winnersCount matches expected without iterating players.
- Integration: claim per mode; multi-mode claiming works; double-claim reverts.
- Regression: ensure “no loops over players” remains true (gas snapshot / code review gate).
