---
name: "adr-microservices-blueprint"
description: "Architecture Decision Record blueprint for microservices modernization. Resolves the target stack, cloud, datastore, migration tool, logging, and test conventions dynamically from the TSA (e.g. Java 17 / Spring Boot 3.2.x / Maven / DB2 / Flyway / Redis / OAuth2-JWT). Optional patterns (multi-tenancy, BFF, messaging) apply ONLY where the TSA declares them."
version: 3
created: "2026-06-09T03:34:24+05:30"
updated: "2026-06-26"
---
## When to Use
Use when creating or documenting architecture decisions for microservices modernization projects migrating a legacy application to a cloud-native service. Apply when setting up a new service, defining API standards, implementing observability, or establishing distributed-system patterns. **Resolve every concrete technology, version, cloud, and tool from the TSA — never hardcode a stack.** This skill is the blueprint; the TSA is the source of truth.

## Deliverable: the ADR document
The primary output is an **Architecture Decision Record (ADR) document** (e.g. `blueprint-adr.md`). Write one ADR per significant decision using the structure: **Context · Decision · Rationale · Consequences (Positive / Negative / Mitigation) · Alternatives Considered** (optionally a short Implementation snippet). Cover the decision areas a legacy→cloud-native migration needs — derive the actual set from the TSA + epic/requirement inputs; for a WEF→Spring Boot migration that typically means: (1) framework migration, (2) endpoint consolidation via the Strategy pattern (e.g. 11 flows → one `/api/v1/...` endpoint keyed on the request context), (3) caching replacement (legacy cache → `tsa.technology.caching.provider`, e.g. Dynacache→Redis), (4) authentication (legacy session → `tsa.technology.security`, e.g. OAuth2/JWT with Cognito), (5) preservation of legacy request/response contracts for functional parity, (6) external-integration resilience (e.g. ESB clients with circuit breaker/retry), (7) database strategy (`tsa.technology.database` access + migration tool, preserve the legacy schema), (8) OTP/token handling, (9) notification dispatch, (10) audit logging, (11) feature-flag management, (12) exception/error-code mapping (preserve legacy codes → HTTP status via `@ControllerAdvice`), (13) Lombok boilerplate reduction, (14) DTO↔Entity mapping (MapStruct), (15) deployment/rollback. **The TSA supersedes any stale example ADR:** if an existing ADR conflicts with the current TSA (e.g. an ADR proposing JMS/ActiveMQ for notifications while `tsa.technology.messaging` disables brokers and mandates a synchronous REST notification client), follow the TSA and update the decision.

## Procedure
1. **Technology Stack Selection (resolve from `tsa.technology`)**: Read `tsa.technology.application.{language, language_version, framework, framework_version, build_tool, boilerplate_tool}`, `tsa.technology.database.{vendor, access, migration_tool}`, `tsa.technology.caching.provider`, `tsa.technology.security.{type, provider}`, and `tsa.technology.observability`. Pin to exactly those versions; never use a language/framework feature newer than the resolved version (defer language rules to the matching `*-best-practices` skill). *Example resolution for the reset-password TSA:* Java 17 LTS, Spring Boot 3.2.x, Maven, Lombok, DB2 via JPA/Hibernate, Flyway, Redis, OAuth2/JWT with AWS Cognito, Micrometer + Prometheus + Actuator.
2. **Project Structure (resolve from `tsa.project`)**: Implement the `tsa.project.structure` (e.g. layered) with the layers/folders from `tsa.project.phase_folder_map` + `subfolder_conventions`. For a layered service: Controller (routing, DTO validation) → Service (business logic, transactions, `service/impl`) → Repository (Spring Data JPA). Separate packages for config, dto, mapper, model, exception, repository, client, util, security. All files under `tsa.project.root_path`, single root namespace (`tsa.project.package`).
3. **API Design Standards (resolve from `tsa.technology.api`)**: Apply the TSA `style`, `versioning` (e.g. URI `/api/v1/...`), `content_type`, and `contract` (e.g. OpenAPI 3.0 via Springdoc). Standardize a response envelope (status, statusCode, message, data, errors[]) and a correlation header. Use HTTP verbs by resource semantics; keep controllers thin.
4. **Multi-Tenant Architecture (ONLY if the TSA declares multi-tenancy)**: If `tsa` defines tenancy (e.g. a tenant discriminator / per-tenant routing), implement application-level routing (e.g. `AbstractRoutingDataSource`) and include the tenant column on tenant-scoped tables, cached per the TSA cache provider. **If the TSA describes a single-tenant service (as in reset-password), do NOT add tenant columns, tenant headers, or routing datasources.**
5. **BFF Pattern (ONLY if the TSA declares a BFF/aggregation tier)**: If the service `type` is a BFF or the TSA defines downstream aggregation, create the BFF layer with declarative REST clients + Resilience4j (circuit breaker, retry, timeout, bulkhead). **For a DOMAIN service with no aggregation tier, do NOT introduce a BFF, Feign aggregation, or upward dependencies.**
6. **Observability & Tracing (resolve from `tsa.technology.observability`)**: Implement the TSA logging stack (e.g. SLF4J + Logback with structured JSON + correlation/trace IDs in MDC), metrics (e.g. Micrometer with the registry named in the TSA, e.g. Prometheus), and health via Actuator (`/actuator/health`, readiness/liveness). Add the custom metrics listed in `tsa.technology.observability` where present. Use the logging framework the TSA names — do not substitute another.
7. **Caching Strategy (resolve from `tsa.technology.caching`)**: Use the TSA cache provider (e.g. Redis via Spring Cache abstraction) for the declared `use_cases` with the declared `eviction_policy`. Annotate with `@Cacheable`/`@CacheEvict`; cache DTOs (never Hibernate proxies/entities). Apply manual invalidation on the events the TSA calls out (e.g. invalidate user profile cache on password reset).
8. **Testing Requirements (resolve from `tsa.testing`)**: Meet `tsa.testing.unit_tests.coverage_target` (e.g. 80% line) enforced by JaCoCo. Use the TSA frameworks: JUnit 5 (Jupiter) + Mockito with `@ExtendWith(MockitoExtension.class)` for unit tests, `@WebMvcTest`/`@DataJpaTest` for slices, Spring Boot Test + Testcontainers for integration. On Spring Boot 3.2.x use `@MockBean` (the `@MockitoBean` replacement is Spring Boot 3.4+/4.x — do not use it on 3.2). No test skipping in CI.
9. **Inter-Service / Outbound Communication**: Use the non-reactive stack (Spring MVC) unless the TSA says otherwise; enable virtual threads only when the resolved Spring Boot version supports them (3.2+ via `spring.threads.virtual.enabled`). Use the framework's idiomatic HTTP client (`RestClient`/`WebClient`/`RestTemplate`) for outbound REST integrations (e.g. the notification client in `tsa.technology.messaging`); use a declarative client (Feign) only where the TSA standardizes on it. Use MapStruct for compile-time DTO↔Entity mapping.
10. **Database & Migrations (resolve from `tsa.technology.database`)**: Use the TSA `vendor` dialect and `migration_tool`. For DB2 + Flyway: write Db2-dialect DDL under `src/main/resources/db/migration/` as `V<n>__<desc>.sql`; never edit an applied migration. Preserve the legacy schema (e.g. `OCP_*` tables) per `tsa.migration`. Defer engine specifics to the matching DB skill (db2/oracle/postgresql/mongodb).
11. **Security & Configuration (resolve from `tsa.technology.security` + `compliance_and_security`)**: Implement the TSA auth (e.g. OAuth2 resource server validating Cognito-issued JWTs, stateless, `@PreAuthorize` RBAC with the TSA roles). Store secrets in the vault the TSA names (e.g. AWS Secrets Manager). Constructor injection with final fields; safe error messages (never expose stack traces); propagate correlation IDs; redact PII from logs.
12. **CI/CD Quality Gates**: Fail the build on: Checkstyle violations, test failures, JaCoCo coverage below `tsa.testing` target, and dependency-scan findings above the agreed CVSS threshold (e.g. OWASP Dependency Check). No test skipping.
13. **Naming Conventions**: packages (lowercase reverse-DNS from `tsa.project.package`), Classes/Records (PascalCase), methods/variables (camelCase), constants (UPPER_SNAKE_CASE), REST paths (kebab-case + versioning, e.g. `/api/v1/password-reset`).

## Pitfalls
- Do NOT hardcode a stack/version/cloud — resolve them from the TSA; never exceed the resolved language/framework version.
- Do NOT put business logic in controllers — controllers only route and validate DTOs.
- Avoid field injection — use constructor injection with final fields.
- Never hardcode secrets/credentials — use the vault named in `tsa.technology.security` / `deployment` (e.g. AWS Secrets Manager).
- Do NOT expose stack traces in API responses — use safe messages with a correlation/trace id.
- Use the logging framework the TSA names — for `tsa.technology.observability.logging = SLF4J + Logback`, use Logback (NOT Log4j2); do not add or exclude logging backends the TSA did not specify.
- Use the migration tool the TSA names — for `tsa.technology.database.migration_tool = Flyway`, use Flyway (NOT Liquibase); never edit an applied migration.
- Do NOT add multi-tenant columns/headers/routing unless the TSA declares tenancy.
- Do NOT add a BFF tier, Feign aggregation, or upward dependencies unless the TSA declares a BFF.
- Match the test-double API to the resolved Spring Boot version — `@MockBean` on Spring Boot 3.2.x (NOT `@MockitoBean`); JUnit 5 only (exclude junit-vintage-engine).
- Never load Spring context in unit tests — use `@ExtendWith(MockitoExtension.class)`; use `@WebMvcTest`/`@DataJpaTest` for slices.
- Do NOT skip the parent POM — inherit from `spring-boot-starter-parent` at the resolved Spring Boot version.
- Never use `@Data` on `@Entity` classes — use `@Getter`/`@Setter` (+ `@EqualsAndHashCode` on the business/`@Id` key); apply Lombok per `tsa.technology.boilerplate_tool` everywhere else.
- Avoid FetchType.EAGER — use LAZY with explicit fetch joins; never expose JPA entities in REST responses (DTOs only).
- Never skip `@Transactional(readOnly = true)` on read service methods.
- Use the HTTP client the TSA implies (`RestClient`/`WebClient`/`RestTemplate` for the notification client) — do not force Feign where the TSA does not standardize on it.
- Do NOT cache JPA entities/Hibernate proxies — cache DTOs; pair `@Cacheable` with a key + `unless`, and `@CacheEvict` on writes.
- Avoid catching `Exception` broadly; do not return null from public APIs (use Optional/empty collections).
- Never use `RELEASE`/dynamic Maven versions — pin via dependencyManagement.
- Never commit `target/`, `.idea/`, `.vscode/`; do not exclude `*.md`; no unused imports; files end with a newline.
- Never leave commented-out functional code, TODO/FIXME/STUB (zero-TODO policy).

## Validation Rules
- Resolved language/framework/build-tool/DB/migration-tool/logging/cache/security match `tsa.technology.*`; no construct exceeds the resolved version.
- Project structure matches `tsa.project.structure` + `phase_folder_map`; all files under `root_path`; single root namespace.
- API versioning/contract match `tsa.technology.api`; standardized error envelope + correlation id.
- Logging uses the TSA-named framework (Logback for reset-password); migrations use the TSA-named tool (Flyway).
- JaCoCo coverage ≥ `tsa.testing` target; JUnit 5 + correct test-double API for the resolved Spring Boot version; no skipped tests.
- Multi-tenant / BFF / messaging present only if declared in the TSA.
- Secrets from the TSA vault; constructor injection; no entities exposed; LAZY relationships; readOnly read transactions.

## RAG Sources
- tsa.technology / tsa.project / tsa.testing / tsa.deployment / tsa.compliance_and_security / tsa.migration / tsa.execution_chain
- the project ADR artifact (e.g. blueprint-adr.md) for the ADR structure + decision set, and the epic/requirement inputs for the decisions to record — TSA wins on any conflict
- spring-boot-docs
- openapi-3-spec
- pair with java17-springboot3-best-practicesv2, build-toolchain-alignmentv2, and the matching db/security/messaging skills
