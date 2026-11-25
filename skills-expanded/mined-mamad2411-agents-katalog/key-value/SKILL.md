---
name: key-value
description: Key-value data model, distributed caching, and in-memory stores
license: MIT
compatibility: opencode
metadata:
  audience: developers
  category: databases
---

## What I do
- Design key-value schemas and data models
- Implement caching strategies and policies
- Optimize for low-latency access patterns
- Work with distributed hash tables
- Handle data partitioning and replication

## When to use me
When building high-performance applications requiring fast lookups, caching layers, session stores, or distributed caching systems.

## Key Concepts

### Data Modeling
- Key design patterns (natural keys, composite keys)
- Value serialization (JSON, protobuf, msgpack)
- Time-to-live (TTL) and expiration
- Namespace and prefix patterns

### Caching Strategies
- Cache-aside (lazy loading)
- Write-through caching
- Write-back caching
- Cache invalidation patterns
- Bloom filters for cache miss reduction

### Distributed Key-Value
- Consistent hashing
- Data partitioning (sharding)
- Replication strategies
- CAP theorem trade-offs
- CRDTs for conflict resolution

### Performance Optimization
- In-memory vs disk-backed stores
- Data structure choices (B-trees, LSM trees, hash tables)
- Connection pooling
- Batch operations
- Compression

## Common Use Cases
- Session storage
- Caching layer
- Configuration stores
- Rate limiting
- Leader election
- Distributed locks

## Tools & Technologies
- Redis, Memcached
- etcd, Consul
- DynamoDB, Cassandra
- Riak, CockroachDB
