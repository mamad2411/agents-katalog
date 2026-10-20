---
description: Performance optimization guidelines for code, memory, database, and frontend performance
globs: "**/*.{ts,tsx,js,jsx,sql}"
alwaysApply: true
---

# Performance and Optimization Rules

## General Performance Principles
- Profile before optimizing
- Focus on algorithmic efficiency first
- Optimize bottlenecks, not everything
- Consider time vs space trade-offs
- Measure actual performance impact
- Document optimization decisions

## Code-Level Optimization
- Use appropriate data structures
- Minimize object creation in hot paths
- Avoid premature optimization
- Use efficient algorithms
- Minimize function call overhead
- Optimize loops and iterations
- Cache expensive computations

## Memory Management
- Understand memory allocation patterns
- Avoid memory leaks
- Use object pooling when appropriate
- Minimize garbage collection pressure
- Profile memory usage
- Consider memory-mapped files for large data
- Use weak references appropriately

## Database Performance
- Design efficient schemas
- Use appropriate indexes
- Optimize query patterns
- Use connection pooling
- Implement query caching
- Avoid N+1 query problems
- Monitor query execution plans
- Use database-specific optimizations

## Network and I/O
- Minimize network round trips
- Use compression when beneficial
- Implement proper caching strategies
- Use async I/O operations
- Batch operations when possible
- Consider CDN usage
- Optimize payload sizes
- Use connection pooling

## Frontend Performance
- Minimize bundle sizes
- Use code splitting
- Implement lazy loading
- Optimize images and assets
- Use browser caching effectively
- Minimize DOM manipulation
- Use virtual scrolling for large lists
- Optimize critical rendering path
## Monitoring and Metrics
- Implement performance monitoring
- Track key performance indicators
- Set performance budgets
- Monitor resource usage
- Track user experience metrics
- Use application performance monitoring
- Implement alerting for performance issues
- Regular performance audits

## Scalability Considerations
- Design for horizontal scaling
- Use load balancing strategies
- Implement proper caching layers
- Consider microservices architecture
- Use async processing for heavy tasks
- Implement rate limiting
- Plan for traffic spikes
- Monitor system capacity
