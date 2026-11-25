---
name: managing-celery
description: |
  Use when working with Celery — celery worker management, task monitoring,
  queue routing, Flower dashboard analysis, and task result tracking.
connection_type: celery
preload: false
---

# Celery Management Skill

Analyze and manage Celery task queues with safe, read-only operations.

## MANDATORY: Two-Phase Execution

**You MUST follow this two-phase pattern. Skipping Phase 1 causes hallucinated worker/task names.**

### Phase 1: Discovery (ALWAYS run first)

```bash
#!/bin/bash

# 1. List active workers
celery -A "$CELERY_APP" inspect active_queues

# 2. Worker stats
celery -A "$CELERY_APP" inspect stats

# 3. List registered tasks
celery -A "$CELERY_APP" inspect registered

# 4. Active tasks
celery -A "$CELERY_APP" inspect active

# 5. Flower API (if available)
curl -s "http://${FLOWER_HOST:-localhost}:5555/api/workers" | jq 'keys'
```

**Phase 1 outputs:**
- Active workers and their queues
- Registered task names
- Worker stats (pool size, prefetch count)

### Phase 2: Analysis (only after Phase 1)

Only reference workers, tasks, and queues confirmed in Phase 1.

## Shell Script Patterns

### Helper Function

```bash
#!/bin/bash

# Core Celery inspect helper — always use this
celery_inspect() {
    local command="$1"
    celery -A "${CELERY_APP}" inspect "$command" --json 2>/dev/null
}

# Celery control helper (read-only commands only)
celery_control() {
    local command="$1"
    celery -A "${CELERY_APP}" control "$command" --json 2>/dev/null
}

# Flower API helper
flower_api() {
    local endpoint="$1"
    curl -s "http://${FLOWER_HOST:-localhost}:${FLOWER_PORT:-5555}/api/$endpoint"
}

# Redis broker queue length (if using Redis)
redis_queue_len() {
    local queue="${1:-celery}"
    redis-cli -h "${REDIS_HOST:-localhost}" -p "${REDIS_PORT:-6379}" LLEN "$queue"
}
```

## Anti-Hallucination Rules

- **NEVER reference a task name** without confirming via `inspect registered`
- **NEVER reference a worker name** without confirming via `inspect stats` or Flower API
- **NEVER assume queue names** — always check `inspect active_queues`
- **NEVER guess task IDs** — always get from active/reserved inspection or Flower
- **NEVER assume broker type** — could be Redis, RabbitMQ, or others

## Safety Rules

- **READ-ONLY ONLY**: Use only inspect commands (stats, active, registered, reserved, scheduled, active_queues)
- **FORBIDDEN**: control commands (shutdown, pool_restart, rate_limit, revoke) without explicit user request
- **NEVER revoke tasks** without explicit user request
- **NEVER change rate limits** without explicit user request
- **Use Flower API** (GET only) for dashboard metrics

## Common Operations

### Worker Health Overview

```bash
#!/bin/bash
echo "=== Active Workers ==="
celery_inspect stats | jq 'to_entries[] | {worker: .key, pool: .value.pool, concurrency: .value.pool."max-concurrency", prefetch_count: .value.prefetch_count, total_tasks: .value.total, uptime: .value.clock}'

echo ""
echo "=== Active Queues ==="
celery_inspect active_queues | jq 'to_entries[] | {worker: .key, queues: [.value[].name]}'

echo ""
echo "=== Registered Tasks ==="
celery_inspect registered | jq 'to_entries[] | {worker: .key, tasks: .value}'

echo ""
echo "=== Worker Ping ==="
celery -A "$CELERY_APP" inspect ping --json 2>/dev/null
```

### Task Monitoring

```bash
#!/bin/bash
echo "=== Active Tasks ==="
celery_inspect active | jq 'to_entries[] | {worker: .key, tasks: [.value[] | {id, name, args: (.args | tostring | .[0:50]), time_start, worker_pid}]}'

echo ""
echo "=== Reserved Tasks (prefetched) ==="
celery_inspect reserved | jq 'to_entries[] | {worker: .key, count: (.value | length), tasks: [.value[] | {id, name}]}'

echo ""
echo "=== Scheduled Tasks (ETA/countdown) ==="
celery_inspect scheduled | jq 'to_entries[] | {worker: .key, tasks: [.value[] | {id: .request.id, name: .request.name, eta: .eta}]}'

echo ""
echo "=== Revoked Tasks ==="
celery_inspect revoked | jq 'to_entries[] | {worker: .key, revoked: .value}'
```

### Queue Depth Analysis

```bash
#!/bin/bash
echo "=== Queue Lengths (Redis broker) ==="
for QUEUE in $(celery_inspect active_queues | jq -r '.[][][].name' | sort -u); do
    LEN=$(redis_queue_len "$QUEUE" 2>/dev/null || echo "N/A")
    echo "$QUEUE: $LEN messages"
done

echo ""
echo "=== Queue Lengths (RabbitMQ broker) ==="
curl -s -u "${RMQ_USER:-guest}:${RMQ_PASSWORD:-guest}" \
    "http://${RMQ_HOST:-localhost}:15672/api/queues/%2F" 2>/dev/null | \
    jq '.[] | select(.name | test("celery|default")) | {name, messages, consumers}' 2>/dev/null || echo "RabbitMQ not available"
```

### Flower Dashboard

```bash
#!/bin/bash
echo "=== Workers (Flower) ==="
flower_api "workers" | jq 'to_entries[] | {name: .key, status: .value.status, active: (.value.active | length), completed: .value.stats.total, concurrency: .value.stats.pool."max-concurrency"}'

echo ""
echo "=== Task Types (Flower) ==="
flower_api "tasks" | jq 'to_entries | group_by(.value.name) | map({name: .[0].value.name, count: length, states: (map(.value.state) | group_by(.) | map({state: .[0], count: length}))})' 2>/dev/null

echo ""
echo "=== Recent Tasks (Flower) ==="
flower_api "tasks?limit=20" | jq 'to_entries | sort_by(-.value.received) | .[0:20] | .[] | {id: .key, name: .value.name, state: .value.state, runtime: .value.runtime, received: .value.received}'
```

## Output Format

Present results as a structured report:
```
Managing Celery Report
══════════════════════
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

- **Prefetch multiplier**: High prefetch_count causes uneven task distribution — check worker prefetch settings
- **Task serialization**: Task args must be serializable — pickle is dangerous, use JSON
- **Result backend**: Without result backend, task results are lost — check CELERY_RESULT_BACKEND
- **Worker memory leaks**: Long-running workers can leak memory — check `--max-tasks-per-child`
- **Queue routing**: Tasks without explicit routing go to default queue — check task_routes configuration
- **Visibility timeout**: Redis broker visibility timeout defaults to 1h — long tasks may be redelivered
- **Beat scheduling**: Celery Beat runs scheduled tasks — ensure only one Beat instance runs
