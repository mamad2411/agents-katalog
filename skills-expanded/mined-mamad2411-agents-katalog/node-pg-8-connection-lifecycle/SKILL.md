---
name: node-pg-8-connection-lifecycle
description: Designs and reviews secure Node pg 8.x Pool and Client setup, TLS configuration, health checks, shutdown, and connection lifecycle behavior. Use when connecting to or closing PostgreSQL connections.
license: MIT
compatibility: Node applications using Node pg 8.x.
---

# Node pg 8 Connection Lifecycle

This skill guides safe setup and shutdown of PostgreSQL connections in Node `pg` 8.x applications.

## When to Use

Use this skill when the task involves:

- creating a `Pool` or `Client`
- configuring `DATABASE_URL`, `PGHOST`, `PGUSER`, TLS, or timeouts
- adding health checks
- writing scripts or workers that must close connections
- fixing hanging tests or processes
- handling database failover or idle client errors

## Core Guidance

1. Prefer a shared `Pool` for long-running services.
2. Use `Client` for short-lived scripts only when pooling is unnecessary.
3. Keep pool creation in one module.
4. Configure timeouts and TLS explicitly.
5. Add idle error handling on the pool.
6. Close pools during graceful shutdown and test teardown.
7. Never log secrets or full connection strings.

## Workflows

Use `workflows/configure-pg-connection-workflow.md` when setting up or reviewing database connection lifecycle.

## Resources

Use `resources/connection-config-checklist.md` before finalizing pool or client configuration.

## Examples

Use `examples/pool-module-example.md` for a shared pool module pattern.

## Script Guidance

This skill has no scripts.
