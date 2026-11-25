---
name: quarkus-expert
description: High-performance Quarkus framework expertise covering reactive patterns, CDI, build-time augmentation, and cloud-native development. Use for general Quarkus questions.
version: 1.1.0
keywords: [quarkus, java, cloud-native, microservices, reactive, cdi]
---

# quarkus-expert

> Keyword: quarkus | Platforms: gemini,claude,codex

High-Performance Quarkus Framework Expert Skill - Deep production-grade knowledge of the Quarkus ecosystem.

## Core Mandates

- **Build-Time First:** Move processing to augmentation phase, minimize runtime classpath scanning
- **Java 21+ Excellence:** Leverage Virtual Threads (`@RunOnVirtualThread`) for blocking operations
- **Reactive Discipline:** Use Mutiny (`Uni`, `Multi`) for non-blocking I/O
- **Dependency Discipline:** Always use Quarkus BOM for version management
- **Constructor Injection:** Mandate constructor injection over field injection

## Architectural Patterns

### Persistence Strategy
- **Imperative:** Hibernate ORM with Panache (Active Record or Repository pattern)
- **Reactive:** Reactive SQL Clients (MySQL, PostgreSQL, Oracle)
- **Dev Services:** Zero-config databases and brokers during development

### Cloud-Native Observability
- **OpenTelemetry (OTel):** Standard for tracing and metrics
- **Health Checks:** Implement `Liveness` and `Readiness` probes using MicroProfile Health

### Security Architecture
- Use Proactive Authentication and RBAC with `@RolesAllowed`
- Prefer OIDC/JWT for stateless microservices

## Testing

- **Integration Testing:** Use `@QuarkusTest` for full-stack tests
- **Mocking:** Utilize `@InjectMock` and `@InjectSpy`
- **Parity:** Use Testcontainers via Dev Services

## Extension Development

- **Build-Time (Deployment):** Write `BuildStep` methods for bean registration, bytecode generation
- **Runtime Init:** Differentiate between `STATIC_INIT` and `RUNTIME_INIT`

## Troubleshooting

- **ClassLoader Leaks:** Monitor custom dynamic class loading
- **ContextNotActiveException:** Ensure CDI contexts propagate correctly with Mutiny
- **Native Image Failures:** Analyze reports and provide `reflection-config.json`

## 🌐 Knowledge Sources & Deep Dives

> **Directive:** Use `web_fetch` to read specific guides if the user's question involves a particular extension (e.g., Hibernate, Kafka, OIDC).

- **Mutiny Mastery:** [SmallRye Mutiny Documentation](https://smallrye.io/smallrye-mutiny/latest/guides/) - Core reactive patterns.
- **Persistence Guide:** [Hibernate ORM with Panache](https://quarkus.io/guides/hibernate-orm-panache) - Data access patterns.
- **Messaging:** [Apache Kafka with Quarkus](https://quarkus.io/guides/kafka) - Event-driven architecture.
- **CDI/Arc:** [Contexts and Dependency Injection in Quarkus](https://quarkus.io/guides/cdi-reference) - Bean lifecycle and injection.
- **Virtual Threads:** [Quarkus and Virtual Threads](https://quarkus.io/guides/virtual-threads) - Blocking I/O optimization.

## References

- [Quarkus Official Documentation](https://quarkus.io/guides/)
- [Quarkus GitHub Repository](https://github.com/quarkusio/quarkus)
- [Mutiny Javadoc](https://smallrye.io/smallrye-mutiny/latest/apidocs/)

## Skill Interoperability

The **quarkus-expert** ⚡ skill is a comprehensive framework built on:
- **java-expert** ☕: Core language and JVM features.
- **vertx-expert** 🌀: Reactive engine for non-blocking operations.
- **graalvm-expert** 🚀: Native Image generation and AOT optimization.
