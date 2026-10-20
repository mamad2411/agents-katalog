---
name: spring-security-review
category: spring
description: "Spring/Java 보안 리뷰 — SQL Injection, Spring Security 오설정, Mass Assignment, 역직렬화 공격, IDOR, 로깅 정보 노출, 암호·비밀번호 처리, OWASP Dependency-Check/SpotBugs 도구. Use when Spring 애플리케이션 보안 리뷰나 취약점 점검이 필요할 때."
effort: xhigh
deprecated: false
---

# Spring / Java 보안 리뷰

설정 자체는 [`spring-security`](../spring-security/SKILL.md), 언어 무관 원칙은 [`secure-coding`](../secure-coding/SKILL.md) / [`owasp-top10`](../owasp-top10/SKILL.md).
여기서는 **Spring 코드에서 실제로 틀리는 지점**을 다룬다.

## Security Review Checklist

Java/Spring 코드 리뷰 시 반드시 점검해야 할 보안 항목. Red team 공격 시나리오 기반.

### SQL Injection

```java
// ❌ VULNERABLE: 문자열 연결
String query = "SELECT * FROM users WHERE id = " + userId;
Statement stmt = conn.createStatement();
ResultSet rs = stmt.executeQuery(query);
// 🔓 Attack: userId = "1; DROP TABLE users; --"

// ✅ HARDENED: PreparedStatement
PreparedStatement ps = conn.prepareStatement("SELECT * FROM users WHERE id = ?");
ps.setLong(1, userId);
ResultSet rs = ps.executeQuery();

// ✅ Spring Data JPA: 기본적으로 안전
userRepository.findById(userId);  // 파라미터 바인딩 자동

// ❌ VULNERABLE: @Query에 SpEL 직접 삽입
@Query("SELECT u FROM User u WHERE u.name = '#{#name}'")  // SpEL injection
// ✅ HARDENED
@Query("SELECT u FROM User u WHERE u.name = :name")
```

### Spring Security Misconfigurations

```java
// ❌ VULNERABLE: CSRF 비활성화 + 전체 허용
@Bean
SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
    return http
        .csrf(csrf -> csrf.disable())
        .authorizeHttpRequests(auth -> auth.anyRequest().permitAll())
        .build();
}

// ✅ HARDENED: 최소 권한 + CSRF 보호
@Bean
SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
    return http
        .csrf(Customizer.withDefaults())  // SPA는 CookieCsrfTokenRepository 사용
        .authorizeHttpRequests(auth -> auth
            .requestMatchers("/api/public/**").permitAll()
            .requestMatchers("/api/admin/**").hasRole("ADMIN")
            .anyRequest().authenticated()
        )
        .sessionManagement(s -> s.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
        .build();
}
```

### Mass Assignment / Over-Posting

```java
// ❌ VULNERABLE: Entity를 직접 RequestBody로 사용
@PostMapping("/users")
public User createUser(@RequestBody User user) {
    return userRepository.save(user);  // isAdmin=true 주입 가능
}
// 🔓 Attack: {"name":"hacker","isAdmin":true}

// ✅ HARDENED: DTO 분리
public record CreateUserRequest(
    @NotBlank String name,
    @Email String email
) {}

@PostMapping("/users")
public UserResponse createUser(@Valid @RequestBody CreateUserRequest req) {
    User user = User.create(req.name(), req.email());
    return UserResponse.from(userRepository.save(user));
}
```

### Deserialization Attacks

```java
// ❌ VULNERABLE: Java 직렬화 사용
ObjectInputStream ois = new ObjectInputStream(inputStream);
Object obj = ois.readObject();  // RCE 가능 (gadget chain)
// 🔓 Attack: ysoserial 등으로 악성 직렬화 페이로드 생성

// ✅ HARDENED: JSON (Jackson) 사용 + 타입 검증
// Jackson에서도 DefaultTyping 사용 금지
// ❌ mapper.enableDefaultTyping()
// ✅ 명시적 타입만 허용
@JsonTypeInfo(use = JsonTypeInfo.Id.NAME, property = "type")
@JsonSubTypes({@JsonSubTypes.Type(value = Dog.class, name = "dog")})
```

### IDOR (Insecure Direct Object Reference)

```java
// ❌ VULNERABLE: 소유자 검증 없음
@GetMapping("/orders/{id}")
public Order getOrder(@PathVariable Long id) {
    return orderRepository.findById(id).orElseThrow();
    // 🔓 Attack: 다른 사용자의 주문 조회 가능
}

// ✅ HARDENED: 소유자 검증
@GetMapping("/orders/{id}")
public Order getOrder(@PathVariable Long id, @AuthenticationPrincipal UserDetails user) {
    Order order = orderRepository.findById(id).orElseThrow();
    if (!order.getUserId().equals(user.getId())) {
        throw new AccessDeniedException("Not your order");
    }
    return order;
}
```

### Logging & Information Disclosure

```java
// ❌ VULNERABLE: PII/시크릿 로깅
log.info("Login: user={}, password={}", username, password);
log.error("Payment failed: card={}", cardNumber);

// ✅ HARDENED: 민감 정보 마스킹
log.info("Login: user={}", username);
log.error("Payment failed: card=****{}", cardNumber.substring(cardNumber.length()-4));

// ❌ VULNERABLE: 스택 트레이스 API 응답에 노출
@ExceptionHandler(Exception.class)
public ResponseEntity<String> handle(Exception e) {
    return ResponseEntity.status(500).body(e.toString());  // 내부 정보 노출
}

// ✅ HARDENED: generic 응답 + 내부 로깅
@ExceptionHandler(Exception.class)
public ResponseEntity<ErrorResponse> handle(Exception e) {
    log.error("Unhandled exception", e);
    return ResponseEntity.status(500).body(new ErrorResponse("Internal server error"));
}
```

### Crypto & Password

```java
// ❌ VULNERABLE: MD5/SHA-1 비밀번호 해싱
String hashed = DigestUtils.md5Hex(password);

// ✅ HARDENED: BCrypt (Spring Security 기본)
PasswordEncoder encoder = new BCryptPasswordEncoder(12);
String hashed = encoder.encode(password);
boolean matches = encoder.matches(rawPassword, hashed);
```

### Security Tools

```bash
# SpotBugs + FindSecBugs — 정적 보안 분석
./gradlew spotbugsMain

# OWASP Dependency-Check — 의존성 CVE 스캔
./gradlew dependencyCheckAnalyze

# SonarQube — 종합 코드 품질 + 보안
sonar-scanner -Dsonar.projectKey=myproject

# Snyk — 의존성 + 코드 취약점
snyk test
snyk code test
```

## 참조 스킬

- [`spring-security`](../spring-security/SKILL.md) — SecurityFilterChain / Method Security / CORS
- [`spring-oauth2`](../spring-oauth2/SKILL.md) — OAuth2 / JWT 검증
- [`secure-coding`](../secure-coding/SKILL.md) — 언어 공통 입력 검증 / 인코딩
- [`owasp-top10`](../owasp-top10/SKILL.md) — A01~A10 매핑
- [`supply-chain-security`](../supply-chain-security/SKILL.md) — 의존성 취약점 / SBOM
- [`jvm-performance`](../jvm-performance/SKILL.md) — 성능 튜닝
