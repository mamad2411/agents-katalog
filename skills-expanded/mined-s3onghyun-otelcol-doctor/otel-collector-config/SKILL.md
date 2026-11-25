---
name: otel-collector-config
description: >-
  Use when authoring, debugging, or reviewing an OpenTelemetry Collector (otelcol)
  configuration — defining receivers/processors/exporters/connectors, wiring service
  pipelines, choosing between the core and contrib distributions, or exporting to
  OTLP/Prometheus/Loki/Tempo/Mimir. Also use when a Collector starts but no data
  arrives, a component is rejected at startup, or metrics lack expected labels.
  Triggers on "otelcol", "otel collector config", "collector pipeline",
  "receivers/processors/exporters", "memory_limiter", "otlp exporter",
  "prometheusremotewrite", "spanmetrics", "tail_sampling".
---

# OpenTelemetry Collector config — doctor

Generate correct configs from a plain-English description, and diagnose broken
ones. The Collector is a small set of concepts with a lot of sharp edges; this
skill encodes the edges so the output validates on the first try.

## Mental model (get this right and everything follows)

A Collector config has four component blocks plus a `service` block that wires
them:

```
receivers:   # where data comes IN  (otlp, prometheus, hostmetrics, filelog, kafka…)
processors:  # what happens in the MIDDLE, in order (memory_limiter, batch, transform…)
exporters:   # where data goes OUT  (otlp, otlphttp, debug, prometheus, prometheusremotewrite…)
connectors:  # bridge one pipeline's OUTPUT into another's INPUT (spanmetrics, routing…)
extensions:  # collector-level features, not in the data path (health_check, pprof, zpages…)

service:
  extensions: [health_check]
  pipelines:
    traces:  { receivers: [...], processors: [...], exporters: [...] }
    metrics: { receivers: [...], processors: [...], exporters: [...] }
    logs:    { receivers: [...], processors: [...], exporters: [...] }
  telemetry: { ... }   # the Collector's OWN logs/metrics
```

**The #1 rule everyone violates:** defining a component under `receivers:` /
`processors:` / `exporters:` does **nothing** on its own. A component only runs
if it is referenced inside a `service.pipelines.<signal>` list. A config can be
"valid" yet do nothing because a pipeline was never wired. Always check the
`service` block last, and confirm every component you defined is actually used
(and every name used is actually defined — that one fails validation).

**Pipelines are per-signal.** `traces`, `metrics`, `logs` are separate
pipelines. A receiver/exporter must support the signal of the pipeline it sits
in (e.g. the `prometheus` receiver is metrics-only; putting it in a `traces`
pipeline fails). You may run multiple named pipelines of the same signal
(`metrics/internal`, `metrics/app`).

## Workflow

### 1. Pin the three questions
- **Signals?** traces / metrics / logs (any subset).
- **Sources (receivers)?** app via OTLP? scrape Prometheus targets? host metrics? tail log files? Kafka?
- **Destinations (exporters)?** an OTLP backend (Tempo/Jaeger/vendor)? Prometheus (pull) or remote-write (push)? Loki? Mimir?

### 2. Choose the distribution — core vs contrib (this trips people constantly)
Many common components ship **only** in `otelcol-contrib`, not core `otelcol`:
`prometheus` receiver, `hostmetrics`, `filelog`, `kafka`, `resourcedetection`,
`transform`/`filter` (OTTL) processors, `tail_sampling`, the `spanmetrics`
connector, `prometheusremotewrite`/`loki` exporters. If the config uses any of
these, it needs the **contrib** image (`otel/opentelemetry-collector-contrib`)
or a custom build via the OpenTelemetry Collector Builder (`ocb`). Calling for a
contrib component on the core image is a startup crash, not a YAML error — flag it.

### 3. Order processors correctly (order is significant and load-bearing)
Processors run **in the listed order**. The canonical safe order:

```
processors: [memory_limiter, <resource/detection>, <sampling/filter/transform>, batch]
```

- **`memory_limiter` goes FIRST.** It must see data before anything buffers it,
  otherwise it can't shed load. Putting `batch` before it defeats the purpose.
- **`batch` goes LAST** (just before export) so it batches the final shape.
- **`tail_sampling`** (traces) must come before `batch`, and needs whole traces —
  don't shard the same trace across replicas without a load-balancing exporter
  in front.

### 4. Pick exporters deliberately
- `otlp` = OTLP over **gRPC** (default 4317). `otlphttp` = OTLP over **HTTP** (4318). Match the backend's port/protocol.
- `debug` is the console exporter (use `verbosity: detailed` while debugging). The old `logging` exporter is **removed/deprecated → use `debug`**.
- Metrics to Prometheus: **`prometheus`** = Collector exposes a `/metrics` endpoint for Prometheus to **scrape** (pull). **`prometheusremotewrite`** = Collector **pushes** to a remote-write endpoint (Mimir/Thanos/Cortex/Prometheus `--web.enable-remote-write-receiver`). Don't confuse pull vs push.
- Loki: the dedicated `loki` exporter was **removed** from contrib — send OTLP to Loki's native OTLP endpoint via `otlphttp` (`endpoint: http://loki:3100/otlp`).
- Tempo/Jaeger: send via `otlp`/`otlphttp` — the `jaeger` **exporter** is gone (Jaeger ingests OTLP natively). The `jaeger` **receiver** still exists (beta, in core+contrib) for *ingesting* legacy Jaeger-protocol spans during a migration; don't call it removed.

### 5. Always include the safety/ops basics
- `memory_limiter` processor in every pipeline that can be flooded.
- `health_check` extension (and wire it into `service.extensions`).
- For secrets/endpoints use env expansion: `endpoint: ${env:OTLP_ENDPOINT}` (note the `env:` prefix — bare `${VAR}` is deprecated syntax).
- Set `service.telemetry.logs.level` and, if needed, expose the Collector's own metrics.

### 6. Validate before declaring done
Never hand back a config you haven't validated. The Collector has a built-in
validator that loads and type-checks the full config without starting it:

```
otelcol validate --config=config.yaml          # core
otelcol-contrib validate --config=config.yaml   # contrib
```

The bundled `scripts/validate.sh` wraps this (auto-detects the contrib binary,
falls back to a Docker run if no local binary). If `otelcol` isn't available,
say so explicitly rather than claiming the config is validated.

## Fixing an existing config — run this checklist

When handed a broken or "it starts but nothing arrives" config, check in order:

1. **Unwired components** — every receiver/processor/exporter defined but not referenced in any `service.pipelines.*`? (silent no-op)
2. **Undefined references** — a name used in a pipeline that isn't defined above? (validation error)
3. **Signal mismatch** — a metrics-only receiver in a traces pipeline, etc.
4. **core vs contrib** — a contrib-only component on the core image? (crash on start)
5. **Processor order** — `batch` before `memory_limiter`? `memory_limiter` not first?
6. **pull vs push exporter** — `prometheus` where `prometheusremotewrite` was meant (or vice-versa)?
7. **Removed components** — `logging` exporter (→`debug`), `loki` exporter (→`otlphttp`), `jaeger` **exporter** (→`otlp`; the jaeger *receiver* is still fine), bare `${VAR}` env syntax (→`${env:VAR}`).
8. **Endpoint/protocol** — gRPC vs HTTP port mismatch (4317 vs 4318); `tls`/`insecure` set correctly for the environment.
9. **Endpoint binding** — receiver bound to `localhost` when traffic comes from other containers (needs `0.0.0.0`), or bound to `0.0.0.0` in a context where that's a security concern.

State the diagnosis as "what was wrong → why it failed → the fix", then output
the corrected config and validate it.

## The hard parts — get these right every time (see `references/advanced.md`)

A capable model already handles the basics above. These six are the ones it gets
*inconsistently* right; treat them as load-bearing and pull the exact patterns
from `references/advanced.md`:

1. **OTTL statement form** (`transform`/`filter` processors). The function syntax
   itself — `set(attributes["x"], "y") where <cond>`, `delete_key(...)`,
   `replace_pattern(...)` — is usually recalled correctly. What isn't: there are
   **two forms with different path syntax**, and mixing them fails to parse. Flat
   list → prefix every path (`span.attributes[...]`); inside a `context: span`
   block → write paths bare (`attributes[...]`). Pick one per statement list. See
   `references/advanced.md` §1. Always set `error_mode`; regexes are RE2 (no
   lookahead).
2. **spanmetrics (and any connector) is wired in TWO pipelines** — as an *exporter*
   in the source pipeline and a *receiver* in the destination pipeline. Wiring it
   once silently produces no metrics (or a validation error).
3. **Sampling must sit *downstream* of metric generation.** If `tail_sampling` (or any
   sampler) runs before the `spanmetrics` connector, RED metrics are computed from only
   the surviving fraction — request rate is wrong by the sampling ratio and *nothing looks
   broken*. Fork instead: the ingest pipeline exports to `[spanmetrics, forward/sampled]`;
   a second traces pipeline receives `forward/sampled`, applies `tail_sampling`, and
   exports to the trace backend. spanmetrics must see 100% of spans.
4. **`resource_to_telemetry_conversion` is a trade-off, not a default-on.** Off (the
   default), resource attributes land only on the `target_info` series — so
   `sum by (service_name)` returns nothing and you must join
   (`... * on (job, instance) group_left(service_name) target_info`). On, it copies
   **every** resource attribute onto **every** series — including `k8s.pod.name`,
   `host.id`, `container.id`, multiplying series count per pod. Rule: enable it only
   after dropping the high-cardinality resource attributes; otherwise leave it off and
   keep `target_info: enabled: true` for the join. State which you chose and why.
5. **`tail_sampling` at >1 replica needs a `loadbalancing` tier** keyed by `traceID`,
   so all spans of a trace reach the same sampler instance. Tail-sampling directly
   behind a plain load balancer is broken sampling. `tail_sampling` goes before `batch`.
6. **Exporter reliability — and the queue key is per-exporter.** Production exporters
   need `retry_on_failure` *plus a queue*, but the key differs: `otlp`/`otlphttp` use
   `sending_queue` (add `storage: file_storage/...` when data loss is unacceptable),
   while **`prometheusremotewrite` uses `remote_write_queue`** and rejects
   `sending_queue` at startup. If validation rejects a queue key, look up that
   exporter's own key — do **not** conclude the exporter has no queue and ship it with
   retry only. Defaults drop data on a transient backend blip.
   Durability differs too: `remote_write_queue` is memory-only (it takes no `storage:`),
   so a restart loses the backlog — but that does **not** mean the exporter has no
   on-disk option. `prometheusremotewrite` has its own `wal:` (`directory`,
   `buffer_size`, `truncate_frequency`). For survive-a-restart, use `wal` here, or move
   the path to `otlphttp` + `sending_queue.storage` against an OTLP-capable backend.

When the request touches any of these, encode the pattern explicitly rather than
trusting recall — that's the difference this skill is for.

## References
- `references/components.md` — curated catalog of the most-used receivers / processors / exporters / connectors with the gotcha for each, and the core-vs-contrib split.
- `references/advanced.md` — the hard parts in depth: OTTL patterns, spanmetrics dual-wiring, `resource_to_telemetry_conversion`, tail_sampling load-balancing topology, exporter reliability.
- `examples/` — a before/after pair (broken → corrected, validated) and `spanmetrics-config.yaml`, a validated advanced config (spanmetrics connector + OTTL + remote-write labels + retry/queue).

## Output discipline
- Emit **valid YAML only** inside config blocks — no `...` placeholders that won't parse.
- **Before emitting, cross-check every name in `service.pipelines` against the blocks
  above it.** Connectors are the usual miss: they appear in two pipelines, so it's easy
  to reference `forward/x` or `spanmetrics` without ever declaring it under `connectors:`.
  A config that needs a "one thing to fix before you deploy" footnote is a failed answer.
- Comment the non-obvious lines (why `memory_limiter` is first, why this exporter).
- Prefer the smallest config that satisfies the request; don't bolt on components the user didn't ask for.
- If a component is contrib-only, say so and name the image/build needed.
