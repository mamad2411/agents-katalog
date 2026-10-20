---
name: "compilation-error-triage"
description: "Systematic error classification and resolution order for Java/Spring Boot compilation, test, and runtime errors in microservices migration projects. Versions, datastore, migration tool, and logging backend are resolved from the TSA (e.g. Java 17 / Spring Boot 3.2.x / Maven / DB2 / Flyway / Logback)."
version: 2
created: "2026-06-09T03:34:24+05:30"
updated: "2026-06-26"
---
## When to Use
Use when encountering build failures, compilation errors, test failures, or runtime errors during microservices development or migration. Apply when facing multiple error types simultaneously and need a prioritized resolution order. **Resolve the target Java/Spring Boot versions, datastore, migration tool, and logging backend from the TSA** (`tsa.technology.application.{language_version, framework_version, build_tool}`, `tsa.technology.database.{vendor, migration_tool}`, `tsa.technology.observability.logging`) — never assume a version. Essential for Maven/JPA/framework integration issues on the TSA-pinned stack (e.g. Spring Boot 3.2.x / Java 17).

## Procedure
1. STEP 1: Classify All Errors - Run the build (`mvn clean compile`) and collect all output. Categorize each error: COMPILE (syntax, missing class, unresolved dependency), TEST (test compilation/execution/assertion), RUNTIME (startup, bean creation, configuration). Document error count per category. Prioritize: COMPILE → TEST → RUNTIME (fix in this order).
2. STEP 2: Resolve Dependency Errors First - Verify the parent POM inherits `spring-boot-starter-parent` at the TSA-resolved version (e.g. 3.2.x — never bump to a version the TSA did not specify). Verify required starters are declared (`spring-boot-starter-web`, `-data-jpa`, `-security`, `-validation`, `-actuator`, plus the DB driver from `tsa.technology.database.vendor`, e.g. `db2jcc`). Run `mvn dependency:tree` for conflicts; resolve via `dependencyManagement`. Exclude `junit-vintage-engine`. Only adjust the logging backend if the TSA logging stack requires it (for SLF4J + Logback, keep Spring Boot's default Logback — do NOT swap in Log4j2). Re-run `mvn clean compile`.
3. STEP 3: Fix Schema Mapping Errors - Ensure entity `@Table`/`@Column(name=...)` match the actual DB schema exactly, honoring the target vendor's identifier casing (`tsa.technology.database.vendor`; for DB2 preserve the legacy `OCP_*` table/column names). Add missing `@Id`/`@GeneratedValue`; map relationships with `FetchType.LAZY`. Ensure migrations exist under `src/main/resources/db/migration/` using the TSA migration tool (Flyway `V<n>__*.sql`). Validate entities compile (`spring.jpa.hibernate.ddl-auto=validate`).
4. STEP 4: Resolve Import and Package Errors - Fix missing/unused imports. Use the `jakarta.*` namespace (Spring Boot 3 baseline) — never `javax.*` for servlet/persistence/validation. Verify reverse-DNS lowercase packages under the TSA root namespace (e.g. `com.omantel.resetpassword.service`). Keep classes in the correct layer packages (controllers in `.controller`, services in `.service`, etc.); no duplicate class names. Recompile after each fix batch.
5. STEP 5: Fix Type Errors and Annotations - For records used as DTOs add `@JsonProperty` where stable JSON names are required. Use constructor injection with final fields (`@RequiredArgsConstructor`; no field `@Autowired`). `@RestController`/`@Service`/`@Repository extends JpaRepository`. Fix generic mismatches. `@Transactional` on service methods; `@Valid` on controller DTOs. MapStruct mappers use `@Mapper(componentModel="spring")`. Stay within the TSA `language_version` (for Java 17: no switch pattern matching / record patterns / unnamed variables).
6. STEP 6: Resolve Test Compilation Errors - Use JUnit 5 (`org.junit.jupiter.api`, NOT `org.junit`). Use `@ExtendWith(MockitoExtension.class)` for unit tests (not `@RunWith`). For the test double, match the resolved Spring Boot version: on **Spring Boot 3.2.x use `@MockBean`** (the `@MockitoBean` replacement only exists in Spring Boot 3.4+/4.x — do NOT use it on 3.2). Use AssertJ (`assertThat`). Add missing test deps (`spring-boot-starter-test` brings JUnit Jupiter, Mockito, AssertJ). Ensure `application-test.yml` exists.
7. STEP 7: Fix Test Execution Failures - Run `mvn clean test`. For 'No qualifying bean' in slice tests add `@MockBean` for external collaborators. For 'Unable to find @SpringBootConfiguration' ensure the test sits in/under the `@SpringBootApplication` package. For Testcontainers failures verify Docker is running, use the container image matching `tsa.technology.database.vendor` (e.g. Db2, or H2 for fast unit slices), and register via `@DynamicPropertySource`. Use BDD mocking (`given(...).willReturn(...)`); assert `assertThat(actual).isEqualTo(expected)`.
8. STEP 8: Document and Track - Create an error log (type, message, root cause, resolution). Track resolution order/time per category. Document recurring patterns (missing dependency X → error Y). Record known issues/fixes for the next iteration.

## Pitfalls
- DO NOT fix errors in random order — dependencies first, then compile, then test, then runtime.
- DO NOT assume all errors are code-related — many are pom.xml dependency/config issues; use `mvn dependency:tree`.
- DO NOT bump Spring Boot / Java above the TSA-resolved version to satisfy a newer ambient runtime — align the toolchain instead (see `build-toolchain-alignmentv2`).
- DO NOT skip parent POM inheritance — extend `spring-boot-starter-parent` at the TSA version.
- DO NOT use `javax.*` on Spring Boot 3 — use `jakarta.*` for servlet/persistence/validation.
- DO NOT swap the logging backend the TSA names — for SLF4J + Logback keep Logback; do not introduce Log4j2 (or vice-versa) unless the TSA specifies it.
- DO NOT use the wrong migration tool — use the TSA tool (e.g. Flyway), and never edit an applied migration.
- DO NOT mismatch DB identifier casing/dialect — match the target vendor (`tsa.technology.database.vendor`) and preserve legacy schema names.
- DO NOT fix test failures before compilation errors — tests cannot run if code does not compile.
- DO NOT use `@SpringBootTest` for unit tests — use `@ExtendWith(MockitoExtension.class)` to avoid slow context loads.
- DO NOT use JUnit 4 — JUnit 5 (Jupiter); exclude `junit-vintage-engine`.
- DO NOT use `@MockitoBean` on Spring Boot 3.2.x — it is 3.4+/4.x; use `@MockBean`.
- DO NOT use a Java feature newer than the TSA `language_version` (for Java 17: no switch pattern matching, record patterns, or unnamed variables — those are Java 21).
- DO NOT ignore schema mapping errors — entities must match the DB schema exactly (names, types).
- DO NOT assume error messages are literal — 'Cannot find symbol' often means a missing dependency, not missing code; fix root causes, not symptoms.

## Verification
1. `mvn clean compile` succeeds with zero errors on a JDK whose major == `tsa.technology.application.language_version` (e.g. 17).
2. `mvn dependency:tree` shows no conflicts; required starters + the TSA DB driver present.
3. `mvn clean test` passes with no mocking/bean-creation failures.
4. JaCoCo coverage meets `tsa.testing.unit_tests.coverage_target` (e.g. ≥ 80% line) — `mvn jacoco:report`.
5. Application starts via `mvn spring-boot:run` with no bean/configuration errors and no startup WARN/ERROR.
6. DB schema matches JPA entities (validate via `ddl-auto=validate` or the TSA migration tool, e.g. `flyway:validate`).
7. All entities have `@Id`, correct `@Table`/`@Column` names; `jakarta.*` imports only; no `javax.*`.
8. No deprecated APIs/warnings; no source feature exceeding the TSA `language_version`.
9. `mvn checkstyle:check` passes (if configured).

## RAG Sources
- tsa.technology.application / tsa.technology.database / tsa.technology.observability / tsa.testing
- spring-boot-docs
- maven-docs
- pair with java17-springboot3-best-practicesv2, build-toolchain-alignmentv2, spring-boot-3-test-stabilizationv2
