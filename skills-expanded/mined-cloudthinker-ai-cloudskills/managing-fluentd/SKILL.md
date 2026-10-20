---
name: managing-fluentd
description: |
  Use when working with Fluentd — fluentd log collector management with plugin
  status, buffer monitoring, routing rule analysis, match/filter configuration,
  and input health. Covers pipeline analysis, buffer overflow detection, retry
  monitoring, and configuration validation. Use when managing Fluentd plugins,
  analyzing buffer health, reviewing routing rules, or troubleshooting log
  pipelines.
connection_type: fluentd
preload: false
---

# Fluentd Management Skill

Monitor and manage Fluentd log collection pipelines via the monitoring API.

## API Conventions

### Authentication
Fluentd monitoring API is typically unauthenticated (local access) or uses reverse proxy auth.

### Base URL
- Monitor API: `http://<host>:24220/api/`
- RPC: `http://<host>:24444/api/`
- Use connection-injected `FLUENTD_BASE_URL`.

### Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Use `jq` to extract only needed fields
- NEVER dump full plugin listings — summarize by type and status

### Core Helper Function

```bash
#!/bin/bash

fluentd_api() {
    local endpoint="$1"
    curl -s "${FLUENTD_BASE_URL}/api${endpoint}"
}

fluentd_rpc() {
    local action="$1"
    curl -s "${FLUENTD_RPC_URL:-${FLUENTD_BASE_URL}}/api/${action}"
}

fluentd_config() {
    local config_path="${1:-/etc/fluent/fluent.conf}"
    cat "$config_path" 2>/dev/null
}
```

## Parallel Execution

```bash
{
    fluentd_api "/plugins.json" &
    fluentd_api "/config" &
    fluentd_api "/uptime" &
}
wait
```

## Anti-Hallucination Rules

**NEVER assume plugin names, tag patterns, or buffer configurations. ALWAYS discover first.**

### Phase 1: Discovery

```bash
#!/bin/bash
echo "=== Fluentd Plugins ==="
fluentd_api "/plugins.json" \
    | jq -r '.plugins[] | "\(.type)\t\(.plugin_category)\t\(.plugin_id // "unnamed")\t\(.output_plugin ? // "")"' \
    | head -20

echo ""
echo "=== Plugin Categories ==="
fluentd_api "/plugins.json" \
    | jq -r '.plugins | group_by(.plugin_category) | .[] | "\(.[0].plugin_category): \(length)"'

echo ""
echo "=== Fluentd Uptime ==="
fluentd_api "/uptime" | jq '.'
```

## Common Operations

### Plugin Health Overview

```bash
#!/bin/bash
echo "=== Plugin Summary ==="
fluentd_api "/plugins.json" | jq -r '
    .plugins | group_by(.plugin_category) | .[] |
    "\(.[0].plugin_category):",
    (.[] | "  \(.plugin_id // .type)\t\(.type)\tretry:\(.retry_count // 0)")
' | head -30

echo ""
echo "=== Plugins with Errors ==="
fluentd_api "/plugins.json" \
    | jq -r '.plugins[] | select(.retry_count > 0 or .buffer_total_queued_size > 0) | "\(.plugin_id // .type)\tretries:\(.retry_count)\tqueued:\(.buffer_total_queued_size // 0)"'
```

### Buffer Status Monitoring

```bash
#!/bin/bash
echo "=== Buffer Status ==="
fluentd_api "/plugins.json" \
    | jq -r '.plugins[] | select(.buffer_total_queued_size != null) | {
        plugin: (.plugin_id // .type),
        queued_size: .buffer_total_queued_size,
        queue_length: .buffer_queue_length,
        available_buffer: .buffer_available_buffer_space_ratios,
        retry_count: .retry_count
    }' | head -30

echo ""
echo "=== Buffer Overflow Risk ==="
fluentd_api "/plugins.json" \
    | jq -r '.plugins[] | select(.buffer_available_buffer_space_ratios != null and .buffer_available_buffer_space_ratios < 20) | "WARNING: \(.plugin_id // .type) buffer at \(.buffer_available_buffer_space_ratios)% available"'

echo ""
echo "=== Total Buffer Queue ==="
fluentd_api "/plugins.json" \
    | jq '[.plugins[] | .buffer_total_queued_size // 0] | add | "Total queued: \(. / 1048576 | . * 100 | round / 100)MB"' -r
```

### Routing Rules Analysis

```bash
#!/bin/bash
echo "=== Match Rules (Output Routing) ==="
CONFIG_PATH="${1:-/etc/fluent/fluent.conf}"

if [ -f "$CONFIG_PATH" ]; then
    grep -E "^<match|^  @type|^  tag|^</match>" "$CONFIG_PATH" | head -30
else
    echo "Config not accessible locally. Using API:"
    fluentd_api "/plugins.json" \
        | jq -r '.plugins[] | select(.plugin_category == "output") | "\(.plugin_id // .type)\tpattern:\(.tag_pattern // "N/A")\ttype:\(.type)"'
fi

echo ""
echo "=== Filter Chain ==="
fluentd_api "/plugins.json" \
    | jq -r '.plugins[] | select(.plugin_category == "filter") | "\(.plugin_id // .type)\ttype:\(.type)"'
```

### Input Health

```bash
#!/bin/bash
echo "=== Input Plugins ==="
fluentd_api "/plugins.json" \
    | jq -r '.plugins[] | select(.plugin_category == "input") | "\(.plugin_id // .type)\ttype:\(.type)\t\(.emit_records // 0) records"'

echo ""
echo "=== Input Throughput ==="
fluentd_api "/plugins.json" \
    | jq -r '.plugins[] | select(.plugin_category == "input" and .emit_records != null) | "\(.plugin_id // .type)\t\(.emit_records) total records\t\(.emit_size // 0) bytes"' \
    | sort -t$'\t' -k2 -rn | head -10
```

### Configuration Validation

```bash
#!/bin/bash
CONFIG_PATH="${1:-/etc/fluent/fluent.conf}"

echo "=== Configuration Sections ==="
if [ -f "$CONFIG_PATH" ]; then
    echo "--- Sources ---"
    grep -c "^<source>" "$CONFIG_PATH" | xargs -I{} echo "{} source(s)"
    echo "--- Matches ---"
    grep -c "^<match" "$CONFIG_PATH" | xargs -I{} echo "{} match(es)"
    echo "--- Filters ---"
    grep -c "^<filter" "$CONFIG_PATH" | xargs -I{} echo "{} filter(s)"

    echo ""
    echo "--- Plugin Types Used ---"
    grep "@type" "$CONFIG_PATH" | awk '{print $2}' | sort | uniq -c | sort -rn
else
    echo "Config file not accessible at $CONFIG_PATH"
fi

echo ""
echo "=== Validation ==="
fluentd --dry-run -c "$CONFIG_PATH" 2>&1 | tail -5
```

## Output Format

Present results as a structured report:
```
Managing Fluentd Report
═══════════════════════
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

- **Monitor plugin required**: The monitoring API requires `<source> @type monitor_agent` in config — not enabled by default
- **Port defaults**: Monitor agent=24220, forward input=24224, RPC=24444
- **Buffer types**: `file` buffers persist across restarts, `memory` buffers do not — know which is configured
- **Retry backoff**: Exponential retry can hide failures — check `retry_count` alongside `buffer_queue_length`
- **Tag routing**: Match rules are evaluated in order — first match wins, unmatched tags are dropped
- **Config includes**: `@include` directives may load external files — check all included configs
- **Worker processes**: Multi-worker mode splits processing — metrics are per-worker
- **Graceful shutdown**: Use `fluentd_rpc "processes.flushBuffersAndKillWorkers"` for graceful stop — do NOT kill process
