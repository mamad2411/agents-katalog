---
name: opentelemetry-configuration-validation
description: >
  Validates an OpenTelemetry Collector pipeline configuration before
  deploying it — confirming every receiver/processor/exporter is actually
  wired into `service.pipelines` (not just declared and silently
  inert), tuning sampling rates deliberately instead of by copied
  default, checking resource-attribute correctness, and catching
  processor ordering/sizing mistakes that silently drop spans, metrics,
  or logs with no alert. Use when the user asks to "validate this OTel
  Collector config before deploying," "will this Collector pipeline drop
  spans," "check my OpenTelemetry sampling rate," "why is the Collector
  silently dropping telemetry," "review this Collector config for
  mistakes," or "set up CI validation for OTel Collector config changes."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: observability-and-platform-extras
  maturity: stable
---

# OpenTelemetry Configuration Validation

## Purpose

An OpenTelemetry Collector config that parses as valid YAML and starts
without error can still be functionally wrong in ways that only surface as
a quiet gap in a dashboard weeks later — a processor defined at the top
level but never referenced inside a specific signal's `service.pipelines`
block, a `memory_limiter` sized against a different environment's traffic,
a tail-sampling policy that unintentionally discards the very requests an
on-call engineer needs during an incident, or a resource attribute typo
that silently splits one service's telemetry into two differently-named
services in every downstream backend. None of these produce a Collector
startup error. This skill covers validating a Collector config **before**
it's deployed — structural checks, pipeline-wiring verification, sampling-
rate review, and resource-attribute correctness — as a distinct, narrower
concern from designing the pipeline in the first place, which is covered
in
[opentelemetry-instrumentation-and-collector-configuration](../opentelemetry-instrumentation-and-collector-configuration/SKILL.md)
and assumed already understood here.

## When to use

- Before merging or deploying any change to an OpenTelemetry Collector
  config (`receivers`, `processors`, `exporters`, or `service.pipelines`
  blocks).
- Setting up a CI check that validates Collector config changes on every
  PR, rather than discovering a wiring mistake after telemetry has
  already gone missing in production.
- Reviewing or tuning a sampling configuration (head-based probabilistic
  sampling at the SDK, or tail-based sampling at the Collector) to
  confirm it isn't silently discarding the traces an investigation would
  need.
- Diagnosing why telemetry that "should" be flowing through a validated-
  looking config isn't reaching a backend, to confirm which specific
  piece of the pipeline is responsible.
- Auditing an existing production Collector config for the common,
  silent misconfigurations covered here (an orphaned processor, an
  undersized `memory_limiter`, a resource-attribute mismatch) as a health
  check, not only after an incident.

## Prerequisites & environment

- The candidate Collector config file(s) — the actual rendered config the
  Collector process will start with, not just a Helm `values.yaml` or a
  templated fragment (render it first if deployed via Helm/templating,
  the same discipline as validating any templated infrastructure config).
- The `otelcol`/`otelcol-contrib` binary (matching the distribution and
  version actually deployed) available locally or in CI to run the
  Collector's own config-validation mode without needing a full running
  fleet.
- Read access to a running Collector's own internal telemetry
  (`:8888/metrics` by default) for the post-deploy confirmation step —
  static validation reduces risk but does not replace watching real
  behavior against real traffic.
- Familiarity with what each processor/exporter in the config is meant to
  do — see
  [opentelemetry-instrumentation-and-collector-configuration](../opentelemetry-instrumentation-and-collector-configuration/SKILL.md)
  for what `memory_limiter`, `batch`, `tail_sampling`, and the various
  exporters actually control if unfamiliar; this skill assumes that
  context rather than re-explaining it.

## Step-by-step guidance

1. **Run the Collector's own structural validation** before anything
   else — this parses the config and confirms every component name
   resolves to a component actually compiled into the distribution in
   use, catching typos and distribution mismatches (e.g. referencing the
   `loki` exporter against a `core`-only build that doesn't include it):
   ```bash
   otelcol-contrib validate --config=otel-collector-config.yaml
   ```
   For Helm-deployed Collectors, render the final config first — the raw
   `values.yaml` is not what the Collector process actually receives:
   ```bash
   helm template otel-collector open-telemetry/opentelemetry-collector \
     -f values-production.yaml --show-only templates/configmap-agent.yaml \
     > rendered-otel-config.yaml
   otelcol-contrib validate --config=rendered-otel-config.yaml
   ```

2. **Confirm every declared receiver/processor/exporter is actually
   referenced inside `service.pipelines` for the signal it's meant to
   affect** — this is the single most common silent-drop mistake, and
   structural validation in step 1 does not catch it, since a component
   defined at the top level but never wired into a pipeline is still
   perfectly valid YAML:
   ```bash
   # quick manual cross-check: list every top-level component name,
   # then confirm each appears somewhere under service.pipelines
   yq '.receivers | keys' otel-collector-config.yaml
   yq '.processors | keys' otel-collector-config.yaml
   yq '.exporters | keys' otel-collector-config.yaml
   yq '.service.pipelines' otel-collector-config.yaml
   ```
   Treat any top-level component name that doesn't appear in at least one
   `service.pipelines.<signal>` list as a blocking review finding, not a
   harmless unused declaration — it usually means someone intended to
   route a signal somewhere and the wiring step was simply forgotten.

3. **Verify `memory_limiter` is present and first in every pipeline's
   processor list**, sized with real headroom under the container/host
   memory limit — a missing or undersized `memory_limiter`, or one placed
   after `batch`/other processors, is the most common cause of
   unexplained data loss under load:
   ```bash
   yq '.service.pipelines.traces.processors[0]' otel-collector-config.yaml
   # expect: "memory_limiter"
   ```
   Compare `limit_mib`/`spike_limit_mib` against the container's actual
   memory request/limit — a `limit_mib` set close to or above the pod's
   memory limit gives the limiter no room to act before the container is
   OOMKilled by the runtime instead.

4. **Review sampling configuration for what it actually discards, not
   just its stated percentage.** A probabilistic/baseline sampling rate
   that looks reasonable in isolation can still silently drop the
   specific traces an investigation would need if error/latency-based
   policies aren't layered on top:
   ```yaml
   tail_sampling:
     policies:
       - name: sample-errors
         type: status_code
         status_code: { status_codes: [ERROR] }
       - name: sample-slow
         type: latency
         latency: { threshold_ms: 500 }
       - name: sample-baseline
         type: probabilistic
         probabilistic: { sampling_percentage: 10 }
   ```
   > **Warning:** a bare probabilistic sampler with no error/latency
   > policy layered above it will, on average, discard 90% of the exact
   > failing/slow requests an on-call engineer needs during an incident —
   > confirm every sampling config guarantees errors and high-latency
   > requests are always kept, with the probabilistic rate applied only
   > to the remaining "boring" baseline traffic. Review this every time a
   > sampling percentage changes, not only when it's first configured.

5. **Check resource attributes for consistency, not just presence.** A
   typo'd or environment-inconsistent `service.name`/
   `deployment.environment` doesn't error — it silently creates a second,
   differently-named identity for what should be the same service in
   every downstream backend:
   ```bash
   # confirm the same service reports a consistent service.name across
   # every instance/replica hitting this Collector
   curl -s 'http://<TEMPO>/api/search?tags=service.name' | jq
   ```
   Cross-check any `resource` processor `upsert`/`insert` actions in the
   Collector config against what the application's own
   `OTEL_RESOURCE_ATTRIBUTES` sets — an `upsert` at the Collector
   silently overriding an app-set value can be intentional (environment
   tagging) or an accidental collision; confirm which before deploying.

6. **Confirm exporter reliability settings exist for anything that can
   burst** — an exporter with no `sending_queue`/`retry_on_failure`
   configured drops data on any transient backend hiccup instead of
   buffering through it:
   ```bash
   yq '.exporters.[].sending_queue' otel-collector-config.yaml
   yq '.exporters.[].retry_on_failure' otel-collector-config.yaml
   ```
   Flag any production exporter missing both as under-configured for
   real-world backend blips (a Tempo/Loki/Prometheus remote-write
   restart, a network partition) rather than assuming the happy path is
   the only path.

7. **Wire structural + wiring validation into CI** so a bad config fails
   the PR instead of failing quietly at deploy time:
   ```yaml
   # GitHub Actions example
   - name: Validate OTel Collector config
     run: |
       docker run --rm -v "${{ github.workspace }}/otel-collector-config.yaml:/etc/otelcol/config.yaml" \
         otel/opentelemetry-collector-contrib:0.105.0 validate --config=/etc/otelcol/config.yaml
   - name: Check every component is pipeline-wired
     run: ./scripts/check_otel_pipeline_wiring.sh otel-collector-config.yaml
   ```
   The wiring check (step 2) is easy to script as a small lint step (diff
   the set of top-level component names against the set referenced under
   `service.pipelines`) so it runs automatically on every PR rather than
   depending on a reviewer noticing by eye.

8. **After deploying, confirm the config behaves as validated** using the
   Collector's own internal telemetry — static validation reduces risk
   but doesn't replace watching real ingestion/export behavior:
   ```bash
   curl -s http://<OTEL_COLLECTOR>:8888/metrics | grep -E \
     'otelcol_processor_(refused|dropped)_spans_total|otelcol_exporter_(send_failed|queue_size)'
   ```
   > **Warning:** a Collector pipeline can silently and continuously drop
   > spans/metrics/logs (a misconfigured processor, an exhausted exporter
   > queue, a `memory_limiter` refusing data under sustained load) with no
   > default alert firing anywhere — unless `otelcol_processor_dropped_*`
   > and `otelcol_exporter_send_failed_*` are explicitly scraped and
   > alerted on, this failure mode is invisible until someone notices a
   > gap during an actual investigation. Treat wiring an alert on these
   > metrics as part of shipping the pipeline, not an optional follow-up.

## Best practices

- Run `validate` (or the Docker equivalent) in CI on every PR touching
  Collector config — treat a failing structural check the same as a
  failing unit test.
- Never validate a Helm `values.yaml` directly — always render the
  actual templated config first, since that's what the Collector process
  receives.
- Script the pipeline-wiring cross-check (every declared component
  appears in some `service.pipelines.<signal>` list) as an automated CI
  lint, not a manual reviewer habit — it is the single mistake structural
  validation cannot catch and the single most common cause of silently
  missing telemetry.
- Review every sampling-rate change for what it discards under real
  failure conditions, not just its headline percentage — always confirm
  error and high-latency traces are exempted from probabilistic dropping.
- Size `memory_limiter` against the actual container memory limit with
  real headroom, and confirm it's first in every pipeline's processor
  list on every review, not just when first configured.
- Alert on `otelcol_processor_dropped_*`/`otelcol_exporter_send_failed_*`
  as a standing dashboard/alert, not just when someone reports missing
  telemetry — silent drops are otherwise invisible until an investigation
  needs the very data that was dropped.
- Treat a resource-attribute inconsistency (a typo'd `service.name`, a
  Collector-side `upsert` colliding with an app-set value) as a real bug,
  not a cosmetic issue — it fragments one service's telemetry into
  multiple identities across every downstream backend.

## Common pitfalls

- **Symptom:** `validate` passes cleanly and the Collector starts without
  error, but a specific signal (often traces) never reaches its intended
  backend even though metrics/logs from the same service work fine.
  **Fix:** `validate` only checks that named components resolve and the
  YAML is structurally sound, not that every component is actually
  referenced inside `service.pipelines` for the relevant signal (step 2)
  — this is exactly the mistake structural validation misses since an
  orphaned component is still valid config. Cross-check the
  top-level component list against `service.pipelines` explicitly.

- **Symptom:** The Collector silently drops data under real production
  load, with no error in application logs and no obvious config mistake
  on read-through.
  **Fix:** `memory_limiter` is either missing, undersized relative to the
  container's actual memory limit, or not first in the processor chain
  (step 3) — none of which fail `validate`. Confirm ordering and sizing
  explicitly, and watch `otelcol_processor_refused_spans_total` after any
  change.

- **Symptom:** A tail-sampling change is deployed to "reduce storage
  cost," and during the next incident the on-call engineer can't find any
  trace for the specific failing requests they need.
  **Fix:** The sampling policy applied a flat probabilistic rate with no
  error/latency policy layered above it (step 4), so most of the failing
  requests were dropped along with the "boring" baseline traffic that was
  the actual intended target for reduction. Add explicit error-status and
  latency-threshold policies ahead of the probabilistic baseline, and
  re-review the change with "what would this drop during an incident" as
  the explicit test, not just the storage-cost delta.

- **Symptom:** A dashboard shows the same logical service split across
  two entries (e.g. `checkout-service` and `checkout_service`, or
  `checkout-service` and `unknown_service`), even though only one service
  is actually deployed.
  **Fix:** A `resource.name` typo or inconsistency between what the
  application sets via `OTEL_RESOURCE_ATTRIBUTES` and what a Collector-
  side `resource` processor `upsert`s (step 5) creates two distinct
  service identities in every downstream backend. Standardize the exact
  attribute value in one place (ideally the application's own resource
  configuration) and treat any Collector-side override as a deliberate,
  reviewed decision, not an incidental default.

- **Symptom:** A brief backend outage (Tempo/Loki/Prometheus remote-write
  restart) causes a permanent gap in telemetry for that window, instead
  of the Collector catching up once the backend recovers.
  **Fix:** The affected exporter has no `sending_queue`/
  `retry_on_failure` configured (step 6), so it drops rather than buffers
  during the outage. Add both with a queue size sized to survive the
  expected outage duration at current throughput.

## Worked example

**Scenario:** A PR proposes lowering the tail-sampling baseline rate from
25% to 5% "to cut Tempo storage cost," and separately adds a new
`attributes/pii-scrub` processor intended to strip a sensitive header from
span attributes.

1. Run structural validation first:
   ```bash
   otelcol-contrib validate --config=otel-collector-config.yaml
   ```
   Passes — both changes are structurally valid.

2. Run the pipeline-wiring cross-check:
   ```bash
   yq '.service.pipelines.traces.processors' otel-collector-config.yaml
   ```
   Reveals `attributes/pii-scrub` was added under `processors:` at the top
   level but **not** added to `service.pipelines.traces.processors` — the
   new scrubbing rule would have done nothing, silently shipping the
   sensitive header downstream despite the PR's stated intent. Flagged as
   a blocking finding; fixed by adding it to the pipeline's processor
   list, ahead of `batch`.

3. Review the sampling change against step 4's "what does this discard"
   test:
   ```diff
     - name: sample-baseline
       type: probabilistic
   -   probabilistic: { sampling_percentage: 25 }
   +   probabilistic: { sampling_percentage: 5 }
   ```
   Confirmed the existing config already has `sample-errors` and
   `sample-slow` policies ahead of the baseline policy, so the change only
   reduces sampling of already-successful, fast requests — not the traces
   an incident investigation would need. Approved as-is.

4. Post-deploy, `otelcol_processor_dropped_spans_total` and
   `otelcol_exporter_send_failed_spans_total` are checked and remain flat,
   confirming the fixed pipeline wiring and the sampling change both
   behave as validated, not just as configured.

## Cross-references

- [opentelemetry-instrumentation-and-collector-configuration](../opentelemetry-instrumentation-and-collector-configuration/SKILL.md) — designing the receiver/processor/exporter pipeline and instrumentation this skill validates before deployment.
- [distributed-tracing-with-tempo-and-jaeger](../distributed-tracing-with-tempo-and-jaeger/SKILL.md) — the backend-side sampling strategy and storage this Collector's tail-sampling and exporter configuration feeds into.
- [loki-configuration-validation](../loki-configuration-validation/SKILL.md) — the equivalent pre-deploy validation discipline applied to the Loki backend this Collector's `loki` exporter feeds.
