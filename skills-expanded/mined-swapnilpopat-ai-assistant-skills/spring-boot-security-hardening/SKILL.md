---
name: spring-boot-security-hardening
description: Secure Spring Boot applications with practical authentication, authorization, and secure defaults. Use when adding or reviewing security in Spring Boot services.
context: fork
agent: general-purpose
allowed-tools: Read, Grep, Glob, Write, Edit
---

# Spring Boot Security Hardening

Apply strong, practical security controls to a Spring Boot 3.x service: component-based `SecurityFilterChain`, OAuth2 Resource Server (JWT), method-level authorization, secure HTTP headers, CORS/CSRF policy, secret hygiene, and OWASP API Security Top 10 (2023) coverage.

## Context

You are implementing or auditing security in a Spring Boot 3.x service. Default to deny-by-default, validate at the boundary, and never leak internal details. Spring Security 6 removed `WebSecurityConfigurerAdapter`; configuration is component-based via `SecurityFilterChain` beans.

## When to Use This Skill

- Adding authentication/authorization to a new API.
- Migrating Spring Security 5 (`WebSecurityConfigurerAdapter`) to Spring Security 6.
- Pre-release hardening pass before exposing externally.
- Triaging a finding from a pen test or SAST/DAST scan.

## Prerequisites

- `spring-boot-starter-security` (always for any externally-reachable service).
- For JWT/OAuth2: `spring-boot-starter-oauth2-resource-server`.
- For OIDC login: `spring-boot-starter-oauth2-client`.
- Identity provider decided (Keycloak, Auth0, Cognito, Entra ID, ...).
- Secrets backend decided (env vars, K8s `Secret`, Vault, AWS/GCP Secrets Manager).

## Instructions

### 1. Choose Authentication Per Interface, Document It

| Interface | Default | Notes |
| --- | --- | --- |
| Public API (browser SPA) | OAuth2/OIDC PKCE flow at the SPA, JWT bearer to the API | Server is OAuth2 **Resource Server** |
| Service-to-service | OAuth2 Client Credentials | Short-lived JWTs, audience-scoped |
| Internal admin | OIDC login + session, MFA enforced at IdP | Use `oauth2Login()` |
| Webhooks | HMAC signature verification + nonce + replay window | Plus IP allow-list if possible |

Reject mixing strategies on the same endpoint.

### 2. `SecurityFilterChain` (Spring Security 6 idiomatic)

Resource server with JWT, deny-by-default, stateless:

```java
@Configuration
@EnableWebSecurity
@EnableMethodSecurity              // enables @PreAuthorize / @PostAuthorize
class SecurityConfig {

    @Bean
    SecurityFilterChain api(HttpSecurity http, JwtAuthConverter jwt) throws Exception {
        http
            .securityMatcher("/api/**")
            .authorizeHttpRequests(a -> a
                .requestMatchers(HttpMethod.GET, "/api/v1/health/public").permitAll()
                .anyRequest().authenticated())
            .oauth2ResourceServer(o -> o
                .jwt(j -> j.jwtAuthenticationConverter(jwt)))
            .sessionManagement(s -> s.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
            .csrf(CsrfConfigurer::disable)                 // stateless JWT API
            .cors(Customizer.withDefaults())
            .headers(h -> h
                .httpStrictTransportSecurity(hsts -> hsts.includeSubDomains(true).maxAgeInSeconds(31536000))
                .contentTypeOptions(Customizer.withDefaults())
                .frameOptions(FrameOptionsConfig::deny)
                .referrerPolicy(r -> r.policy(ReferrerPolicy.STRICT_ORIGIN_WHEN_CROSS_ORIGIN))
                .permissionsPolicy(p -> p.policy("geolocation=(), camera=(), microphone=()"))
                .contentSecurityPolicy(csp -> csp.policyDirectives("default-src 'none'; frame-ancestors 'none'")));
        return http.build();
    }

    @Bean
    SecurityFilterChain actuator(HttpSecurity http) throws Exception {
        http
            .securityMatcher(EndpointRequest.toAnyEndpoint())
            .authorizeHttpRequests(a -> a
                .requestMatchers(EndpointRequest.to("health", "info")).permitAll()
                .anyRequest().hasAuthority("SCOPE_actuator"))
            .httpBasic(Customizer.withDefaults())
            .csrf(CsrfConfigurer::disable);
        return http.build();
    }

    @Bean
    CorsConfigurationSource corsConfigurationSource(@Value("${security.cors.allowed-origins}") List<String> origins) {
        var c = new CorsConfiguration();
        c.setAllowedOrigins(origins);                       // explicit list, NEVER "*"
        c.setAllowedMethods(List.of("GET","POST","PUT","PATCH","DELETE"));
        c.setAllowedHeaders(List.of("Authorization","Content-Type","If-Match","Idempotency-Key"));
        c.setExposedHeaders(List.of("ETag","Location"));
        c.setAllowCredentials(true);
        c.setMaxAge(3600L);
        var src = new UrlBasedCorsConfigurationSource();
        src.registerCorsConfiguration("/api/**", c);
        return src;
    }
}
```

JWT to authorities (use scopes/roles claim from your IdP):

```java
@Component
class JwtAuthConverter implements Converter<Jwt, AbstractAuthenticationToken> {
    @Override
    public AbstractAuthenticationToken convert(Jwt jwt) {
        var scopes = ((Collection<String>) jwt.getClaimAsMap("realm_access").getOrDefault("roles", List.of()));
        var authorities = scopes.stream().map(r -> new SimpleGrantedAuthority("ROLE_" + r)).toList();
        return new JwtAuthenticationToken(jwt, authorities, jwt.getSubject());
    }
}
```

```yaml
spring:
  security:
    oauth2:
      resourceserver:
        jwt:
          issuer-uri: https://idp.acme.com/realms/orders
          # Spring auto-discovers JWKS via OIDC discovery
```

### 3. Method-Level Authorization

```java
@Service
class OrderService {

    @PreAuthorize("hasRole('order.read') or @ownership.canRead(#id, authentication)")
    public OrderResponse get(UUID id) { ... }

    @PreAuthorize("hasRole('order.write')")
    public OrderResponse place(CreateOrderRequest req) { ... }
}
```

Use SpEL with helper beans (`@ownership`) for resource-scoped checks. Avoid copy-pasting auth checks across controllers.

### 4. CSRF Policy

| Auth model | CSRF |
| --- | --- |
| Stateless JWT (Authorization header) | Disable (`csrf.disable()`) - no ambient credentials |
| Session-cookie auth | **Enable** with `CookieCsrfTokenRepository.withHttpOnlyFalse()` for SPA |
| Mixed | Per-chain config; do not "just disable" globally |

If you disable CSRF for an API, document why in code.

### 5. Input Validation, Authorization Bypass (OWASP API Top 10)

The most common API security failures (2023 Top 10):

- **API1 BOLA** (Broken Object-Level Authorization): every resource access must verify the caller owns/may access the object. Don't rely on URL hiding.
- **API2 Broken Authentication**: validate JWT signature *and* `iss`, `aud`, `exp`, `nbf`. Reject `alg: none`.
- **API3 BOPLA** (Property-level): never bind request directly into JPA entity (mass assignment); use DTO records with explicit fields.
- **API4 Unrestricted Resource Consumption**: rate limit, cap page size, body size (`spring.servlet.multipart.max-file-size`, `server.tomcat.max-http-form-post-size`).
- **API5 BFLA** (Function-level): `@PreAuthorize` on every privileged method, deny-by-default route matchers.
- **API6 Sensitive Business Flows**: rate limit + bot defenses on signup, password reset, checkout.
- **API7 SSRF**: validate outbound URLs; allow-list hosts; block link-local / metadata IPs (`169.254.0.0/16`, `127.0.0.0/8`).
- **API8 Security Misconfiguration**: actuator lockdown, headers, no debug endpoints in prod.
- **API9 Improper Inventory**: keep an OpenAPI spec; gate prod deploy of undocumented endpoints.
- **API10 Unsafe Consumption of APIs**: validate responses from upstream; timeouts; circuit breakers.

### 6. Secrets and Sensitive Data

- No secrets in source, `application.yml`, or git history (verify with `gitleaks`/`trufflehog` in CI).
- Inject via env / K8s `Secret` mounted file / external secret manager. Use `spring.config.import=optional:file:/etc/secrets/`.
- Rotate JWT signing keys (IdP responsibility) and downstream API keys; track expiry.
- Mask in logs: never log `Authorization`, `Cookie`, `Set-Cookie`, tokens, passwords, full PII. Configure log scrubbers.
- Hash passwords (only if you do password auth - prefer IdP) with `BCryptPasswordEncoder` (cost >= 12) or `Argon2PasswordEncoder`.

### 7. Error Behavior

Return RFC 9457 ProblemDetail with stable codes (see exception-handling module). Never reveal:

- Whether a username exists ("invalid credentials" only).
- Stack traces.
- Internal endpoints or beans.

Configure:

```yaml
server:
  error:
    include-message: never
    include-stacktrace: never
    include-exception: false
```

### 8. Operational Hardening

- Actuator: expose only `health,info,prometheus` in prod; secure others; consider a separate `management.server.port` not exposed to internet.
- Run on a non-root container user (see docker-kubernetes module).
- Enforce HTTPS at the ingress; set `server.forward-headers-strategy=framework`.
- Dependency vulnerability scan in CI: OWASP Dependency-Check, Snyk, GitHub Dependabot, or Trivy on the image.
- SAST: SonarQube / Semgrep / CodeQL for Spring rules.
- DAST: OWASP ZAP baseline scan on staging.
- Audit logs: log AuthN success/failure, AuthZ denial, admin actions with actor ID + traceId.

### 9. Rate Limiting

Spring does not ship rate limiting. Options:

- Edge: API gateway (Kong, NGINX, AWS API Gateway, Spring Cloud Gateway) - preferred.
- In-process: `bucket4j-spring-boot-starter` + Redis.

Per-endpoint limits, lower for write/auth endpoints. Return 429 with `Retry-After` header.

### 10. Tests for Security

```java
@WebMvcTest(OrderController.class)
@Import(SecurityConfig.class)
class OrderSecurityTest {
    @Autowired MockMvc mvc;

    @Test
    void anonymousIsRejected() throws Exception {
        mvc.perform(get("/api/v1/orders/{id}", UUID.randomUUID()))
            .andExpect(status().isUnauthorized());
    }

    @Test
    @WithMockUser(roles = "order.read")
    void readerCannotPlaceOrder() throws Exception {
        mvc.perform(post("/api/v1/orders").contentType(MediaType.APPLICATION_JSON).content("{}"))
            .andExpect(status().isForbidden());
    }

    @Test
    void hstsHeaderPresent() throws Exception {
        mvc.perform(get("/api/v1/health/public"))
            .andExpect(header().string("Strict-Transport-Security", containsString("max-age=31536000")));
    }
}
```

## Common Pitfalls

| Anti-pattern | Fix |
| --- | --- |
| `permitAll()` on `/**` "for now" | Deny-by-default; explicit `permitAll` per matcher |
| `cors.allowedOrigins("*")` with `allowCredentials=true` | Explicit origin list; never `*` with credentials |
| CSRF disabled globally on a session-cookie app | Enable CSRF for cookie auth; only disable on stateless API |
| Returning JPA entity bound from request body | Mass assignment / over-posting - DTO records |
| Storing secrets in `application.yml` | External secret store + `spring.config.import` |
| Logging the `Authorization` header during debugging | Add log scrubber + remove |
| `actuator/*` exposed publicly | Whitelist `health,info,prometheus`; secure rest |
| Skipping `aud` claim validation | Validate audience; otherwise tokens for other services accepted |
| Trusting `X-Forwarded-For` when not behind a known proxy | Set `forward-headers-strategy` only when behind a real proxy |
| Disabling SSL verification on outbound `RestClient` | Never do this; fix the trust store |

## Output Format

When applying this skill, deliver:

1. Authentication model per interface.
2. Authorization matrix (endpoint -> required role/scope/ownership).
3. `SecurityFilterChain` config + JWT converter.
4. CORS + CSRF + headers policy.
5. Secret-handling plan (where stored, rotated by whom).
6. Rate-limit plan + code/config.
7. Test matrix (anon, role boundaries, header presence).
8. OWASP API Top 10 review checklist with status per item.

## Authoritative References

- Spring Security reference: https://docs.spring.io/spring-security/reference/
- Spring Security 6 migration: https://docs.spring.io/spring-security/reference/migration-6/index.html
- OAuth2 Resource Server: https://docs.spring.io/spring-security/reference/servlet/oauth2/resource-server/index.html
- Method security: https://docs.spring.io/spring-security/reference/servlet/authorization/method-security.html
- OWASP API Security Top 10 (2023): https://owasp.org/API-Security/editions/2023/en/0x00-header/
- OWASP Cheat Sheets: https://cheatsheetseries.owasp.org/
- OWASP Secure Headers Project: https://owasp.org/www-project-secure-headers/
- OAuth 2.0 Security Best Current Practice (RFC 9700): https://www.rfc-editor.org/rfc/rfc9700.html
- JWT Best Current Practices (RFC 8725): https://www.rfc-editor.org/rfc/rfc8725.html
- CIS Benchmarks (OS / container): https://www.cisecurity.org/cis-benchmarks
