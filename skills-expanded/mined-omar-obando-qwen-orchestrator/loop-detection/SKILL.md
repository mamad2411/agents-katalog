---
name: loop-detection
description: Use when identifying and preventing infinite loops, detecting loop patterns, implementing loop exit strategies, and creating loop safety mechanisms. Includes loop analysis, timeout patterns, and loop monitoring. Based on programming best practices and loop safety patterns.
license: MIT
---

# Loop Detection Skill — Monitor & Loop Guardian

## Overview

This skill provides comprehensive guidance for detecting and preventing infinite loops. It covers loop pattern identification, exit strategy implementation, timeout patterns, and loop monitoring following programming best practices and loop safety patterns.

## When to Use

**Use this skill when:**

- Identifying potential infinite loops in code
- Detecting loop patterns in algorithms
- Implementing loop exit strategies
- Adding timeout mechanisms to loops
- Creating loop safety guards
- Analyzing loop termination conditions
- Implementing loop counters
- Creating loop monitoring
- Detecting loop stagnation
- Implementing loop backoff strategies
- Creating loop retry mechanisms
- Adding loop progress tracking
- Implementing loop cancellation
- Creating loop documentation
- Analyzing loop performance
- Detecting loop resource leaks
- Implementing loop limits
- Creating loop validation
- Detecting loop edge cases
- Implementing loop error handling
- Creating loop optimization strategies
- Adding loop logging
- Implementing loop health checks

**Do NOT use this skill when:**

- Writing application business logic (use domain-driven skill)
- Designing database schemas (use database-design skill)
- Writing API endpoint specifications (use api-design skill)
- Performing security audits (use security-auditor skill)
- Writing SQL queries (use sql-best-practices skill)
- Designing multi-page website layouts (use design-system skill)
- Analyzing deployment configurations (use deployment skill)
- Writing documentation (use documentation-best-practices skill)

## Loop Patterns

### Common Loop Patterns

```
┌─────────────────────────────────────────────────────────────┐
│              Loop Patterns                                  │
├─────────────────────────────────────────────────────────────┤
│  While Loop:                                                │
│  while condition:                                           │
│      # Loop body                                            │
│      # Must modify condition                                │
│                                                              │
│  For Loop:                                                  │
│  for i in range(n):                                         │
│      # Loop body                                            │
│      # Uses counter or iterator                             │
│                                                              │
│  Do-While Loop:                                             │
│  do {                                                       │
│      # Loop body                                            │
│  } while (condition);                                       │
│                                                              │
│  Nested Loop:                                               │
│  for i in range(n):                                         │
│      for j in range(m):                                     │
│          # Nested loop body                                 │
│                                                              │
│  Infinite Loop:                                             │
│  while true:                                                │
│      # Must have break condition                            │
│      if exit_condition:                                     │
│          break                                              │
└─────────────────────────────────────────────────────────────┘
```

### Loop Exit Strategies

```
┌─────────────────────────────────────────────────────────────┐
│              Loop Exit Strategies                           │
├─────────────────────────────────────────────────────────────┤
│  1. Counter-Based:                                          │
│     for i in range(max_iterations):                         │
│         if condition:                                       │
│             break                                           │
│                                                              │
│  2. Condition-Based:                                        │
│     while not done:                                         │
│         if success:                                         │
│             done = True                                     │
│                                                              │
│  3. Timeout-Based:                                          │
│     start_time = time.now()                                 │
│     while time.now() - start_time < timeout:                │
│         if condition:                                       │
│             break                                           │
│                                                              │
│  4. State-Based:                                            │
│     while state != 'completed':                             │
│         state = update_state(state)                         │
│                                                              │
│  5. Resource-Based:                                         │
│     while resources_available():                            │
│         process_resource()                                  │
└─────────────────────────────────────────────────────────────┘
```

## Loop Safety Mechanisms

### Timeout Pattern

```python
# ✅ Good: Timeout-based loop
import time

def process_with_timeout(max_duration=30):
    start_time = time.time()
    while not task_completed():
        if time.time() - start_time > max_duration:
            raise TimeoutError("Loop timed out")
        time.sleep(0.1)
```

### Counter Pattern

```python
# ✅ Good: Counter-based loop
def process_with_max_iterations(max_iterations=1000):
    count = 0
    while not task_completed():
        if count >= max_iterations:
            raise RuntimeError("Max iterations reached")
        count += 1
        process_iteration()
```

### Backoff Pattern

```python
# ✅ Good: Exponential backoff
import time

def retry_with_backoff(max_retries=5, base_delay=1):
    for attempt in range(max_retries):
        try:
            return perform_task()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            delay = base_delay * (2 ** attempt)
            time.sleep(delay)
```

## Loop Detection Techniques

### Static Analysis

```
┌─────────────────────────────────────────────────────────────┐
│              Static Analysis                                │
├─────────────────────────────────────────────────────────────┤
│  Check for:                                                 │
│  - Missing loop termination condition                       │
│  - Loop variable not updated                                │
│  - Condition always true                                    │
│  - No break statements                                      │
│  - Infinite recursion in loops                              │
│                                                              │
│  Tools:                                                     │
│  - Linters (ESLint, Pylint)                                 │
│  - Static analysis tools (SonarQube)                        │
│  - IDE warnings                                             │
└─────────────────────────────────────────────────────────────┘
```

### Dynamic Analysis

```
┌─────────────────────────────────────────────────────────────┐
│              Dynamic Analysis                               │
├─────────────────────────────────────────────────────────────┤
│  Monitor at runtime:                                        │
│  - Loop iteration count                                     │
│  - Execution time                                           │
│  - Resource usage                                           │
│  - State changes                                            │
│                                                              │
│  Techniques:                                                │
│  - Add counters to loops                                    │
│  - Log loop progress                                        │
│  - Monitor memory usage                                     │
│  - Track execution time                                     │
└─────────────────────────────────────────────────────────────┘
```

### Loop Health Monitoring

```
┌─────────────────────────────────────────────────────────────┐
│              Loop Health Monitoring                         │
├─────────────────────────────────────────────────────────────┤
│  Metrics:                                                   │
│  - Iteration count                                          │
│  - Duration per iteration                                   │
│  - Total loop duration                                      │
│  - Memory usage per iteration                               │
│  - CPU usage per iteration                                  │
│                                                              │
│  Alerts:                                                    │
│  - Iteration limit exceeded                                 │
│  - Duration threshold exceeded                              │
│  - Resource usage spike                                     │
│  - No progress detected                                     │
└─────────────────────────────────────────────────────────────┘
```

## Loop Best Practices

### Loop Design Checklist

```
┌─────────────────────────────────────────────────────────────┐
│              Loop Design Checklist                          │
├─────────────────────────────────────────────────────────────┤
│  [ ] Loop has clear termination condition                   │
│  [ ] Loop variable is properly updated                      │
│  [ ] Loop has timeout mechanism                             │
│  [ ] Loop has max iteration limit                           │
│  [ ] Loop handles edge cases                                │
│  [ ] Loop has error handling                                │
│  [ ] Loop has progress logging                              │
│  [ ] Loop has cancellation support                          │
│  [ ] Loop has resource cleanup                              │
│  [ ] Loop has documentation                                 │
└─────────────────────────────────────────────────────────────┘
```

### Loop Documentation Template

```python
def process_items(items, max_iterations=1000, timeout=30):
    """
    Process items with safety mechanisms.

    Args:
        items: List of items to process
        max_iterations: Maximum number of iterations (default: 1000)
        timeout: Maximum duration in seconds (default: 30)

    Returns:
        Processed items list

    Raises:
        RuntimeError: If max iterations reached
        TimeoutError: If timeout exceeded
    """
    start_time = time.time()
    count = 0

    for item in items:
        count += 1
        if count >= max_iterations:
            raise RuntimeError("Max iterations reached")
        if time.time() - start_time > timeout:
            raise TimeoutError("Loop timed out")

        # Process item
        process(item)

    return items
```

## Real-World Impact

**Before this skill:**

- Infinite loops causing crashes
- Resource exhaustion
- No loop monitoring
- Difficult debugging
- Production outages

**After this skill:**

- Safe loops with exit strategies
- Proper resource management
- Loop monitoring and alerts
- Easy debugging
- Production stability

## Cross-References

- **`debugging`** - For loop debugging
- **`performance`** - For loop optimization
- **`testing-strategy`** - For loop testing

## References

- [Loop Safety Patterns](https://martinfowler.com/)
- [Python Loop Best Practices](https://docs.python.org/)
- [JavaScript Loop Patterns](https://developer.mozilla.org/)
- [Loop Invariants](https://en.wikipedia.org/wiki/Loop_invariant)
