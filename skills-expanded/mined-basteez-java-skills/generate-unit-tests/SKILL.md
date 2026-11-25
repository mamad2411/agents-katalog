---
name: generate-unit-tests
description: >
  Generate JUnit unit tests for a Java class with Mockito mocks and AssertJ assertions.
  Supports Spring Boot, Quarkus, and Micronaut with framework-appropriate mock patterns.
  Use when creating test coverage for a Java source file.
argument-hint: "[path-to-java-class]"
disable-model-invocation: true
allowed-tools: Read Write Edit Glob Grep
---

# Generate Unit Tests

## Purpose

This skill generates a comprehensive JUnit unit test class for a given Java source class. It analyzes the target class's public methods, detects dependencies, and produces compilable test code covering happy paths, edge cases, and exception flows using Mockito for mocking and AssertJ for assertions.

## Usage

```
/generate-unit-tests <path-to-java-class>
```

**Argument**: `$ARGUMENTS` — the file path (relative or absolute) to the target `.java` source file. Required; no default.

### Examples

```
/generate-unit-tests src/main/java/com/example/service/OrderService.java
```

Generates `src/test/java/com/example/service/unit/OrderServiceTest.java` with test methods for every public method, mock setup for dependencies, and edge case coverage.

If `OrderServiceTest.java` already exists in the `.unit` subpackage, the skill detects which methods are already covered and generates tests only for uncovered methods.

### Expected Output

For a class with constructor-injected dependencies, the skill generates a test class with `@Mock` fields for each dependency, `@InjectMocks` for the class under test, `@Nested` inner classes grouping tests by method, and test methods following the `shouldBehaviorWhenCondition` naming convention with Arrange-Act-Assert structure.

## Behavior Summary

- **Concrete classes**: Generates full test class with happy-path and edge-case tests
- **Classes with dependencies**: Detects constructor and field injection, generates `@Mock`/`@InjectMocks` setup
- **Records**: Tests accessors and custom methods without mock setup
- **Enums with methods**: Tests like utility classes on relevant constants
- **Interfaces/abstract classes**: Rejected with informational message
- **Existing test file**: Supplements with tests for uncovered methods only

---

## Instructions

You are generating a JUnit unit test class for a Java source file. Follow each section below in order.

### Step 0: Detect Framework

Before reading the target class, detect the project's Java framework by scanning build files.

Read [reference/framework-patterns.md](reference/framework-patterns.md) for the complete detection matrix and framework-specific mock patterns.

**Detection signals**:
- **Spring Boot**: `spring-boot-starter-*` dependencies or `org.springframework.boot` Gradle plugin
- **Quarkus**: `quarkus-bom` BOM or `io.quarkus` Gradle plugin or `quarkus-*` dependencies
- **Micronaut**: `micronaut-platform` BOM or `io.micronaut.application`/`io.micronaut.library` Gradle plugin

**If no supported framework is detected**, inform the user:
> "No supported framework detected. This skill requires Spring Boot, Quarkus, or Micronaut."
Then **stop**.

Record the detected framework. This determines the mock runner annotations in Step 5.

### Step 1: Read and Analyze the Target Class

Read the file at `$ARGUMENTS`.

**If the file does not exist or is not a `.java` file**, inform the user and stop.

Analyze the class and determine:

1. **Package name**: Extract from the `package` declaration
2. **Class name**: The simple class name
3. **Class kind**: Determine if it is a `class`, `record`, or `enum`
   - If it is an **interface** or **abstract class**, inform the user: "Unit tests require a concrete class. Consider testing an implementation of this interface/abstract class instead." Then **stop**.
4. **Public methods**: Extract all public methods (instance and static). Include method name, return type, parameter types/names/annotations, declared exceptions, and whether the method is static.
   - If there are **no public methods**, inform the user: "No testable public methods found in this class." Then **stop**.

### Step 2: Detect Dependencies

Scan the target class for dependencies that need to be mocked:

1. **Constructor injection**: Find the biggest constructor. Each parameter is a dependency with injection method `CONSTRUCTOR`.
2. **Field injection**: Find fields annotated with `@Inject`, `@Autowired`, or `@Resource` that are NOT already covered by constructor parameters. Each is a dependency with injection method `FIELD`.

For each dependency, record:
- The type (simple name and fully qualified if available)
- The field/parameter name
- The injection method (`CONSTRUCTOR` or `FIELD`)

**Records**: Records have no mutable dependencies — skip dependency detection. Tests should focus on accessors and custom methods.

**Enums with methods**: Enums typically have no injected dependencies — skip dependency detection. Test methods by invoking them on relevant enum constants.

### Step 3: Resolve Test File Path

Determine the test file location using the `.unit` subpackage convention:

1. Take the source file path (e.g., `src/main/java/com/example/service/OrderService.java`)
2. Mirror it under `src/test/java` with a `.unit` subpackage (e.g., `src/test/java/com/example/service/unit/OrderServiceTest.java`)
3. The test class name is `<ClassName>Test`

**Check if the test file already exists.** If it does, proceed to **Step 7 (Supplementation)** instead of generating a new file.

### Step 4: Detect JUnit Version

Determine whether the target project uses JUnit 4 or JUnit 5:

1. Check existing test files in `src/test/java` for import patterns:
   - `org.junit.jupiter` → **JUnit 5**
   - `org.junit.Test` (without `jupiter`) → **JUnit 4**
2. Check build configuration (`pom.xml` or `build.gradle`/`build.gradle.kts`) for dependency declarations:
   - `junit-jupiter` or `junit-bom` with version 5.x → **JUnit 5**
   - `junit:junit:4.x` → **JUnit 4**
3. If no signal is found, **default to JUnit 5**.

Adapt generated code based on the detected version:

| Aspect | JUnit 5 | JUnit 4 |
|--------|---------|---------|
| Test annotation | `@Test` from `org.junit.jupiter.api.Test` | `@Test` from `org.junit.Test` |
| Mock runner | `@ExtendWith(MockitoExtension.class)` | `@RunWith(MockitoJUnitRunner.class)` |
| Setup method | `@BeforeEach` | `@Before` |
| Nested classes | `@Nested` supported | Not available — flatten test methods |
| Imports | `org.junit.jupiter.api.*` | `org.junit.*` |
| Mockito imports | `org.mockito.junit.jupiter.MockitoExtension` | `org.mockito.junit.MockitoJUnitRunner` |

### Step 5: Generate Test Class Scaffolding

Generate the test class structure based on the detected framework. Read [reference/framework-patterns.md](reference/framework-patterns.md) for complete code patterns.

#### Spring Boot

```java
package <same.as.source>.unit;

import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import static org.assertj.core.api.Assertions.*;
import static org.mockito.Mockito.*;
import static org.mockito.ArgumentMatchers.*;

@ExtendWith(MockitoExtension.class)
class <ClassName>Test {

    @Mock
    private <DependencyType> <dependencyName>;

    @InjectMocks
    private <ClassName> <classNameCamelCase>;
}
```

#### Quarkus

```java
package <same.as.source>.unit;

import io.quarkus.test.junit.QuarkusTest;
import io.quarkus.test.InjectMock;
import jakarta.inject.Inject;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;

import static org.assertj.core.api.Assertions.*;
import static org.mockito.Mockito.*;
import static org.mockito.ArgumentMatchers.*;

@QuarkusTest
class <ClassName>Test {

    @InjectMock
    <DependencyType> <dependencyName>;

    @Inject
    <ClassName> <classNameCamelCase>;
}
```

#### Micronaut

```java
package <same.as.source>.unit;

import io.micronaut.test.extensions.junit5.annotation.MicronautTest;
import jakarta.inject.Inject;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;

import static org.assertj.core.api.Assertions.*;
import static org.mockito.Mockito.*;
import static org.mockito.ArgumentMatchers.*;

@MicronautTest
class <ClassName>Test {

    @io.micronaut.test.annotation.MockBean(<DependencyType>.class)
    <DependencyType> <dependencyName>() {
        return mock(<DependencyType>.class);
    }

    @Inject
    <ClassName> <classNameCamelCase>;

    @Inject
    <DependencyType> <dependencyName>;
}
```

**Import rules**:
- Include ALL types referenced in the test: source class, dependency types, return types, parameter types, exception types
- Use static imports for AssertJ (`org.assertj.core.api.Assertions.*`) and Mockito (`org.mockito.Mockito.*`, `org.mockito.ArgumentMatchers.*`)
- If the class has no dependencies, omit mock annotations and imports. Instantiate the class directly in each test (for Spring Boot, also omit `@ExtendWith`; for Quarkus/Micronaut, keep the test annotation but omit mock declarations).

### Step 6: Generate Test Methods

For each public method, generate test methods grouped in a `@Nested` inner class named after the method (PascalCase, e.g., `FindById` for `findById`).

Every test method MUST:
- Follow `shouldBehaviorWhenCondition` camelCase naming
- Use the Arrange-Act-Assert pattern with blank lines separating each section
- Include meaningful test data (not just `null` or `0` everywhere)

#### Happy-Path Tests

Generate at least one happy-path test per public method:
- Set up mock return values using `when(...).thenReturn(...)`
- Call the method on the class under test
- Assert the expected result using AssertJ

#### Edge-Case Tests

For each public method, analyze the signature and apply these heuristics to generate additional tests:

| Signal | Edge Case | Test Pattern |
|--------|-----------|-------------|
| Reference parameter without `@NonNull`/`@NotNull` | Null input | Pass `null` for that parameter, assert exception or graceful handling |
| `Collection`, `List`, `Set`, `Map`, or array parameter | Empty collection | Pass empty collection/array, assert behavior |
| `Optional<T>` return type | Empty optional | Stub dependencies to cause empty result, `assertThat(result).isEmpty()` |
| `Optional<T>` return type | Present optional | Stub for success, `assertThat(result).isPresent().contains(value)` |
| `boolean` return type | Both branches | Two tests: one asserting `isTrue()`, one asserting `isFalse()` |
| `void` return type | Side effects | `verify(mock).methodCall(args)` to confirm interaction |
| `throws` clause or method that delegates to a dependency that can throw | Exception path | Stub dependency to throw, `assertThatThrownBy(() -> sut.method()).isInstanceOf(Exception.class)` |
| `String` parameter | Empty string | Pass `""`, assert behavior |

**Priority**: Generate tests in this order: happy path → null inputs → empty collections → exceptions → boolean branches → void verification.

For non-obvious edge case tests, include a brief inline comment explaining why the test exists, e.g.:
```java
@Test
void shouldReturnEmptyListWhenStatusIsNull() {
    // Null status could bypass filtering — verify defensive behavior
    ...
}
```

#### Mock Stubbing Patterns

Use the appropriate Mockito pattern based on the method being stubbed:

- **Methods with return values**: `when(mock.method(args)).thenReturn(value)`
- **Void methods with side effects**: `verify(mock).method(args)` in the assert block
- **Exception scenarios**: `when(mock.method(args)).thenThrow(new SomeException("message"))`
- **Argument matching**: Use `any()`, `anyLong()`, `anyString()`, `eq(value)` as appropriate. Prefer exact values when meaningful.

### Step 7: Supplement Existing Test File

**This step only applies when a test file already exists at the resolved path.**

1. Read both the source class and the existing test file.
2. Extract all public method names from the source class.
3. For each public method, check if it is already covered in the existing test file using these signals:
   - **High confidence**: Method name appears in a `@Nested` class name (e.g., `class FindById` covers `findById`)
   - **High confidence**: Method is called on the `@InjectMocks` instance inside a `@Test` method
   - **Medium confidence**: Method name is a substring of a test method name
4. For methods that are NOT covered:
   - Generate new `@Nested` classes with test methods following all the rules above
   - Append them at the end of the test class (before the closing brace)
   - Add any new `@Mock` fields needed by the new tests (at the top, with existing mocks)
   - Add any new import statements needed
5. **Never** modify, reorder, or duplicate existing test methods.
6. If all public methods are already covered, inform the user: "All public methods in `<ClassName>` already have test coverage in `<TestClassName>`." and make no changes.

### Step 8: Handle Records and Enums

#### Records

For Java records:
- Test each accessor method (component accessor)
- Test any custom methods defined on the record
- Test `equals`/`hashCode`/`toString` only if they are explicitly overridden
- Do NOT generate mock setup — records typically have no dependencies
- Instantiate the record directly with test data

#### Enums with Methods

For enums that have methods beyond the standard `values()`/`valueOf()`:
- Test each custom method by invoking it on relevant enum constants
- Do NOT generate mock setup
- Use direct enum constant references (e.g., `Status.ACTIVE.getLabel()`)

---

## Additional resources

- For a complete input/output example showing an `OrderService` class and its generated test class, see [examples/example-output.md](examples/example-output.md). Read this file when generating test output to follow the exact format and patterns.

---

Now generate the unit test class for the file at: `$ARGUMENTS`
