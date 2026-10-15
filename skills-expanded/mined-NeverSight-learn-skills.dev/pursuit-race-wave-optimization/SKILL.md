---
name: pursuit-race-wave-optimization
description: |
  Algorithm for optimal wave/bib assignment in pursuit-start races (Verfolgungsrennen)
  where slower athletes start first and everyone aims to finish simultaneously.
  Use when: (1) assigning start waves based on expected performance, (2) optimizing
  lane pairings by similar swim times, (3) minimizing the last finisher's clock time.
  Covers: total-time sorting, distance-scaled expected times, lane-pair optimization,
  and the mathematical proof that current assignment is optimal.
author: Claude Code
version: 1.0.0
date: 2026-03-16
---

# Pursuit Race Wave Optimization

## Problem
In a pursuit start race (Verfolgungsrennen), slower athletes start first so everyone
finishes together. The assignment of athletes to waves and lanes requires optimizing
multiple criteria simultaneously.

## Key Insight: Sort by Total Expected Race Time, Not Swim Time

Sorting only by swim time misses athletes who swim fast but run slow (they should
start earlier despite fast swim). Use **scaled total expected time** as the primary
sort key:

```python
# Contest 1: 1.0km Swim + 8.4km Run
exp_total = swim_s * 1.0 + run_s * 0.84

# Contest 2: 0.5km Swim + 4.2km Run
exp_total = swim_s * 0.5 + run_s * 0.42

# Sort descending: slowest (highest total time) gets lowest bib
sorted_participants = sorted(participants, key=lambda x: x['exp_total'], reverse=True)
```

## Lane Pair Optimization (Minimize Swim Time Difference)

Within each wave, pairs (bib 1+2, 3+4, 5+6...) share a swim lane.
Pair athletes with similar swim times to avoid collisions:

```python
def pair_by_swim(wave_participants):
    # Sort by swim time descending
    by_swim = sorted(wave_participants, key=lambda x: x['swim_s'], reverse=True)

    # Pair adjacent (most similar swim times)
    pairs = []
    for i in range(0, len(by_swim), 2):
        if i + 1 < len(by_swim):
            pairs.append([by_swim[i], by_swim[i+1]])
        else:
            pairs.append([by_swim[i]])  # lone swimmer

    # Sort pairs by avg total time (descending) → slower pairs get lower bibs
    pairs.sort(key=lambda p: sum(x['exp_total'] for x in p) / len(p), reverse=True)

    # Within each pair: slower total time gets lower (odd) bib
    result = []
    for pair in pairs:
        result.extend(sorted(pair, key=lambda x: x['exp_total'], reverse=True))
    return result
```

## Minimizing Last Finish Time: Mathematical Proof

For waves with start times S1 < S2, and max expected times T1, T2:
- Last finish = max(S1 + T1, S2 + T2)
- Since wave gap (S2-S1) is typically 30 min but athlete time range < 30 min,
  **S2 + T2 is ALWAYS the last finish**
- To minimize: put athletes with **smallest T values** in wave 2

This means: current optimal assignment puts fastest athletes (smallest expected time)
in the later wave. Trying to "improve" by moving slower athletes to wave 2 makes it worse.

## Pool Conflict Check

When scheduling waves, verify each wave's swim completes before next wave starts:

```python
def pool_free_time(start_str, wave_participants, contest):
    max_swim_race = max(p['swim_s'] * (1.0 if contest==1 else 0.5)
                        for p in wave_participants)
    h, m = map(int, start_str.split(':'))
    t = datetime(year, month, day, h, m) + timedelta(seconds=max_swim_race)
    return t.strftime("%H:%M")
```

## Expected Finish Time Calculation

```python
from datetime import datetime, timedelta

def finish_uhr(start_str, exp_secs, race_date):
    h, m = map(int, start_str.split(':'))
    t = datetime(race_date.year, race_date.month, race_date.day, h, m)
    return (t + timedelta(seconds=int(exp_secs))).strftime("%H:%M")
```

## Notes
- Wave size constraint: lanes × max_per_lane (e.g., 5 lanes × 2 = 10 per wave)
- With N participants and max 10 per wave: first wave(s) get 10, last gets remainder
- The "pursuit" concept only works when wave gaps ≈ time spread between wave groups
- For Contest 2 with only 17 participants: 10+7 split is forced; current is optimal
- Changing wave start times is the only way to improve beyond mathematical optimum
