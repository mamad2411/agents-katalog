---
name: fluent-bit-log-forwarding-configuration
description: >
  Configures Fluent Bit as a lightweight log forwarder — INPUT sources
  (`tail`, `systemd`, Kubernetes container logs), FILTER stages
  (`kubernetes` metadata enrichment, `parser`, `grep`, `modify`,
  `nest`/`lift`), and OUTPUT routing to Loki, Elasticsearch/OpenSearch,
  or S3, including multiple outputs via tags/`Match` and backpressure/
  buffering settings. Use when the user asks to "set up Fluent Bit,"
  "forward Kubernetes pod logs to Loki/Elasticsearch/S3," "write a
  Fluent Bit parser for my log format," "route different logs to
  different outputs," or "Fluent Bit is dropping logs / backing up."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: observability-and-platform-extras
  maturity: stable
---

# Fluent Bit Log Forwarding Configuration

## Purpose

Fluent Bit's entire job is moving log data reliably from wherever it's
produced to wherever it needs to land, through a pipeline of **INPUT**
(where logs come from), **FILTER** (enrichment/transformation/dropping),
and **OUTPUT** (where logs go) sections connected by **tags** and
`Match` patterns — and because it typically runs as a DaemonSet on every
node, a misconfigured pipeline doesn't just misroute logs, it can
silently drop them cluster-wide or exhaust node memory buffering
backpressure from a slow downstream. This skill covers building that
INPUT → FILTER → OUTPUT pipeline for the common Kubernetes case
(container log tailing, Kubernetes metadata enrichment, routing to
Loki/Elasticsearch/S3) and the buffering/backpressure settings that
determine what happens when an output is slow or unavailable. It assumes
the destination (Loki) is already configured to receive pushed logs —
see
[loki-log-aggregation-configuration](../loki-log-aggregation-configuration/SKILL.md)
— and does not cover writing queries against the logs once they land
(see
[logql-query-authoring](../logql-query-authoring/SKILL.md)).

## When to use

- Standing up Fluent Bit (as a Kubernetes DaemonSet or standalone
  process) to forward application/container logs somewhere.
- Adding Kubernetes metadata (pod name, namespace, labels) to raw
  container log lines before they're shipped.
- Writing a custom parser for an application's log format (multiline
  stack traces, a custom timestamp format, JSON with nested fields).
- Routing different log streams to different destinations (e.g.
  application logs to Loki, audit logs to S3 for compliance retention,
  security-relevant logs to Elasticsearch/OpenSearch) from the same
  Fluent Bit pipeline.
- Fluent Bit is dropping logs, falling behind, or a node running it is
  under memory/disk pressure because of buffering.
- Migrating from Fluentd to Fluent Bit and needing the equivalent
  pipeline stages.

## Prerequisites & environment

- Fluent Bit 2.x (1.9+ config syntax is largely compatible, but 2.x is
  assumed for the YAML config format shown below — the classic `.conf`
  INI-style format is also still supported and shown where the
  distinction matters).
- For Kubernetes: DaemonSet deployment with a hostPath volume mount for
  `/var/log/containers` (and `/var/log/pods`, `/var/lib/docker/
  containers` depending on the container runtime's log location) and a
  ServiceAccount with RBAC to read Pod/Namespace metadata for the
  `kubernetes` filter.
- The destination(s) already reachable and, for Loki/Elasticsearch,
  already configured to accept the expected volume — see
  [loki-log-aggregation-configuration](../loki-log-aggregation-configuration/SKILL.md)
  for Loki-side ingestion limits that a misconfigured Fluent Bit output
  can otherwise slam into.
- Persistent local disk (or emptyDir with enough size) available on each
  node for `storage.path` if using filesystem-backed buffering — required
  for genuine at-least-once delivery guarantees under backpressure.

## Step-by-step guidance

1. **Configure the INPUT to tail container logs**, tagging by pod/
   container path so downstream filters/outputs can route on it:
   ```yaml
   # fluent-bit.yaml (Fluent Bit 2.x YAML config)
   pipeline:
     inputs:
       - name: tail
         path: /var/log/containers/*.log
         tag: kube.*
         refresh_interval: 5
         mem_buf_limit: 50MB
         skip_long_lines: on
         db: /var/log/flb_kube.db
         storage.type: filesystem
   ```
   `db` (the SQLite position database) lets Fluent Bit resume from where
   it left off after a restart instead of re-reading or skipping logs;
   `storage.type: filesystem` (see step 6) is what actually makes
   buffering durable across a Fluent Bit restart, not just the `db` file
   alone.

2. **Enrich with Kubernetes metadata using the `kubernetes` filter**
   before any routing decision that depends on namespace/labels:
   ```yaml
     filters:
       - name: kubernetes
         match: kube.*
         kube_url: https://kubernetes.default.svc:443
         kube_tag_prefix: kube.var.log.containers.
         merge_log: on
         merge_log_key: log_processed
         k8s-logging.parser: on
         k8s-logging.exclude: on
   ```
   `k8s-logging.exclude: on` (paired with a
   `fluentbit.io/exclude: "true"` pod annotation) lets specific
   noisy/irrelevant pods opt out of shipping entirely — cheaper than
   filtering their volume downstream after ingestion.

3. **Parse application-specific log formats** with a dedicated `parser`
   filter (or `Parser` set directly on the `tail` input for a single
   known format) rather than shipping unstructured lines and hoping the
   backend parses them:
   ```yaml
   parsers:
     - name: app_json
       format: json
       time_key: timestamp
       time_format: "%Y-%m-%dT%H:%M:%S.%L%z"
     - name: multiline_stacktrace
       format: regex
       regex: '^(?<time>\d{4}-\d{2}-\d{2}[^ ]* )(?<level>\w+) (?<message>.*)'
   ```
   ```yaml
     filters:
       - name: parser
         match: kube.payments-api.*
         key_name: log
         parser: app_json
         reserve_data: on
   ```
   For multi-line stack traces specifically, use the `multiline` filter
   (or `multiline.parser` on the `tail` input in newer versions) rather
   than a regex parser alone — a plain parser processes line-by-line and
   cannot join a Java/Python stack trace's continuation lines back into
   one log entry on its own.

4. **Drop or redact fields that shouldn't be shipped downstream** —
   secrets accidentally logged, overly verbose fields, or fields that
   would become unbounded labels at the Loki destination:
   ```yaml
     filters:
       - name: modify
         match: kube.*
         remove: authorization
         remove: password
       - name: grep
         match: kube.*
         exclude: log healthcheck
   ```
   > **Warning:** never rely on a downstream system (Loki, Elasticsearch)
   > to redact secrets that were accidentally logged — filter them out at
   > the forwarder, as close to the source as practical, since anything
   > that reaches the destination is retained per its retention policy
   > and may be readable by anyone with query access.

5. **Route to multiple outputs by tag/`Match`**, sending different log
   classes to the destination appropriate for each — this is the core of
   "different logs, different backends":
   ```yaml
     outputs:
       - name: loki
         match: kube.payments.*
         host: loki-gateway.monitoring.svc
         port: 3100
         labels: job=fluentbit, namespace=$kubernetes['namespace_name'], app=$kubernetes['labels']['app']
         line_format: json

       - name: es
         match: kube.security-audit.*
         host: opensearch.security.svc
         port: 9200
         index: security-audit
         suppress_type_name: on

       - name: s3
         match: kube.compliance-audit.*
         bucket: <S3_BUCKET_NAME>
         region: <AWS_REGION>
         total_file_size: 50M
         upload_timeout: 10m
         use_put_object: on
   ```
   > **Warning — Loki label cardinality:** the `labels` field on the
   > `loki` output plugin becomes indexed Loki stream labels exactly like
   > any other Loki label — never map an unbounded Kubernetes field
   > (pod name, pod IP, a per-request annotation) into it. Stick to
   > `namespace_name`, `app`/`container_name`, and similarly bounded
   > values, per
   > [loki-log-aggregation-configuration](../loki-log-aggregation-configuration/SKILL.md).

6. **Enable filesystem-backed buffering for genuine delivery
   guarantees under backpressure** — the default in-memory-only buffering
   drops logs once `mem_buf_limit` is hit if the output is slow/down:
   ```yaml
   service:
     flush: 5
     storage.path: /var/log/flb-storage
     storage.sync: normal
     storage.checksum: off
     storage.max_chunks_up: 128
     storage.backlog.mem_limit: 64MB
   ```
   Filesystem buffering (`storage.type: filesystem` on the relevant
   inputs, plus `service.storage.path` set) persists chunks to local
   disk when memory limits are reached, trading some latency/disk usage
   for not silently dropping logs during a downstream outage — worth it
   for anything where log loss during an incident is unacceptable
   (audit/compliance streams especially).

7. **Set retry and backoff behavior on outputs** so a transient
   destination outage doesn't either drop data immediately or retry so
   aggressively it worsens an already-struggling downstream:
   ```yaml
     outputs:
       - name: loki
         match: kube.payments.*
         host: loki-gateway.monitoring.svc
         port: 3100
         retry_limit: 5
         net.connect_timeout: 10
   ```

8. **Validate and dry-run the pipeline before rolling out broadly** —
   see
   [fluent-bit-configuration-validation](../fluent-bit-configuration-validation/SKILL.md)
   for the full pre-deploy validation workflow (`fluent-bit --dry-run`,
   testing parsers against sample lines); at minimum, confirm the
   pipeline is emitting before a cluster-wide rollout:
   ```bash
   fluent-bit -c fluent-bit.yaml -o stdout -m '*'
   ```

## Best practices

- Add Kubernetes metadata enrichment before any tag-based routing
  decision that depends on namespace/labels — routing on the raw
  container log path alone is fragile across runtime/log-location
  changes.
- Use `k8s-logging.exclude`/a pod annotation to opt noisy, low-value pods
  out of shipping entirely rather than filtering their volume downstream
  after it's already been ingested (and, for Loki, already counted
  against ingestion limits).
- Redact known-sensitive fields (`authorization`, `password`, API keys
  accidentally logged) at the Fluent Bit filter stage, as close to the
  source as practical — never depend on the destination to scrub them
  after the fact.
- Map only bounded, low-cardinality Kubernetes fields into a Loki
  output's `labels` — namespace and app/service name, not pod name, pod
  IP, or any per-request value.
- Enable `storage.type: filesystem` buffering for any log stream where
  loss during a downstream outage is unacceptable (audit/compliance
  logs, anything feeding a security pipeline) — accept the in-memory-only
  default only for genuinely disposable/best-effort telemetry.
- Route different log classes to the backend suited to their access
  pattern — high-volume operational logs to Loki, long-term compliance
  logs to S3, search-heavy security logs to Elasticsearch/OpenSearch —
  rather than forcing everything through one output and one retention
  policy.
- Set explicit `retry_limit`/timeouts on every output — an output with
  unlimited retries against a persistently failing destination can pile
  up buffered chunks and pressure the node, while an output with none
  drops data on the first transient blip.

## Common pitfalls

- **Symptom:** Logs stop appearing at the destination during a
  downstream outage (Loki/Elasticsearch restart, network blip), and some
  log lines from that window never show up even after the destination
  recovers.
  **Fix:** Buffering was in-memory only (`storage.type` not set to
  `filesystem`), so once `mem_buf_limit` was hit during the outage,
  Fluent Bit dropped further input rather than queuing it to disk. Enable
  filesystem-backed buffering (step 6) for any stream where this loss is
  unacceptable.

- **Symptom:** A node running the Fluent Bit DaemonSet runs low on disk
  space or memory, and it's traced back to log forwarding.
  **Fix:** Filesystem buffering was enabled without a bounded
  `storage.backlog.mem_limit`/`storage.max_chunks_up`, or `mem_buf_limit`
  on the `tail` input was left too high relative to node capacity, so
  buffered chunks accumulated unbounded during a prolonged downstream
  outage instead of being capped. Set explicit limits sized to the
  node's actual available resources, and pair with alerting on Fluent
  Bit's own buffer/retry metrics so this is caught before it becomes a
  node-level incident.

- **Symptom:** Multi-line Java/Python stack traces show up in the
  destination as dozens of separate single-line log entries instead of
  one coherent trace.
  **Fix:** A `regex`/`json` parser was applied line-by-line without a
  `multiline` filter (or `multiline.parser` on the input) to join
  continuation lines. Add multiline handling explicitly for any log
  format that spans multiple physical lines per logical entry.

- **Symptom:** A Loki output starts getting `429`/rejected ingestion
  shortly after a new field was added to the `labels` mapping on the
  `loki` output plugin.
  **Fix:** The new label maps an unbounded Kubernetes field (pod name,
  pod IP) into Loki's indexed labels, exploding stream count on the Loki
  side. Remove it from the output's `labels` mapping and, if the field
  is genuinely useful for querying, ship it as part of the log line
  content instead (parsed at query time via LogQL, per
  [logql-query-authoring](../logql-query-authoring/SKILL.md)).

- **Symptom:** After adding a new `grep`/`modify` filter meant to
  redact a sensitive field, the field still shows up at the destination.
  **Fix:** The filter's `Match` pattern doesn't actually match the tag
  of the logs carrying that field (commonly a tag-prefix mismatch after
  the `kubernetes` filter's `kube_tag_prefix` rewrites tags), so the
  filter is silently never applied to the intended stream. Confirm with
  `fluent-bit -c fluent-bit.yaml -o stdout -m '*'` that the filter's
  `match` pattern actually catches the target tag before assuming the
  filter itself is broken.

- **Symptom:** Two teams' logs, meant to go to two different outputs
  (e.g. `payments` to Loki, `security-audit` to Elasticsearch), both end
  up in both destinations.
  **Fix:** Both outputs' `match` patterns are broader than intended
  (e.g. both using `kube.*` instead of a properly scoped tag), so every
  output matches every input. Scope `match` patterns as narrowly as the
  actual tag structure allows (`kube.payments.*` vs.
  `kube.security-audit.*`), and verify with the stdout dry-run before
  rolling out to production destinations.

## Worked example

**Scenario:** A Kubernetes cluster needs Fluent Bit configured to: ship
`payments` namespace application logs to Loki with Kubernetes metadata,
ship `security-audit` namespace logs to OpenSearch, and archive
`compliance-audit` namespace logs to S3 for 7-year retention — with
filesystem buffering so a Loki maintenance window doesn't lose payments
logs.

```yaml
service:
  flush: 5
  storage.path: /var/log/flb-storage
  storage.sync: normal
  storage.backlog.mem_limit: 64MB

pipeline:
  inputs:
    - name: tail
      path: /var/log/containers/*.log
      tag: kube.*
      db: /var/log/flb_kube.db
      storage.type: filesystem
      mem_buf_limit: 50MB

  filters:
    - name: kubernetes
      match: kube.*
      kube_tag_prefix: kube.var.log.containers.
      merge_log: on
      k8s-logging.exclude: on
    - name: modify
      match: kube.*
      remove: authorization
      remove: password

  outputs:
    - name: loki
      match: kube.var.log.containers.*payments*
      host: loki-gateway.monitoring.svc
      port: 3100
      labels: job=fluentbit, namespace=$kubernetes['namespace_name'], app=$kubernetes['labels']['app']
      retry_limit: 5

    - name: es
      match: kube.var.log.containers.*security-audit*
      host: opensearch.security.svc
      port: 9200
      index: security-audit
      retry_limit: 3

    - name: s3
      match: kube.var.log.containers.*compliance-audit*
      bucket: <S3_BUCKET_NAME>
      region: <AWS_REGION>
      total_file_size: 100M
      upload_timeout: 10m
```

`storage.type: filesystem` on the shared `tail` input means that when
Loki goes into a planned maintenance window, payments logs buffer to
local disk (bounded by `storage.backlog.mem_limit`) instead of being
dropped, and drain automatically once Loki is reachable again — verified
before rollout with the stdout dry-run and the checks in
[fluent-bit-configuration-validation](../fluent-bit-configuration-validation/SKILL.md).

## Cross-references

- [fluent-bit-configuration-validation](../fluent-bit-configuration-validation/SKILL.md) — dry-running and syntax-checking this exact pipeline before a production rollout.
- [loki-log-aggregation-configuration](../loki-log-aggregation-configuration/SKILL.md) — the ingestion-side limits and label-cardinality rules that this forwarder's `loki` output must respect.
- [logql-query-authoring](../logql-query-authoring/SKILL.md) — querying logs once they land in Loki, including parsing fields that were deliberately kept out of the `labels` mapping here.
- [incident-investigation-using-metrics-logs-traces](../incident-investigation-using-metrics-logs-traces/SKILL.md) — using logs forwarded by this pipeline as one leg of a live cross-signal investigation.
