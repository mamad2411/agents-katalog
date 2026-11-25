---
name: managing-logstash
description: |
  Use when working with Logstash — logstash pipeline management with
  input/filter/output analysis, pipeline statistics, event processing metrics,
  and queue monitoring. Covers pipeline health, plugin performance, JVM stats,
  hot threads analysis, and configuration review. Use when managing Logstash
  pipelines, analyzing throughput, reviewing filter performance, or
  troubleshooting event processing.
connection_type: logstash
preload: false
---

# Logstash Management Skill

Monitor and manage Logstash event processing pipelines via the monitoring API.

## API Conventions

### Authentication
Logstash monitoring API is typically unauthenticated (localhost access). Connection handles auth if configured.

### Base URL
- Monitoring API: `http://<host>:9600/`
- Use connection-injected `LOGSTASH_BASE_URL`.

### Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Use `jq` to extract only relevant pipeline and plugin metrics
- NEVER dump full node stats — always filter to specific sections

### Core Helper Function

```bash
#!/bin/bash

logstash_api() {
    local endpoint="$1"
    curl -s "${LOGSTASH_BASE_URL}${endpoint}"
}

logstash_stats() {
    local section="${1:-}"
    if [ -n "$section" ]; then
        logstash_api "/_node/stats/${section}"
    else
        logstash_api "/_node/stats"
    fi
}

logstash_pipelines() {
    logstash_api "/_node/stats/pipelines"
}
```

## Parallel Execution

```bash
{
    logstash_api "/" &
    logstash_stats "jvm" &
    logstash_stats "process" &
    logstash_stats "pipelines" &
}
wait
```

## Anti-Hallucination Rules

**NEVER assume pipeline names, plugin IDs, or filter configurations. ALWAYS discover first.**

### Phase 1: Discovery

```bash
#!/bin/bash
echo "=== Logstash Info ==="
logstash_api "/" | jq '{version: .version, status: .status, pipeline: .pipeline}'

echo ""
echo "=== Pipeline Names ==="
logstash_stats "pipelines" | jq -r '.pipelines | keys[]'

echo ""
echo "=== Plugin Summary per Pipeline ==="
logstash_stats "pipelines" | jq -r '.pipelines | to_entries[] | "\(.key): inputs=\(.value.plugins.inputs | length) filters=\(.value.plugins.filters | length) outputs=\(.value.plugins.outputs | length)"'
```

## Common Operations

### Pipeline Health Overview

```bash
#!/bin/bash
echo "=== Pipeline Status ==="
logstash_stats "pipelines" | jq -r '.pipelines | to_entries[] | {
    pipeline: .key,
    events_in: .value.events.in,
    events_out: .value.events.out,
    events_filtered: .value.events.filtered,
    queue_events: .value.queue.events_count,
    queue_type: .value.queue.type
}'

echo ""
echo "=== Event Throughput ==="
logstash_stats "pipelines" | jq -r '.pipelines | to_entries[] | "\(.key)\tin:\(.value.events.in)\tout:\(.value.events.out)\tfiltered:\(.value.events.filtered)\tduration_ms:\(.value.events.duration_in_millis)"'
```

### Input/Filter/Output Performance

```bash
#!/bin/bash
PIPELINE="${1:-main}"

echo "=== Input Plugins (${PIPELINE}) ==="
logstash_stats "pipelines" | jq -r ".pipelines.\"${PIPELINE}\".plugins.inputs[] | \"\(.name)\tid:\(.id)\tevents:\(.events.out)\"" | head -10

echo ""
echo "=== Filter Plugins (${PIPELINE}) ==="
logstash_stats "pipelines" | jq -r ".pipelines.\"${PIPELINE}\".plugins.filters[] | \"\(.name)\tid:\(.id)\tevents_in:\(.events.in)\tevents_out:\(.events.out)\tduration:\(.events.duration_in_millis)ms\"" | head -15

echo ""
echo "=== Output Plugins (${PIPELINE}) ==="
logstash_stats "pipelines" | jq -r ".pipelines.\"${PIPELINE}\".plugins.outputs[] | \"\(.name)\tid:\(.id)\tevents_in:\(.events.in)\tevents_out:\(.events.out)\tduration:\(.events.duration_in_millis)ms\"" | head -10

echo ""
echo "=== Slowest Filters ==="
logstash_stats "pipelines" | jq -r ".pipelines.\"${PIPELINE}\".plugins.filters | sort_by(-.events.duration_in_millis)[:5][] | \"\(.name)\t\(.id)\t\(.events.duration_in_millis)ms total\""
```

### Queue Monitoring

```bash
#!/bin/bash
echo "=== Queue Status ==="
logstash_stats "pipelines" | jq -r '.pipelines | to_entries[] | {
    pipeline: .key,
    queue_type: .value.queue.type,
    events_count: .value.queue.events_count,
    queue_size_bytes: .value.queue.queue_size_in_bytes,
    max_queue_size: .value.queue.max_queue_size_in_bytes
}'

echo ""
echo "=== Queue Utilization ==="
logstash_stats "pipelines" | jq -r '.pipelines | to_entries[] | select(.value.queue.max_queue_size_in_bytes > 0) | "\(.key)\t\(.value.queue.queue_size_in_bytes / .value.queue.max_queue_size_in_bytes * 100 | round)% used"'
```

### JVM & Process Health

```bash
#!/bin/bash
echo "=== JVM Memory ==="
{
    logstash_stats "jvm" | jq -r '.jvm.mem | {
        heap_used_pct: .heap_used_percent,
        heap_used_mb: (.heap_used_in_bytes / 1048576 | round),
        heap_max_mb: (.heap_max_in_bytes / 1048576 | round),
        non_heap_mb: (.non_heap_used_in_bytes / 1048576 | round)
    }' &

    echo "=== GC Stats ==="
    logstash_stats "jvm" | jq -r '.jvm.gc.collectors | to_entries[] | "\(.key)\tcollections:\(.value.collection_count)\ttime:\(.value.collection_time_in_millis)ms"' &

    echo "=== Process Stats ==="
    logstash_stats "process" | jq -r '.process | {
        cpu_percent: .cpu.percent,
        open_file_descriptors: .open_file_descriptors,
        max_file_descriptors: .max_file_descriptors,
        uptime_ms: .uptime_in_millis
    }' &
}
wait
```

### Hot Threads Analysis

```bash
#!/bin/bash
echo "=== Hot Threads ==="
logstash_api "/_node/hot_threads?human=true" | head -40

echo ""
echo "=== Pipeline Workers ==="
logstash_stats "pipelines" | jq -r '.pipelines | to_entries[] | "\(.key)\tworkers:\(.value.workers)\tbatch_size:\(.value.batch_size)"'
```

## Output Format

Present results as a structured report:
```
Managing Logstash Report
════════════════════════
Resources discovered: [count]

Resource       Status    Key Metric    Issues
──────────────────────────────────────────────
[name]         [ok/warn] [value]       [findings]

Summary: [total] resources | [ok] healthy | [warn] warnings | [crit] critical
Action Items: [list of prioritized findings]
```

Target ≤50 lines of output. Use tables for multi-resource comparisons.

## Counter-Rationalizations

| Shortcut | Counter | Why |
|----------|---------|-----|
| "I'll skip discovery and check known resources" | Always run Phase 1 discovery first | Resource names change, new resources appear — assumed names cause errors |
| "The user only asked for a quick check" | Follow the full discovery → analysis flow | Quick checks miss critical issues; structured analysis catches silent failures |
| "Default configuration is probably fine" | Audit configuration explicitly | Defaults often leave logging, security, and optimization features disabled |
| "Metrics aren't needed for this" | Always check relevant metrics when available | API/CLI responses show current state; metrics reveal trends and intermittent issues |
| "I don't have access to that" | Try the command and report the actual error | Assumed permission failures prevent useful investigation; actual errors are informative |

## Common Pitfalls

- **Pipeline names**: Default pipeline is `main` — multi-pipeline setups use `pipelines.yml` for naming
- **Plugin IDs**: Auto-generated IDs are hashes — use custom `id` in config for readable names
- **Queue types**: `memory` (default, volatile), `persisted` (disk-backed, survives restarts)
- **Duration metrics**: `duration_in_millis` is cumulative total — divide by event count for per-event time
- **Filter ordering**: Filters execute in config order — a slow grok filter blocks downstream filters
- **Dead letter queue**: Failed events go to DLQ if enabled — check `/data/dead_letter_queue/`
- **Port default**: Monitoring API on port 9600 — must be enabled with `api.enabled: true`
- **JVM pressure**: If `heap_used_percent` consistently >75%, increase JVM heap or reduce batch size
