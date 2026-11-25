---
name: "java17-springboot3-best-practices"
description: "Java 17 LTS and Spring Boot 3.2.x coding guidelines for microservices: language-feature ceiling, jakarta namespace, constructor injection, records, sealed types — without Java 21-only or Spring Boot 4-only constructs."
version: 1
created: "2026-06-10T03:34:24+05:30"
updated: "2026-06-26"
---
## When to Use
Use when `tsa.technology.application.language` = Java AND `language_version` resolves to 17 (and/or `framework` = Spring Boot with `framework_version` in the 3.x line, e.g. 3.2.x). Apply when writing, reviewing, or fixing JVM code for such a target. **Version guard (read first):** resolve the exact language and framework versions from the TSA — `tsa.technology.application.{language_version, framework_version}` — and NEVER use a language or framework feature newer than that version, even if the runtime offers it. If the TSA targets a different Java/Spring Boot version, defer to the matching skill instead of this one.

## Procedure
1. **Pin the feature ceiling to the TSA version.** For Java 17 targets, restrict yourself to features available in Java 17. Do NOT emit Java 21+ constructs (see Anti-Patterns). Set `maven-compiler-plugin` `<release>17</release>` (or Gradle `sourceCompatibility = 17`) explicitly; never let it float to the ambient JDK.
2. **Use Java 17 records for immutable DTOs.** Records are available in 17 — add `@JsonProperty` on components when JSON field names must be stable. Records give you equals/hashCode/toString for free.
3. **Use sealed classes/interfaces** (available in 17) for closed type hierarchies, paired with a regular `switch` over an enum/`instanceof` chain — NOT switch *pattern matching* (that is Java 21).
4. **Use plain text blocks** (`"""`) for multi-line SQL/JSON (available since Java 15). Do NOT place raw XML entity sequences (`&amp;`, `&lt;`) immediately after the opening `"""` delimiter — build via concatenation or escape to avoid "illegal text block delimiter" errors.
5. **Constructor injection with `private final` fields** (or Lombok `@RequiredArgsConstructor`). Never field injection (`@Autowired` on fields).
6. **Use the `jakarta.*` namespace** (Spring Boot 3 baseline: Spring Framework 6.1, Jakarta EE 10) — never `javax.*` for servlet/persistence/validation imports.
7. **Spring Boot 3.2 specifics:** virtual threads are opt-in via `spring.threads.virtual.enabled=true` (supported in 3.2+); use only 3.x APIs — avoid any API introduced in Spring Boot 4. Use `@RestControllerAdvice` for global error handling and `@ConfigurationProperties` for externalized config.
8. **Validate the build runtime** matches Java 17 before compiling (see the `build-toolchain-alignmentv2` skill) — a newer ambient JDK with an old compiler plugin causes `TypeTag :: UNKNOWN`.

## Patterns
- Records for DTOs/value objects (Java 17)
- Sealed interfaces + enum/`instanceof` dispatch (NOT switch patterns)
- Plain text blocks for SQL/JSON (entities via concatenation)
- Constructor injection with final fields / `@RequiredArgsConstructor`
- `jakarta.*` imports; Spring Framework 6.1 / Jakarta EE 10 baseline
- Explicit `<release>17</release>` / `sourceCompatibility = 17`
- `@RestControllerAdvice` global exception mapping; `@ConfigurationProperties` config binding

## Anti-Patterns
- **Switch pattern matching / `case Type t when ...` guards** — Java 21, NOT 17
- **Record patterns / deconstruction in `switch` or `instanceof`** — Java 21, NOT 17
- **Unnamed variables/patterns (`_`)** — Java 21+, NOT 17
- **Spring Boot 4-only APIs** — target is 3.x
- `javax.*` imports (legacy; Spring Boot 3 uses `jakarta.*`)
- Field injection; hardcoded URLs/credentials/timeouts; business logic in controllers
- Raw `&amp;`/`&lt;` immediately after a `"""` text-block delimiter
- Letting the compiler `release`/source version float to the ambient JDK

## Tool Selection
- Build: Maven (`maven-compiler-plugin` with `<release>17</release>`) or Gradle toolchain pinned to 17
- Boilerplate: Lombok per `tsa.technology.application.boilerplate_tool`
- Web: `spring-boot-starter-web`; Validation: `spring-boot-starter-validation` (`jakarta.validation`)
- Pair with `build-toolchain-alignmentv2` (runtime) and `spring-boot-3-test-stabilizationv2` (tests)

## Validation Rules
- Reject any source using Java 21+ syntax when `language_version`=17
- `maven-compiler-plugin`/Gradle source-target must equal the TSA `language_version`
- All servlet/persistence/validation imports use `jakarta.*`, never `javax.*`
- No Spring Boot 4-only dependency or API references when `framework_version` is 3.x
- Build must compile with **zero** errors on a JDK whose major == `language_version`

## RAG Sources
- spring-boot-docs
- openapi-3-spec
- tsa.technology.application (resolve language_version / framework_version)
- the project best-practices artifact (e.g. best-practices.md) for service-specific Spring Boot 3.x / Java 17 conventions; broader (non-language) topics live in the dedicated skills (rest-api-design, jpa, oauth2, testing, …)
