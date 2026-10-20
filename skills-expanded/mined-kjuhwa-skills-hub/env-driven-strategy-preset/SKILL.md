---
name: env-driven-strategy-preset
description: Expose one env var that selects a named preset, where each preset is a tuple of behavior weights (innovate / optimize / repair). Default preset is "balanced"; operators swap presets for incident response without touching code.
category: configuration
version: 1.0.0
version_origin: extracted
confidence: medium
tags: [configuration, strategy, env-var, presets, feature-weights]
source_type: extracted-from-git
source_url: https://github.com/EvoMap/evolver.git
source_ref: main
source_commit: 4c51382092f9cb125d3ec55475861ead8d1463a6
source_project: evolver
imported_at: 2026-04-18T02:45:00Z
---

# Env-Driven Strategy Preset

## When to use

Your loop has multiple competing intents (new features vs. hardening vs. repair). You want operators to shift the balance without a redeploy or a config file edit.

## Shape

One env var (`EVOLVE_STRATEGY` in the source repo), finite preset names, table of weights:

| Preset | Innovate | Optimize | Repair | When to use |
|---|---|---|---|---|
| `balanced` (default) | 50% | 30% | 20% | Daily operation |
| `innovate` | 80% | 15% | 5% | System stable, ship features fast |
| `harden` | 20% | 40% | 40% | After major changes, focus on stability |
| `repair-only` | 0% | 20% | 80% | Emergency — all-out repair |

The loop reads `EVOLVE_STRATEGY` once per iteration, looks up the tuple, and uses the weights as the mixing distribution for its next action selection.

## Rules

- **Fail open to the default.** Unknown values → `balanced`, logged once.
- **No partial weights from env.** Operators cannot pass raw numbers; they pick a named preset. This keeps the search space small and documented.
- **Reload per iteration.** The env var is re-read on each loop tick so operators can change strategy on a running daemon without restarting.
- **Presets are tuples, not booleans.** The invariant `innovate + optimize + repair = 100` must hold; a unit test enforces it.
- **Auto preset (optional).** An `auto` preset can inspect recent failure rate and pick `repair-only` / `harden` / `balanced` dynamically, so operators don't have to flip manually during incidents.

## Anti-patterns

- Exposing each weight as its own env var. Now operators debug three knobs instead of one named dial, and the weights can go out of sync.
- Putting the weights in code. Ops can't change them without a deploy.
- Silent fallback on typo. Always log "unknown strategy 'X', using balanced" so misconfigs surface.
