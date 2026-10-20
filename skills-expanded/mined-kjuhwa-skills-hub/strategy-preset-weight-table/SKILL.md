---
name: strategy-preset-weight-table
description: When an autonomous loop has to pick between multiple intent classes each iteration (innovate / optimize / repair / …), expose them as a small set of named presets with explicit percentage weights, let one env var flip between presets, and document the use-case-per-preset in the same table operators read.
category: configuration
version: 1.0.0
version_origin: extracted
tags: [strategy, presets, weighted-choice, env-config, autonomous-loop]
confidence: medium
source_type: extracted-from-git
source_url: https://github.com/EvoMap/evolver.git
source_ref: main
source_commit: 4c51382092f9cb125d3ec55475861ead8d1463a6
source_project: evolver
source_paths:
  - README.md (With Strategy Preset section)
  - src/config.js
imported_at: 2026-04-18T03:00:00Z
---

# Named Strategy Presets as a Weight Table

Use this when a long-running agent must choose between structurally-similar actions each tick, and the right mix depends on the phase the operator is in (steady state vs. post-incident vs. feature push vs. firefighting).

## Shape

A preset is nothing more than a named row in a weight table.

| Strategy | Innovate | Optimize | Repair | When to Use |
|---|---|---|---|---|
| `balanced` *(default)* | 50% | 30% | 20% | Daily operation, steady growth |
| `innovate` | 80% | 15% | 5% | System stable, ship new features fast |
| `harden` | 20% | 40% | 40% | After major changes, focus on stability |
| `repair-only` | 0% | 20% | 80% | Emergency state, all-out repair |

Operators select one row with a single env var: `EVOLVE_STRATEGY=harden node index.js --loop`.

## Why this beats per-iteration flags

1. **One axis of change, not three.** The operator doesn't have to keep three percentages consistent — the preset enforces the invariant `sum == 100` for them.
2. **Self-documenting.** The *When to Use* column is what you want in the README anyway; by making it a column of the same table operators paste into their shell, the doc and the config can't drift.
3. **Encodes institutional knowledge.** "`harden` after major changes" is the kind of tacit rule that usually lives in Slack history. A named preset turns it into a first-class config.

## Implementation sketch

```js
const PRESETS = {
  balanced:     { innovate: 0.50, optimize: 0.30, repair: 0.20 },
  innovate:     { innovate: 0.80, optimize: 0.15, repair: 0.05 },
  harden:       { innovate: 0.20, optimize: 0.40, repair: 0.40 },
  'repair-only':{ innovate: 0.00, optimize: 0.20, repair: 0.80 },
};

function pickIntent(rng = Math.random) {
  const key = process.env.EVOLVE_STRATEGY || 'balanced';
  const w = PRESETS[key] || PRESETS.balanced;
  let r = rng();
  for (const [intent, weight] of Object.entries(w)) {
    if ((r -= weight) <= 0) return intent;
  }
  return 'repair'; // safety fallthrough
}
```

## Extensions worth considering

- **`auto` preset**: compute weights from a recent-health signal instead of using a fixed row. Keep it as a separate preset key — don't mutate the fixed ones.
- **`early-stabilize` / `steady-state`**: phase-of-project presets layered on top of action-mix presets. Two env vars > four pre-multiplied rows if the dimensions are independent.
- **Telemetry**: log the chosen preset and the rolled intent per iteration, so post-mortems can answer "was the loop in repair mode when this happened?"

## Anti-patterns

- Accepting `EVOLVE_INNOVATE_PCT` + `EVOLVE_OPTIMIZE_PCT` + `EVOLVE_REPAIR_PCT` as separate env vars. The sum-to-100 invariant becomes a support burden.
- Hiding the weights inside code. The table is the feature.
- Using preset names that describe *how the loop works internally* (`mode_a`, `mode_b`). Names must describe the operator's situation.
