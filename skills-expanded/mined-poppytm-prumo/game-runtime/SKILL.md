# Game Runtime Engineering

## Purpose
Implement a stable, deterministic game runtime: fixed-timestep main loop with render interpolation, scene/state management with clean transitions, tick-spiral protection, device-loss handling, and frame-time discipline backed by benchmarks.

## Use when
- Implementing or fixing the main loop, tick accumulator, or render-interpolation logic.
- Adding scene management: loading, transitions, stacking, pause/resume, and state machines.
- Auditing frame-time stability, tick spirals, or determinism of state updates.
- Handling device loss, window resize, suspend/resume, or focus-loss behavior.

## Do not use when
- Designing ECS layouts or subsystem decoupling (use `game-engine-architecture`).
- Building asset cooking or streaming (use `asset-pipeline`).
- Implementing audio mixing internals (use `audio-engineering`).

## Required context
- Main-loop contract: tick rate, accumulator model, and render-interpolation policy.
- Scene inventory: states, transitions, and per-scene update budgets.
- Target frame-time budget and device-loss/resize handling requirements.

## Procedure
1. **Fix the Tick Contract**: Choose a fixed simulation step (e.g., 60 Hz, dt = 1/60 s) and an accumulator loop: `acc += frame_time; while acc >= dt and steps < MAX_STEPS: step(dt); acc -= dt`. Cap `MAX_STEPS` (e.g., 5) and clamp `frame_time` (e.g., ≤ 100 ms) so a hitch degrades gracefully instead of spiraling.
2. **Interpolate Rendering**: Store previous + current simulation state; render at `alpha = acc / dt` between them. Simulation stays deterministic while presentation stays smooth on arbitrary refresh rates. Never render raw extrapolated state without a documented reason.
3. **Manage Scenes Explicitly**: Model scenes as a stack or pushdown state machine with lifecycle hooks (`enter`, `exit`, `pause`, `resume`). Transitions are atomic: load next scene fully (or to a verified checkpoint), then swap; the old scene's resources release only after the swap commits.
4. **Isolate Update Budgets**: Assign per-scene update budgets (e.g., AI ≤ 2 ms, physics ≤ 4 ms at 60 Hz) and assert them in debug builds. Overruns log with scene + system attribution; three consecutive overruns trip a visible warning, never a silent slowdown.
5. **Handle Hostile Environment Events**: On device loss, resize, suspend, or focus loss: pause simulation deterministically, release/recreate GPU resources through the documented path, and resume from the exact paused tick — never by re-seeding or skipping updates.
6. **Verify**: Run `scripts/verify.sh`. Prove determinism (fixed input script → identical state hash at tick N across runs), no tick spiral under injected 250 ms hitches, and scene transitions with zero leaked resources.

## Decision rules
- **Fixed Step, Always**: Variable-dt simulation is forbidden for gameplay/physics; only interpolation may vary.
- **Spiral Guard Mandatory**: Unbounded catch-up stepping is a defect; clamp frame time and cap steps per frame.
- **Atomic Transitions**: Half-loaded scenes are never visible; transitions commit or roll back cleanly.
- **Deterministic Resume**: Suspend/resume and device-loss recovery reproduce the exact paused state, bit for bit.

## Evidence required
- Determinism log: identical state hashes at fixed ticks across repeated runs.
- Hitch-injection test: 250 ms stalls with bounded catch-up and no spiral.
- Scene-transition resource audit: zero leaks across 50 transition cycles.
- Passing execution log from `scripts/verify.sh`.

## Output contract
- Fixed-timestep main loop with interpolated rendering.
- Scene/state management with deterministic transitions.
- Frame-time benchmark evidence with zero-tick-spiral guarantee.

## Stop conditions
- Loop stable at target tick with deterministic scene transitions.
- Hitch and device-loss handling proven without state corruption.
- Token budget exhausted.

## Escalation rules
- Escalate to lead architect if the target device cannot hold the tick budget even with budgets enforced (needs scope or fidelity tradeoff).
- Escalate immediately on nondeterministic state divergence between identical runs (simulation purity defect).
