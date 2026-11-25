---
name: test-junit
description: Use this skill when writing or fixing unit tests with JUnit 5 (Java).
---

# JUnit 5 Testing Skill

JUnit 5 (Jupiter) is the standard Java testing framework. It is composed of three modules: JUnit Platform, JUnit Jupiter (the API), and JUnit Vintage (for legacy JUnit 4 tests).

## Detection

JUnit 5 is in use when:
- `pom.xml` includes `junit-jupiter` or `junit-jupiter-api` dependency
- `build.gradle` includes `testImplementation 'org.junit.jupiter:junit-jupiter'`
- Test files use `@Test` from `org.junit.jupiter.api`
- Test files follow `*Test.java` or `*Tests.java` naming convention

## File Structure

```
src/
  main/java/com/example/
    Foo.java               # production file
  test/java/com/example/
    FooTest.java           # test file (mirrors main structure)
```

## Basic Test Structure

```java
package com.example;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

class FooTest {

  private Foo foo;

  @BeforeEach
  void setUp() {
    foo = new Foo();
  }

  @AfterEach
  void tearDown() {
    // cleanup if needed
  }

  @Test
  void methodName_shouldReturnExpectedValue_whenGivenValidInput() {
    // Arrange
    String input = "hello";

    // Build
    String result = foo.process(input);

    // Assert
    assertEquals("HELLO", result);
  }

  @Test
  void methodName_shouldThrow_whenInputIsNull() {
    assertThrows(IllegalArgumentException.class, () -> foo.process(null));
  }
}
```

## Naming Conventions

Use the pattern: `methodName_shouldExpectedBehavior_whenCondition`

Examples:
- `processInput_shouldReturnUpperCase_whenGivenLowerCaseString`
- `connect_shouldThrowException_whenHostIsUnreachable`
- `calculate_shouldReturnZero_whenListIsEmpty`

## Annotations

| Annotation | Purpose |
|---|---|
| `@Test` | Marks a method as a test |
| `@BeforeEach` | Run before each test method |
| `@AfterEach` | Run after each test method |
| `@BeforeAll` | Run once before all tests (must be `static`) |
| `@AfterAll` | Run once after all tests (must be `static`) |
| `@Disabled` | Skip a test (add reason as value) |
| `@DisplayName` | Human-readable test name |
| `@Nested` | Nested test class for grouping |
| `@ParameterizedTest` | Run test with multiple inputs |

## Common Assertions

```java
assertEquals(expected, actual)
assertEquals(expected, actual, "message on failure")
assertNotEquals(unexpected, actual)
assertNull(value)
assertNotNull(value)
assertTrue(condition)
assertFalse(condition)
assertThrows(ExpectedException.class, () -> { code(); })
assertDoesNotThrow(() -> { code(); })
assertAll(
  () -> assertEquals(1, a),
  () -> assertEquals(2, b)
)
```

## Parameterized Tests

```java
@ParameterizedTest
@ValueSource(strings = { "hello", "world", "foo" })
void isNonEmpty_shouldReturnTrue_whenGivenNonEmptyString(String input) {
  assertTrue(StringUtil.isNonEmpty(input));
}

@ParameterizedTest
@CsvSource({ "1, 1, 2", "2, 3, 5", "0, 0, 0" })
void add_shouldReturnSum(int a, int b, int expected) {
  assertEquals(expected, calculator.add(a, b));
}

@ParameterizedTest
@MethodSource("provideInputs")
void process_shouldHandleAllCases(String input, String expected) {
  assertEquals(expected, foo.process(input));
}

static Stream<Arguments> provideInputs() {
  return Stream.of(
    Arguments.of("hello", "HELLO"),
    Arguments.of("", "")
  );
}
```

## Nested Tests

```java
@Nested
@DisplayName("when input is valid")
class WhenInputIsValid {

  @Test
  void shouldReturnResult() { ... }

  @Test
  void shouldNotThrow() { ... }
}

@Nested
@DisplayName("when input is null")
class WhenInputIsNull {

  @Test
  void shouldThrowIllegalArgument() { ... }
}
```

## Running Tests

```bash
# Maven
mvn test

# Run a specific test class
mvn test -Dtest=FooTest

# Run a specific method
mvn test -Dtest=FooTest#methodName

# Gradle
./gradlew test

# Run specific test
./gradlew test --tests "com.example.FooTest"
```

## pom.xml Dependency

```xml
<dependency>
  <groupId>org.junit.jupiter</groupId>
  <artifactId>junit-jupiter</artifactId>
  <version>5.10.0</version>
  <scope>test</scope>
</dependency>
```

Also ensure the Surefire plugin version supports JUnit 5:
```xml
<plugin>
  <groupId>org.apache.maven.plugins</groupId>
  <artifactId>maven-surefire-plugin</artifactId>
  <version>3.1.2</version>
</plugin>
```

## Common Pitfalls

- `@BeforeAll` / `@AfterAll` methods must be `static` unless `@TestInstance(Lifecycle.PER_CLASS)` is used
- JUnit 5 test classes and methods do NOT need to be `public` — package-private is preferred
- `assertThrows` returns the thrown exception — use it to assert the exception message too: `assertEquals("msg", ex.getMessage())`
- Do not mix JUnit 4 (`org.junit.*`) and JUnit 5 (`org.junit.jupiter.*`) imports in the same file
- Never write tests for Spring Boot Configuration classes; By default only create tests for business logic and utility classes.
