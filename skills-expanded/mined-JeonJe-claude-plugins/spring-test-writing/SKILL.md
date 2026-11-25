---
name: spring-test-writing
description: Java/Spring 테스트 코드 작성 가이드. 단위(Mockito)·컨트롤러(@WebMvcTest + REST Docs)·MyBatis Testcontainers 통합 테스트의 구조와 패턴, AssertJ 단언 스타일, fixture 패턴, 커밋 전 품질 체크리스트. Spring 테스트 작성, 단위 테스트, 컨트롤러 테스트, Mockito, Testcontainers 시 사용.
---

# Spring Test Writing

Test-writing methodology for Java/Spring, distilled from a production multi-module codebase. Entry point: pick the test type, read its reference, and run the quality checklist before commit.

## AI 테스트 작성 시 필수 확인

1. **given/when/then** 주석 구조 사용
2. **`@DisplayName`** 으로 비즈니스 의도 명시 (팀 언어로)
3. **`@Nested`** 로 시나리오 그룹화
4. **`@MockitoBean`** 사용 — `@MockBean`은 Spring Boot 3.4+에서 레거시
5. **`Thread.sleep` 금지** — `@Transactional` 자동 롤백과 관찰 가능한 조건 대기 활용
6. 테스트 후 반드시 빌드 검증: `./gradlew :{module}:test --tests "ClassName"`
7. 테스트 데이터는 **고정 날짜** 사용 (`LocalDate.of(...)`) — `LocalDate.now()` 금지
8. soft-delete 프로젝트라면 프로덕션 코드의 미삭제 조건 누락 여부를 테스트에서 확인
9. 커밋 전 [references/quality-check.md](references/quality-check.md) 실행

## 테스트 타입 선택

| 타입 | 문서 | 언제 사용 |
|------|------|----------|
| 단위 테스트 | [references/unit-test.md](references/unit-test.md) | Service, Domain 로직 (Spring Context 불필요) |
| 컨트롤러 테스트 | [references/controller-test.md](references/controller-test.md) | REST API 엔드포인트 + API 문서 자동 생성 |
| DB 통합 테스트 | [references/testcontainers-db-test.md](references/testcontainers-db-test.md) | Mapper/Repository 쿼리 검증 — 실 DB 엔진으로 |
| 품질 검증 | [references/quality-check.md](references/quality-check.md) | 작성 완료 후, 커밋 전 |

## 모듈별 베이스 클래스 원칙

테스트를 새로 쓰기 전에 **그 모듈의 기존 베이스 클래스를 먼저 찾는다** (컨트롤러용 RestDocs 베이스, 통합 테스트 베이스, Testcontainers 베이스). 모듈마다 헬퍼 시그니처·Mock 구성이 다를 수 있으므로, 같은 모듈의 최근 테스트 1개를 열어 패턴을 확인한 뒤 동일하게 작성한다. 베이스 클래스가 없는 모듈에서 처음 만들 때만 인접 모듈 것을 참조해 신설한다.

## 도메인 테스트 퀵레퍼런스 (복잡 도메인 권장)

핵심 도메인(결제·예약·정산 등)은 테스트 가이드와 별도로 **그 도메인 전용 퀵레퍼런스 문서**를 유지한다. 새 사람(또는 새 세션의 AI)이 "이 도메인을 건드리면 무엇부터 테스트해야 하나"를 문서 하나로 파악하게 하는 것이 목적. 구성:

1. **우선순위 매트릭스** — Critical(배포 전 필수) / High / Medium으로 시나리오를 분류. Critical은 "이게 깨지면 돈/데이터가 틀어지는 것"만.
2. **진입점별 테스트 맵** — 커맨드 서비스의 공개 메서드마다 필요한 테스트 케이스 나열.
3. **핵심 예외 시나리오** — 이 도메인 특유의 실패 경로 (중복 요청, 한도 초과, 역순 콜백 등).
4. **DB 검증 체크리스트** — 성공 케이스 후 테이블별 기대 상태 (어느 테이블에 몇 행, 어떤 컬럼 값). "응답 200"이 아니라 영속 상태가 성공의 정의다.
5. **부수효과 검증** — 알림·이벤트·캐시 무효화가 발생/미발생해야 하는 조건.
6. **패턴 체인 검증** — Factory/Strategy 등 분기 구조가 있으면 각 분기의 선택 조건 테스트.

이 문서는 도메인 레포의 `docs/{domain}/testing.md`에 두고, 도메인 로직이 바뀌면 같은 MR에서 갱신한다.

## 마이그레이션 중인 패턴 처리

프로젝트가 패턴 전환 중일 수 있다 (`@MockBean`→`@MockitoBean`, 레거시 베이스 클래스 등). 원칙: **신규 코드는 항상 신 패턴**, 기존 코드는 해당 파일 수정 시 점진 전환. 전환 현황표가 프로젝트 문서에 있으면 따르고, 없으면 신·구 패턴이 한 파일에 섞이지 않게만 유지한다.
