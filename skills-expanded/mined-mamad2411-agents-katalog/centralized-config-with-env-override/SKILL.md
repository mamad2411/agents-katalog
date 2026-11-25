---
name: centralized-config-with-env-override
description: Centralized config thresholds with environment variable override pattern for timeouts and limits
category: cli
version: 1.0.0
version_origin: extracted
confidence: high
tags: [evolver, cli, config, env-vars]
source_type: extracted-from-git
source_url: https://github.com/EvoMap/evolver.git
source_ref: main
source_commit: 22773782475cecf43dc9c1af264bf5f9cacc28bc
source_project: evolver
source_paths:
  - src/config.js
imported_at: 2026-04-18T00:00:00Z
---

# Centralized config with env-override helpers

Define all runtime thresholds (timeouts, retry counts, size limits, score thresholds) in a single config module. Expose tiny typed helpers — `envInt(name, default)`, `envFloat(name, default)`, `envStr(name, default)` — that safely parse env vars and fall back.

## Why

Prevents "magic numbers" from spreading across modules and gives ops a single, grep-friendly surface for tuning. Helpers guard against `NaN` from malformed env input.

## Mechanism

```js
const envInt = (n, d) => {
  const v = parseInt(process.env[n], 10);
  return Number.isFinite(v) ? v : d;
};

module.exports = {
  VALIDATION_TIMEOUT_MS: envInt('VALIDATION_TIMEOUT_MS', 180_000),
  HEARTBEAT_MS: envInt('HEARTBEAT_MS', 360_000),
  SOLIDIFY_RETRIES: envInt('SOLIDIFY_RETRIES', 2),
  BROADCAST_SCORE_MIN: envFloat('BROADCAST_SCORE_MIN', 0.7),
  // ...
};
```

## When to reuse

Any daemon or long-running CLI with dozens of tunable knobs. Prefer this over `dotenv` spread through the codebase.
