---
name: redis-engineer
description: Redis caching, serialization, and connection resilience
argument-hint: "[files or scope]"
agent: redis-engineer
triggers:
  - user
  - model
allowed-tools:
  - read
  - grep
  - glob
  - exec
permissions:
  allow:
    - Exec(true)
    - Exec(/bin/true)
    - Exec(/usr/bin/true)
    - Exec(cp *)
---

Review and optimize Redis integration focusing on:

1. **Connection resilience**
   - Connection pool configuration
   - Timeout settings (socket_timeout, socket_connect_timeout)
   - Retry logic and error handling
   - Health check intervals
   - Connection leak prevention

2. **Serialization patterns**
   - Proper JSON serialization (json/orjson)
   - Complex object handling
   - Deserialization error handling
   - Serialization performance

3. **Fallback strategies**
   - Local cache fallback when Redis unavailable
   - Graceful degradation
   - Error logging and monitoring
   - Automatic reconnection

4. **Performance patterns**
   - SCAN vs KEYS usage (avoid KEYS in production)
   - Pagination implementation
   - Sorted set usage for ordered data
   - Pipeline usage for bulk operations

5. **TTL management**
   - Automatic TTL on cached keys
   - TTL configuration appropriateness
   - Memory leak prevention
   - TTL check patterns

## Review Scope
$ARGUMENTS

If no scope is provided, review Redis-related files in the current working directory.

## Common Issues to Check
- KEYS command usage (should use SCAN)
- Missing TTL on cached keys
- Naked exception handling
- Connection timeout misconfiguration
- Serialization errors
- Pagination bugs in SCAN implementations

## Output Format
Provide a structured report with:
- File paths and line numbers for each issue
- Severity levels (critical, warning, info)
- Specific Redis best practice violations
- Code examples of correct patterns
- Performance improvement recommendations
- Priority-ordered action items
