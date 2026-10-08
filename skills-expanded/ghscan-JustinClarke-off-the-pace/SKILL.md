---
title: "Isolating corner technique from car performance"
sidebarTitle: "Corner-Phase Skill"
description: "A driver skill index built from braking, mid-corner, and exit deviations relative to each driver's own car baseline so a fast car can't flatter a driver."
---

Raw corner speeds mix the car and the driver: a quick car looks like a quick driver. Corner-phase skill uses ghost-car-style recombination to separate the two. It first estimates what each corner looks like for a driver's specific car, then measures how much the driver deviates from that car baseline across the braking, mid-corner, and exit phases. A driver in a slow car ranks on technique, not machinery; a driver in a fast car who under-delivers ranks lower than their car would suggest.

## What it shows

The skill index is built in four steps:

- **Car effect estimation**: for each `(season, constructor, corner)`, the model averages braking point, apex speed, and throttle point across all valid laps by that constructor the car's characteristic geometry at that turn.
- **Driver deviation**: each driver's per-corner geometry is subtracted from their car's average. Negative deviation = more aggressive than the machinery baseline (earlier brake, higher apex, earlier throttle) the skill residual.
- **Phase z-scores**: braking, mid-corner, and exit residuals are each standardised across the driver pool within the season. This makes all three phases contribute equally and removes the exit dominance in raw deltas (exit has 4–6× the spread of the other phases).
- **Skill index**: the sum of the three z-scores. Lower = a faster corner driver.

<Note>
  Safety-car, VSC, pit, inaccurate, and deleted laps are excluded before car averages are formed, so safety-car geometry can't contaminate the baseline. Car-corner cells with fewer than 5 observations are dropped, and only drivers with ≥100 mapped corner observations are shown.
</Note>

## How to use it

1. **Select a season** from the filter bar; the skill index reloads.
2. **Read the index ranking** lower is a stronger corner driver, independent of car speed.
3. **Break it down by phase** to see whether a driver's edge is on entry (braking), mid-corner, or exit.
4. **Compare a slow-car driver to a fast-car driver** the car baseline is removed, so the ranking is technique, not machinery.

## Reading the signal correctly

The index is **relative to each driver's own car**, so it rewards out-performing the machinery not absolute corner speed. A driver in a dominant car can post a weak index if they merely match what the car wants to do, while a driver dragging a slow car beyond its baseline ranks well.

<Warning>
  The car baseline is a per-constructor average; a team running very different setups between drivers can blur it. The ≥100-observation floor reduces but does not eliminate this read low-sample drivers with caution.
</Warning>

## Data source

The chart queries `mart_corner_skill_driver` via DuckDB-Wasm in the browser, aggregated to season level.

| Column | Meaning |
|---|---|
| `skill_index` | Sum of the three phase z-scores (lower = faster) |
| `braking_z` / `midcorner_z` / `exit_z` | Standardised per-phase deviation from the car baseline |
| `n_corner_obs` | Mapped corner observations; gates display at `≥ 100` |

The data window covers **2018–2024**.

For the full model definition, see the [`mart_corner_skill_driver` reference](/reference/models/fct/mart_corner_skill_driver).
