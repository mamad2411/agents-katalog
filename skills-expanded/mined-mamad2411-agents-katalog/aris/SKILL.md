# ARIS Project - Cursor Rules

## 📋 프로젝트 개요

**ARIS (Advanced Request & Issue Management System)**
IT 프로젝트의 SR(Service Request), SPEC, 승인, 장애 등을 통합 관리하는 엔터프라이즈급 관리 시스템

### 기술 스택
- **Backend**: Spring Boot 3.x (Java 17)
- **Database**: PostgreSQL 15+
- **Infrastructure**: Docker & Docker Compose
- **Authentication**: JWT (JSON Web Token)
- **ORM**: Spring Data JPA
- **Migration**: Flyway
- **Documentation**: Swagger/OpenAPI 3.0
- **Testing**: JUnit 5, Mockito, TestContainers

---

## 🎯 MVP 3단계 전략

### Phase 1: 핵심 기반 (Core Foundation)
- 사용자 인증/인가 (JWT)
- 권한 관리 (RBAC)
- 사용자 관리
- 기본 UI 프레임워크

### Phase 2: 핵심 업무 흐름 (Core Business Flow)
- IT 사업/프로젝트 관리
- SR 관리 (개발/운영)
- SPEC 관리
- 승인 프로세스

### Phase 3: 확장 기능 (Extended Features)
- 이슈 관리
- 릴리즈 관리
- 장애/인시던트 관리
- 통계 및 리포트
- 파트너/자산 관리
- 알림 및 배치

---

## 🏗️ 프로젝트 구조

```
ARIS/
├── backend/
│   ├── src/main/java/com/aris/
│   │   ├── domain/              # 도메인별 패키지
│   │   │   ├── user/            # 사용자 도메인
│   │   │   │   ├── entity/      # JPA Entity
│   │   │   │   ├── dto/         # DTO (Request/Response)
│   │   │   │   ├── repository/  # Repository Interface
│   │   │   │   ├── service/     # Business Logic
│   │   │   │   └── controller/  # REST Controller
│   │   │   ├── auth/            # 인증/인가
│   │   │   ├── project/         # 프로젝트
│   │   │   ├── sr/              # SR 관리
│   │   │   ├── spec/            # SPEC 관리
│   │   │   └── approval/        # 승인
│   │   └── global/              # 공통 모듈
│   │       ├── config/          # Configuration
│   │       ├── security/        # Security 설정
│   │       ├── exception/       # 예외 처리
│   │       ├── common/          # 공통 유틸리티
│   │       └── entity/          # BaseEntity 등
│   ├── src/main/resources/
│   │   ├── application.yml      # 설정 파일
│   │   ├── application-dev.yml  # 개발 환경
│   │   ├── application-prod.yml # 운영 환경
│   │   └── db/migration/        # Flyway migrations
│   └── src/test/                # 테스트 코드
├── docker-compose.yml
├── .cursorrules
└── docs/
    ├── MVP_3Phase_Plan.md
    ├── Database_Schema_Design.md
    ├── API_Specification.md
    └── Development_Guide.md
```

---

## 💻 코딩 컨벤션

### 1. 네이밍 규칙

#### Java Class/Interface
```java
// Entity
public class User extends BaseEntity { }
public class ServiceRequest extends BaseEntity { }

// DTO - Request
public class UserCreateRequest { }
public class SrCreateRequest { }

// DTO - Response
public class UserResponse { }
public class SrDetailResponse { }

// Repository
public interface UserRepository extends JpaRepository<User, Long> { }

// Service
@Service
public class UserService { }

// Controller
@RestController
@RequestMapping("/api/users")
public class UserController { }
```

#### 변수명
```java
// Camel Case
private String userName;
private Long userId;
private LocalDateTime createdAt;

// Boolean은 is/has 접두사
private boolean isActive;
private boolean hasPermission;

// Collection은 복수형
private List<User> users;
private Set<Role> roles;
```

#### 메서드명
```java
// CRUD
public User create(UserCreateRequest request)
public User findById(Long id)
public User update(Long id, UserUpdateRequest request)
public void delete(Long id)

// Query
public List<User> findAllByCompany(String companyName)
public Optional<User> findByEmail(String email)

// Business Logic
public void assignRole(Long userId, Long roleId)
public void activateUser(Long userId)
public boolean validatePassword(String rawPassword, String encodedPassword)
```

### 2. 레이어별 책임

#### Controller Layer
- HTTP 요청/응답 처리
- DTO 변환
- 간단한 유효성 검증 (`@Valid`)
- 예외는 GlobalExceptionHandler에게 위임

```java
@RestController
@RequestMapping("/api/users")
@RequiredArgsConstructor
@Tag(name = "User", description = "사용자 관리 API")
public class UserController {
    
    private final UserService userService;
    
    @PostMapping
    @Operation(summary = "사용자 등록", description = "새로운 사용자를 등록합니다.")
    public ResponseEntity<UserResponse> createUser(
            @Valid @RequestBody UserCreateRequest request) {
        UserResponse response = userService.createUser(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }
}
```

#### Service Layer
- 비즈니스 로직 구현
- 트랜잭션 관리 (`@Transactional`)
- 도메인 규칙 검증
- 여러 Repository 조합

```java
@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class UserService {
    
    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    
    @Transactional
    public UserResponse createUser(UserCreateRequest request) {
        // 중복 검증
        if (userRepository.existsByEmail(request.getEmail())) {
            throw new DuplicateEmailException("이미 존재하는 이메일입니다.");
        }
        
        // Entity 생성
        User user = User.builder()
                .email(request.getEmail())
                .password(passwordEncoder.encode(request.getPassword()))
                .name(request.getName())
                .build();
        
        // 저장 및 반환
        User savedUser = userRepository.save(user);
        return UserResponse.from(savedUser);
    }
}
```

#### Repository Layer
- 데이터 접근 로직
- Query Method 또는 @Query 사용
- 복잡한 동적 쿼리는 QueryDSL 활용

```java
@Repository
public interface UserRepository extends JpaRepository<User, Long> {
    
    Optional<User> findByEmail(String email);
    
    boolean existsByEmail(String email);
    
    @Query("SELECT u FROM User u WHERE u.company.id = :companyId AND u.deletedAt IS NULL")
    List<User> findActiveUsersByCompany(@Param("companyId") Long companyId);
}
```

### 3. Entity 설계 원칙

```java
@Entity
@Table(name = "users")
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
@EntityListeners(AuditingEntityListener.class)
public class User extends BaseEntity {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(nullable = false, unique = true, length = 100)
    private String email;
    
    @Column(nullable = false)
    private String password;
    
    @Column(nullable = false, length = 50)
    private String name;
    
    @Column(length = 20)
    private String phoneNumber;
    
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "company_id")
    private Company company;
    
    @ManyToMany
    @JoinTable(
        name = "user_roles",
        joinColumns = @JoinColumn(name = "user_id"),
        inverseJoinColumns = @JoinColumn(name = "role_id")
    )
    private Set<Role> roles = new HashSet<>();
    
    @Builder
    public User(String email, String password, String name, String phoneNumber, Company company) {
        this.email = email;
        this.password = password;
        this.name = name;
        this.phoneNumber = phoneNumber;
        this.company = company;
    }
    
    // Business Methods
    public void changePassword(String newPassword) {
        this.password = newPassword;
    }
    
    public void assignRole(Role role) {
        this.roles.add(role);
    }
}
```

#### BaseEntity (공통 엔티티)
```java
@Getter
@MappedSuperclass
@EntityListeners(AuditingEntityListener.class)
public abstract class BaseEntity {
    
    @CreatedDate
    @Column(nullable = false, updatable = false)
    private LocalDateTime createdAt;
    
    @CreatedBy
    @Column(nullable = false, updatable = false, length = 50)
    private String createdBy;
    
    @LastModifiedDate
    @Column(nullable = false)
    private LocalDateTime updatedAt;
    
    @LastModifiedBy
    @Column(nullable = false, length = 50)
    private String updatedBy;
    
    @Column
    private LocalDateTime deletedAt;
    
    @Version
    private Long version;
    
    // Soft Delete
    public void delete() {
        this.deletedAt = LocalDateTime.now();
    }
    
    public boolean isDeleted() {
        return deletedAt != null;
    }
}
```

### 4. DTO 패턴

```java
// Request DTO
@Getter
@NoArgsConstructor
public class UserCreateRequest {
    
    @NotBlank(message = "이메일은 필수입니다.")
    @Email(message = "올바른 이메일 형식이 아닙니다.")
    private String email;
    
    @NotBlank(message = "비밀번호는 필수입니다.")
    @Size(min = 8, max = 20, message = "비밀번호는 8~20자여야 합니다.")
    private String password;
    
    @NotBlank(message = "이름은 필수입니다.")
    @Size(max = 50, message = "이름은 50자 이내여야 합니다.")
    private String name;
    
    @Pattern(regexp = "^01[0-9]-[0-9]{4}-[0-9]{4}$", message = "올바른 전화번호 형식이 아닙니다.")
    private String phoneNumber;
    
    private Long companyId;
}

// Response DTO
@Getter
@Builder
public class UserResponse {
    private Long id;
    private String email;
    private String name;
    private String phoneNumber;
    private String companyName;
    private List<String> roles;
    private LocalDateTime createdAt;
    
    public static UserResponse from(User user) {
        return UserResponse.builder()
                .id(user.getId())
                .email(user.getEmail())
                .name(user.getName())
                .phoneNumber(user.getPhoneNumber())
                .companyName(user.getCompany() != null ? user.getCompany().getName() : null)
                .roles(user.getRoles().stream()
                        .map(Role::getName)
                        .collect(Collectors.toList()))
                .createdAt(user.getCreatedAt())
                .build();
    }
}
```

### 5. 예외 처리 전략

```java
// Custom Exception
public class BusinessException extends RuntimeException {
    private final ErrorCode errorCode;
    
    public BusinessException(ErrorCode errorCode) {
        super(errorCode.getMessage());
        this.errorCode = errorCode;
    }
}

// Error Code
@Getter
@RequiredArgsConstructor
public enum ErrorCode {
    // User
    USER_NOT_FOUND("U001", "사용자를 찾을 수 없습니다."),
    DUPLICATE_EMAIL("U002", "이미 존재하는 이메일입니다."),
    INVALID_PASSWORD("U003", "비밀번호가 일치하지 않습니다."),
    
    // Auth
    UNAUTHORIZED("A001", "인증이 필요합니다."),
    FORBIDDEN("A002", "권한이 없습니다."),
    INVALID_TOKEN("A003", "유효하지 않은 토큰입니다."),
    
    // Common
    INVALID_INPUT("C001", "입력값이 올바르지 않습니다."),
    INTERNAL_SERVER_ERROR("C999", "서버 오류가 발생했습니다.");
    
    private final String code;
    private final String message;
}

// Global Exception Handler
@RestControllerAdvice
@Slf4j
public class GlobalExceptionHandler {
    
    @ExceptionHandler(BusinessException.class)
    public ResponseEntity<ErrorResponse> handleBusinessException(BusinessException e) {
        log.error("BusinessException: {}", e.getMessage());
        ErrorResponse response = ErrorResponse.of(e.getErrorCode());
        return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(response);
    }
    
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ErrorResponse> handleValidationException(MethodArgumentNotValidException e) {
        log.error("ValidationException: {}", e.getMessage());
        ErrorResponse response = ErrorResponse.of(ErrorCode.INVALID_INPUT, e.getBindingResult());
        return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(response);
    }
    
    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> handleException(Exception e) {
        log.error("Unexpected Exception: {}", e.getMessage(), e);
        ErrorResponse response = ErrorResponse.of(ErrorCode.INTERNAL_SERVER_ERROR);
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(response);
    }
}
```

---

## 🔐 보안 가이드라인

### 1. JWT 인증 구현
```java
@Component
@RequiredArgsConstructor
public class JwtTokenProvider {
    
    @Value("${jwt.secret}")
    private String secretKey;
    
    @Value("${jwt.access-token-validity}")
    private long accessTokenValidity;
    
    @Value("${jwt.refresh-token-validity}")
    private long refreshTokenValidity;
    
    public String createAccessToken(String email, List<String> roles) {
        Claims claims = Jwts.claims().setSubject(email);
        claims.put("roles", roles);
        
        Date now = new Date();
        Date validity = new Date(now.getTime() + accessTokenValidity);
        
        return Jwts.builder()
                .setClaims(claims)
                .setIssuedAt(now)
                .setExpiration(validity)
                .signWith(SignatureAlgorithm.HS256, secretKey)
                .compact();
    }
}
```

### 2. Security Configuration
```java
@Configuration
@EnableWebSecurity
@EnableMethodSecurity
@RequiredArgsConstructor
public class SecurityConfig {
    
    private final JwtTokenProvider jwtTokenProvider;
    
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .csrf(csrf -> csrf.disable())
            .sessionManagement(session -> 
                session.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/api/auth/**").permitAll()
                .requestMatchers("/swagger-ui/**", "/v3/api-docs/**").permitAll()
                .anyRequest().authenticated())
            .addFilterBefore(new JwtAuthenticationFilter(jwtTokenProvider), 
                UsernamePasswordAuthenticationFilter.class);
        
        return http.build();
    }
    
    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }
}
```

### 3. 메서드 레벨 보안
```java
@Service
@RequiredArgsConstructor
public class UserService {
    
    @PreAuthorize("hasRole('ADMIN')")
    public void deleteUser(Long userId) {
        // Only ADMIN can delete users
    }
    
    @PreAuthorize("hasRole('ADMIN') or #userId == authentication.principal.id")
    public UserResponse getUserDetail(Long userId) {
        // ADMIN can view anyone, users can view their own profile
    }
}
```

---

## 🗄️ 데이터베이스 원칙

### 1. Soft Delete 원칙
- 모든 엔티티는 `BaseEntity`를 상속
- 물리적 삭제 금지, `deletedAt` 필드로 논리적 삭제
- 조회 시 `deletedAt IS NULL` 조건 필수

### 2. Auditing 자동화
```java
@Configuration
@EnableJpaAuditing
public class JpaConfig {
    
    @Bean
    public AuditorAware<String> auditorProvider() {
        return () -> {
            Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
            if (authentication == null || !authentication.isAuthenticated()) {
                return Optional.of("system");
            }
            return Optional.of(authentication.getName());
        };
    }
}
```

### 3. 인덱스 전략
```java
@Entity
@Table(name = "users", indexes = {
    @Index(name = "idx_user_email", columnList = "email"),
    @Index(name = "idx_user_company", columnList = "company_id"),
    @Index(name = "idx_user_deleted", columnList = "deleted_at")
})
public class User extends BaseEntity {
    // ...
}
```

### 4. 연관관계 매핑
- `@ManyToOne`: 기본 `FetchType.LAZY`
- `@OneToMany`: 기본 `FetchType.LAZY` (변경 금지)
- N+1 문제 발생 시 `@EntityGraph` 또는 `JOIN FETCH` 사용
- 양방향 연관관계는 꼭 필요한 경우만 사용

---

## 🧪 테스트 전략

### 1. 테스트 구조
```
src/test/java/com/aris/
├── domain/
│   └── user/
│       ├── controller/
│       │   └── UserControllerTest.java  # MockMvc
│       ├── service/
│       │   └── UserServiceTest.java     # Unit Test
│       └── repository/
│           └── UserRepositoryTest.java  # @DataJpaTest
└── integration/
    └── UserIntegrationTest.java         # TestContainers
```

### 2. Repository 테스트
```java
@DataJpaTest
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
@Testcontainers
class UserRepositoryTest {
    
    @Container
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:15-alpine");
    
    @Autowired
    private UserRepository userRepository;
    
    @Test
    @DisplayName("이메일로 사용자를 조회할 수 있다")
    void findByEmail() {
        // given
        User user = User.builder()
                .email("test@example.com")
                .password("password")
                .name("Test User")
                .build();
        userRepository.save(user);
        
        // when
        Optional<User> found = userRepository.findByEmail("test@example.com");
        
        // then
        assertThat(found).isPresent();
        assertThat(found.get().getEmail()).isEqualTo("test@example.com");
    }
}
```

### 3. Service 테스트
```java
@ExtendWith(MockitoExtension.class)
class UserServiceTest {
    
    @Mock
    private UserRepository userRepository;
    
    @Mock
    private PasswordEncoder passwordEncoder;
    
    @InjectMocks
    private UserService userService;
    
    @Test
    @DisplayName("사용자를 생성할 수 있다")
    void createUser() {
        // given
        UserCreateRequest request = new UserCreateRequest();
        // ... set request fields
        
        given(userRepository.existsByEmail(anyString())).willReturn(false);
        given(passwordEncoder.encode(anyString())).willReturn("encodedPassword");
        given(userRepository.save(any(User.class))).willReturn(user);
        
        // when
        UserResponse response = userService.createUser(request);
        
        // then
        assertThat(response).isNotNull();
        verify(userRepository).save(any(User.class));
    }
}
```

### 4. Controller 테스트
```java
@WebMvcTest(UserController.class)
@AutoConfigureMockMvc(addFilters = false)
class UserControllerTest {
    
    @Autowired
    private MockMvc mockMvc;
    
    @MockBean
    private UserService userService;
    
    @Autowired
    private ObjectMapper objectMapper;
    
    @Test
    @DisplayName("사용자 생성 API를 호출할 수 있다")
    void createUser() throws Exception {
        // given
        UserCreateRequest request = new UserCreateRequest();
        // ... set request
        
        UserResponse response = UserResponse.builder()
                .id(1L)
                .email("test@example.com")
                .build();
        
        given(userService.createUser(any(UserCreateRequest.class))).willReturn(response);
        
        // when & then
        mockMvc.perform(post("/api/users")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.id").value(1L))
                .andExpect(jsonPath("$.email").value("test@example.com"));
    }
}
```

---

## 📝 문서화 규칙

### 1. Swagger 어노테이션
```java
@Tag(name = "User", description = "사용자 관리 API")
@RestController
@RequestMapping("/api/users")
public class UserController {
    
    @Operation(
        summary = "사용자 목록 조회",
        description = "필터 조건에 맞는 사용자 목록을 페이징하여 조회합니다."
    )
    @ApiResponses({
        @ApiResponse(responseCode = "200", description = "조회 성공"),
        @ApiResponse(responseCode = "401", description = "인증 실패"),
        @ApiResponse(responseCode = "403", description = "권한 없음")
    })
    @GetMapping
    public ResponseEntity<Page<UserResponse>> getUsers(
            @Parameter(description = "페이지 번호 (0부터 시작)") @RequestParam(defaultValue = "0") int page,
            @Parameter(description = "페이지 크기") @RequestParam(defaultValue = "20") int size) {
        // ...
    }
}
```

### 2. JavaDoc (복잡한 비즈니스 로직만)
```java
/**
 * SR 승인 프로세스를 처리합니다.
 * 
 * <p>승인 단계:
 * 1. 요청부서 팀장 승인
 * 2. IT 부서 검토
 * 3. PM 최종 승인
 * 
 * @param srId SR ID
 * @param request 승인 요청 정보
 * @return 승인된 SR 정보
 * @throws SrNotFoundException SR을 찾을 수 없는 경우
 * @throws InvalidApprovalStateException 승인할 수 없는 상태인 경우
 */
@Transactional
public SrResponse approveSr(Long srId, ApprovalRequest request) {
    // ...
}
```

---

## 🌿 Git 브랜치 전략

### Branch Naming
- `main`: 운영 배포 브랜치
- `develop`: 개발 통합 브랜치
- `feature/[MVP-PHASE]-[FEATURE-NAME]`: 기능 개발 브랜치
  - 예: `feature/mvp1-user-auth`, `feature/mvp2-sr-management`
- `bugfix/[ISSUE-NUMBER]`: 버그 수정 브랜치
- `hotfix/[ISSUE-NUMBER]`: 긴급 수정 브랜치

### Commit Message Convention
```
[TYPE] 간단한 설명 (50자 이내)

상세 설명 (선택사항, 72자 줄바꿈)

Related to: #123
```

**TYPE**:
- `feat`: 새로운 기능
- `fix`: 버그 수정
- `refactor`: 리팩토링
- `docs`: 문서 수정
- `test`: 테스트 코드
- `chore`: 빌드, 설정 변경

**예시**:
```
[feat] 사용자 등록 API 구현

- UserCreateRequest DTO 추가
- UserService.createUser() 메서드 구현
- 이메일 중복 검증 로직 추가

Related to: #10
```

---

## 🚀 개발 워크플로우

### 1. 로컬 개발 환경 실행
```bash
# PostgreSQL 실행
docker-compose up -d postgres

# Backend 실행 (IDE 또는 Maven)
./mvnw spring-boot:run -Dspring-boot.run.profiles=dev

# 또는 전체 Docker 환경
docker-compose up
```

### 2. API 테스트
- Swagger UI: `http://localhost:8080/swagger-ui.html`
- H2 Console (dev): `http://localhost:8080/h2-console`

### 3. 개발 순서 (Feature 단위)
1. Issue 생성 및 Branch 생성
2. Entity 설계 및 Flyway Migration 작성
3. Repository 작성 및 테스트
4. Service 작성 및 테스트
5. Controller 작성 및 테스트
6. Swagger 문서 확인
7. PR 생성 및 리뷰
8. Merge to develop

---

## ⚙️ 환경 설정

### application.yml (공통)
```yaml
spring:
  application:
    name: aris
  
  jpa:
    hibernate:
      ddl-auto: validate
    show-sql: false
    properties:
      hibernate:
        format_sql: true
        default_batch_fetch_size: 100
  
  flyway:
    enabled: true
    baseline-on-migrate: true

jwt:
  secret: ${JWT_SECRET:your-secret-key-must-be-at-least-256-bits-long}
  access-token-validity: 3600000  # 1 hour
  refresh-token-validity: 604800000  # 7 days

springdoc:
  api-docs:
    path: /v3/api-docs
  swagger-ui:
    path: /swagger-ui.html
    tags-sorter: alpha
    operations-sorter: alpha
```

### application-dev.yml (개발)
```yaml
spring:
  datasource:
    url: jdbc:postgresql://localhost:5432/aris_db
    username: aris_user
    password: aris_password
  
  jpa:
    show-sql: true
    properties:
      hibernate:
        format_sql: true

logging:
  level:
    com.aris: DEBUG
    org.hibernate.SQL: DEBUG
    org.hibernate.type.descriptor.sql.BasicBinder: TRACE
```

---

## 📌 중요 원칙

### DO ✅
- Entity는 직접 반환하지 말고 DTO로 변환
- 비즈니스 로직은 Service Layer에 작성
- @Transactional은 Service Layer에만 사용
- Soft Delete 원칙 준수
- 예외는 명확한 ErrorCode와 함께 발생
- 테스트 코드 작성 (최소 커버리지 80%)
- Swagger 문서 작성
- Git Commit Convention 준수

### DON'T ❌
- Controller에 비즈니스 로직 작성 금지
- Entity를 직접 Request/Response로 사용 금지
- 물리적 삭제 금지 (deletedAt 사용)
- 하드코딩된 상수 사용 금지 (Enum 사용)
- N+1 문제 방치 금지
- 트랜잭션 범위 과도하게 넓히지 말기
- @Transactional(readOnly = true) 없이 조회 금지
- 테스트 없이 PR 금지

---

## 🔄 Phase별 개발 우선순위

### MVP Phase 1 (2-3주)
1. Spring Boot 프로젝트 초기 설정
2. Docker & PostgreSQL 환경 구축
3. BaseEntity, AuditingConfig 구현
4. User, Role, Company Entity 설계
5. JWT 인증/인가 구현
6. 사용자 CRUD API 구현
7. Swagger 문서화

### MVP Phase 2 (3-4주)
1. Project Entity 설계
2. SR (ServiceRequest) Entity 설계
3. Spec Entity 설계
4. Approval Entity 및 Workflow 설계
5. SR CRUD API 구현
6. Spec CRUD API 구현
7. 승인 프로세스 API 구현
8. 파일 첨부 기능 구현

### MVP Phase 3 (4-5주)
1. Issue Entity 설계
2. Release Entity 설계
3. Incident Entity 설계
4. 이슈/릴리즈/장애 관리 API 구현
5. 통계 API 구현
6. 알림 시스템 구현
7. 배치 작업 구현
8. 파트너/자산 관리 API 구현

---

## 📚 참고 자료

- [Spring Boot Documentation](https://docs.spring.io/spring-boot/docs/current/reference/html/)
- [Spring Data JPA](https://docs.spring.io/spring-data/jpa/docs/current/reference/html/)
- [Spring Security](https://docs.spring.io/spring-security/reference/index.html)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Flyway Documentation](https://flywaydb.org/documentation/)
- [TestContainers](https://www.testcontainers.org/)

---

**Last Updated**: 2025-10-15
**Version**: 1.0.0









