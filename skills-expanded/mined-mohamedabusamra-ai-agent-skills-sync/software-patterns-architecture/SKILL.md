---
name: software-patterns-architecture
description: Apply software architectural patterns, design patterns, and best practices when designing, writing, or reviewing code. Use when generating new code, reviewing architecture, refactoring, or when the user asks about patterns, architecture, design, scalability, or system design.
---

# Software Patterns & Architecture Guide

Apply architectural patterns, design patterns, and best practices when designing and implementing software systems. This guide covers patterns from system-level architecture to component-level design.

## Architectural Patterns by Abstraction Level

### System / Enterprise Level

**Microservices:**
- Independent, deployable services with clear boundaries
- Each service owns its data and business logic
- Communicate via APIs (REST, gRPC, messaging)
- Scale services independently

**Modular Monolith:**
- Single codebase with clear module boundaries
- Feature isolation within modules
- Easier to evolve into microservices if needed

**Event-Driven Architecture:**
- Components communicate via events
- Async event handling across system
- Decoupled, scalable, reactive systems
- Use message queues, event buses, webhooks

**CQRS (Command Query Responsibility Segregation):**
- Separate read and write models
- Optimize reads independently from writes
- Use for complex domains with different read/write patterns

**Serverless / Function-First:**
- Independent cloud functions
- Pay-per-use scaling
- Stateless, event-triggered execution

### Application / Service Level

**Layered Architecture (N-tier):**
```
Presentation → Business → Persistence → Database
```
- Clear separation of concerns
- Each layer depends only on layers below
- Common in traditional web applications

**Clean / Hexagonal / Onion Architecture:**
- Domain logic at the center
- Decouple from frameworks and external dependencies
- Ports and adapters pattern
- Business logic independent of infrastructure

**Feature-Based Architecture:**
- Organize by business domains (e.g., inventory, orders, users)
- Each feature is self-contained
- Better for large applications with distinct domains

**Domain-Driven Design (DDD):**
- Bounded contexts define domain boundaries
- Aggregates, entities, value objects
- Ubiquitous language
- Rich domain models

**API-First / Contract-First:**
- API specification drives development
- Define contracts before implementation
- Ensures interoperability and clear interfaces

### Component / Module Level

**Atomic Design:**
- Atoms → Molecules → Organisms → Templates → Pages
- Build UI from smallest to largest components
- Reusable, composable components

**MVVM (Model-View-ViewModel):**
- Separate UI (View), state/logic (ViewModel), and data (Model)
- ViewModel mediates between View and Model
- Common in frontend frameworks

**State-Centric Architecture:**
- Centralized state management
- Predictable state flows
- Single source of truth

### Data / Infrastructure Level

**Caching Patterns:**
- In-memory caching (Redis, Memcached)
- API response caching
- Client-side caching (IndexedDB, localStorage)
- Cache invalidation strategies

**Data Transfer Object (DTO) Pattern:**
- Type-safe structured data movement
- Separate internal models from API contracts
- Validation at boundaries

**Adapter / Facade Patterns:**
- Simplify integration with external systems
- Wrap complex APIs with simpler interfaces
- Isolate external dependencies

**Circuit Breaker & Bulkhead:**
- Prevent cascading failures
- Isolate failures to specific components
- Graceful degradation

## Design Patterns

### Creational Patterns

**Factory Pattern:**
- Create objects without specifying exact class
- Centralize object creation logic
- Support multiple implementations

**Singleton Pattern:**
- Single instance shared across application
- Use sparingly (prefer dependency injection)
- Thread-safe implementation when needed

### Structural Patterns

**Repository Pattern:**
- Abstract data access layer
- Business logic independent of data source
- Easier testing and swapping implementations

**Facade Pattern:**
- Simplified interface to complex subsystem
- Hide complexity behind simple API
- Reduce coupling

**Adapter Pattern:**
- Convert interface of one class to another
- Integrate incompatible systems
- Wrap third-party libraries

**Decorator Pattern:**
- Add behavior to objects dynamically
- Compose functionality without inheritance
- Open/closed principle

### Behavioral Patterns

**Observer Pattern:**
- One-to-many dependency between objects
- Notify observers of state changes
- Event-driven systems

**Strategy Pattern:**
- Encapsulate algorithms in separate classes
- Interchangeable algorithms
- Select algorithm at runtime

**Module Pattern:**
- Encapsulate code in modules
- Namespace and organize code
- Control public API

## State Management Patterns

**Store Pattern:**
- Centralized global state (Pinia, Redux, Vuex)
- Modular stores per domain
- Predictable state updates

**Composable Pattern:**
- Reusable logic hooks
- Share stateful logic between components
- Composition over inheritance

**Reactive State Pattern:**
- Computed/derived values
- Reactive refs and watchers
- Automatic dependency tracking

**Persistence Pattern:**
- Local storage, IndexedDB
- Cache management
- Sync strategies

## Component / UI Patterns

**Composition Pattern:**
- Compose components from smaller parts
- Props, slots, children
- Flexible component APIs

**Container/Presentational Pattern:**
- Containers handle logic and state
- Presentational components handle UI
- Clear separation of concerns

**Slot Patterns:**
- Flexible component composition
- Named slots for different sections
- Scoped slots for data passing

**Design Tokens:**
- Centralized design values (colors, spacing, typography)
- Consistent theming
- Design system foundation

## Data Access Patterns

**Backend-First Approach:**
- Design API contracts first
- Frontend consumes well-defined APIs
- Clear data flow

**DTO Pattern:**
- Transform data at boundaries
- Type-safe data transfer
- Validation and sanitization

**Caching Strategy:**
- Cache frequently accessed data
- Invalidate on updates
- Stale-while-revalidate pattern

## Error Handling Patterns

**Defensive Programming:**
- Validate inputs
- Handle edge cases
- Null checks and type guards

**Error Boundary Pattern:**
- Catch errors in component tree
- Graceful error UI
- Prevent full app crashes

**Graceful Recovery:**
- User-friendly error messages
- Retry mechanisms
- Fallback UI

## Performance Patterns

**Lazy Loading:**
- Load code/data on demand
- Code splitting
- Dynamic imports

**Memoization:**
- Cache expensive computations
- React.memo, useMemo, computed properties
- Prevent unnecessary recalculations

**Virtual Scrolling:**
- Render only visible items
- Handle large lists efficiently
- Infinite scroll patterns

**Throttling & Debouncing:**
- Limit function execution frequency
- Optimize event handlers
- Reduce API calls

## Security Patterns

**Role-Based Access Control (RBAC):**
- Permissions based on user roles
- Feature-level permissions
- Principle of least privilege

**Token-Based Authentication:**
- JWT tokens
- Refresh token rotation
- Secure token storage

**Zero Trust Architecture (ZTA):**
- Never trust, always verify
- Verify every request
- Least privilege access

**Secrets Management:**
- Never commit secrets to code
- Use environment variables
- Secure vaults for production

## Code Organization Patterns

**Separation of Concerns:**
- Single responsibility per module
- Clear boundaries
- Independent, testable units

**Feature Isolation:**
- Self-contained features
- Minimal cross-feature dependencies
- Clear module boundaries

**Shared Utilities:**
- Common code in shared modules
- Avoid duplication
- DRY principle

**Encapsulation:**
- Private implementation details
- Public APIs only
- Information hiding

## Development Patterns

**Type-Driven Development:**
- TypeScript strict mode
- Types as documentation
- Catch errors at compile time

**Test-Driven Development (TDD):**
- Write tests first
- Red-Green-Refactor cycle
- Testable design

**Documentation-Driven Development:**
- Document architecture decisions
- API documentation
- Code comments for complex logic

## When Writing New Code

Apply patterns proactively:

1. **Choose appropriate architecture level:**
   - System level: Microservices, event-driven, CQRS
   - Application level: Clean architecture, DDD, layered
   - Component level: Atomic design, MVVM
   - Data level: Repository, caching, DTO

2. **Apply design patterns:**
   - Use Repository for data access
   - Use Factory for object creation
   - Use Strategy for interchangeable algorithms
   - Use Observer for event handling

3. **State management:**
   - Centralized store for global state
   - Composables for reusable logic
   - Local state for component-specific data

4. **Error handling:**
   - Defensive programming
   - Error boundaries
   - Graceful degradation

5. **Performance:**
   - Lazy load when possible
   - Memoize expensive operations
   - Cache appropriately

6. **Security:**
   - Validate all inputs
   - Use RBAC for permissions
   - Never expose secrets

## Pattern Selection Guidelines

**For new services:**
- Start with Clean/Hexagonal architecture
- Use Repository pattern for data access
- Apply DDD if domain is complex
- Consider CQRS if read/write patterns differ significantly

**For frontend components:**
- Use Atomic Design for UI
- Apply Container/Presentational pattern
- Use composables for shared logic
- Implement proper error boundaries

**For data access:**
- Always use Repository pattern
- Implement DTOs at API boundaries
- Add caching where appropriate
- Use adapters for external services

**For state management:**
- Local state for component-specific data
- Composable for shared logic
- Global store for app-wide state
- Persist critical state

## Anti-Patterns to Avoid

- **God Object:** Classes/objects doing too much
- **Spaghetti Code:** Unclear dependencies and flow
- **Premature Optimization:** Optimize without profiling
- **Copy-Paste Programming:** Duplicate code instead of extracting
- **Magic Numbers/Strings:** Hard-coded values without constants
- **Tight Coupling:** Direct dependencies on concrete implementations
- **Anemic Domain Model:** Data structures without behavior

## Review Checklist

When reviewing code for patterns:

- [ ] Appropriate architecture level chosen
- [ ] Design patterns applied correctly
- [ ] Separation of concerns maintained
- [ ] Dependencies properly abstracted
- [ ] Error handling comprehensive
- [ ] Performance considerations addressed
- [ ] Security patterns followed
- [ ] Code organized by feature/domain
- [ ] No anti-patterns present
- [ ] Patterns consistently applied

## Additional Resources

For advanced patterns and detailed implementations:
- Event Sourcing, CQRS, Reactive Architecture: See [advanced-patterns.md](advanced-patterns.md)
- Multi-tenancy, API Gateway/BFF: See [advanced-patterns.md](advanced-patterns.md)
- Observability, Testing, Concurrency: See [advanced-patterns.md](advanced-patterns.md)
- Functional patterns, Plugin architecture: See [advanced-patterns.md](advanced-patterns.md)
