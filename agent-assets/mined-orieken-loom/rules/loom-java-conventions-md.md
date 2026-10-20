# Java Conventions

**No internal Saturday-Java reference repo exists yet** (unlike Python and C#, which are grounded
against their own `saturday-monorepo-*` repos). Everything below is a well-established industry-standard
pick, chosen for consistency with the rest of the Saturday family where a natural equivalent exists —
treat this file as more provisional than the Python/C# ones until an actual Saturday-Java port confirms
or overrides these choices.

## Project Tooling
- **Build tool**: Gradle (Kotlin DSL) is the modern-default recommendation — better incremental build
  performance and dependency management ergonomics than Maven. Maven remains a reasonable, more
  traditional alternative; pick based on team familiarity rather than treating this as a hard rule the
  way the testing-tooling picks below are.
- **Java version**: 17+ (LTS) — enables records, sealed classes, and pattern matching, all already
  referenced in this framework's own Java Quick Reference (`CLAUDE.md`).

## Testing & QA Tooling
- **Unit testing framework**: JUnit 5 + Mockito — already the established default in this framework's
  own Java Quick Reference (`@Nested` for grouping, `@Mock` for mocking).
- **BDD**: Cucumber-JVM — for consistency with the rest of the Saturday family's per-language BDD choice
  (Cucumber.js for TypeScript, Reqnroll for C#, pytest-bdd for Python), this is the natural pick if
  Java ever gets its own Saturday port, not a confirmed decision yet.
- **Browser automation**: Playwright (Java) — official Microsoft-maintained binding
  (`com.microsoft.playwright:playwright`).
- **Fake/synthetic data (faker-equivalent)**: [DataFaker](https://www.datafaker.net/)
  (`net.datafaker:datafaker`) — the actively maintained fork/successor of the now-unmaintained
  `javafaker` (`com.github.javafaker:javafaker`). A lot of existing tutorials still reference the old,
  dead `javafaker` — don't use it for new code.
- **Factories / fixtures (fishery-equivalent)**: [Instancio](https://www.instancio.org/) — modern,
  fluent, actively maintained Java object-generation library with good Java 17+ support.
  [EasyRandom](https://github.com/j-easy/easy-random) (formerly `random-beans`) and the older `Podam`
  are still-used alternatives if a team is already invested in one of them, but Instancio is the
  current recommendation for new code.
- **Mutation testing** (ADR-008 clause 2): PIT (`pitest`) — a candidate, **not yet verified** against a
  real project. Verify before relying on its score: a mutant that did not compile, or timed out,
  must never be counted as killed.
- **Performance testing**: k6 — same as every other language here, k6 scripts stay JavaScript
  regardless of the target service's language.
- **Reporting**: [Allure](https://allurereport.org/) — the most widely adopted cross-language test
  reporting tool, with first-class JUnit 5 and Cucumber integration (relevant if Cucumber-JVM is
  adopted for BDD). `ExtentReports` is a Java-specific alternative if Allure's broader ecosystem
  positioning isn't a fit.
