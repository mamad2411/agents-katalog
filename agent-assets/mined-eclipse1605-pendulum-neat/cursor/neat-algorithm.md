---
description: NEAT genome, population, speciation, and network build conventions
globs: neat/**/*.py
alwaysApply: false
---

# NEAT Module

## Module map

| File | Responsibility |
|------|----------------|
| `genome.py` | `Genome`, `NodeGene`, `ConnectionGene`, cycle detection |
| `network.py` | `FeedForwardNetwork`, topological sort, activation |
| `population.py` | Evolution loop, elitism, stagnation |
| `species.py` | Compatibility distance, speciation |
| `innovation.py` | Global innovation numbers for crossover alignment |

## Invariants

- Networks must be **feed-forward** — `repair_feed_forward()` disables cycles and invalid endpoints.
- `InnovationTracker` is per-population; do not share across independent runs without intent.
- `num_inputs` / `num_outputs` come from config; observation size must match `DoublePendulumCart.get_observation()`.
- Default activation: `tanh` (config `neat.activation_function`).

## Genome ↔ controller boundary

`neat` knows nothing about physics. Controllers live in `pendulum_neat.controllers`:

```python
# ✅ GOOD — genome stays in pendulum_neat layer
controller = EvolvedController(genome)
action = controller.action(observation)
```

## Mutation / crossover changes

- Update `tests/test_neat_crossover.py` and `tests/test_neat_speciation.py`.
- Verify `test_neat_cycle.py` still passes after topology changes.
- Keep compatibility coefficients configurable via TOML (`species_threshold`, etc.).

## Parallel evaluation

`Population` uses `neat.parallel_workers` for multiprocessing — ensure evaluator calls are picklable and stateless.
