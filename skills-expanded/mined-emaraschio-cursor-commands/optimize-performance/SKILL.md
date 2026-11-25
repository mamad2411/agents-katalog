---
name: optimize-performance
description: Profile and optimize performance bottlenecks
user-invocable: false
---
## Overview

Analyze the current code for performance bottlenecks and provide optimization recommendations, focusing on measurable improvements while maintaining code quality and readability.

## Steps

1. **Performance Analysis**
    - Identify slow algorithms and inefficient data structures
    - Find memory leaks and excessive allocations
    - Identify slow queries and improve them specifically for Solid Queue and n+1 queries
    - Detect unnecessary computations and redundant operations
    - Analyze database queries and API calls
2. **Optimization Strategies**
    - Suggest algorithm improvements and better data structures
    - Recommend caching strategies where appropriate
    - Propose lazy loading and pagination solutions
    - Identify opportunities for parallel processing
3. **Implementation**
    - Provide optimized code with explanations
    - Include performance impact estimates
    - Suggest profiling and monitoring approaches
    - Consider trade-offs between performance and maintainability

## Optimize Performance Checklist

- [ ] Identified slow algorithms and inefficient data structures
- [ ] Found memory leaks and excessive allocations
- [ ] Detected unnecessary computations and redundant operations
- [ ] Analyzed database queries and API calls
- [ ] Suggested algorithm improvements and better data structures
- [ ] Recommended caching strategies where appropriate
- [ ] Provided optimized code with explanations
- [ ] Included performance impact estimates
- [ ] Considered trade-offs between performance and maintainability

## Guardrails

- Measure first: profile to find the real bottleneck before changing code.
- Do not trade readability for unmeasured micro-gains.
- Do not commit, push, merge, or run production scripts without consent; wait for an explicit request before any destructive git action.
- Do not print, log, or commit secrets or credentials encountered while profiling or optimizing; flag any exposed secret instead.