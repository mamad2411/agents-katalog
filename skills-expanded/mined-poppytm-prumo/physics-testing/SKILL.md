# Physics Testing

## Purpose
Test 2D/3D physics behavior for correctness and determinism: collision layers and masks, trigger volumes, one-way platforms, joints and constraints, continuous collision detection, and fixed-timestep replay determinism with visual debug verification.

## Use when
- Verifying collision layers, masks, and groups route contacts to the right handlers and nowhere else.
- Testing trigger enter/stay/exit semantics, one-way platforms, ladders, and hazard volumes.
- Validating joints, springs, ragdoll constraints, and break-force thresholds under load.
- Proving simulation determinism: identical inputs and fixed timestep reproduce identical trajectories bit-for-bit.
- Auditing tunneling, sleeping-body wakeups, or stacking stability in physics-heavy scenes.

## Do not use when
- Implementing netcode prediction or state replication over physics state (use `multiplayer-networking`).
- Profiling physics solver CPU cost or cache behavior (use `performance-native`).
- Scripting bot playthroughs or input-replay harnesses beyond determinism replay (use `playtest-automation`).

## Required context
- Physics engine and version (e.g., Rapier 0.22, Box2D 3.0, PhysX 5.4, Godot GodotPhysics) with solver iteration counts and gravity vector.
- Fixed timestep contract (e.g., 60 Hz, max 4 substeps, spiral-of-death clamp at 100 ms frame).
- Collision matrix: layer names, mask bits, and intended interaction pairs.
- Determinism scope: float vs fixed-point policy, RNG seed handling, and cross-platform bit-equality requirements.

## Procedure
1. **Lock the timestep contract**: Set fixed `dt = 1/60 s` with an accumulator, clamp catch-up to 4 substeps, and log any spiral-of-death clamp event; assert wall-clock never advances the simulation by a variable delta.
2. **Verify the collision matrix exhaustively**: For every layer pair in the 8-layer matrix (Player, Enemy, Projectile, World, Pickup, Trigger, OneWay, Debris), spawn the pair in contact and assert collision callbacks fire exactly for intended pairs and never for masked-out pairs (64 pair-cases, automated).
3. **Exercise triggers and one-way platforms**: Drive a capsule through trigger volumes asserting enter/exit ordering with no missed exits at 300 px/s; drop through and land back on one-way platforms from above, below, and while holding drop-through input.
4. **Stress joints and fast bodies**: Load a 6-link rope joint chain with a 40 kg weight and assert constraint error stays below 2 cm over 10 s; fire 900 px/s projectiles at 8 px walls with CCD enabled and assert zero tunneling across 1,000 shots.
5. **Prove determinism by replay**: Record 30 s of inputs at 60 Hz with RNG seed 90210, run the simulation twice headless, and assert trajectory hashes (SHA-256 of positions each tick) match exactly; repeat after scene reload to catch static-initialization order bugs.
6. **Inspect debug visualization**: Capture debug-draw frames (contact normals, AABBs, joint anchors) for the failing cases and run `scripts/verify.sh` to confirm artifact completeness.

## Decision rules
- **Fixed timestep is non-negotiable**: Variable-delta physics steps are forbidden in gameplay simulation; visual interpolation covers render smoothness.
- **Masked pairs must be silent**: Any callback from a masked-out layer pair is a blocking defect, not a quirk.
- **Tunneling budget is zero**: Any pass-through of a CCD-enabled body at declared max speed fails the gate.
- **Determinism is bitwise**: Trajectory hashes must match exactly across runs on the same platform; tolerance-based "close enough" replay is rejected.
- **Sleeping bodies must wake**: Any contact, force, or teleport that leaves a sleeping body unresponsive is a P1 defect.

## Evidence required
- Collision-matrix test log: all 64 layer-pair cases with expected vs observed callback counts.
- Joint-load and CCD soak logs with constraint-error and tunneling counts.
- Two headless replay hashes plus post-reload hash, all identical (SHA-256 records).
- Debug-draw captures for investigated failures.
- Completed `templates/physics-testing-spec.md` with matrix and verdicts.
- Passing execution log from `scripts/verify.sh`.

## Output contract
- Physics test specification with collision matrix, timestep contract, and determinism verdicts.
- Automated layer, trigger, joint, CCD, and replay tests in the game's test suite.
- Debug-draw capture set archived with the build under test.

## Stop conditions
- All layer pairs, triggers, joints, and CCD cases pass with bitwise replay determinism proven.
- Zero tunneling events and zero masked-pair callbacks in the verification run.
- Token budget exhausted.
- Blocked on external dependency.

## Escalation rules
- Escalate to the engine owner if determinism breaks across identical runs (solver nondeterminism, unordered contact iteration, or static-init ordering).
- Escalate to design if requested behavior violates physics plausibility (e.g., stacking 40 crates stably at 4 solver iterations).
- Escalate immediately if a physics bug allows out-of-bounds escape or sequence-breaking level skips.
