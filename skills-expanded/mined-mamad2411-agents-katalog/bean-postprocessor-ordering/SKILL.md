---
name: bean-postprocessor-ordering
category: spring
description: BeanPostProcessor 등록 순서/초기화 시점/프록시 래핑 타이밍 오류로 인한 런타임 누락 패턴 방지. static @Bean + ObjectProvider + Before/After 선택 기준을 강제하는 체크리스트.
---

# BeanPostProcessor Ordering (M1: 비동기/순서 가정 오류)

Spring 의 `BeanPostProcessor`(BPP) 는 컨테이너의 핵심 확장점이지만 **빈 초기화 순서**와 **다른 BPP 의 래핑 타이밍**을 잘못 가정하면 메트릭/계측/AOP 가 **silent 하게 누락**된다.

> Claude mental model 오류: "BPP 는 그냥 등록하면 모든 빈에 적용된다" → 실제로는 BPP 자신이 너무 일찍 초기화되거나, 대상 빈이 이미 다른 BPP 에 의해 프록시로 래핑된 뒤 도착하면 적용 자체가 실패한다.

---

## 3가지 함정 패턴

### 함정 1. non-static @Bean 으로 BPP 등록 → @Configuration 클래스 조기 초기화

```java
// ❌ 다른 빈(OpenTelemetry) 이 BPP 처리 자격을 잃음
@Configuration
class HikariOtelConfig {
    @Bean
    BeanPostProcessor hikariMetricsPostProcessor(OpenTelemetry otel) { ... }
}
// 로그: Bean 'openTelemetry' is not eligible for getting processed by all BeanPostProcessors
```

원인: `@Bean` 메서드가 non-static 이면 `@Configuration` 클래스 자체를 **빈 컨테이너가 BPP 보다 먼저 생성** → 의존 빈도 함께 조기 초기화 → 그 빈들은 다른 BPP 의 처리 자격을 잃는다.

```java
// ✅ static @Bean — Spring 공식 권장 (BPP/BFPP 모두)
@Configuration
class HikariOtelConfig {
    @Bean
    static BeanPostProcessor hikariMetricsPostProcessor(ObjectProvider<OpenTelemetry> otelProvider) {
        return new BeanPostProcessor() {
            @Override
            public Object postProcessBeforeInitialization(Object bean, String name) {
                if (bean instanceof HikariDataSource ds) {
                    OpenTelemetry otel = otelProvider.getIfAvailable();
                    if (otel != null) {
                        ds.setMetricsTrackerFactory(HikariTelemetry.create(otel).createMetricsTrackerFactory());
                    }
                }
                return bean;
            }
        };
    }
}
```

핵심 규칙:
- **static @Bean** — `@Configuration` 클래스 조기 초기화 회피
- **`ObjectProvider<T>`** — 직접 주입 대신 지연 조회 (Spring Boot `MeterRegistryPostProcessor` 동일 패턴)
- **`@Lazy`** 보조 — 일부 컨테이너에서 BPP 등록 자체를 지연

### 함정 2. postProcessAfterInitialization 사용 — 이미 프록시로 래핑된 빈을 받음

OTel/Spring AOP/datasource-proxy 등은 `After` 단계에서 원본 DataSource 를 `OpenTelemetryDataSource` 같은 프록시로 래핑한다. 우리 BPP 가 **After 단계에 동작**하면 다른 BPP 보다 늦게 와서 `instanceof HikariDataSource` 가 실패한다.

```java
// ❌ After — OTel 프록시 래핑 뒤에 도착하여 타입 매칭 실패
public Object postProcessAfterInitialization(Object bean, String name) {
    if (bean instanceof HikariDataSource ds) { ... } // 매칭 안 됨
}

// ✅ Before — OTel DataSourcePostProcessor 의 래핑 전에 원본 빈 처리
public Object postProcessBeforeInitialization(Object bean, String name) {
    if (bean instanceof HikariDataSource ds) { ... } // 매칭 성공
}
```

선택 기준:
- **Before** — 원본 빈 자체에 옵션 주입 / 메트릭 부착 (HikariCP `setMetricsTrackerFactory` 등)
- **After** — 빈을 프록시로 감싸고 싶을 때 (자체 AOP 패턴)

### 함정 3. BPP 사이의 명시적 순서 부재

여러 BPP 가 같은 빈을 만진다면 `@Order` / `Ordered` / `PriorityOrdered` 로 순서를 강제해야 한다.

```java
@Bean
static BeanPostProcessor myBpp() {
    return new MyBpp();   // → Ordered 미구현 → 순서 불확정
}

// ✅ 우선순위 명시
@Bean
@Order(Ordered.HIGHEST_PRECEDENCE)
static BeanPostProcessor myBpp() { ... }

// PriorityOrdered 가 Ordered 보다 먼저 실행됨에 주의
```

---

## 자가 검증 체크리스트

BPP 추가/수정 시:

- [ ] `@Bean` 메서드가 **static** 인가? (non-static 이면 의존 빈 조기 초기화 위험)
- [ ] 의존 빈을 **`ObjectProvider<T>`** 로 받는가? (직접 주입 시 빈 그래프 순서 강제)
- [ ] **Before / After** 선택이 명시적인가? (래핑 BPP 와 충돌 여부 확인)
- [ ] 같은 빈을 만지는 다른 BPP 와 **`@Order`** 충돌 없는가?
- [ ] **WARN 로그** `is not eligible for getting processed by all BeanPostProcessors` 가 없는가? (앱 startup 로그 grep 필수)
- [ ] 메트릭/계측 적용 후 **Prometheus/exporter 에서 실제 수집** 확인 (silent 실패 차단)

---

## 검증 SQL/쿼리

수정 후 반드시 실데이터 확인:

```promql
# HikariCP 메트릭 — 빈이 0 row 면 BPP 미적용
db_client_connections_max{...}
db_client_connections_usage{...}
```

또는 INFO 로그 한 줄 강제:

```java
log.info("OTel HikariCP metrics attached to dataSource: {}", ds.getPoolName());
```

---

## 외부 근거

- [BeanPostProcessor (Spring Framework Javadoc)](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/beans/factory/config/BeanPostProcessor.html) — thread-safety / 등록 시점 명세
- [Controlling Bean Creation Order with @DependsOn — Baeldung](https://www.baeldung.com/spring-depends-on)
- Spring Boot `MeterRegistryPostProcessor` — `ObjectProvider` + static @Bean 표준 예시

---

## 안티패턴 vs 권장 1줄 요약

| 안티패턴 | 권장 |
|---|---|
| `@Bean BeanPostProcessor x(OpenTelemetry otel)` | `@Bean static BeanPostProcessor x(ObjectProvider<OpenTelemetry>)` |
| `postProcessAfterInitialization` 로 원본 타입 매칭 | `postProcessBeforeInitialization` 로 원본 단계에서 매칭 |
| BPP 간 순서 가정 | `@Order` / `PriorityOrdered` 로 명시 |
| BPP 등록 후 적용 확인 없음 | 메트릭/로그/exporter 데이터로 검증 |
