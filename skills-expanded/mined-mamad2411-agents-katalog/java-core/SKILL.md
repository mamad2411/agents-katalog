---
name: java-core
description: >
  MIND CTI Java coding standards and best practices for JDK 17. Covers naming, structure, error handling,
  collections, streams, concurrency, logging principles, testing, and documentation. This skill is
  language-level only — framework-specific patterns (Spring Boot, Quarkus, Jakarta EE) are in their
  respective skills. Use this skill whenever working on any Java file.
paths: "**/*.java"
---

# Java Core — MIND CTI Coding Standards (JDK 17)

> MIND CTI company-wide standard — language-level and library-level practices.
> Framework-specific patterns are in their own skills: `spring-boot`, `quarkus`, `jakarta-ee`.

## When This Applies

This skill applies to **every `.java` file** across all MIND CTI projects, regardless of framework. It covers Java language features, naming, structure, error handling, collections, concurrency, logging principles, and testing fundamentals. For DI, web, data access, and framework config, see the appropriate framework skill.

**Target:** Java 17 (LTS). JDK 17 features (records, sealed classes, text blocks, pattern matching for `instanceof`) are encouraged for new code. V10.00 legacy modules on Java 11 should follow these rules except where explicitly noted as JDK 17+.

## Core Principles

1. **Clarity over cleverness** — Code is read 10x more than it is written. Favor readability.
2. **Immutability by default** — Use `final` fields, records, and unmodifiable collections unless mutation is required.
3. **Fail fast** — Validate inputs at system boundaries. Throw early, catch late.
4. **Convention over configuration** — Follow MIND CTI conventions so developers can move between projects seamlessly.
5. **Progressive modernization** — New code uses modern Java features. Existing code is modernized opportunistically, not forcibly.

## Quick Reference — Top 15 Rules

1. **Constructor injection** — Prefer constructor injection for DI. See your framework skill for the specific mechanism (`@RequiredArgsConstructor` in Spring Boot, `@Inject` in Quarkus/Jakarta EE).
2. **Records for immutable DTOs** — New read-only value objects should be Java records.
3. **Immutability by default** — Use `final` fields, `List.of()`, `List.copyOf()`, `Collections.unmodifiable*()` unless mutation is needed.
4. **`var` when type is obvious** — `var list = new ArrayList<String>()` is fine. `var x = service.call()` is not.
5. **Unchecked exceptions** for business errors — extend `RuntimeException`, carry error codes.
6. **Fail fast** — Validate at system boundaries. `Objects.requireNonNull()` in constructors.
7. **`@Nullable`/`@NonNull`** at API boundaries for null-safety documentation.
8. **Streams** for transformation/filtering pipelines. Traditional loops for mutations, side effects, or simple iterations.
9. **`Optional`** — return from methods that may have no result. Never use as a field or method parameter.
10. **AssertJ for test assertions** — `assertThat(x).isEqualTo(y)`, not JUnit `assertEquals`.
11. **`@ExtendWith(MockitoExtension.class)`** — Not `MockitoAnnotations.initMocks()`.
12. **Test naming:** `methodName_scenario_expectedBehavior` — e.g., `getAccount_withInvalidId_throwsNotFoundException`.
13. **Logging** — Use parameterized messages, never string concatenation. See your framework skill for which logging library.
14. **`com.mind.*`** package prefix for all MIND CTI code.
15. **Adapter pattern** for DTO↔Entity mapping — hand-written `*Adapter` classes. Do not introduce MapStruct.

## Detailed Reference

- For class, method, variable, and package naming rules → [naming-conventions.md](docs/naming-conventions.md)
- For package organization, class design, and SOLID principles → [code-structure.md](docs/code-structure.md)
- For exception hierarchy, try-with-resources, and error patterns → [error-handling.md](docs/error-handling.md)
- For streams, Optional, collections, and JDK 17 features → [collections-and-streams.md](docs/collections-and-streams.md)
- For thread safety, CompletableFuture, and concurrent collections → [concurrency.md](docs/concurrency.md)
- For log levels, message formatting, and sensitive data → [logging.md](docs/logging.md)
- For JUnit 5, Mockito, AssertJ, and test organization → [testing.md](docs/testing.md)
- For Javadoc standards and inline comment rules → [documentation.md](docs/documentation.md)

## Project-Specific Notes — MIND CTI

- **Package prefix**: All code lives under `com.mind.*` (e.g., `com.mind.csr.api`, `com.mind.auth`, `com.mind.pos`)
- **Database**: Oracle is the sole production database. H2 for tests.
- **Parent BOMs**: `MindBill-BOM` (V10.00), `MindBill-GitBOM` (git/ projects) manage dependency versions centrally.
- **Dual codebase**: V10.00 (legacy J2EE, ~340 modules) coexists with modern microservices (git/). Rules apply to both; framework-specific adjustments are noted in each framework skill.
- **Adapter pattern**: MIND CTI uses hand-written `*Adapter` classes for DTO↔Entity mapping. This is the approved approach — do not introduce MapStruct.
