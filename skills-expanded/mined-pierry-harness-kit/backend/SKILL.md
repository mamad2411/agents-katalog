---
name: backend
description: Backend engineering conventions for team. Java/Kotlin servers. Project conventions in .claude/conventions/backend.md override these defaults.
user_invocable: false
---

Backend conventions, team default.

Project override: if `{repo}/.claude/conventions/backend.md` exists, overrides any rule here. See guides/conventions-override.md.

## Defaults

Illustrative defaults for JVM-leaning backend. Override per repo via `.claude/conventions/backend.md`.

Stack:
- Java or Kotlin (check pom.xml or build.gradle.kts)
- Spring Boot (current major) or Ktor for Kotlin services
- Build: Maven (mvn) or Gradle (gradlew)
- Deploy: JAR with embedded server
- Package prefix: match repo convention

Persistence:
- Custom JDBC AbstractRepository + SQL templates. Avoid JPA except where repo already uses it.
- Migrations via Flyway, naming `V{YYYYMMDD}__{description}.sql`.

Mapping:
- Orika 1.5.x. Avoid MapStruct unless repo already uses it.

Lombok:
- `@Data`, `@Builder`, `@RequiredArgsConstructor` OK.
- Avoid `@SneakyThrows`. Be explicit about checked exceptions.

Null handling:
- `Objects.equals()` for equality.
- `Boolean.TRUE.equals(...)` for nullable booleans.
- Guards and early returns. Avoid deep nesting.

Streams:
- Fluent: `.stream().filter(...).findAny().orElseThrow(...)`.
- Avoid stream-of-stream when guard would do.

Transactions:
- `@Transactional` on service methods, not repositories.

Tests:
- JUnit 4 + Mockito legacy; JUnit 5 + Mockito for newer.
- `@RunWith(MockitoJUnitRunner.class)` (JUnit 4) or `@ExtendWith(MockitoExtension.class)` (JUnit 5).
- Naming: `givenX_WhenY_ShouldZ` or `shouldDoSomethingWhenCondition`.
- Cover positive, negative, edge cases.
- `verify()` with `never()`, `times()`, arg matchers.

## Before writing code

Read at least 3 similar files in target repo to confirm:
- framework version
- build tool
- package layout
- test framework
- helpers in use (Lombok, Orika, custom)

Never assume. Stack varies per repo.

## Forbidden in PR

- new JPA usage in repos that use AbstractRepository
- MapStruct in repos using Orika
- Composition API in Vue 2 repos (web side)
- code without tests
- `@SuppressWarnings` to silence real issues
- placeholder TODO comments without ticket reference

## Mark gaps

If you cannot find pattern in repo, do not invent:

```java
// TBD - verify with tech lead: {what you searched, what is missing}
```

Read actual code first. TODO with context beats fabricated code.
