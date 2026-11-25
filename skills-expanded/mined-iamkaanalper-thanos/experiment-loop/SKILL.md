---
name: experiment-loop
description: Autonomous experiment loop - modify code, measure, keep/discard, iterate until target met. Metrik bazlı karar verme ile performans, boyut veya kalite optimizasyonu. Grok-native with hooks and compound integration.
when-to-use: When optimizing performance, bundle size, latency, relevance, or any measurable quality in a repeatable way. Especially useful in Phase 3/5 of swarms or after compound learnings identifies a pattern worth tuning.
---

# Experiment Loop Skill

A disciplined, automated-friendly loop for turning "I think this will be faster/smaller/better" into data-driven decisions.

## When to Use
- Performance or cost optimization where you can measure before/after.
- After compound evolution surfaces a recurring expensive pattern.
- In swarms for performance_sensitive tracks.

## The Loop (Repeat until target met or budget exhausted)

1. **Baseline** — Run the current measurement (load test, bundle size, query latency, recall@K, etc.). Record with context (git sha, env, load profile).

2. **Hypothesis** — "If we do X, metric Y will improve by Z% because of W."

3. **Change** — Small, isolated, reversible change (one variable at a time).

4. **Measure** — Same measurement as baseline. Use the same tools/hooks (our load-tester, profiler, vector patterns, etc.).

5. **Decide** — Keep if target hit or statistically better + no regression in other metrics. Discard otherwise. Record the result as friction or working solution.

6. **Compound** — Feed the outcome (what worked, what didn't, why) into compound evolution so the pattern becomes permanent (new rule, skill, or preflight item).

## Guardrails (Production Contract)
- One variable per experiment.
- Reproducible measurement (our hooks + ledger for tracking attempts).
- Budget (max N experiments or time).
- Rollback plan always ready.
- Friction record for every experiment (even failures are gold for compound).

## Integration with Our Ported System
- Use load-tester, profiler, vector-db-expert, etc. for measurement.
- on_swarm_phase or on_run_completion can trigger or record experiments.
- Results feed directly into compound_analyzer_trigger + evolution.
- Pre-flight: "Is this a measurable thing that is worth an experiment loop instead of guessing?"

## Example
Baseline checkout p95 = 980ms under 500 users.
Hypothesis: "Adding connection pool + DataLoader will drop it to <600ms."
Experiment 1: implement change.
Measure: 420ms. Keep.
Record in friction + promote "checkout-optimization-pattern" via compound.

This turns ad-hoc tuning into a repeatable, learnable capability.