---
name: code-architecture
description: Software architecture patterns, design principles, and system design.
---

# Code Architecture & System Design

Architectural patterns and design principles for scalable systems.

## Architectural Patterns
- **Monolith**: Modular monolith, layered, clean architecture
- **Microservices**: Service boundaries, API contracts, saga pattern
- **Event-Driven**: Event sourcing, CQRS, message queues, streams
- **Serverless**: FaaS, BaaS, cold start optimization
- **Hexagonal**: Ports and adapters, domain isolation

## Design Principles
1. **SOLID**: Single responsibility, open-closed, Liskov, interface segregation, dependency inversion
2. **DRY**: Don't repeat yourself — extract shared logic
3. **KISS**: Keep it simple — avoid premature abstraction
4. **YAGNI**: You aren't gonna need it — don't build for hypotheticals
5. **Law of Demeter**: Least knowledge — minimize coupling

## System Design
- **Load Balancing**: L4/L7, health checks, session affinity
- **Caching**: Cache-aside, read-through, write-through, write-behind
- **Database Sharding**: Horizontal/vertical, consistent hashing
- **Message Queues**: At-least-once, at-most-once, exactly-once semantics
- **CDN**: Edge caching, cache invalidation, origin shield

## API Design
- **REST**: Resource naming, versioning, pagination, HATEOAS
- **GraphQL**: Schema design, resolvers, N+1 prevention, DataLoader
- **gRPC**: Protobuf, streaming, interceptors, deadline propagation
- **WebSocket**: Connection management, heartbeat, reconnection

## Design Patterns (GoF)
- Creational: Factory, Builder, Singleton, Prototype, Abstract Factory
- Structural: Adapter, Bridge, Composite, Decorator, Facade, Proxy
- Behavioral: Observer, Strategy, Command, State, Template Method, Visitor

## Documentation
- ADR (Architecture Decision Records) for major decisions
- C4 Model for visual architecture (Context, Container, Component, Code)
- Sequence diagrams for critical flows
- API contracts with OpenAPI/AsyncAPI
