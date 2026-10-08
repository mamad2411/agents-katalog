<!-- Copyright (c) 2026 Metrum AI, Inc. -->
<!-- SPDX-License-Identifier: Apache-2.0 -->

# Skill: analyze strategic telemetry NDJSON

## When to use

The user has a `metrum-ai-bench-cli-strategic` NDJSON file from `--ndjson` and
asks for power, energy, J/token, GPU util, KV cache, or preemption trends.

## Instructions

1. Read [ANALYSIS.md](ANALYSIS.md) and the strategic telemetry section of
   [../OUTPUT_SCHEMA.md](../OUTPUT_SCHEMA.md). Do not invent metric names.
2. Confirm `kind: run` `schema_version` is `metrum-ai-bench-cli.telemetry.v1`.
3. Decompress if needed (`zstd -d` / `gunzip`).
4. Run or emit recipes from [../queries/](../queries/):
   - `python3 docs/queries/analyze.py /path/to/run.ndjson`
   - or DuckDB CLI with the `.sql` files (`read_ndjson_auto`)
5. Join telemetry to `phase = measure` stages via `t_ns` in
   `[t_start_ns, t_end_ns)`. Counters: always Δ in the window. Gauges:
   time-weight for means; trapezoid for ∫power when no energy counter.
6. Treat `request.telemetry_at_done` as debug sugar only.
7. Prefer metric names present in the file; fall back to
   [exporters.md](exporters.md) / [examples/](examples/) for expected labels.
8. Default hardware source for this repo: Metrum
   [chetan-metrum-ai/all-smi](https://github.com/chetan-metrum-ai/all-smi) at
   `http://127.0.0.1:9090/metrics`.

## Do not

- Call a non-existent `correlate` CLI or assume DuckDB is bundled.
- Average raw counters.
- Use wall-clock timestamps for stage windows (`t0_wall` is metadata).
