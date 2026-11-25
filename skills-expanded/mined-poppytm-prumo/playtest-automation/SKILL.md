# Playtest Automation

## Purpose
Drive games with deterministic, replayable input sequences and inspect runtime state as evidence: scripted bot traversals, seeded RNG runs, screenshot and telemetry capture, and crash/hang detection across full playthroughs without human hands on the controller.

## Use when
- Regression-testing full levels or quest chains with recorded input replays that must reproduce exact outcomes.
- Soaking builds for crashes, hangs, memory growth, or stuck-bot states over multi-hour unattended runs.
- Collecting gameplay telemetry (completion times, death heatmaps, economy balances) from scripted bot cohorts.
- Verifying difficulty, pacing, or spawn logic changes against a stable bot baseline before human playtests.

## Do not use when
- Asserting pixel-level UI focus, safe areas, or localization correctness frame by frame (use `game-ui-testing`).
- Proving physics bitwise determinism or collision-matrix correctness (use `physics-testing`).
- Measuring netcode behavior under latency, loss, or reconnect drills (use `multiplayer-networking`).

## Required context
- Playable build with automation hooks: synthetic input injection, time-scale control, and state-query API (positions, quest flags, RNG state).
- Bot behavior set: waypoint routes, combat policies, and stuck-detection heuristics for the levels under test.
- Determinism controls: fixed timestep, seeded RNG streams, and recorded input log format with versioning.
- Pass/fail oracles: expected completion windows, telemetry thresholds, and crash/hang definitions (e.g., no progress for 90 s equals stuck).

## Procedure
1. **Instrument the build**: Enable headless or time-scaled mode (`--playtest-headless --timescale 4`), expose `/state` query endpoint (player position, quest flags, RNG seed), and verify input injection latency stays below one tick.
2. **Record golden input sequences**: Capture a 12-minute designer playthrough of Harbor Approach on seed 4417 as `inputs_harbor_v6.bin` (60 Hz); replay it and assert identical quest-flag timeline and completion time within 2 s before accepting it as golden.
3. **Build the bot cohort**: Script 5 bot archetypes (speeder, explorer, completionist, combat-heavy, idle) over waypoint graphs; run each 10 times and record median completion, death positions, and coin balances into `telemetry/run_2026-09-13.csv`.
4. **Run soak and stuck detection**: Launch a 4-hour unattended soak at timescale 4 with watchdog heartbeats every 5 s; flag stuck when position variance is zero for 90 s or frame production halts for 10 s, capturing a screenshot, state dump, and last 60 s of inputs per incident.
5. **Diff telemetry against baseline**: Compare cohort medians with the previous build using the 5% tolerance rule (completion time, deaths per checkpoint, economy totals); investigate any metric breaching tolerance as a gameplay regression, not noise.
6. **Archive evidence and verify**: Store input logs, state dumps, screenshots, and telemetry CSVs under `playtest/2026-09-13/` and run `scripts/verify.sh` to confirm artifact completeness.

## Decision rules
- **Golden replays are bitwise-stable or they are not golden**: Any quest-flag or outcome divergence on identical seed invalidates the recording; re-record, never widen tolerance.
- **Stuck detection is mandatory on every run**: No unattended run ships evidence without watchdog heartbeats and stuck incident reports (including zero-incident reports).
- **Telemetry tolerance is 5%**: Cohort median shifts beyond 5% against baseline require a design-signed explanation before merge.
- **Timescale must not change physics**: Runs above timescale 4 require a determinism re-proof; any divergence caps automation at real-time.
- **Screenshots accompany every failure**: A stuck, crash, or oracle failure without screenshot plus state dump is an incomplete report.

## Evidence required
- Golden replay acceptance log: identical quest timeline and completion within 2 s on seed 4417.
- Cohort telemetry CSV (50 runs) with baseline diff report inside 5% tolerance or signed waivers.
- Soak log: 4-hour run with heartbeat record and per-incident screenshot plus state dump.
- Completed `templates/playtest-automation-spec.md` with routes, seeds, and verdicts.
- Passing execution log from `scripts/verify.sh`.

## Output contract
- Playtest specification with routes, bot archetypes, seeds, oracles, and verdicts.
- Replayable input logs and bot scripts committed alongside the build under test.
- Telemetry dataset and diff report archived for design review.

## Stop conditions
- Golden replays reproduce exactly and the cohort completes with telemetry inside tolerance.
- Soak finishes with zero unexplained stuck or crash incidents (all incidents root-caused or fixed).
- Token budget exhausted.
- Blocked on external dependency.

## Escalation rules
- Escalate to design when telemetry shifts beyond 5% look intentional (rebalance) rather than accidental; never silently re-baseline.
- Escalate to engine owners when determinism breaks between identical automation runs (RNG stream leak, unordered updates).
- Escalate immediately on crashes with memory corruption, GPU hangs, or save-data loss signatures.
