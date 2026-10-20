---
name: spring-api-build
description: Spring Boot 기반 REST API 구현 가이드 스킬. web-backend 에이전트가 사용한다. Controller/Service/Repository/DTO 4-Layer 패턴, Bean Validation, GlobalExceptionHandler, 트랜잭션 경계, JPA N+1 회피, 표준 응답 포맷을 표준화한다. 6_SPEC.html의 확정된 API 계약을 SSOT로 받아 정확히 일치하는 응답 shape의 코드를 생성한다. "Spring Boot API", "Controller 만들기", "REST API 구현", "회원가입 API 개발" 같은 작업에 사용된다.
---

# Spring API Build

Spring Boot REST API 구현 표준 워크플로우. 프론트와 정확히 일치하는 응답 shape을 보장한다.

## 입력

- `track_dir`: Track 경로 (6_SPEC.html의 "API 계약" 섹션이 SSOT)
- `target_endpoints`: 구현할 엔드포인트 목록
- `mode`: `"initial"` | `"partial-rerun"`

## 워크플로우

### Step 1: 프로젝트 컨벤션 감지

기존 코드에서 다음을 샘플링하여 따른다 (CLAUDE.md "외과적 변경"):
- 패키지 구조 (`controller`, `service`, `repository`, `dto`, `entity` 분리 또는 도메인별 패키징)
- 응답 래퍼 클래스 존재 여부 (`ApiResponse<T>` 등)
- 예외 처리 방식 (`@ControllerAdvice` + `GlobalExceptionHandler`)
- DTO 변환 패턴 (수동 매핑 / MapStruct / Lombok @Builder)
- ORM (JPA / MyBatis)
- 인증/인가 (Spring Security 설정)

신규 패턴 도입은 금지. 컨벤션 없으면 아래 표준 패턴을 따른다.

### Step 2: 레이어별 구현

각 endpoint마다 다음 순서로 작성:

#### 2-1. Entity (신규 테이블 필요시만)

```java
@Entity
@Table(name = "users")
@Getter @NoArgsConstructor(access = AccessLevel.PROTECTED)
public class User {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true, length = 100)
    private String email;

    @Column(nullable = false)
    private String passwordHash;

    @Column(nullable = false, length = 16)
    private String nickname;

    @Column(nullable = false, updatable = false)
    private LocalDateTime createdAt;

    @Builder
    private User(String email, String passwordHash, String nickname) {
        this.email = email;
        this.passwordHash = passwordHash;
        this.nickname = nickname;
        this.createdAt = LocalDateTime.now();
    }
}
```

DDL 스크립트는 `{track_dir}/sql/{NN}_create_users.sql`에 저장.

#### 2-2. Repository

```java
public interface UserRepository extends JpaRepository<User, Long> {
    boolean existsByEmail(String email);
    Optional<User> findByEmail(String email);
}
```

#### 2-3. DTO (Request/Response 분리)

```java
public class SignupRequest {
    @NotBlank @Email
    private String email;

    @NotBlank @Size(min = 8)
    @Pattern(regexp = ".*[A-Za-z].*", message = "영문 필수")
    @Pattern(regexp = ".*[0-9].*", message = "숫자 필수")
    private String password;

    @NotBlank @Size(min = 2, max = 16)
    private String nickname;

    // getters
}

public class SignupResponse {
    private Long userId;
    private String email;
    private String createdAt;

    public static SignupResponse from(User u) {
        SignupResponse r = new SignupResponse();
        r.userId = u.getId();
        r.email = u.getEmail();
        r.createdAt = u.getCreatedAt().toString();
        return r;
    }
    // getters
}
```

**중요:** 6_SPEC.html의 API 계약과 필드명/타입을 1:1로 일치시킨다. 임의로 바꾸지 않는다.

#### 2-4. Service

```java
@Service
@RequiredArgsConstructor
public class SignupService {
    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;

    @Transactional
    public SignupResponse signup(SignupRequest req) {
        if (userRepository.existsByEmail(req.getEmail())) {
            throw new DuplicateEmailException(req.getEmail());
        }
        User user = User.builder()
            .email(req.getEmail())
            .passwordHash(passwordEncoder.encode(req.getPassword()))
            .nickname(req.getNickname())
            .build();
        userRepository.save(user);
        return SignupResponse.from(user);
    }
}
```

규칙:
- 쓰기 작업: `@Transactional`
- 읽기 작업: `@Transactional(readOnly = true)`
- 비즈니스 예외는 도메인 예외 클래스로 (`DuplicateEmailException` 등)

#### 2-5. Controller

```java
@RestController
@RequestMapping("/api/users")
@RequiredArgsConstructor
public class UserController {
    private final SignupService signupService;

    @PostMapping
    public ResponseEntity<SignupResponse> signup(@Valid @RequestBody SignupRequest req) {
        SignupResponse res = signupService.signup(req);
        return ResponseEntity.status(HttpStatus.CREATED).body(res);
    }
}
```

규칙:
- `@Valid`로 Bean Validation 트리거
- HTTP 상태 코드는 6_SPEC.html의 약속을 따름
- Controller에 비즈니스 로직 절대 금지

### Step 3: 예외 처리

GlobalExceptionHandler가 이미 있으면 새 도메인 예외만 추가. 없으면 신규 생성:

```java
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ErrorResponse> handleValidation(MethodArgumentNotValidException e) {
        List<FieldError> errors = e.getBindingResult().getFieldErrors().stream()
            .map(f -> new FieldError(f.getField(), f.getDefaultMessage()))
            .toList();
        return ResponseEntity.badRequest()
            .body(new ErrorResponse("VALIDATION_ERROR", errors));
    }

    @ExceptionHandler(DuplicateEmailException.class)
    public ResponseEntity<ErrorResponse> handleDuplicateEmail(DuplicateEmailException e) {
        return ResponseEntity.status(HttpStatus.CONFLICT)
            .body(new ErrorResponse("DUPLICATE_EMAIL", List.of(
                new FieldError("email", "이미 사용 중")
            )));
    }
}
```

에러 응답 shape은 6_SPEC.html의 계약과 일치해야 함.

### Step 4: test-generator 백그라운드 디스패치

API 클래스가 구현 50% 이상 도달하면 즉시:

```
Agent(
  subagent_type="test-generator",
  description="회원가입 API 테스트 생성",
  prompt="...{track_dir}/6_SPEC.html를 시나리오로 사용하여 SignupController + SignupService의 단위 테스트(Mock 기반) 작성...",
  model="opus",
  run_in_background=true
)
```

백그라운드 실행 중 본 구현 계속 진행. 완료 시 결과 통합.

### Step 5: 6_SPEC.html 갱신

API 계약 섹션에 실제 구현 클래스 경로 매핑 추가:

```diff
  ### POST /api/users
  ...
+ **구현:**
+ - Controller: `com.example.user.UserController#signup`
+ - Service: `com.example.user.SignupService#signup`
+ - 응답 DTO: `com.example.user.SignupResponse`
```

### Step 6: test-coverage-check 자동 트리거

구현 + 테스트 완료 직후 `test-coverage-check` 스킬 실행 (CLAUDE.md 룰).

### Step 7: DDL/DATABASE.md 정리

새 테이블/컬럼 추가 시:
- `{track_dir}/sql/` 폴더에 DDL 저장
- `{track_dir}/DATABASE.md`(없으면 신규 생성)에 ER 다이어그램 + 컬럼 정의 추가

## N+1 회피 체크리스트

- 컬렉션 연관 + 반복 접근: `@EntityGraph(attributePaths = ...)` 또는 fetch join
- 의심되면 `spring.jpa.show_sql=true`로 쿼리 횟수 확인
- 복잡한 조회는 QueryDSL 또는 native query 고려

## 보안 체크리스트

- [ ] 모든 외부 입력 `@Valid` 검증
- [ ] 비밀번호는 `PasswordEncoder`로 해시 (평문 저장 금지)
- [ ] SQL Injection: PreparedStatement / JPA 사용 (문자열 연결 금지)
- [ ] 인증 필요 엔드포인트는 SecurityConfig에 명시
- [ ] 응답에 민감 정보 노출 없음 (passwordHash 등)

## partial-rerun 모드

1. 6_SPEC.html의 변경된 endpoint 식별
2. 영향 Controller/Service만 수정
3. 테스트 케이스 갱신 (test-generator 재호출)
4. 회귀 테스트 실행 확인

## 완료 체크리스트

- [ ] target_endpoints의 모든 API 구현
- [ ] 컴파일 + 단위 테스트(Mock 기반) 통과
- [ ] test-coverage-check 통과
- [ ] 6_SPEC.html "API 계약" 섹션의 응답 shape과 실제 응답 일치
- [ ] DDL 스크립트 + DATABASE.md 갱신 (해당 시)
- [ ] 4_PLAN.html의 Phase 3 status = "done"
