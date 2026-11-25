# Realtime Synchronization

## Purpose
Implement deterministic multiplayer synchronization with fixed tick rates, lockstep or rollback netcode, snapshot interpolation, jitter buffering, and reconnect resync, verified under measured RTT, jitter, and packet loss.

## Use when
- Building lockstep simulation, GGPO-style rollback, or snapshot-interpolation state sync for multiplayer games.
- Choosing tick rates, input delay, prediction windows, or snapshot cadence for a networked game.
- Implementing reconnect, resync, host migration, or late-join flows.
- Diagnosing desyncs, rubber-banding, mispredict storms, or clock drift between peers.

## Do not use when
- Simulating packet loss, latency, or partitions without changing sync logic (use `network-testing`).
- Defining wire encodings for packets without sync semantics (use `serialization`).
- Measuring web page performance without realtime state (use `performance-web`).

## Required context
- Topology: client-server authoritative versus peer-to-peer lockstep, player count, spectator support.
- Network budget: target RTT in milliseconds, jitter, acceptable packet loss (for example 80 ms RTT, 15 ms jitter, 1 percent loss).
- Simulation spec: tick rate, input size in bytes, snapshot size, determinism requirements (fixed-point versus float).
- Platform clocks: NTP availability, monotonic timer resolution, render frame rate versus tick rate.

## Procedure
1. **Fix the timeline first**: set server tick rate (20 Hz for shooters, 10 Hz for strategy), decouple render frames from ticks with an accumulator, use integer tick IDs as the single source of time, and drive all gameplay from tick-indexed state.
2. **Choose the sync model deliberately**: lockstep with input delay for deterministic 2–4 player strategy; rollback with prediction up to 8 frames for fighting and platform fighters; server-authoritative snapshot interpolation at 10–20 Hz snapshots for shooters and battle royale.
3. **Implement prediction, reconciliation, and interpolation**: predict local inputs immediately, reconcile against authoritative snapshots within 100 ms, interpolate remote entities over a 100 ms jitter buffer, and never extrapolate beyond 250 ms without snapping or freezing.
4. **Harden determinism and bandwidth**: use fixed-point or quantized floats for simulated state, hash state per tick (for example FNV-1a over positions) and compare across peers to detect desync within 5 ticks, delta-compress snapshots, and cap per-client downstream at 64 kbps.
5. **Build reconnect and resync**: snapshot full state every 30 ticks, allow late-join download plus input-log catch-up, support 10-second reconnect grace with resync, and migrate host authority with a 5-second election timeout.
6. **Verify under real network profiles**: run 4-player soak with 80 ms RTT, 15 ms jitter, 1 percent loss via netem, assert zero desyncs over 30 minutes, mispredict rate under 5 percent, then execute scripts/verify.sh from the repo root.

## Decision rules
- **Authoritative truth lives in one place**: clients predict for feel but the server tick decides hits, deaths, and scores.
- **Determinism is tested, not assumed**: per-tick state hashes compared across peers in CI; float math in simulation is guilty until proven innocent.
- **Never extrapolate blind**: past 250 ms without authoritative data, freeze or snap with a visual cue instead of hallucinating positions.
- **Bandwidth is a budget**: per-client downstream capped at 64 kbps; exceeding snapshots shed detail (LOD) before shedding players.
- **Desyncs are fatal and logged**: any state-hash divergence halts the match path into resync with a full diagnostic dump, never silently continues.

## Evidence required
- Tick configuration and sync-model decision record with RTT and bandwidth math.
- Soak test logs: 4 players, 30 minutes, 80 ms RTT with jitter and loss, zero desyncs.
- Mispredict rate, snapshot size, and bandwidth measurements against budget.
- Passing execution log from scripts/verify.sh.

## Output contract
- Tick-driven sync implementation with prediction, reconciliation, interpolation, and resync.
- Determinism harness with per-tick hashes and desync diagnostics.
- Network-profile test evidence meeting the stated loss and latency budgets.

## Stop conditions
- Sync model implemented with zero desyncs over the 30-minute soak and mispredicts under 5 percent.
- Player count or RTT target changes invalidate the chosen model and need re-decision.
- Token budget exhausted.
- Blocked on external dependency.

## Escalation rules
- Escalate to Lead Architect if determinism is unachievable with float physics and a fixed-point rewrite is required.
- Escalate to network-testing owner if measured player RTT distributions exceed the design budget persistently.
