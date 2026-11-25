---
name: redis-7-production-ops
description: Reviews Redis 7 configuration, persistence, memory, eviction, replication, health checks, incidents, and operational readiness. Use when working with redis.conf, Docker Redis, diagnostics, latency, memory pressure, or production runbooks.
license: MIT
compatibility: Requires Redis Open Source 7.x and optional redis-cli for scripts.
---

# Redis 7 Production Operations

Use this skill for Redis 7 configuration review, operational readiness, and incident triage.

## Workflows

- `workflows/config-review-workflow.md`: Use when reviewing `redis.conf`, container Redis config, runtime config, persistence, memory, and operational guardrails.
- `workflows/incident-triage-workflow.md`: Use when Redis is slow, unavailable, evicting unexpectedly, using too much memory, or showing replication/persistence issues.

## Resources

- `resources/redis-conf-review-checklist.md`: Redis 7 configuration review checklist.

## Examples

- `examples/docker-compose-redis-7.yml`: Local/staging Docker Compose example.
- `examples/redis-7-production-baseline.conf`: Baseline config example that must be adapted before production.

## Scripts

- `scripts/redis-7-config-check.sh`: Static Redis config review helper.
- `scripts/redis-7-health-check.sh`: Read-only Redis health check helper.

Run scripts with `--help` before using them.

## Operating Principles

- Prefer config files for durable Redis configuration.
- Avoid runtime-only config changes unless they are part of an incident runbook and are persisted or intentionally temporary.
- Treat persistence, replication, eviction, and maxmemory as workload-specific decisions.
- Collect evidence with read-only commands before changing Redis state.
- Do not run destructive commands without backup context and explicit human approval.
- Separate local, staging, and production Redis credentials and endpoints.
- Do not assume managed Redis providers expose every Redis command.

## Safe Read-Only Diagnostics

Prefer these first during triage when permitted by ACLs:

```text
PING
INFO server
INFO clients
INFO memory
INFO persistence
INFO stats
INFO replication
INFO commandstats
SLOWLOG LEN
SLOWLOG GET <small-count>
LATENCY LATEST
CLIENT LIST
ROLE
CONFIG GET maxmemory
CONFIG GET maxmemory-policy
CONFIG GET appendonly
CONFIG GET save
```

## Dangerous Operations

Require explicit approval before:

```text
FLUSHALL
FLUSHDB
SHUTDOWN
CONFIG SET
CONFIG REWRITE
MODULE LOAD
MODULE UNLOAD
SCRIPT FLUSH
FUNCTION FLUSH
FUNCTION DELETE
DEBUG
CLUSTER RESET
REPLICAOF NO ONE
SLAVEOF NO ONE
```
