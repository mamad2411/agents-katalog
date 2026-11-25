---
name: archunit-layer-rules
description: >
  ArchUnit layer and package dependency rules for owned Java/Kotlin codebases:
  layeredArchitecture, slice rules, no-cycles, adapter boundaries, and JUnit
  architecture tests in CI. Use when enforcing hexagonal/clean architecture or
  preventing domain→infrastructure leaks — not for runtime network security testing.
---

# ArchUnit Layer Rules

## Scope And Authorization

- **In scope:** Java/Kotlin repositories you own or may modify under authorization.
- **Out of scope:** Scanning third-party binaries you cannot change; using ArchUnit as a substitute for runtime appsec testing.
- Prefer failing CI on architecture violations over wiki-only diagrams.
- Start with package conventions that match the real codebase; do not invent layers nobody uses.
- Pair with `code-quality-standards` and `java-style-and-javadoc` / language packs as needed.

## When To Use

- Enforcing controller → service → persistence direction (or ports/adapters).
- Preventing domain packages from importing Spring Web / JPA types.
- Guarding against cyclic package dependencies.
- Documenting architecture as executable tests for new team members.
- Tightening module boundaries before a modular monolith split.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| SpotBugs / general Java quality | `java-style-and-javadoc` + `code-quality-standards` |
| Runtime authn/z testing | API/auth skills |
| Kotlin-specific style | Kotlin style skill if present |
| Multi-repo service contracts | API docs / AsyncAPI skills |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Concept | Guidance |
| --- | --- |
| Layers | Explicit `whereLayer(...).mayOnlyBeAccessedByLayers(...)` |
| Slices | `slices().matching("..module.(*)..").should().notDependOnEachOther()` |
| Naming | Align packages: `..api..`, `..domain..`, `..application..`, `..infrastructure..` |
| Freezing | `FreezingArchRule` for legacy debt with intentional thaw process |
| CI | Run architecture tests in unit test phase; keep fast |
| Tooling | ArchUnit + JUnit 4/5; optional ArchUnit Spring extensions |

## Typical Layer Map

| Layer package | May depend on | Must not depend on |
| --- | --- | --- |
| `..presentation..` / `..web..` | application, domain | infrastructure internals (optional strict) |
| `..application..` | domain | frameworks if hexagonal pure |
| `..domain..` | nothing upward | Spring, JPA, HTTP clients |
| `..infrastructure..` | domain, application ports | — (implements adapters) |

Adjust names to your repo (`com.example.order.domain`, etc.).

## Workflow

### 1. Confirm scope and success criteria

1. Record module(s), package root, build tool (Maven/Gradle), current architecture intent.
2. Success: ArchUnit tests green in CI; forbidden imports fail the build; documented freezes for legacy only.
3. Agree owners for exceptions (who may thaw freeze rules).

### 2. Inventory packages and debt

```bash
# Example: show package tree (adjust)
find src/main/java -type d | head -n 80
./mvnw -q test -Dtest=ArchitectureTest
# or
./gradlew test --tests '*Architecture*'
```

1. List actual top-level packages; draw the intended dependency direction.
2. Note worst offenders (domain importing `org.springframework.*`).
3. Decide: strict layers vs incremental freeze.

### 3. Baseline

1. Add ArchUnit dependency (test scope) matching Java version support.
2. Create `ArchitectureTest` (or `OnionArchitectureTest`) under `src/test/java`.
3. Run once with loose rules or freezes to quantify violations.

**Maven dependency sketch:**

```xml
<dependency>
  <groupId>com.tngtech.archunit</groupId>
  <artifactId>archunit-junit5</artifactId>
  <version>1.3.0</version>
  <scope>test</scope>
</dependency>
```

### 4. Write layer and safety rules

```java
import com.tngtech.archunit.core.importer.ImportOption;
import com.tngtech.archunit.junit.AnalyzeClasses;
import com.tngtech.archunit.junit.ArchTest;
import com.tngtech.archunit.lang.ArchRule;

import static com.tngtech.archunit.library.Architectures.layeredArchitecture;
import static com.tngtech.archunit.lang.syntax.ArchRuleDefinition.noClasses;
import static com.tngtech.archunit.library.dependencies.SlicesRuleDefinition.slices;

@AnalyzeClasses(packages = "com.example.app", importOptions = ImportOption.DoNotIncludeTests.class)
class ArchitectureTest {

  @ArchTest
  static final ArchRule layers = layeredArchitecture()
      .consideringAllDependencies()
      .layer("Web").definedBy("..web..", "..api..")
      .layer("Application").definedBy("..application..")
      .layer("Domain").definedBy("..domain..")
      .layer("Infrastructure").definedBy("..infrastructure..")
      .whereLayer("Web").mayNotBeAccessedByAnyLayer()
      .whereLayer("Application").mayOnlyBeAccessedByLayers("Web")
      .whereLayer("Domain").mayOnlyBeAccessedByLayers("Application", "Infrastructure", "Web")
      .whereLayer("Infrastructure").mayOnlyBeAccessedByLayers("Application", "Web");

  @ArchTest
  static final ArchRule domain_must_not_use_spring = noClasses()
      .that().resideInAPackage("..domain..")
      .should().dependOnClassesThat().resideInAnyPackage(
          "org.springframework..", "jakarta.persistence..", "javax.persistence..");

  @ArchTest
  static final ArchRule no_package_cycles = slices()
      .matching("com.example.app.(*)..")
      .should().beFreeOfCycles();
}
```

**Additional useful rules**

1. Controllers (`..web..`) must not call repositories directly if you require application services.
2. Only infrastructure may use JDBC/Kafka client drivers.
3. `noClasses().should().useAccessors()`-style rules only when team agrees (avoid noise).

**Legacy freezes**

```java
import com.tngtech.archunit.library.freeze.FreezingArchRule;

@ArchTest
static final ArchRule frozen_layers = FreezingArchRule.freeze(layers);
```

1. Commit freeze store; require PR review to expand violations.
2. Track burn-down of frozen lines in tech-debt tickets.

### 5. Verify with evidence

```bash
./mvnw -q test -Dtest=ArchitectureTest
# Introduce a deliberate bad import in a branch and confirm failure message is clear
./gradlew test --tests ArchitectureTest
```

1. Ensure violation messages name the offending class (developer UX).
2. Confirm tests run on main CI, not only local.
3. Document intentional exceptions with owner + expiry (or freeze entry).

### 6. Observe and harden

1. When adding modules, extend `definedBy` packages in the same PR.
2. Fail builds on cycles early — cycles grow silently.
3. Revisit layer map when adopting hexagonal ports (`..domain.port..` vs adapters).

### 7. Hand off

1. Short architecture ADR + link to `ArchitectureTest`.
2. Onboarding: “architecture is enforced in CI.”
3. Pair with code review checklist for cross-layer leaks.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Packages | Real packages match layers | Fictional `..domain..` nobody uses |
| Rules | Few strict high-value rules | 50 noisy rules, all ignored |
| Debt | FreezingArchRule + burn-down | `@Disabled` on architecture tests |
| Domain purity | No Spring in domain | “Just this one EntityManager” |
| CI | ArchitectureTest always on | Only run before releases |
| Scope | Own codebase | Analyzing unowned jars for fun |

## Output Checklist

- [ ] Package map and intended dependency direction documented
- [ ] ArchUnit test dependency added (test scope)
- [ ] Layer rules encode real boundaries
- [ ] Domain/framework isolation rules where required
- [ ] Cycle checks enabled at agreed slice grain
- [ ] Freeze/exceptions owned if legacy debt exists
- [ ] CI runs architecture tests; deliberate violation fails
- [ ] ADR/onboarding notes updated
- [ ] `code-quality-standards` applied to test code

## Rules

- Executable architecture over slide decks alone.
- Keep rules understandable; delete rules the team will not enforce.
- Do not weaken production security controls via this skill — it is structural, not runtime authz.
- Prefer small package renames + freezes over a big-bang rewrite.
- Focus on ArchUnit layer/slice rules; route style and runtime security to other skills.
