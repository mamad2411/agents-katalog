---
name: guhada-common-convention
description: |
  guhada/kglowing 프로젝트(캠페인, 인플루언서, 시딩 도메인)의 공통 개발 컨벤션.
  GuhadaApiResponse, GuhadaApiRuntimeException, BaseEntity, MapStruct DtoMapper 등
  프로젝트 고유 패턴을 강제한다.
  guhada, kglowing, 캠페인, 인플루언서, 시딩, 구하다 프로젝트에서
  코드 작성, 구현, 리뷰, 리팩토링 시 자동 트리거된다.
  Entity/DTO/MapStruct/예외처리/테스트 코드 예시는 references/code-examples.md 참조.
paths:
  - "**/campaign/**/*.java"
  - "**/influencer/**/*.java"
  - "**/seeding/**/*.java"
  - "**/campaign/**/*.kt"
  - "**/influencer/**/*.kt"
  - "**/seeding/**/*.kt"
---

# guhada/kglowing 공통 컨벤션

guhada 및 kglowing 프로젝트에서 코드를 작성할 때 반드시 따라야 하는 규칙이다.

> 코드 예시가 필요하면 Read 도구로 이 스킬의 `references/code-examples.md`를 읽어서 참조하라.

---

## 1. 기술 스택

| 항목 | 버전/스펙 |
|------|----------|
| Java | 17 |
| Spring Boot | 2.7.x (기존) / 3.x (신규) |
| Database | MySQL 8.x |
| ORM | JPA + MyBatis (하이브리드) |
| Cache | Redis, Caffeine (로컬) |
| Search | ElasticSearch 7.6.x |
| Build | Gradle |
| DTO 변환 | MapStruct 1.5.x |
| 유틸리티 | Lombok |

---

## 2. 아키텍처

4-Layer 구조를 따른다. 레이어 간 역할을 넘지 마라.

```
Controller → Service → Repository → Entity
```

| 레이어 | 허용 | 금지 |
|--------|------|------|
| Controller | HTTP 요청/응답, 입력 검증 | 비즈니스 로직 |
| Service | 비즈니스 로직, 트랜잭션 | Repository 외 DB 접근 |
| Repository | 데이터 접근 | 비즈니스 로직 |
| Entity | 도메인 모델, 도메인 로직 | 인프라 의존성 |

### 의존성 방향 (DIP)

- Entity는 DTO를 알지 못한다.
- DTO-Entity 변환은 반드시 MapStruct(`{Domain}DtoMapper`)로 처리하라.

---

## 3. 설계 원칙

### 필수 적용

- **SOLID 원칙** 준수 (특히 SRP, DIP)
- **Early Return**으로 중첩을 줄여라
- **매직 넘버/문자열**은 상수 또는 Enum으로 정의하라
- **null 대신 Optional** 사용 (반환 타입으로만)
- **일급 컬렉션**으로 컬렉션 로직을 캡슐화하라 (불변 보장)
- 메서드 파라미터는 3개 이하로 유지하라

---

## 4. 네이밍 컨벤션

### 클래스명

| 구분 | 패턴 | 예시 |
|------|------|------|
| Controller | `{Domain}Controller` | `CampaignController` |
| Service | `{Domain}Service` | `CampaignService` |
| Repository | `{Domain}Repository` | `CampaignRepository` |
| MyBatis Mapper | `{Domain}Mapper` | `CampaignMapper` |
| MapStruct | `{Domain}DtoMapper` | `CampaignDtoMapper` |
| Entity | `{Domain}` | `Campaign` |
| DTO | `{Domain}Dto` | `CampaignDto` |
| Request | `{Domain}{Action}Request` | `CampaignCreateRequest` |
| Response | `{Domain}{Action}Response` | `CampaignSearchResponse` |
| Exception | `{Domain}NotFoundException` | `CampaignNotFoundException` |

### 메서드명

| 동작 | 접두사 | 예시 |
|------|--------|------|
| 단건 조회 | `find`, `get` | `findById()` |
| 목록 조회 | `findAll`, `getList` | `findAllCampaigns()` |
| 저장 | `save`, `create` | `saveCampaign()` |
| 수정 | `update`, `modify` | `updateCampaign()` |
| 삭제 | `delete`, `remove` | `deleteCampaign()` |
| 존재 확인 | `exists`, `is` | `existsById()` |
| 개수 조회 | `count` | `countByCampaignId()` |

---

## 5. 패키지 구조

### 신규 프로젝트 (수직 분할 - 권장)

도메인 중심으로 패키지를 나눠라. 도메인 간 순환 참조를 방지하기 위함이다.

```
com.guhada.{project}
├── {domain}/
│   ├── controller/
│   ├── service/
│   ├── repository/
│   ├── mapper/          ← MapStruct DtoMapper
│   ├── model/
│   │   ├── dto/
│   │   │   ├── request/
│   │   │   └── response/
│   │   └── entity/
│   ├── exception/
│   └── config/
└── common/
    ├── config/
    ├── exception/       ← GuhadaApiRuntimeException 등
    └── response/        ← GuhadaApiResponse 등
```

### 레거시 (수평 분할)

기존 프로젝트에서 이미 수평 분할 구조를 사용하고 있으면 그대로 유지하라.

```
com.guhada.{project}
├── controller/{domain}/
├── service/{domain}/
├── repository/{domain}/
├── mapper/
├── model/{domain}/
└── exception/
```

---

## 6. 핵심 설계 규칙

### Entity

- `@Getter` + `@NoArgsConstructor(access = PROTECTED)` 사용. `@Data` 금지.
- `BaseEntity`를 상속하라 (createdBy, createdAt, updatedBy, updatedAt 자동 관리).
- `@Builder`는 private 생성자에 붙여라.
- 도메인 로직은 Entity 안에 작성하라 (상태 변경 등).
- 정적 팩토리 메서드(`create()`)로 생성 의도를 명확히 하라.
- 모든 연관관계는 `FetchType.LAZY` 필수.

### DTO

- Request DTO: `@Getter` + `@NoArgsConstructor(access = PRIVATE)` + Bean Validation.
- Response DTO: `@Getter` + `@Builder` (불변).
- Entity를 API에 직접 노출하지 마라. 반드시 DTO로 변환하라.

### MapStruct

- `@Mapper(componentModel = "spring")` 사용.
- 인터페이스명은 `{Domain}DtoMapper`.
- Entity -> Response: `toResponse()`, `toResponseList()`.
- Request -> Entity: `toEntity()` (id 등 자동 생성 필드는 `@Mapping(target, ignore = true)`).

### 응답

- 모든 API 응답은 `GuhadaApiResponse`로 감싸라. 프로젝트 전체 응답 일관성을 위함이다.
- Controller에서 `responseApi()` (BaseController 메서드)를 사용하라.
- 에러 응답은 `GuhadaApiErrorResponse` + `GuhadaApiResult` enum 조합으로 반환하라.

### 예외 처리

- 도메인별 예외 클래스를 만들어라 (예: `CampaignNotFoundException`).
- 공통 예외는 `GuhadaApiRuntimeException` + `GuhadaApiResult`를 사용하라.
- `@ExceptionHandler`로 처리하고, 최상위 `Exception` catch 금지.
- 예외를 삼키지(swallow) 마라.

### 테스트

- 단위 테스트: `@ExtendWith(MockitoExtension.class)` + given/when/then 구조.
- 통합 테스트는 작성하지 않는다 (`@SpringBootTest` 금지). 테스트는 단위 테스트 + Mock으로만 구성한다.
- 테스트 메서드명은 한글 허용 (예: `findById_존재하는_캠페인_조회_성공`).

---

## 7. 성능 규칙

- `Pattern`, `ObjectMapper` 등 고비용 객체는 `static final`로 캐싱하라.
- 반복문 내 `String +` 대신 `StringBuilder`를 사용하라.
- 반복문 내 DB/API 호출 금지. Bulk 연산으로 처리하라.
- 컬렉션 조회는 `Fetch Join` 또는 `EntityGraph`로 N+1을 방지하라.
- 조회 전용 메서드에는 `@Transactional(readOnly = true)`를 붙여라.

---

## 8. 문서화

작업 완료 후 아래 문서를 작성하라.

| 문서 | 내용 |
|------|------|
| `ARCHITECTURE.html` | 시스템 아키텍처, 데이터 흐름, 핵심 로직 (ASCII 다이어그램), 관련 이슈 번호 |
| `SPEC.md` | 기능 설명, API 명세, 사용자 인터페이스, 관련 이슈 번호 |

---

## 9. Git 컨벤션

- `git add`까지만 진행하라. commit은 별도 요청 시에만.
- 커밋 메시지: `{type}({scope}): {description}`
  - type: feat, fix, refactor, test, docs, chore
  - scope: 도메인명
  - description: 변경 내용 (한글 가능)
