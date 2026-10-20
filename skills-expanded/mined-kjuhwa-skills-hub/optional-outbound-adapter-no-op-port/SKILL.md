---
tags: [arch, optional, outbound, adapter, port]
name: optional-outbound-adapter-no-op-port
description: Register a No-Op implementation of an optional outbound port with @ConditionalOnMissingBean so services boot when the real adapter (Kafka audit, tracing, notifications) is absent.
trigger: Hexagonal-architecture outbound port whose backing infrastructure is optional; service fails to boot in dev/test because an audit/tracing/notification adapter is missing.
source_project: lucida-domain-apm
version: 1.0.0
category: arch
---

# Optional Outbound Adapter — No-Op Port

In hexagonal architecture, some outbound ports (audit, tracing, notifications, metrics egress) aren't required in every environment. Registering a No-Op implementation when the real adapter bean is missing lets the service boot without the backing infrastructure.

## Why

Without this, a missing Kafka / audit / telemetry backend hard-fails the application on startup (`UnsatisfiedDependencyException`). That's the wrong failure mode for *optional* concerns: the core domain doesn't depend on "audit was written"; a dev or test environment shouldn't have to stand up Kafka to boot. Making the No-Op explicit keeps the core code unaware of optionality — it always sees a port bean.

## Pattern

```java
@Configuration
class NoOpAuditServicePortConfig {
    @Bean
    @ConditionalOnMissingBean(AuditServicePort.class)
    AuditServicePort noOpAuditServicePort() {
        log.info("AuditServicePort: using No-Op (no audit backend configured)");
        return event -> { /* swallow */ };
    }
}
```

## Steps

1. Define the port interface in `port.out`.
2. Implement the real adapter normally; let it become a bean only when its own dependencies exist (e.g. `@ConditionalOnProperty`, `@ConditionalOnBean(KafkaTemplate.class)`).
3. Add a config class providing a No-Op bean guarded by `@ConditionalOnMissingBean(<Port>.class)`.
4. **Log at INFO on startup** that the No-Op is active. Silent no-ops confuse production diagnosis.
5. Expose the state through actuator so ops can see `audit=noop` at a glance.

## Counter / Caveats

- Only use this for ports with truly optional side effects. A No-Op persistence port is almost never correct — silent data loss is not graceful degradation.
- If the port returns data, the No-Op must return a safe empty value (`Optional.empty()`, `List.of()`), and callers must already handle empty — don't paper over a missing dependency by returning fake data.
- Don't chain No-Ops. If more than one outbound port is No-Op in production, that's a configuration bug, not a feature.
