---
name: spring-security
description: Spring Boot security review — Spring Security config (SecurityFilterChain), OAuth2/OIDC client and resource-server, method-level @PreAuthorize, JWT validation, actuator endpoint lockdown, CSRF model for web vs API, and recent Spring CVE patterns (Spring4Shell, SpEL injection, authorization bypasses).
---

# Spring Boot Security

## When to use

This skill is the Spring-specific layer on top of `secure-coding` and `api-security`. Spring Security is powerful and exactly therefore foot-gun-rich: small letters in the config decide whether your app is safe or wide open.

Triggers on:

- A question like "review our Spring Security config", "OAuth2 client setup", "lock down actuator endpoints", "JWT validation on a Spring Resource Server", "@PreAuthorize review".
- Presence of `spring-boot-starter-security`, `spring-security-oauth2-client`, `SecurityFilterChain` beans, `@EnableWebSecurity`, `@PreAuthorize`/`@PostAuthorize` annotations, `application.yml` with `spring.security.*` or `management.*`.
- A PR that touches `.permitAll()`, `.disable()` on CSRF/CORS, custom `AuthenticationProvider`, `UserDetailsService`, or a JWT filter.
- Spring version bumps around security releases.
- A handoff from `security-review` or `api-security` where Spring is in the stack.

### When NOT (handoff)

- General Java secure-coding → `secure-coding`.
- API design and OWASP API Top 10 — large overlap, but that skill is framework-agnostic. Use `api-security` for conceptual questions (what is IDOR, how do you validate a schema), this skill for Spring-specific implementation.
- SAST with Semgrep `p/java-spring` or CodeQL → `sast-orchestrator`.
- Dep vulns (incl. Log4Shell-class vulns in transitive deps) → `cve-triage`.
- Infra around Spring (Kubernetes deploy, container image) → `container-hardening` + `k8s-security`.
- Secrets (application.properties with DB passwords) → `secrets-scanner`.

## Approach

Six phases. Phase 1 (SecurityFilterChain) is where most production bugs live.

### 1. SecurityFilterChain config

Spring Security 6+ uses the Lambda DSL. Each chain decides which auth mode goes with which path and what "open" means.

Common foot-guns:

- **`.permitAll()` on too broad a path.** `http.authorizeHttpRequests(auth -> auth.requestMatchers("/api/**").permitAll())` opens the entire API. Look for `.permitAll()` on wildcards and challenge each one.
- **Order of matchers.** The filter chain matches top-down. A `/api/**` permitAll above a `/api/admin/**` authenticated rule overrules the latter. Always go from specific to general.
- **`.anyRequest().permitAll()`** — as the last rule this is catch-all open. Almost always wrong. The last rule should be `.anyRequest().authenticated()`, with an exception for a purely public app.
- **Multiple `SecurityFilterChain` beans** with `@Order`. First match wins. A too-broad first chain can render later chains redundant.
- **`.csrf(csrf -> csrf.disable())`** without context. CSRF on by default for stateful web auth. Disabling is correct for stateless JWT APIs, wrong for form-based auth. If in doubt: leave it on.
- **CORS config.** `.cors(cors -> cors.configurationSource(source))` with a `CorsConfigurationSource` that returns wildcards is a standard misconception. `allowedOrigins("*")` together with `allowCredentials(true)` does not work (Spring rejects it), but it is a signal that the config flow has not been thought through.

Concrete reference config for a stateless JWT API:

```java
@Bean
SecurityFilterChain api(HttpSecurity http) throws Exception {
    http
        .securityMatcher("/api/**")
        .authorizeHttpRequests(auth -> auth
            .requestMatchers(HttpMethod.GET, "/api/health").permitAll()
            .requestMatchers("/api/admin/**").hasRole("ADMIN")
            .anyRequest().authenticated())
        .oauth2ResourceServer(rs -> rs.jwt(Customizer.withDefaults()))
        .csrf(csrf -> csrf.disable())  // correct for stateless API
        .sessionManagement(s -> s.sessionCreationPolicy(SessionCreationPolicy.STATELESS));
    return http.build();
}
```

### 2. Method-level authorization

Route-level auth is never enough. Methods with sensitive logic deserve `@PreAuthorize` or equivalent.

- **`@EnableMethodSecurity`** (Spring Security 6) replaces `@EnableGlobalMethodSecurity`. Without this annotation, `@PreAuthorize`/`@PostAuthorize` do not work.
- **`@PreAuthorize("hasRole('ADMIN')")`** — role-based.
- **`@PreAuthorize("hasAuthority('SCOPE_write:documents')")`** — for JWT scopes.
- **`@PreAuthorize("#id == authentication.name or hasRole('ADMIN')")`** — per-resource ownership, the fix for IDOR (see `api-security` API1 BOLA).
- **`@PostAuthorize`** — filter the return value after execution. Rarely needed, has performance impact.

Common miss: ownership check in the service method but not in the controller, or vice versa. One place is enough, but it must be unambiguous which one.

### 3. Actuator lockdown

Spring Boot Actuator exposes operational endpoints. The default config (older) was wide open. Since Boot 2.x the defaults are `/health` and `/info` public, the rest authenticated. Reviewer rule: confirm you have not fallen back to the older model.

- **`management.endpoints.web.exposure.include`** — what gets exposed. `"*"` is wrong in prod. Limit to what Ops actually needs: `health,info,prometheus,metrics`.
- **`management.endpoint.env.show-values=NEVER`** or `ALWAYS`/`WHEN_AUTHORIZED`. `/env` shows all env vars, including secrets when misconfigured.
- **`management.endpoint.heapdump.enabled=false`** in prod. Heap dump via HTTP is a memory-exfil primitive.
- **`management.server.port`** on a separate port that is not externally routable. Plus firewall/NetworkPolicy (see `k8s-security`).
- **Actuator security on the SecurityFilterChain**: a separate chain with `EndpointRequest.toAnyEndpoint()` matcher, role `ACTUATOR` or equivalent.

### 4. JWT and OAuth2

Spring has three OAuth2 roles: client (consumer), resource-server (you, validating tokens), authorization-server (you, issuing tokens). Each has its own foot-guns.

- **Resource-server (JWT validation)**:
  - **Issuer validation** required: `spring.security.oauth2.resourceserver.jwt.issuer-uri` or an explicit `JwtDecoder` with `NimbusJwtDecoder.withIssuerLocation(issuer)`.
  - **Audience-claim validation** must be built explicitly (not default). `OAuth2TokenValidatorFactories.create().andValidate(JwtIssuerValidator).andValidate(JwtAudienceValidator)`.
  - **Algorithm whitelist**: accept `RS256` / `ES256`, reject `HS256` unless explicitly intended. Algorithm confusion is a classic attack. See also `api-security` phase 2.
  - **Clock skew**: `.setClockSkew(Duration.ofMinutes(2))` is reasonable, not 1 hour.
- **Client (OAuth consumer)**:
  - **PKCE required** for public clients (mobile, SPA that Spring only serves).
  - **Redirect URI strictly** registered, no wildcards.
  - **Scopes minimal** when requesting.
- **Authorization-server**:
  - Spring Authorization Server is relatively young (stable since 2022). Use a vendor IdP (Keycloak, Auth0, Okta) unless you have a strong reason to self-host.

### 5. CVE patterns from recent years

The Spring ecosystem has a few infamous CVEs; each is a pattern to look for.

- **Spring4Shell (CVE-2022-22965)**. Spring Framework RCE via class-loader manipulation in data binding. Patched in 5.2.20, 5.3.18. Historical but still relevant as a reviewer reflex: Java apps using `ServletRequestDataBinder` without an allowlist are exposed. Spring Boot's default binder has been patched since the fix release.
- **CVE-2022-22963 Spring Cloud Function** — SpEL injection via the `spring.cloud.function.routing-expression` header. Lesson: SpEL evaluation on untrusted input is RCE. Search your code for `SpelExpressionParser().parseExpression(userInput)`.
- **CVE-2023-20860 / -20861 Spring Framework** — mass-binding and security bypass via `matchers` combined with `mvcMatchers`. Fixed in 5.3.26, 6.0.7. Reviewer rule: mixing `antMatchers` and `mvcMatchers` is a foot-gun — use one consistently and prefer `requestMatchers` (Spring Security 6).
- **CVE-2024-22257 Spring Security authorization bypass** — possible bypass when `AuthenticatedVoter` was configured without additional checks. `[verify against https://spring.io/security/cve-2024-22257]` for the exact patched versions in your context.
- **More recent CVEs** — `[verify against https://spring.io/security/]` — check the CVE feed on every version bump or review. No invented IDs in findings.

### 6. Misc and verification-loop

- **`@JsonIgnore` on sensitive entity fields** (password_hash, internal notes) to keep them out of JSON responses (mass-response, the mirror of mass-assignment).
- **`@JsonProperty(access = WRITE_ONLY)`** for input-only fields.
- **Use DTOs** instead of serializing entities directly. Prevents accidental field exposure when the DB schema changes.
- **Session fixation**: Spring Security prevents this by default (`SessionAuthenticationStrategy`). Do not turn it off without reason.
- **Password hashing**: `BCryptPasswordEncoder` default. Argon2 variant via `Argon2PasswordEncoder` if the library is included. Never `NoOpPasswordEncoder` outside tests.

Verification-loop: Layer 1 (SecurityFilterChain config coherent? Actuator endpoints explicitly locked down? JWT issuer + audience both validated?), Layer 2 (CVE IDs confirmed via spring.io/security, OAuth flow names correct, no invented Spring annotations in examples).

## Output

```
Spring Security review — <service/module>
Spring Boot: <x.y.z> | Spring Security: <x.y.z> | Version status: <current | N releases behind>

SecurityFilterChain:
  Chains present:         N
  permitAll() matchers:   <list + context>
  .anyRequest() last:     <authenticated | permitAll — FINDING>
  CSRF status:            <enabled | disabled with context>
  CORS config:            <scoped | wildcard — FINDING>

Method security:
  @EnableMethodSecurity:  <yes/no>
  @PreAuthorize coverage: <controllers with/without>
  Ownership checks:       <present on resource endpoints?>

Actuator:
  Exposure:               <list of endpoints>
  /env show-values:       <NEVER | WHEN_AUTHORIZED | ALWAYS — FINDING>
  /heapdump:              <disabled | exposed — FINDING>
  Separate port or filter:<yes/no>

OAuth2 / JWT:
  Role:                   <client | resource-server | both>
  Issuer validation:      <yes/no>
  Audience validation:    <yes/no>
  Algorithm whitelist:    <yes/no>

CVE check:
  Spring4Shell patched:   <yes>
  Recent security release:<within N days of upstream?>
  cve-triage handoff:     <N open>

Findings (severity-sorted, follow security-review format)
Verification-loop: ...
```

## References

- Spring Security Reference — [https://docs.spring.io/spring-security/reference/](https://docs.spring.io/spring-security/reference/). Canonical docs, Lambda DSL and config patterns.
- Spring Security CVE feed — [https://spring.io/security/](https://spring.io/security/). All Spring projects CVEs, canonical source for verification.
- Spring Boot Actuator — [https://docs.spring.io/spring-boot/reference/actuator/index.html](https://docs.spring.io/spring-boot/reference/actuator/index.html). Endpoint config and security implications.
- OWASP Java Security Cheat Sheet — [https://cheatsheetseries.owasp.org/cheatsheets/Java_Security_Cheat_Sheet.html](https://cheatsheetseries.owasp.org/cheatsheets/Java_Security_Cheat_Sheet.html).
- Spring Framework Reference (RequestMapping, Binding) — [https://docs.spring.io/spring-framework/reference/](https://docs.spring.io/spring-framework/reference/). For patterns that include Spring4Shell-style attacks.
- RFC 8725 (JWT BCP) — [https://datatracker.ietf.org/doc/html/rfc8725](https://datatracker.ietf.org/doc/html/rfc8725). JWT-specific gotchas.
- OAuth 2.0 Security BCP — [https://datatracker.ietf.org/doc/html/draft-ietf-oauth-security-topics](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-security-topics).
- NIST NVD — [https://nvd.nist.gov/](https://nvd.nist.gov/). For CVE verification on every cite.

## Categories

- appsec
