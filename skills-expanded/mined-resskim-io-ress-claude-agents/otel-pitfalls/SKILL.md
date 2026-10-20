---
name: otel-pitfalls
category: observability
description: "OTel 실전 Pitfalls — 실전 트러블슈팅 기반 OpenTelemetry 실전 함정. SDK 버전 충돌 / label cardinality / exporter protocol / agent vs starter 이중 계측. Use when working with observability 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# OTel 실전 Pitfalls

실전 트러블슈팅 기반 OpenTelemetry 실전 함정. SDK 버전 충돌 / label cardinality / exporter protocol / agent vs starter 이중 계측.
Spring Boot + OTel Java Agent 환경 중심.

---

## 1. Spring Boot BOM 충돌

### 문제
`io.spring.dependency-management` 플러그인이 Spring Boot BOM의 OTel 버전(1.49.0)을 강제 → OTel Instrumentation BOM(2.25.0)이 요구하는 SDK 1.59.0과 충돌 → `ComponentLoader` class not found.

### Gradle 해결
```groovy
// BAD: platform()과 dependency-management 플러그인 혼용
implementation platform("io.opentelemetry.instrumentation:opentelemetry-instrumentation-bom:2.25.0")

// GOOD: dependencyManagement 블록에서 BOM import (순서 중요)
dependencyManagement {
    imports {
        mavenBom "io.opentelemetry.instrumentation:opentelemetry-instrumentation-bom:2.25.0"
        // Spring Boot BOM은 그 다음 (먼저 선언된 BOM이 우선)
    }
}
```

### Maven 해결
`<dependencyManagement>`에서 OTel BOM을 Spring Boot BOM **앞에** 선언.

### 근거
2026-02-28 사고. Spring Boot 3.5.x에서 여전히 발생 (2026-04 확인).

---

## 2. Java Agent 메모리 요구사항

### 실측값
- 시작 시 ~100MB non-heap 메모리 증가
- 런타임: 50-100MB 추가 heap (계측 대상 수에 따라)
- **512Mi container → OOMKilled 반복** (2026-03-20 확인)

### 권장
| 환경 | requests.memory | limits.memory |
|------|----------------|---------------|
| Dev | 768Mi | 1Gi |
| Prod | 1Gi | 1.5Gi |

### 오버헤드 줄이기
```
-Dotel.instrumentation.jdbc.enabled=false      # JDBC 미사용 시
-Dotel.instrumentation.kafka.enabled=false      # Kafka 미사용 시
-Dotel.instrumentation.lettuce.enabled=false    # Redis Lettuce 미사용 시
```

공식 최소값은 없음 — 애플리케이션별 프로파일링 필요.

---

## 3. OTLP Protocol 변경 (2.0.0+)

### 변경사항
OTel Java Agent/Starter 2.0.0부터 기본 protocol이 `grpc` → `http/protobuf`로 변경.

| 설정 | 기본값 (2.0+) | 포트 |
|------|-------------|------|
| `OTEL_EXPORTER_OTLP_PROTOCOL` | `http/protobuf` | 4318 |
| 이전 기본값 | `grpc` | 4317 |

### 영향
OTel Collector endpoint가 4317(gRPC)만 열려있으면 → Agent가 4318(http)로 보내서 실패.

### 해결
```yaml
# 명시적으로 protocol 설정
env:
  - name: OTEL_EXPORTER_OTLP_PROTOCOL
    value: "grpc"
  - name: OTEL_EXPORTER_OTLP_ENDPOINT
    value: "http://otel-collector:4317"
```

OTel Collector는 기본적으로 4317(gRPC) + 4318(http) 모두 수신.

---

## 4. HikariCP BeanPostProcessor 초기화 순서

### 문제
OTel의 `BeanPostProcessor`가 Spring DataSource 초기화보다 먼저 실행 → HikariCP proxy 래핑 실패 → 메트릭 미수집.

### 해결
```java
@Bean
@DependsOn("openTelemetry")
public DataSource dataSource() { ... }
```

또는 `@Lazy` 어노테이션으로 DataSource 초기화 지연.

### 근거
2026-03-09 사고. Spring Boot 3.5 + OTel 2.25에서도 발생 가능.

---

## 5. Agent vs Starter 동시 사용 금지

### 문제
OTel Java Agent (`-javaagent:opentelemetry-javaagent.jar`)와 Spring Boot Starter (`spring-boot-starter-actuator` + OTel 자동 설정)을 동시 사용 → 이중 계측.

### 증상
- Span이 2배로 생성
- 메트릭 값 2배
- 메모리 사용량 급증

### 규칙
- **하나만 선택**: Agent(zero-code) 또는 Starter(code-level)
- 실전 사례: OTel Operator `Instrumentation` CR → Agent 방식 사용 중

---

## 6. PII 유출 방지 (보안)

### 자동 수집되는 위험 데이터

| 소스 | 노출 내용 | 예시 |
|------|---------|------|
| `http.url` attribute | URL query params | `?email=user@example.com` |
| `db.statement` attribute | 전체 SQL | `WHERE email = 'user@...'` |
| HTTP header capture | 인증 토큰 | `Authorization: Bearer eyJ...` |
| Exception span | 변수 값 | 스택트레이스 내 connection string |

### 필수 설정
```yaml
env:
  # SQL 파라미터 마스킹
  - name: OTEL_INSTRUMENTATION_COMMON_DB_STATEMENT_SANITIZER_ENABLED
    value: "true"
  # Attribute 값 길이 제한 (URL 내 PII 절단)
  - name: OTEL_ATTRIBUTE_VALUE_LENGTH_LIMIT
    value: "256"
```

### Collector-level 보호
```yaml
processors:
  redaction:
    allow_all_keys: false
    allowed_keys:
      - http.request.method
      - http.response.status_code
      - service.name
    blocked_values:
      - "Bearer .*"
      - "[0-9]{3}-[0-9]{4}-[0-9]{4}"  # 전화번호 패턴
```

### 주의
해싱은 작은 입력 공간(이메일, 전화번호)에 대해 insufficient — truncation이 더 안전.
