---
name: "bff-service-coreframework-guidelines"
description: "BFF (Backend-for-Frontend) service implementation guidelines based on orbt-coreframework-lib-src modules. Defines what BFF MUST and MUST NEVER implement given cross-cutting concerns handled by core-framework-common, core-framework-web, and core-framework-data"
version: 1
created: "2026-06-08"
updated: "2026-06-08"
---
## When to Use
Use when developing BFF services that orchestrate domain service calls, aggregate responses, and handle UI-specific transformation. Apply when implementing Feign clients, caching, multi-tenant context propagation, or security filters in BFF layer. Essential for ensuring BFF services properly leverage CoreFramework modules without duplicating cross-cutting concerns.

## Procedure
1. **Module Dependencies**: MUST include core-framework-web dependency (transitively includes core-framework-common). MUST include core-framework-data if using @Cacheable. ALWAYS exclude logback-classic and junit-vintage-engine. NEVER add core-framework-data as direct dependency in BFF (it's provided by core-framework-web)
2. **Feign Client Header Propagation**: Define Feign clients with ONLY business-relevant parameters (path variables, request bodies, query params). NEVER add Authorization, X-User-ID, X-Tenant-Ids, X-Correlation-ID, X-Trace-ID, X-Tenant-DB, X-USER-NAME as @RequestHeader parameters (DomainFeignInterceptor auto-injects). Configure Feign URLs via environment variables. Configure connectTimeout and readTimeout per client in application.yml
3. **Class-Based Fallback Pattern**: Define class-based fallback (implements <FeignClient>) for EVERY Feign client, annotated with @Component. NEVER use FallbackFactory pattern. Fallback method MUST have same return type plus additional Throwable parameter. MUST log WARN message in fallback indicating failure
4. **Multi-Tenant Context - Parallel Calls**: Use DomainRequestContext.setTenantId(tenantId) before each parallel Feign call in fan-out scenarios. MUST call DomainRequestContext.clear() in finally block. Use parallelStream() with per-thread context setup. NEVER share single DomainRequestContext across threads
5. **Security - Tenant Validation**: Use TenantContextHolder.getEffectiveTenantIds() to retrieve authorized tenants (populated by TenantSecurityFilter). Use TenantContextHolder.getUserId() for authenticated user. NEVER manually extract X-Tenant-Ids from request. NEVER implement custom JWT parsing or tenant authorization (TenantSecurityFilter handles). TenantSecurityFilter computes effectiveTenantIds = requested ∩ authorized
6. **Caching - L2 Redis**: Classify caches: L1+L2 (reference/static data) or L2-only (transient/per-request data). Use @Cacheable with composite SpEL key, unless condition. Add @CacheEvict on ALL write operations. Register cache names in application.yml under cache.l2.cache-names. Use @CacheTtl for method-level TTL overrides. NEVER cache JPA entities (DTOs only)
7. **Logging & MDC**: Use SLF4J logger (private static final or @Slf4j). Use parameterized logging. NEVER manually set MDC fields (correlationId, traceId, tenantId, userId, requestUri, httpMethod, clientIp) - MdcFilter auto-populates. Use LogMaskingUtil.maskEmail() for PII. Pass exception object as last parameter to log.error()
8. **Resilience & Fault Tolerance**: Annotate Feign call wrapper methods with @CircuitBreaker(name=..., fallbackMethod=...), @Retry(name=...), @TimeLimiter(name=...). Configure resilience4j instances per Feign client in application.yml. NEVER implement custom retry/circuit breaker/timeout logic. Fallback MUST return safe default (never throw)
9. **User Identity Resolution**: Use TenantContextHolder.getUserId() to access current user ID. Call orbt-user-api-src ONLY for explicit business use cases (e.g., displaying user profile). NEVER call orbt-user-api-src for header injection (DomainFeignInterceptor handles). NEVER implement custom UserProfileCacheService or TenantDbMappingCacheService (CoreFramework provides)
10. **Token Management**: Use TokenCacheHelper.blacklistAccessToken(accessToken, sessionId, ttlSeconds) on logout. Use TokenCacheHelper.isTokenBlacklisted(accessToken) for validation. NEVER implement custom token blacklisting. NEVER store raw JWT tokens (use SHA-256 hashes). Log only JWT jti and expiresAt (never full token)
11. **Architecture & Code Structure**: Follow Controller → Service → FeignClient layered architecture. Keep controllers thin (routing, DTO validation only). Use @RestControllerAdvice for global exception handling with standardized response format. Use @Valid on all request DTOs. Version APIs as /api/v1/. Use noun-based URIs. Use constructor injection. Enable virtual threads (spring.threads.virtual.enabled: true)
12. **Testing Standards**: Use @ExtendWith(MockitoExtension.class) for unit tests. Use @WebMvcTest for controller slice tests. Use @MockitoBean (Spring Boot 4.x). Use AssertJ assertions (assertThat). Use BDD-style mocking (given/then). Name tests: methodName_scenario_expectedBehavior with @DisplayName. Configure JaCoCo exclusions for DTOs, models, constants. Target: 100% service coverage, 90% controller coverage
13. **Configuration Requirements**: Set spring.threads.virtual.enabled: true. Configure orbt.user.profile.cache.ttl-seconds: 900. Configure management.tracing.sampling.probability: 1.0. Configure feign.client.<service>.url for all domain services. Configure resilience4j instances in application.yml. Register all cache names in cache.l1/l2 sections

## Pitfalls
- NEVER add auto-injected headers (Authorization, X-User-ID, X-Tenant-Ids, X-Correlation-ID, X-Trace-ID) to Feign method signatures - DomainFeignInterceptor handles
- Do NOT implement custom JWT parsing or tenant authorization logic - TenantSecurityFilter handles
- Never re-extract tenant IDs from HTTP headers in controllers/services - use TenantContextHolder
- Do NOT implement custom Redis client or in-memory cache - use CoreFramework CacheService
- Never cache JPA entities - ALWAYS cache DTOs only
- Do NOT use @Cacheable without composite SpEL key and unless condition
- Never skip @CacheEvict on write/update/delete operations
- Do NOT manually set MDC fields already managed by MdcFilter (correlationId, traceId, tenantId, userId)
- Never use System.out.println, e.printStackTrace(), or Logback - use SLF4J + Log4j2
- Do NOT log PII, passwords, or full JWT tokens - use LogMaskingUtil
- Never implement custom retry, circuit breaker, or timeout logic - use Resilience4j annotations
- Do NOT call orbt-user-api-src for header injection - interceptor handles automatically
- Never implement token blacklisting without TokenCacheHelper
- Do NOT access database directly from BFF - BFF communicates via Feign clients ONLY
- Never implement database connection, JPA repositories, or DataSource in BFF
- Do NOT use @SpringBootTest for unit tests - use @ExtendWith(MockitoExtension.class)
- Never use deprecated @MockBean - use @MockitoBean (Spring Boot 4.x)
- Do NOT use FallbackFactory - use class-based fallback implementing Feign interface
- Never omit DomainRequestContext.clear() in finally block - causes ThreadLocal leaks
- Do NOT put business logic in controllers - delegate to service layer
- Never expose JPA entities in REST responses - use DTOs
- Do NOT use field injection - use constructor injection with final fields
- Never configure custom Redis connection factory - core-framework-data manages
- Do NOT expose all actuator endpoints without authentication
- Never use RestTemplate - ALWAYS use FeignClient

## Verification
1. Verify core-framework-web dependency is included in pom.xml
2. Check Feign client interfaces have NO header parameters (Authorization, X-User-ID, X-Tenant-Ids, etc.)
3. Confirm each Feign client has class-based fallback implementing the interface with @Component
4. Validate parallelStream() fan-out uses DomainRequestContext.setTenantId() per-thread with clear() in finally
5. Verify TenantContextHolder.getEffectiveTenantIds() is used instead of manual header extraction
6. Check @Cacheable annotations include composite key, unless condition, and corresponding @CacheEvict
7. Confirm all cache names are registered in application.yml under cache.l2.cache-names
8. Validate logs use SLF4J parameterized logging with NO manual MDC.put() for auto-populated fields
9. Check Resilience4j annotations (@CircuitBreaker, @Retry, @TimeLimiter) on Feign wrapper methods
10. Verify application.yml contains spring.threads.virtual.enabled: true
11. Confirm no @SpringBootTest in unit tests - only @ExtendWith(MockitoExtension.class)
12. Check all tests use @MockitoBean (not deprecated @MockBean), AssertJ, and BDD-style mocking
13. Validate controllers are thin with only routing/validation, business logic in service layer
14. Verify @RestControllerAdvice implements standardized error response format
15. Confirm NO database access (DataSource, repositories) in BFF codebase
16. Check JaCoCo configuration excludes DTOs, models, constants, exceptions