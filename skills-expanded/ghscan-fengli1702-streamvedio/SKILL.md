---
name: jsd-downfirst-scheduler
description: Use when modifying or validating TREAM Shift JSD-triggered local probing so drift triggers a short down-first latency-oriented search under a quality floor, then compare Dyn(NoJSD) and Dyn+JSD on a small DOH workload slice.
---

# JSD Down-First Scheduler Experiment Skill

Use this workflow when changing the TREAM Shift scheduler so JSD-triggered reroute improves latency under a quality floor, then validating against NoJSD on a small DOH workload slice.

## Goal

Make JSD mean only "the workload distribution changed; run a short local search." Direction is not assumed by JSD itself, but the search should be compressed and latency-oriented:

1. Try a downward local move first.
2. If downward move gives clear latency gain and quality drop is small, commit downward immediately.
3. If downward move gives latency gain but quality drops too much, keep the base config.
4. If downward move gives no meaningful latency gain, try upward local move as fallback.
5. Keep `sla_latency` and `quality_min` explicit in the run log; default baseline is `sla_latency=0.7`, `quality_min=0.2`, but both are tunable.

## Do Not Change First

Before editing scheduler logic:

1. Confirm current run is complete and archive status, manifest, infer logs, scheduler logs, and spec metrics.
2. Commit the current code state with a message that says it is the baseline before JSD down-first changes.
3. Do not mix log archives into the code commit unless explicitly requested.

## Baseline Parameters To Keep Aligned

For the comparison, Dyn(NoJSD) and Dyn+JSD should share all common parameters:

```bash
RUN_MODE=dynamic
RUN_SPEC=1
MAX_FRAMES=4000
IB=32
TB=16
SHIFT_COLD_START_WINDOWS=15
SHIFT_COLD_START_MAX_WINDOWS=15
SHIFT_COLD_PROBE_EVERY=1
SHIFT_COLD_PROBE_EPS_FAST=2
SHIFT_COLD_PROBE_EPS_SLOW=0
SHIFT_COLD_RELAX_SAFETY=1
SHIFT_COLD_WHITELIST_PROBE=1
SHIFT_COLD_WHITELIST_BUDGET=12
SHIFT_COLD_WHITELIST_LAT_SLACK=0.15
SHIFT_COLD_WHITELIST_Q_SLACK=0.60
SHIFT_COLD_WHITELIST_MAX_SWITCH=2
SHIFT_MIN_COUNT_FOR_TRUST=1
SHIFT_ADAPT_PROBE_WINDOWS=0
SHIFT_PRE_JSD_CTX_MIN=2
SHIFT_PRE_JSD_INF_MIN=2
SHIFT_JSD_STAGE_CTX_MIN=1
SHIFT_JSD_STAGE_INF_MIN=1
SHIFT_LOCAL_RELAX_ENABLE=1
SHIFT_LOCAL_RELAX_WINDOWS=3
SHIFT_LOCAL_RELAX_RADIUS=1
SHIFT_LOCAL_RELAX_Q_SLACK=0.05
SHIFT_LOCAL_RELAX_LAT_SLACK=0.08
SHIFT_LOCAL_RELAX_DRIFT_THRESHOLD=0.35
SCHEDULER_QUALITY_MIN=0.2
SHIFT_DEFAULT_QUALITY_MIN=0.2
```

Only these should differ:

```bash
# Dyn(NoJSD)
SHIFT_SHOCK_USE_JSD_ONLY=1
SHIFT_SHOCK_DISABLE_DRIFT=1

# Dyn+JSD
SHIFT_SHOCK_USE_JSD_ONLY=1
SHIFT_SHOCK_DISABLE_DRIFT=0
```

## Code Areas To Inspect

- `tream/scheduler_Shift/core.py`
  - `_maybe_jsd_probe_decision`
  - `_update_jsd_probe_observation`
  - `_jsd_probe_window_score`
  - `_estimated_jsd_probe_score`
  - `_stage_lower_bounds`
- `tream/scheduler_Shift/reroute_policy.py`
  - `LocalReroutePolicy.select_next`
  - quality deficit and latency score ordering
- `tream/actors/scheduler_actor.py`
  - env var wiring for JSD probe, local relax, quality min, stage lower bounds

## Intended Patch Semantics

Implement minimal changes:

1. Initial JSD probe stage starts with `probe_down`, not `probe_up`.
2. Store base/down/up observed latency and quality, not only scalar score.
3. Accept downward probe immediately when:
   - `base_latency - down_latency >= down_latency_gain_eps`
   - `base_quality - down_quality <= down_quality_drop_max`
4. Reject downward probe and hold base when:
   - latency improves enough, but quality drop exceeds `down_quality_drop_max`
5. Try upward probe only when downward latency gain is below threshold or downward candidate is absent.
6. Selection target remains quality-floor-constrained latency, not raw quality maximization.

Recommended initial knobs:

```bash
SHIFT_JSD_PROBE_ENABLE=1
SHIFT_JSD_PROBE_DOWN_FIRST=1
SHIFT_JSD_PROBE_DOWN_LAT_GAIN_EPS=0.03
SHIFT_JSD_PROBE_DOWN_Q_DROP_MAX=0.05
SHIFT_JSD_PROBE_CONTINUE_STEPS=0
```

## Smoke Test

Run 6 diverse DOH cases on two GPUs:

```text
A01 (1,1), A08 (2,4), B03 (4,4), C04 (8,2), C06 (8,3), F08 (7,7)
```

Run both groups with the same case list:

1. Dyn(NoJSD): `SHIFT_SHOCK_DISABLE_DRIFT=1`
2. Dyn+JSD: `SHIFT_SHOCK_DISABLE_DRIFT=0`

## Acceptance Criteria

JSD should show clear advantage on medium/large workloads, not necessarily on A01:

1. For `B03/C04/C06/F08`, JSD mean latency should be lower than NoJSD on most cases.
2. Mean JSD accuracy drop on the 6-case set should stay within roughly `0.03` unless explicitly trading accuracy for speed.
3. Scheduler logs should show JSD-triggered down-first decisions before any upward fallback.
4. If JSD triggers but `safe_set_size <= 1` repeatedly, analyze safety/trust/margin constraints before changing thresholds.

## Proposed Future Change: Down-First Gray-Zone Up Probe

Status: proposed only. Do not apply during an active batch because the running launcher bind-mounts this source tree and later case launches may import changed code.

Observed issue:

The current down-first rule uses a single `down_quality_drop_max` threshold. After a `jsd_probe_down`, if downward movement gives enough latency gain but quality drop exceeds the threshold, the current implementation can commit back to base without trying `probe_up`. That is safe, but it can miss cases where down is too lossy while up would be a better local response to the same JSD drift.

Current behavior:

```text
probe_down
if latency_gain >= down_latency_gain_eps:
    if quality_drop <= down_quality_drop_max:
        commit_down
    else:
        commit_base
else:
    probe_up
```

Proposed behavior:

```text
probe_down
if latency_gain >= down_latency_gain_eps and quality_drop <= hard_accept_quality_drop:
    commit_down
elif latency_gain >= down_latency_gain_eps and quality_drop <= gray_zone_quality_drop:
    probe_up
elif latency_gain >= down_latency_gain_eps:
    commit_base or probe_up, depending on safety policy
else:
    probe_up
```

Recommended initial thresholds:

```bash
SHIFT_JSD_PROBE_DOWN_LAT_GAIN_EPS=0.03
SHIFT_JSD_PROBE_DOWN_Q_DROP_HARD_ACCEPT=0.03
SHIFT_JSD_PROBE_DOWN_Q_DROP_GRAY=0.08
```

Rationale:

- `quality_drop <= 0.03`: accept down directly because latency improves and accuracy loss is small.
- `0.03 < quality_drop <= 0.08`: do not accept down yet; run `probe_up` to confirm whether the other direction is better.
- `quality_drop > 0.08`: treat down as too lossy; prefer base unless a follow-up up-probe policy is explicitly enabled.

Evidence from the 6-case down-first smoke:

```text
jsd_probe_down:   27
jsd_probe_up:      4
jsd_probe_commit: 29
```

Most accepted down probes had negative quality drop, meaning accuracy improved after moving down. Several rejected probes were around `quality_drop ~= 0.055`, which suggests a gray-zone policy is better than simply tightening `down_quality_drop_max` to `0.03`.

Expected impact:

- Keeps the useful latency-first down bias.
- Avoids accepting down moves that eat too much quality.
- Gives JSD a chance to test the opposite direction when the down move is ambiguous instead of prematurely returning to base.
