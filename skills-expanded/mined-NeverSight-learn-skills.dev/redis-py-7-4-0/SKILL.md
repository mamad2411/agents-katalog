---
name: redis-py-7-4-0
description: Comprehensive Python client for Redis database and key-value store. Use when building Python applications requiring Redis connectivity, including standalone, cluster, sentinel, and async modes with support for all Redis commands, pipelines, pub/sub, Lua scripting, Redis modules (JSON, Search, TimeSeries), RESP3, client-side caching, connection pooling, and distributed locking.
license: MIT
author: Tangled <noreply@tangledgroup.com>
version: "0.1.0"
tags:
  - redis
  - database
  - key-value-store
  - caching
  - async
  - clustering
  - pubsub
  - pipelines
  - lua-scripting
category: database
external_references:
  - https://redis.readthedocs.io/en/latest
  - https://github.com/redis/redis-py
---

# redis-py 7.4

## Overview

redis-py is the official Python client for Redis, the in-memory data store. Version 7.4 supports Python 3.10+ and works with Redis 7.2 through 8.2. It provides a complete Python interface to all Redis commands, including support for standalone, cluster, and sentinel deployments, both synchronous and asynchronous (asyncio) modes, pipelines, pub/sub, Lua scripting, distributed locking, retry logic with configurable backoff strategies, RESP3 protocol features including client-side caching, native OpenTelemetry metrics integration, and access to Redis modules (Bloom, Cuckoo, Count-Min Sketch, TopK, JSON, Search, TimeSeries).

Key capabilities:

- Full Redis command coverage via `CoreCommands` mixin
- Async support through `redis.asyncio`
- Cluster mode via `redis.cluster.RedisCluster`
- Connection pooling with configurable retry and backoff
- Pipeline batching for reduced round-trips
- Pub/Sub messaging
- Lua scripting with automatic cache management
- Distributed locking (`redis.lock.Lock`)
- RESP3 protocol (default from redis-py 8.0+)
- Client-side caching
- Native OpenTelemetry metrics
- Credential providers for dynamic authentication
- SSL/TLS connections with OCSP validation

## When to Use

- Building Python applications that need Redis connectivity for caching, session storage, or message brokering
- Implementing async Redis clients with `asyncio`
- Working with Redis Cluster deployments requiring automatic slot-based routing
- Batching commands through pipelines for performance optimization
- Setting up pub/sub messaging patterns
- Running Lua scripts atomically on the Redis server
- Implementing distributed locks across processes or machines
- Integrating OpenTelemetry observability into Redis-dependent services
- Using Redis modules for probabilistic data structures, JSON operations, full-text search, or time series
- Configuring retry logic with exponential backoff for resilient connections

## Core Concepts

**Client instances are thread-safe** — `Redis` objects can be shared across threads. Connections are retrieved from the pool during command execution and returned immediately after. However, `PubSub` and `Pipeline` objects are not thread-safe.

**Connection pools** — Each `Redis` instance owns its own `ConnectionPool` by default. Share pools across clients using the `connection_pool` parameter, or use `Redis.from_pool()` for exclusive ownership.

**Response decoding** — By default, responses are returned as bytes. Set `decode_responses=True` to receive decoded strings.

**Protocol versions** — RESP3 is the default from redis-py 8.0+. Use `protocol=3` for RESP3 or `protocol=2` for RESP2 on earlier versions. RESP3 provides better performance with fewer type translations and supports new response types (doubles, maps, booleans, push notifications).

**SELECT command not exposed** — redis-py does not implement `SELECT` on client instances because it creates pool contamination. Use separate `Redis` instances (and pools) per database.

## Advanced Topics

**Connecting to Redis**: Connection methods, URL schemes, SSL/TLS, credential providers, connection pools → [Connecting to Redis](reference/01-connecting-to-redis.md)

**Async Support**: Asyncio client patterns, async pipelines, pub/sub, and connection lifecycle → [Async Support](reference/02-async-support.md)

**Cluster Mode**: Redis Cluster client, target nodes, cluster pipelines, and multi-key commands → [Cluster Mode](reference/03-cluster-mode.md)

**Pipelines and Transactions**: Command batching, WATCH/MULTI/EXEC patterns, and the transaction helper → [Pipelines and Transactions](reference/04-pipelines-and-transactions.md)

**Pub/Sub and Streams**: Channel subscription, pattern matching, stream operations, and consumer groups → [Pub/Sub and Streams](reference/05-pubsub-and-streams.md)

**Lua Scripting**: Script registration, EVAL/EVALSHA, pipeline integration, and cluster limitations → [Lua Scripting](reference/06-lua-scripting.md)

**Distributed Locking**: The `Lock` class, acquire/release patterns, extension, and ownership checks → [Distributed Locking](reference/07-distributed-locking.md)

**Retry and Backoff**: Retry strategies, backoff algorithms, cluster retry behavior → [Retry and Backoff](reference/08-retry-and-backoff.md)

**RESP3 Features**: Push notifications, client-side caching, response unification → [RESP3 Features](reference/09-resp3-features.md)

**OpenTelemetry Integration**: Native metrics collection, OTelConfig, metric groups → [OpenTelemetry Integration](reference/10-opentelemetry.md)

**Redis Modules**: Bloom/Cuckoo filters, JSON, Search, TimeSeries commands → [Redis Modules](reference/11-redis-modules.md)

**Exceptions**: Error types, cluster-specific errors, and handling patterns → [Exceptions](reference/12-exceptions.md)
