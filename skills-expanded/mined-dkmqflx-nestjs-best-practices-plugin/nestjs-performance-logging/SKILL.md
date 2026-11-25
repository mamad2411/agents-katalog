---
name: nestjs-performance-logging
description: NestJS performance and logging/observability best practices. Use when optimizing a NestJS app's throughput or adding structured logging, health checks, or graceful shutdown. Triggers on FastifyAdapter, compression, pino logger, health checks, Terminus, or graceful shutdown.
license: MIT
metadata:
  author: nestjs
  version: "1.0.0"
---

# NestJS Performance & Logging

Practical rules for squeezing throughput out of a NestJS app and making it observable in production: structured logs, correlation IDs, health checks, and clean shutdown.

## When to Apply

- Optimizing request throughput or latency of a NestJS HTTP service
- Replacing `console.log` with production-grade structured logging
- Running in Kubernetes/ECS where readiness/liveness probes and graceful drain matter
- Tracing requests across services or debugging incidents from logs
- Hardening logs so secrets, tokens, and PII never leak

## Rules

- `fastify-adapter-for-throughput` - Prefer FastifyAdapter over Express for higher throughput.
- `enable-compression` - Gzip response payloads to cut bandwidth and latency.
- `structured-json-logging` - Use nestjs-pino for structured JSON logs instead of console.log.
- `avoid-request-scoped-providers` - REQUEST scope re-instantiates per request; keep singletons.
- `graceful-shutdown-hooks` - enableShutdownHooks + OnModuleDestroy to drain cleanly.
- `health-checks-terminus` - Expose @nestjs/terminus health/readiness endpoints for orchestrators.
- `correlation-ids` - Propagate a request/correlation ID through every log line.
- `dont-log-sensitive-data` - Redact secrets, tokens, and PII from logs.

## How to Use

Load this skill when working on NestJS performance or observability. Skim the Rules index, open the relevant `rules/<name>.md` for the why plus an incorrect/correct code pair, and apply the pattern. Rules are tagged by impact (CRITICAL/HIGH/MEDIUM/LOW) so you can prioritize.
