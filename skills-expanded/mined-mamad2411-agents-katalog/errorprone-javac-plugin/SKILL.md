---
name: errorprone-javac-plugin
description: >
  Google Error Prone as a javac plugin for owned Java builds: enable BugChecker
  suite, fail CI on errors, tune severities, suppress carefully, and catch
  common correctness/security footguns at compile time. Use when Error Prone,
  -Xplugin:ErrorProne, BugPattern, or Maven/Gradle Error Prone setup.
---

# Error Prone javac Plugin

## Scope And Authorization

- **In scope:** Java/Kotlin-on-JVM builds you control (Maven/Gradle).
- **Out of scope:** Forcing plugins into third-party proprietary builds without agreement.
- Compile-time checks complement but do not replace runtime security review.
- Suppressions need owners—avoid repo-wide disable.
- Pair with `java-style-and-javadoc` and `code-quality-standards`.

## When To Use

- Adding Error Prone to a monorepo or service.
- Turning on stricter checks after a baseline cleanup.
- Replacing ad-hoc “please don’t do X” review comments with compiler errors.
- Investigating BugChecker false positives and scoped suppressions.
- Aligning JDK version with Error Prone compatibility.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| ESLint for JS security | `eslint-security-plugin` |
| Full SAST program | org SAST tooling |
| Java style/javadoc | `java-style-and-javadoc` |
| Implementation quality baseline | `code-quality-standards` |
| Runtime Express/Java web auth | framework security skills |

## Domain Focus

| Area | Guidance |
| --- | --- |
| Integration | javac plugin via Maven compiler / Gradle |
| Severity | ERROR for high-signal patterns in CI |
| Baseline | Patch-in gradually; don’t disable everything |
| Suppress | `@SuppressWarnings("BugPatternName")` with comment |
| Custom | Org BugCheckers for banned APIs |
| JDK | Match Error Prone version to JDK |

## Workflow

### 1. Confirm scope and success criteria

1. JDK version, build tool, modules in scope.
2. Success: CI fails on Error Prone ERROR; local `./gradlew build` reproduces.

### 2. Inventory build

```bash
# Maven
rg -n "errorprone|maven-compiler-plugin" pom.xml
# Gradle
rg -n "net.ltgt.errorprone|errorprone" *.gradle* build.gradle.kts
java -version
```

### 3. Baseline compile without Error Prone

1. Record clean build time and known warnings.
2. Identify generated code paths to exclude.

### 4. Enable Error Prone

**Gradle (conceptual):**

```kotlin
plugins {
  id("net.ltgt.errorprone") version "X.Y.Z"
}
dependencies {
  errorprone("com.google.errorprone:error_prone_core:2.x.y")
}
tasks.withType<JavaCompile>().configureEach {
  options.errorprone.isEnabled.set(true)
  options.errorprone.disableWarningsInGeneratedCode.set(true)
}
```

**Maven (conceptual):** annotate `maven-compiler-plugin` with annotationProcessorPaths for error_prone_core and `-XDcompilePolicy=simple` / `-Xplugin:ErrorProne` per current upstream docs.

1. Pin versions; read compatibility matrix for your JDK.
2. Start with default checks; promote important ones to error.

### 5. Tune and remediate

| Pattern examples | Why |
| --- | --- |
| `EqualsHashCode` | Contract bugs |
| `MissingOverride` | API drift |
| `StringSplitter` / regex | Footguns |
| `DoNotCall` / banned APIs | Security-sensitive methods |
| `FormatString` | Injection-ish logging bugs |

1. Fix real issues first; suppress only with justification.
2. For generated code: exclude or disable warnings in generated sources.
3. Optional: refaster/Error Prone for mass cleanups.

### 6. Verify with evidence

```bash
./gradlew clean compileJava
# or
mvn -q -DskipTests compile
```

1. Introduce a deliberate bug in a branch; confirm CI red.
2. Document suppressions count trend (should fall over time).

### 7. Hand off

1. Engineer handbook: how to read Error Prone messages and fix/suppress.
2. Version upgrade cadence with JDK upgrades.
3. Consider custom checkers for `Runtime.exec`, insecure random, etc.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| CI | ERROR fails build | Warnings only, ignored |
| Suppress | Line-level + ticket | `@SuppressWarnings("all")` |
| Generated | Excluded cleanly | Thousands of noise findings |
| Rollout | Module-by-module | Big-bang on day one unfixed |
| Versions | Pinned + compatible | Latest floating always |

## Output Checklist

- [ ] Error Prone wired for main modules
- [ ] CI fails on ERROR severity
- [ ] Generated code policy set
- [ ] High-signal checks enabled
- [ ] Suppression guidelines documented
- [ ] Deliberate-bug CI proof
- [ ] JDK compatibility recorded
- [ ] Residual gaps (runtime issues) noted

## Rules

- Owned builds only.
- Prefer fixing over blanket disable.
- Keep plugin versions explicit.
- Not a substitute for security tests.
- Style nits beyond Error Prone → Java style skill.
