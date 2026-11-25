---
name: java-code-rules
description: |
  Java/Kotlin 코드를 작성, 수정, 리팩토링, 생성할 때 반드시 적용해야 하는 코딩 규칙입니다.
  다음 상황에서 자동 트리거됩니다:
  - Java/Kotlin 파일 생성 또는 수정
  - Spring Boot 컨트롤러, 서비스, 리포지토리 작업
  - JPA Entity 생성 또는 수정
  - API 엔드포인트 구현
  - "구현해줘", "코드 작성", "리팩토링", "클래스 만들어줘" 등의 요청
  - build.gradle, pom.xml이 있는 프로젝트에서의 코드 작업
  이 규칙을 무시하거나 건너뛰지 마라. 코드 작성 전에 반드시 읽고 적용하라.
paths:
  - "**/*.java"
  - "**/*.kt"
  - "**/build.gradle"
  - "**/build.gradle.kts"
  - "**/pom.xml"
---

# Java Code Rules

Java/Kotlin 코드 작성 시 **반드시** 적용하는 규칙이다. 예외 없음.

---

## 1. 설계 원칙

모든 코드는 아래 원칙을 기반으로 작성한다.

- **SRP** (Single Responsibility) - 클래스와 메서드는 한 가지 책임만 가진다
- **OCP** (Open-Closed) - 확장에 열려 있고, 변경에 닫혀 있다
- **DIP** (Dependency Inversion) - 구현이 아닌 추상화에 의존한다
- **일급 컬렉션** - 컬렉션을 래핑하여 불변으로 관리하고, 비즈니스 로직을 캡슐화한다
- **디자인 패턴** 적극 활용: Strategy, Factory, Builder, Template Method
- **DRY** - 중복 코드는 즉시 추출한다
- **메서드 단일 기능** - 한 메서드가 두 가지 이상의 일을 하면 분리한다

---

## 2. 금지 항목 (위반 시 즉시 수정)

아래 패턴이 코드에 존재하면 **작성하지 말고**, 이미 있으면 **즉시 수정**하라.

| 금지 패턴 | 대체 방법 | 이유 |
|-----------|----------|------|
| `@Data` | `@Getter` + `@NoArgsConstructor(access = PROTECTED)` + `@Builder` | `@Data`는 `equals`/`hashCode`를 자동 생성하여 JPA Entity에서 순환 참조, 프록시 비교 오류를 일으킨다 |
| `System.out.println()` | SLF4J 로거 (`@Slf4j` + `log.info()`) | 콘솔 출력은 레벨 제어, 파일 기록, 운영 모니터링이 불가능하다 |
| `str != null && !str.isEmpty()` | `StringUtils.hasText(str)` | null + 빈문자열 + 공백문자열을 한 번에 체크한다. 가독성과 안전성이 높다 |
| `Optional` 필드/파라미터 | 반환 타입으로만 사용, `orElseThrow()` 권장 | `Optional`은 직렬화 불가, 필드로 쓰면 의미가 왜곡된다. 반환 타입 전용으로 설계됨 |
| 매직 넘버/문자열 | `static final` 상수 또는 `Enum` | 의미 없는 리터럴은 코드 이해를 방해하고 변경 시 누락을 유발한다 |
| `if-else` 3개 이상 | `switch expression` 또는 `Enum`/`Map` 다형성 | 분기가 늘어날수록 유지보수가 어렵다. 다형성으로 OCP를 지킨다 |
| 최상위 `Exception` catch | 구체적 예외 처리, Custom Exception 정의 | 모든 예외를 잡으면 예상치 못한 에러가 삼켜진다. 명확한 예외 계층이 필요하다 |
| `Entity` API 직접 노출 | `RequestDTO`/`ResponseDTO` 분리, `record` 권장 | Entity가 API에 노출되면 DB 스키마 변경이 API 변경으로 전파된다 |
| `FetchType.EAGER` | 모든 연관관계 `LAZY` 필수 | EAGER는 불필요한 조인을 발생시켜 성능을 심각하게 저하시킨다 |
| 예외 삼키기 (swallow) | 반드시 로깅 또는 재throw | `catch` 블록에서 아무것도 하지 않으면 장애 원인 추적이 불가능하다 |
| `@Setter` (Entity) | 도메인 메서드로 상태 변경 | Setter는 의도를 드러내지 않고, 어디서든 상태를 변경할 수 있어 불변성이 깨진다 |
| `new Date()` / `Calendar` | `LocalDateTime`, `LocalDate`, `Instant` 사용 | `java.util.Date`는 thread-unsafe하고 가변 객체다. `java.time` API를 쓴다 |

### 좋은 예 vs 나쁜 예

**Entity 정의**

```java
// 나쁜 예 - 절대 이렇게 작성하지 마라
@Data
@Entity
public class Member {
    @Id @GeneratedValue
    private Long id;
    private String name;

    @ManyToOne  // EAGER가 기본값
    private Team team;
}
```

```java
// 좋은 예
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
@Entity
public class Member {

    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String name;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "team_id")
    private Team team;

    @Builder
    private Member(String name, Team team) {
        this.name = name;
        this.team = team;
    }

    public void changeTeam(Team team) {
        this.team = team;
    }
}
```

**예외 처리**

```java
// 나쁜 예
try {
    memberRepository.findById(id);
} catch (Exception e) {
    // 삼켜버림
}
```

```java
// 좋은 예
public Member findById(Long id) {
    return memberRepository.findById(id)
        .orElseThrow(() -> new MemberNotFoundException(id));
}
```

**분기 처리**

```java
// 나쁜 예 - if-else 4개
if (status.equals("ACTIVE")) { ... }
else if (status.equals("INACTIVE")) { ... }
else if (status.equals("SUSPENDED")) { ... }
else if (status.equals("DELETED")) { ... }
```

```java
// 좋은 예 - Enum 다형성
public enum MemberStatus {
    ACTIVE {
        @Override
        public void apply(Member member) { /* ... */ }
    },
    INACTIVE {
        @Override
        public void apply(Member member) { /* ... */ }
    };

    public abstract void apply(Member member);
}
```

---

## 3. 성능 위험 지역

아래 패턴은 운영 환경에서 **심각한 성능 문제**를 일으킨다. 반드시 회피하라.

| 위험 패턴 | 올바른 방법 | 이유 |
|-----------|------------|------|
| `Pattern`, `ObjectMapper` 반복 생성 | `static final` 캐싱 | 객체 생성 비용이 높다. 반복 생성 시 GC 부하가 급격히 증가한다 |
| 반복문 내 `String +` | `StringBuilder` 사용 | 문자열 결합마다 새 객체가 생성된다. O(n^2) 메모리 할당이 발생한다 |
| 반복문 내 DB/API 호출 | Bulk 연산으로 변환 | 1,000건 루프 = 1,000번 네트워크 왕복. `saveAll()`, `IN` 절 등으로 묶어라 |
| 컬렉션 조회 (N+1) | `Fetch Join` 또는 `@EntityGraph` | 연관 Entity를 Lazy로 설정해도 루프에서 접근하면 N+1 쿼리가 발생한다 |
| 조회 전용 메서드 | `@Transactional(readOnly = true)` | 읽기 전용 트랜잭션은 JPA 더티체킹을 생략하여 성능이 향상된다 |
| `DateTimeFormatter` 반복 생성 | `static final` 상수 선언 | thread-safe하므로 인스턴스 하나를 재사용한다 |
| `Stream` 중첩 (3단계 이상) | 중간 변수 분리 또는 for 루프 | 과도한 Stream 체이닝은 디버깅이 어렵고 가독성이 떨어진다 |

### 좋은 예 vs 나쁜 예

**고비용 객체 캐싱**

```java
// 나쁜 예
public String serialize(Object obj) {
    ObjectMapper mapper = new ObjectMapper();  // 매 호출마다 생성
    return mapper.writeValueAsString(obj);
}
```

```java
// 좋은 예
private static final ObjectMapper OBJECT_MAPPER = new ObjectMapper();

public String serialize(Object obj) {
    return OBJECT_MAPPER.writeValueAsString(obj);
}
```

**N+1 방지**

```java
// 나쁜 예 - N+1 쿼리 발생
List<Team> teams = teamRepository.findAll();
teams.forEach(team -> {
    log.info("members: {}", team.getMembers().size());  // 팀마다 SELECT 발생
});
```

```java
// 좋은 예 - Fetch Join
@Query("SELECT t FROM Team t JOIN FETCH t.members")
List<Team> findAllWithMembers();
```

---

## 4. 코드 품질

### 상수

- 모든 리터럴 값은 의미 있는 상수로 정의한다
- `private static final`로 선언, `UPPER_SNAKE_CASE` 네이밍

```java
// 나쁜 예
if (age >= 19) { ... }

// 좋은 예
private static final int ADULT_AGE = 19;
if (age >= ADULT_AGE) { ... }
```

### 네이밍

| 대상 | 규칙 | 예시 |
|------|------|------|
| 클래스 | `PascalCase` | `MemberService`, `OrderResponseDto` |
| 메서드/변수 | `camelCase` | `findById`, `memberName` |
| 상수 | `UPPER_SNAKE_CASE` | `MAX_RETRY_COUNT`, `DEFAULT_PAGE_SIZE` |
| 패키지 | `lowercase` | `com.example.member` |

- 이름만 보고 역할을 알 수 있게 명확하게 작성한다
- 축약어를 피한다 (`mem` -> `member`, `cnt` -> `count`)

### 기능 구현 최소 원칙

- 사용하지 않는 메서드/기능은 **절대 생성하지 않는다**
- 요청된 기능에 필요한 **최소한의 코드만** 작성한다
- "나중에 쓸 것 같은" 코드를 미리 만들지 않는다 (YAGNI)
- 불필요한 Getter, Setter, toString, 유틸 메서드 생성 금지

---

## 5. 테스트 규칙

### TDD 필수

테스트 먼저 작성한다. 순서: **테스트 작성 -> 실패 확인 -> 코드 작성 -> 테스트 통과 -> 리팩토링**

### 테스트 품질

- `@DisplayName`으로 한글 테스트 의도를 명시한다
- **Given-When-Then** 패턴을 사용한다
- 하나의 테스트 = 하나의 기능만 검증한다
- 최소 80% 코드 커버리지를 유지한다

```java
@Test
@DisplayName("회원 가입 시 이름이 빈 문자열이면 예외가 발생한다")
void createMember_emptyName_throwsException() {
    // given
    String emptyName = "";

    // when & then
    assertThatThrownBy(() -> new Member(emptyName))
        .isInstanceOf(InvalidMemberNameException.class)
        .hasMessageContaining("이름");
}
```

### 테스트 종류

| 종류 | 어노테이션 | 용도 |
|------|-----------|------|
| 컨트롤러 | `@WebMvcTest` | MockMvc로 HTTP 요청/응답 검증 (Service는 Mock) |
| 서비스 | JUnit + Mockito (`@ExtendWith(MockitoExtension.class)`) | 비즈니스 로직, Mock 의존성 격리 |

> 통합 테스트(`@SpringBootTest`)·리포지토리 테스트(`@DataJpaTest`) 등 DB에 접근하는 테스트는 작성하지 않는다. 테스트는 단위 테스트 + Mock으로만 구성한다.

### 테스트 실행

```bash
./gradlew test                                    # 전체 테스트
./gradlew test --tests {TestClassName}            # 특정 클래스
./gradlew test jacocoTestReport                   # 커버리지 리포트
```

---

## 6. Spring Boot 레이어 규칙

### 레이어 구조

```
Controller → Service → Repository
     │            │
  DTO 변환    비즈니스 로직    (Entity는 Repository 안쪽에서만)
```

각 레이어의 책임을 넘지 않는다. Controller에 비즈니스 로직을 넣지 마라.

### DTO 분리

- `Entity`를 API 응답에 **절대** 직접 사용하지 않는다
- `RequestDTO` / `ResponseDTO`를 분리한다 (Java `record` 권장)
- 변환 로직은 별도 Mapper 또는 정적 팩토리 메서드로 분리한다

```java
// 좋은 예 - record DTO + 정적 팩토리
public record MemberResponse(
    Long id,
    String name,
    String email
) {
    public static MemberResponse from(Member member) {
        return new MemberResponse(
            member.getId(),
            member.getName(),
            member.getEmail()
        );
    }
}
```

### 트랜잭션

| 작업 | 어노테이션 | 이유 |
|------|-----------|------|
| 조회 | `@Transactional(readOnly = true)` | 더티체킹 생략, DB 부하 감소 |
| 변경 | `@Transactional` | 원자성 보장 |
| 컨트롤러 | 트랜잭션 사용 금지 | 서비스 레이어에서만 트랜잭션을 관리한다 |

### 예외 처리

- `@RestControllerAdvice` + `@ExceptionHandler`로 글로벌 처리한다
- Custom Exception 계층 구조를 정의한다
- 에러 응답 DTO를 통일한다

```java
// Custom Exception 예시
public class BusinessException extends RuntimeException {
    private final ErrorCode errorCode;

    public BusinessException(ErrorCode errorCode) {
        super(errorCode.getMessage());
        this.errorCode = errorCode;
    }
}

public class MemberNotFoundException extends BusinessException {
    public MemberNotFoundException(Long id) {
        super(ErrorCode.MEMBER_NOT_FOUND);
    }
}
```

### API 응답 통일

```java
public record ApiResponse<T>(
    boolean success,
    T data,
    String message
) {
    public static <T> ApiResponse<T> ok(T data) {
        return new ApiResponse<>(true, data, null);
    }

    public static ApiResponse<Void> error(String message) {
        return new ApiResponse<>(false, null, message);
    }
}
```

---

## 7. 체크리스트

코드 작성 완료 후, 아래 항목을 **하나씩 확인**하라. 하나라도 위반이면 수정한다.

- [ ] `@Data`, `@Setter` 사용하지 않았는가?
- [ ] `System.out.println()` 대신 SLF4J 로거를 사용했는가?
- [ ] `FetchType.EAGER`가 없는가? (모든 연관관계 `LAZY`)
- [ ] 매직 넘버/문자열을 상수 또는 Enum으로 추출했는가?
- [ ] N+1 쿼리 위험이 없는가? (컬렉션 조회 시 Fetch Join 사용)
- [ ] Entity가 API 응답에 직접 노출되지 않는가? (DTO 분리)
- [ ] 테스트 코드를 작성했는가? (Given-When-Then, `@DisplayName`)
- [ ] 예외를 삼키지 않고 로깅 또는 재throw 했는가?
- [ ] 고비용 객체(`ObjectMapper`, `Pattern`)를 `static final`로 캐싱했는가?
- [ ] 사용하지 않는 메서드/코드가 없는가? (YAGNI)
- [ ] 조회 메서드에 `@Transactional(readOnly = true)`를 적용했는가?
- [ ] `Optional`을 필드/파라미터가 아닌 반환 타입으로만 사용했는가?
