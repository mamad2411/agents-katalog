---
description: TypeScript decorator development standards for server-decorator library
globs: ["**/*.ts", "**/*.spec.ts"]
alwaysApply: true
---

# 🔧 TypeScript Decorator Standards

## Core Patterns
- Always use method decorators with proper type annotations
- Follow pattern: `function decoratorName(target: any, propertyKey: string, descriptor: PropertyDescriptor)`
- Support both sync and async methods in decorators
- Use `originalMethod.apply(this, args)` for method execution
- Return modified descriptor from decorator functions

## Error Handling
- Wrap decorated methods in try/catch/finally blocks
- Always preserve original error by re-throwing
- Use `globalLogger.error()` for error logging
- Track errors with `globalTracker.track()`

## Performance & Metrics
- Measure execution time with `Date.now()` 
- Generate keys as `${target.constructor.name}.${propertyKey}`
- Track both success and error cases
- Log latency in milliseconds

## Code Style
- Use camelCase for method names and variables
- Prefer async/await over Promise chains
- Keep decorators focused and single-purpose
- Export decorators from main index.ts

## Testing
- Create `.spec.ts` files for each decorator
- Test both sync and async method decoration
- Verify error handling and metric collection
- Mock external dependencies (logger, tracker)
