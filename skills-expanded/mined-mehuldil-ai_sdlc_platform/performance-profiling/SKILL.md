# Backend Performance Profiling

---
name: backend-performance-profiling
description: Performance analysis for Java/TEJ backend services
model: sonnet-4-6
token_budget: {input: 6000, output: 2000}
---

## Overview

Analyzes Java/TEJ Spring backend services for performance bottlenecks, latency issues, database query inefficiencies, resource utilization problems, and throughput constraints.

## Performance Analysis Areas

### 1. API Latency Analysis

#### P50/P95/P99 Latency Targets
Compare actual latencies against Non-Functional Requirements (NFR):

```
API Endpoint Benchmarks (typical targets):
- Authentication endpoints: P50 < 100ms, P99 < 500ms
- Read-only GET: P50 < 200ms, P99 < 1000ms
- Create operations: P50 < 300ms, P99 < 1500ms
- Batch operations: P50 < 2000ms, P99 < 5000ms
- Search/filter: P50 < 500ms, P99 < 2000ms (depends on data volume)
```

#### Sources of Latency
- **Slow database queries**: Missing indexes, N+1 problem, complex joins
- **External API calls**: Unoptimized HTTP clients, missing timeouts
- **Synchronous operations**: Blocking calls that should be async
- **Large response payloads**: Serialization overhead, missing pagination
- **Resource contention**: Thread pool exhaustion, connection pool limits

#### Detection Methods
1. Request log analysis:
   - Identify slowest endpoints
   - Find outlier response times
   - Correlate slow requests with resource metrics

2. Application metrics (Spring Boot Actuator, Micrometer):
   - http.server.requests duration
   - Filter by uri, method, status
   - Extract p50, p95, p99 percentiles

3. APM Integration (if available):
   - New Relic, DataDog, Jaeger traces
   - End-to-end request tracking
   - Database time vs. application time breakdown

---

### 2. Database Query Analysis

#### N+1 Query Problem
**Symptom**: One parent query triggers N queries for child data

```java
// WRONG - N+1 problem
List<User> users = userRepository.findAll(); // 1 query
for (User user : users) {
    List<Post> posts = user.getPosts(); // N queries (lazy loading)
}
```

**Detection**:
- Count queries: Look for query count = 1 + N
- Check logs for repeated similar queries in tight loops
- Identify lazy-loaded collections without explicit fetch strategy

**Solution**:
```java
// Correct - eager load or batch fetch
@Query("SELECT u FROM User u LEFT JOIN FETCH u.posts")
List<User> findAllWithPosts();

// Or use JPA hints
@EntityGraph(attributePaths = {"posts"})
List<User> findAll();
```

#### Missing Indexes
**Symptom**: Full table scans on frequently filtered columns

**Check patterns**:
- WHERE clauses on non-indexed columns
- ORDER BY on unindexed columns
- JOIN conditions without indexes
- LIKE queries without leading character

**Example issue**:
```sql
-- Slow: Full table scan
SELECT * FROM users WHERE created_at > '2024-01-01' ORDER BY created_at;

-- Solution: Create index
CREATE INDEX idx_users_created_at ON users(created_at);
```

#### Slow Queries (> 100ms)
**Detection**:
1. Enable query logging:
   ```properties
   spring.jpa.properties.hibernate.generate_statistics=true
   logging.level.org.hibernate.stat.StatisticsFactory=DEBUG
   ```

2. Look for:
   - Complex joins (4+ tables)
   - Subqueries in WHERE clause
   - Missing LIMIT in aggregate queries
   - SELECT * when only few columns needed

#### Query Optimization Patterns

| Pattern | Problem | Solution |
|---------|---------|----------|
| `SELECT * FROM ...` | Retrieves all columns | Select specific columns: `SELECT id, name FROM ...` |
| `WHERE col LIKE '%text'` | Can't use index | Use `LIKE 'text%'` or full-text search |
| `WHERE DATE(col) = X` | Can't use index | Use `WHERE col BETWEEN ... AND ...` |
| Join without ON clause | Cartesian product | Add proper ON condition |
| Subquery in SELECT | Executed for each row | Use JOIN instead |

---

### 3. Connection Pool Analysis

#### HikariCP Configuration Validation

```properties
# Check these settings in application.properties:
spring.datasource.hikari.maximum-pool-size=20    # Default is 10
spring.datasource.hikari.minimum-idle=5          # At least 5
spring.datasource.hikari.connection-timeout=30000 # 30 seconds
spring.datasource.hikari.idle-timeout=600000     # 10 minutes
spring.datasource.hikari.max-lifetime=1800000    # 30 minutes
```

#### Pool Sizing Formula
```
Recommended pool size = (core_count * 2) + effective_spindle_count

For typical web app:
- 4 cores → pool size of 8-10
- 8 cores → pool size of 16-20
- 16 cores → pool size of 32-40
```

#### Issues to Check
- Pool exhaustion (all connections in use)
- Long wait times for connection
- Connection leaks (connections not returned)
- Idle connections timeout too quickly

**Detection**:
```
Metric: hikaricp.connections{pool="HikariPool-1"}
- hikaricp.connections: total active connections
- hikaricp.connections.pending: waiting for connection
- If pending > 0 for sustained time → pool too small
```

---

### 4. Memory Profiling

#### Heap Usage Analysis
Check for:
- **Memory leaks**: Heap size grows over time
- **Large object allocations**: Spikes in memory usage
- **GC pressure**: Frequent full garbage collections

**Metrics**:
```
jvm.memory.used[area=heap]         # Current heap usage
jvm.memory.max[area=heap]          # Max available heap
jvm.gc.memory.promoted             # Objects surviving GC
jvm.gc.pause                       # GC pause duration (should be <100ms)
```

#### Garbage Collection Patterns
- **Young GC (minor)**: Should be fast, < 50ms
- **Full GC (major)**: Minimize frequency, < 1 per minute
- **Stop-the-world time**: Should be < 500ms total

**Red flags**:
- Full GC every < 5 minutes
- Individual GC pause > 500ms
- Heap never drops below 80% (memory leak indicator)

#### Common Memory Issues
- Large response caches without eviction
- Unbounded collections (no max size)
- StringBuilder/string concatenation in loops
- Circular object references preventing GC

---

### 5. Kafka Throughput Analysis

#### Producer Metrics
```
kafka.producer.records.sent      # Messages sent/sec
kafka.producer.record.send.total.time.ms  # Message send latency
kafka.producer.batch.size        # Batch sizes
```

Check:
- Throughput meets requirements (msgs/sec)
- Latency acceptable for use case
- No producer errors or timeouts

#### Consumer Metrics
```
kafka.consumer.lag                    # How far behind the latest message
kafka.consumer.records.consumed       # Messages consumed/sec
kafka.consumer.commit.latency.avg     # Offset commit latency
```

Issues to identify:
- **Consumer lag growing**: Consumer slower than producer
- **Unbalanced partitions**: Some consumers idle while others overloaded
- **Frequent rebalancing**: Hanging the consumer group

#### Remediation
- Increase consumer threads (one per partition max)
- Batch processing: `max.poll.records`
- Connection pooling: `connections.max.idle.ms`
- Partition reassignment if imbalanced

---

### 6. Thread Pool Analysis

#### Executor Configuration
Check ThreadPoolExecutor settings:

```java
// Verify these metrics
@Bean
public Executor asyncExecutor() {
    ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
    executor.setCorePoolSize(5);           // Base threads
    executor.setMaxPoolSize(20);           // Max threads
    executor.setQueueCapacity(100);        // Queue size before rejection
    executor.setThreadNamePrefix("async-"); // For logging
    executor.initialize();
    return executor;
}
```

**Metrics to monitor**:
```
executor.active    # Currently executing tasks
executor.queued    # Waiting in queue
executor.pool.size # Total threads created
```

#### Issues to Check
- **Thread pool exhaustion**: active + queued > max capacity
- **Blocking operations**: Synchronous I/O in async pool
- **Rejected tasks**: Tasks rejected due to full queue
- **Deadlocks**: Circular waiting for threads

#### Optimal Sizing
```
Core threads = CPU count
Max threads = CPU count * 2 to 4
Queue capacity = max_threads * 2 to 4
```

---

### 7. JMeter Load Testing Integration

#### Test Plan Structure
```
Thread Group (simulate N concurrent users)
├── HTTP Request Sampler (GET /api/users)
├── HTTP Request Sampler (POST /api/users)
└── Listeners
    ├── Summary Report
    ├── Response Time Graph
    └── Aggregate Report
```

#### Load Testing Scenarios
1. **Baseline**: 10 users, 5 min ramp-up, 10 min test
2. **Load**: 50 users, measure P50/P95/P99
3. **Stress**: 200+ users until failure point
4. **Endurance**: 25 users for 1-2 hours, check for leaks

#### Key Metrics to Capture
- Response time (min/avg/max/P95/P99)
- Throughput (requests/sec)
- Error rate
- GC pauses during test
- CPU/memory usage

---

## Performance Report Format

```
# Backend Performance Analysis Report

## Executive Summary
- Overall Performance: [EXCELLENT | GOOD | ACCEPTABLE | POOR]
- Key Finding: [Brief summary of worst issue]
- Recommendation: [Primary action item]

## API Latency Analysis
### Critical Endpoints
| Endpoint | P50 | P95 | P99 | NFR Target | Status |
|----------|-----|-----|-----|------------|--------|
| GET /api/users | 150ms | 450ms | 800ms | <200ms / <1000ms | EXCEED |
| POST /api/users | 250ms | 600ms | 1200ms | <300ms / <1500ms | MEET |

### Issues Found
1. **High latency on GET /api/users**
   - Root cause: N+1 query for user posts
   - Impact: 50% slower than baseline
   - Fix: Add @EntityGraph fetch strategy

## Database Performance
### Query Analysis
- Total queries in sample: 1250
- Queries > 100ms: 23 (slow queries)
- N+1 detected: 3 locations
- Missing indexes: 2 columns

### Top Slow Queries
1. SELECT u FROM User u JOIN u.posts - 450ms avg
2. SELECT * FROM orders WHERE created_at > ? - 320ms
3. ... (more details)

## Connection Pool
- Pool size: 10 (recommended: 16-20)
- Active connections: 8 of 10 (peak)
- Connection wait time: < 10ms
- Status: ADEQUATE (consider increasing to 16)

## Memory Analysis
- Heap usage: 1.2GB of 2GB
- GC frequency: 2 minor GCs/min
- Major GC: None in 30 min test
- Memory leak risk: LOW

## Kafka Analysis
- Producer throughput: 5000 msgs/sec
- Consumer lag: < 100 messages
- Partition balance: Even distribution
- Status: HEALTHY

## Thread Pool Analysis
- Active threads: 5 of 20
- Queued tasks: 0
- Rejected tasks: 0
- Status: HEALTHY

## Recommendations
1. [URGENT] Increase connection pool from 10 to 20
2. [HIGH] Fix N+1 query in UserService
3. [MEDIUM] Add index on orders.created_at
4. [LOW] Monitor heap usage for growth trends

## Test Data
- Load test: 50 concurrent users for 10 minutes
- Sample queries: 5000+
- Peak latency: 1.8 seconds
- Error rate: < 0.1%
```

## Related Skills
- [backend-security-scan](../security-scan/SKILL.md) - Security analysis
- [qa-orchestrator](../../qa/qa-orchestrator.md) - Full QA coordination
