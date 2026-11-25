---
name: spring-ddd-arch
description: Java/Spring 백엔드의 계층 구조·DDD 경계·DIP 규칙. Controller→Facade→Service→Repository→Domain 계층, 도메인 이벤트 발행(raise≠dispatch), 커스텀 예외 + 에러레벨 사다리, JPA/QueryDSL 성능 규칙. 백엔드 기능 개발, 도메인 모델 설계, 이벤트 발행, 예외 처리, Spring 아키텍처 결정 시 사용.
---

# Spring DDD Architecture

운영 서비스에서 다듬어진 Java/Spring 백엔드 아키텍처 규칙. 핵심은 **경계** — 계층 간 호출 방향, 도메인과 인프라의 분리(DIP), 발행 책임의 위치를 고정해서 기능이 늘어나도 구조가 무너지지 않게 한다.

## 계층 구조

```
Controller → Facade → Service → Repository → Domain
```

| 계층 | 책임 |
|---|---|
| Controller | 요청 수신, validation, 응답 반환 |
| Facade | 여러 Service 조합, 트랜잭션 경계 |
| Service | 단일 도메인 비즈니스 로직 |
| Repository | 데이터 접근 (JPA/QueryDSL/MyBatis) |
| Domain | 엔티티, VO, 도메인 이벤트 |

**위반 금지**:
- Controller → Repository 직접 호출
- Service → Service 순환 참조
- **Facade = 흐름 제어만.** 캐시/Redis 등 인프라 사용 여부를 몰라야 한다 — 인프라는 포트/Reader 인터페이스 뒤로 (DIP). 발행 경로를 optional 빈(`ObjectProvider`)·조건부로 분기하지 않는다.
- 비즈니스 로직은 Service 또는 Domain 레이어에만.

## 예외 설계 — 기본 예외 직접 throw 금지

`new IllegalArgumentException`, `new RuntimeException` 등 Java 기본 예외를 직접 throw하지 않는다. 프로젝트 커스텀 예외 + **에러 레벨**을 사용해, 예외 하나가 로깅·모니터링·알림 정책까지 결정하게 한다. 상세: [references/exception-design.md](references/exception-design.md)

## 도메인 이벤트 — 기록(raise) ≠ 발송(dispatch)

상태를 바꾸는 도메인이 자신의 이벤트를 책임진다. Facade에서 발행하지 않는다. 엔티티에 `ApplicationEventPublisher`를 주입하지 않는다. 상세: [references/domain-events.md](references/domain-events.md)

## References index

| File | Read when |
|---|---|
| [references/domain-events.md](references/domain-events.md) | 도메인 이벤트 발행/구독을 설계·리뷰할 때 |
| [references/exception-design.md](references/exception-design.md) | 예외 클래스/에러 응답을 만들 때 |
| [references/domain-model-patterns.md](references/domain-model-patterns.md) | 엔티티/VO 설계 — soft delete, audit, 민감정보 암호화, First-Class Collection |
| [references/performance.md](references/performance.md) | JPA/QueryDSL 조회, 직렬화, 캐시, 비동기 코드를 쓸 때 |
| [references/transactions.md](references/transactions.md) | 트랜잭션 경계/선언, 부수효과, 다중 DataSource, 테스트에서의 함정 |
| [references/concurrency.md](references/concurrency.md) | 동시성 제어 — 자원/행위자 이중 직렬화, 락 순서, 메커니즘 선택의 근거 |
| [references/sql-domain-boundary.md](references/sql-domain-boundary.md) | 집계/통계 쿼리 — SQL과 도메인의 책임 분리, 반열림 구간·제로패딩 등 함정 목록 |
| [references/api-contract.md](references/api-contract.md) | API 표면 설계 — 상태코드, 에러 포맷, 컬렉션 규약, 하위호환 변경 절차 |
| [references/db-migration.md](references/db-migration.md) | 스키마 변경 — expand-contract, NOT NULL 절차, 대용량 테이블, 롤백 계획 |
| [references/time-handling.md](references/time-handling.md) | 시간 — 저장 기준 단일화, 타입 선택, Clock 주입, 경계 케이스 박제 |
