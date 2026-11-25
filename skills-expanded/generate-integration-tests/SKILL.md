---
name: generate-integration-tests
description: >
  Generate integration tests for a Java class using Testcontainers.
  Supports Spring Boot (3.1+), Quarkus (3.0+), and Micronaut (4.0+).
  Detects class type (repository, controller, service) and applies
  framework-appropriate test patterns. Requires Java 17+.
argument-hint: "[path-to-java-class]"
disable-model-invocation: true
allowed-tools: Read Write Edit Glob Grep
---

# Generate Integration Tests

## Purpose

This skill generates a comprehensive integration test class for a given Java source file. It detects the project's framework (Spring Boot, Quarkus, or Micronaut), identifies the class type (repository, controller, or service), and produces framework-appropriate integration tests using Testcontainers for real database and external service containers.

## Usage

```
/generate-integration-tests <path-to-java-class>
```

**Argument**: `$ARGUMENTS` — the file path (relative or absolute) to the target `.java` source file. Required; no default.

### Examples

```
/generate-integration-tests src/main/java/com/example/repository/OrderRepository.java
```

Generates `src/test/java/com/example/repository/integration/OrderRepositoryTest.java` with Testcontainers database setup, application context bootstrap, and test methods for each repository method.

### Expected Output

For a Spring Boot repository with a PostgreSQL database, the skill generates a test class with `@SpringBootTest`, `@Testcontainers`, `@ServiceConnection` on a `PostgreSQLContainer`, `@BeforeEach` for data cleanup, and `@Nested` inner classes grouping tests by method with `shouldBehaviorWhenCondition` naming and Arrange-Act-Assert structure.

## Behavior Summary

| Class Type | Detection Signal | Test Strategy |
|------------|-----------------|---------------|
| Repository | Extends `JpaRepository`/`CrudRepository`/`PanacheRepository`; `@Repository` annotation | Database container, CRUD + custom query tests |
| Controller | `@RestController`/`@Controller` (Spring), `@Path` (Quarkus), `@Controller` (Micronaut) | Full-stack boot, HTTP endpoint tests (MockMvc / RestAssured / HttpClient) |
| Service | `@Service`/`@Component`/`@ApplicationScoped`/`@Singleton` with external dependencies | Testcontainers for Kafka/Redis/RabbitMQ, WireMock for HTTP |
| No integration points | None of the above | Rejected — suggest `/generate-unit-tests` |

## Prerequisites

- A Java 17+ project with one of: Spring Boot 3.1+, Quarkus 3.0+, or Micronaut 4.0+
- For Testcontainers-based tests: Docker available on the developer's machine
- For H2 in-memory default: no Docker required

---

## Instructions

You are generating an integration test class for a Java source file. Follow each step below in order.

### Step 1: Read and Validate the Target Class

Read the file at `$ARGUMENTS`.

**If no argument is provided**, inform the user:
> "Please provide a path to a Java source file. Usage: `/generate-integration-tests path/to/MyClass.java`"
Then **stop**.

**If the file does not exist**, inform the user:
> "File not found: `{path}`. Please verify the path and try again."
Then **stop**.

**If the file is not a `.java` file**, inform the user:
> "Expected a `.java` file but got `{extension}`. Please provide a Java source file."
Then **stop**.

Analyze the class and extract:

1. **Package name**: From the `package` declaration
2. **Class name**: The simple class name
3. **Class kind**: `class`, `interface`, `record`, or `enum`
   - **Interfaces** are allowed ONLY if they are repository interfaces (extend a framework repository base). Other interfaces → inform user and stop.
   - **Abstract classes** → inform user: "Integration tests require a concrete class or repository interface." Then stop.
4. **Public methods**: All public methods with name, return type, parameter types/names/annotations, declared exceptions
5. **Dependencies**: Constructor-injected and field-injected dependencies (type + name)

### Step 2: Detect Build Tool

Scan the project for build files:

- Look for `pom.xml` (Maven)
- Look for `build.gradle` or `build.gradle.kts` (Gradle)

**If both exist**: Ask the user which build tool to use.

**If neither exists**: Inform the user that no supported build file was found and **stop**.

Record the build tool type and all build file paths (root + child modules for multi-module projects).

### Step 3: Detect Framework

Read [reference/framework-detection.md](reference/framework-detection.md) now for the complete detection matrix and procedure.

Scan the build files for framework markers. Record the detected framework (`SPRING_BOOT`, `QUARKUS`, or `MICRONAUT`) and the signal that identified it.

**If no supported framework is detected**:
> "No supported framework detected. This skill requires Spring Boot (3.1+), Quarkus (3.0+), or Micronaut (4.0+). For non-framework Java code, try `/generate-unit-tests` instead."
Then **stop**.

**If multiple frameworks are detected**:
> "Multiple frameworks detected: {framework1} and {framework2}. Please confirm which framework this project uses."
Then **stop** and wait for user response.

### Step 4: Detect JUnit Version

Check existing test files and build configuration for JUnit version signals:

1. Scan test files in `src/test/java` for import patterns:
   - `org.junit.jupiter` → **JUnit 5**
   - `org.junit.Test` (without `jupiter`) → **JUnit 4**
2. Check build files for dependency declarations:
   - `junit-jupiter` or `junit-bom` 5.x → **JUnit 5**
   - `junit:junit:4.x` → **JUnit 4**

**If JUnit 5 is detected or no signal is found (default)**: Proceed.

**If JUnit 4 is detected**:
> "Integration test generation requires JUnit 5 (all supported frameworks — Spring Boot, Quarkus, and Micronaut — use JUnit 5 test extensions). Please add the JUnit 5 dependency to your project and try again."
Then **stop**.

### Step 5: Check Testcontainers Dependency and Version

Scan the build files for Testcontainers dependencies:
- Maven: `org.testcontainers` groupId
- Gradle: `org.testcontainers` in any dependency

**If Testcontainers is not found**, inform the user with exact coordinates for their build tool. Read [reference/database-detection.md](reference/database-detection.md) for the dependency coordinates and version requirements. Note that H2 in-memory tests do not require Testcontainers.

**If Testcontainers is found**, check the version:
1. Look for a `<testcontainers.version>` property (Maven) or `ext['testcontainers.version']` (Gradle)
2. Look for a `testcontainers-bom` version in `<dependencyManagement>` (Maven) or `platform(...)` (Gradle)
3. If the version is explicitly set and is **< 1.21.0**, inform the user:
   > "Your Testcontainers version ({version}) may be incompatible with modern Docker runtimes (API v1.40+ required). Upgrade to 1.21.0+ by setting `<testcontainers.version>1.21.0</testcontainers.version>` in your build file."
4. If the version is managed by a framework BOM (Spring Boot, Quarkus, Micronaut) and cannot be extracted, proceed — but include this comment at the top of the generated test file:
   ```java
   // NOTE: Requires Testcontainers 1.21.0+ and a Docker-compatible runtime (API v1.40+).
   // If tests fail with "client version is too old", upgrade Testcontainers in your build file.
   ```

### Step 6: Detect Class Type

Analyze the target class to determine its type:

| Class Type | Detection Signals |
|------------|-------------------|
| **REPOSITORY** | Extends `JpaRepository`, `CrudRepository`, `PagingAndSortingRepository` (Spring Data), `PanacheRepository`, `PanacheEntityBase` (Quarkus Panache), `CrudRepository`, `PageableRepository` (Micronaut Data); or annotated with `@Repository` |
| **CONTROLLER** | Annotated with `@RestController` or `@Controller` (Spring), `@Path` (Quarkus JAX-RS), `@Controller` (Micronaut) |
| **SERVICE** | Annotated with `@Service`, `@Component` (Spring), `@ApplicationScoped`, `@Singleton`, `@RequestScoped` (Quarkus CDI), `@Singleton`, `@Prototype` (Micronaut); AND has at least one dependency on an external system (database, message broker, cache, HTTP API) |

**If none of the above signals match**:
> "No integration points found in `{ClassName}` (no database access, HTTP endpoints, or external service calls). Try `/generate-unit-tests` for unit test coverage instead."
Then **stop**.

### Step 7: Detect Integration Points

Scan the class's constructor parameters and injected fields for external system dependencies:

**Database**: Any repository-type dependency (see REPOSITORY signals above)

**Message Brokers**:
- Spring: `KafkaTemplate`, `RabbitTemplate`, `JmsTemplate`
- Quarkus: `@Channel`, `@Outgoing`, `@Incoming` (SmallRye Reactive Messaging), `@ConnectorAttribute`
- Micronaut: `@KafkaClient`, `@KafkaListener`, `@RabbitClient`, `@RabbitListener`

**Cache**:
- Spring: `RedisTemplate`, `StringRedisTemplate`, `CacheManager`
- Quarkus: `RedisDataSource`, `ReactiveRedisDataSource`
- Micronaut: `RedisCommands`, `StatefulRedisConnection`

**HTTP Clients**:
- Spring: `RestTemplate`, `WebClient`, `RestClient`
- Quarkus: `@RestClient` annotated interfaces
- Micronaut: `@Client` annotated interfaces or injected `HttpClient`

Record each integration point with its type and the Testcontainers module (or WireMock) needed.

### Step 8: Detect Database Type

Read [reference/database-detection.md](reference/database-detection.md) now for the complete detection matrix and procedure.

Follow the detection priority order (driver dependency → datasource URL → JPA dialect). Default to **H2 in-memory** if no database type can be determined.

### Step 9: Resolve Test File Path

Determine the test file location using the `.integration` subpackage convention:

1. Take the source file path (e.g., `src/main/java/com/example/repository/OrderRepository.java`)
2. Mirror it under `src/test/java` with an `.integration` subpackage:
   - `src/test/java/com/example/repository/integration/OrderRepositoryTest.java`
3. The test class name is `<ClassName>Test`

**Check if the test file already exists.** If it does, proceed to **Step 13 (Supplementation)** instead of generating a new file.

### Step 10: Generate Repository Tests

**This step applies only when classType is REPOSITORY.**

Read the framework-specific patterns reference file for the detected framework:
- Spring Boot: [reference/spring-boot-patterns.md](reference/spring-boot-patterns.md)
- Quarkus: [reference/quarkus-patterns.md](reference/quarkus-patterns.md)
- Micronaut: [reference/micronaut-patterns.md](reference/micronaut-patterns.md)

Also read [examples/spring-boot-repository.md](examples/spring-boot-repository.md) for a complete input/output example.

**Extract repository methods**:

1. **Custom query methods**: Methods with `@Query` annotations (Spring/Micronaut), `@NamedQuery` (Quarkus), or derived query methods (e.g., `findByStatus`, `countByCustomerName`)
2. **Inherited CRUD methods**: From the framework base interface (save, findById, findAll, delete, count, etc.)
3. **Entity type**: Extract from the generic type parameter (e.g., `JpaRepository<Order, Long>` → entity is `Order`, ID is `Long`)

**Read the entity class** to understand its fields, relationships, and constraints. This informs test data creation.

**Generate the test class** with:

1. **Class-level annotations**: Framework-appropriate test bootstrap (see reference files)
2. **Container setup**: Testcontainers database container with `@ServiceConnection` (Spring) or DevServices (Quarkus) or Test Resources (Micronaut). For H2 default: test property source instead.
3. **Repository injection**: `@Autowired` (Spring), `@Inject` (Quarkus/Micronaut)
4. **Setup method**: `@BeforeEach` to clean data between tests (for Spring/Micronaut), or `@TestTransaction` per test (for Quarkus)
5. **Test methods**: For **Spring Boot and Micronaut**, group in `@Nested` inner classes by method name (PascalCase). For **Quarkus**, do NOT use `@Nested` classes — Quarkus CDI rejects interceptor bindings (`@TestTransaction`) on inner class methods. Instead, use flat test methods with descriptive names.
   - **CRUD operations**: save, findById (found + not found), findAll, delete
   - **Custom queries**: One happy-path test per custom method with realistic test data that exercises the query logic
   - **Edge cases**: Empty results, null parameters (where applicable)
6. **Test naming**: `shouldBehaviorWhenCondition` camelCase
7. **Assertions**: AssertJ (`assertThat(...)`)
8. **Test data**: Realistic, domain-appropriate values (not nulls, zeros, or "test" strings)

Write the generated test file to the resolved path.

### Step 11: Generate Controller Tests

**This step applies only when classType is CONTROLLER.**

Read the framework-specific patterns reference file for the detected framework (same files as Step 10).

**Extract endpoint mappings**:

1. For each public method in the controller, extract:
   - HTTP method (`GET`, `POST`, `PUT`, `DELETE`, `PATCH`)
   - Path (from `@RequestMapping`/`@GetMapping`/etc. in Spring, `@Path`/`@GET`/etc. in Quarkus, `@Get`/`@Post`/etc. in Micronaut)
   - Path variables and query parameters
   - Request body type and validation annotations (`@Valid`, `@NotNull`, `@Size`, etc.)
   - Response type and status code

**Generate the test class** with:

1. **Class-level annotations**: Full-stack test bootstrap with database container (same as repository tests). For Spring: add `@AutoConfigureMockMvc`.
2. **HTTP client setup**:
   - Spring: `@Autowired MockMvc mockMvc`
   - Quarkus: RestAssured static imports (`given().when().then()`)
   - Micronaut: `@Inject @Client("/") HttpClient client`
3. **Data setup**: Inject the backing repository and insert test data in `@BeforeEach`
4. **Test methods**: For **Spring Boot and Micronaut**, group in `@Nested` inner classes by endpoint. For **Quarkus**, use flat test methods (no `@Nested` — same CDI limitation as repository tests).
   - **GET endpoints**: Test with existing data (assert status + body), test with no data (empty list or 404), test with invalid ID (404)
   - **POST endpoints**: Test with valid body (assert 201 + response body), test with invalid body (assert 400 + validation errors)
   - **PUT/PATCH endpoints**: Test update with valid data, test update of non-existent resource (404)
   - **DELETE endpoints**: Test successful deletion, test deletion of non-existent resource
5. **Validation tests**: For endpoints with `@Valid` request bodies, generate tests that violate each validation constraint

Write the generated test file to the resolved path.

### Step 12: Generate Service Tests

**This step applies only when classType is SERVICE.**

Read the framework-specific patterns reference file for the detected framework.

**For each integration point** detected in Step 7, set up the appropriate test infrastructure:

| Integration Point | Testcontainers Module | Setup Pattern |
|-------------------|-----------------------|---------------|
| Database (via repository) | Per database-detection.md | Same as repository tests |
| Kafka | `org.testcontainers:kafka` | `KafkaContainer` (Spring `@ServiceConnection`), DevServices (Quarkus), Test Resources (Micronaut) |
| Redis | `org.testcontainers:redis` (or `GenericContainer`) | Redis container with exposed port 6379 |
| RabbitMQ | `org.testcontainers:rabbitmq` | `RabbitMQContainer` |
| HTTP API (external) | None | WireMock (`WireMockExtension`) with stub setup |

**Generate the test class** with:

1. **Container setup**: One container per unique external dependency
2. **Service injection**: Direct injection of the service under test
3. **Test methods** per integration point:
   - **Message publishing**: Send a message through the service, consume from the topic/queue to verify
   - **Cache operations**: Put/get values through the service, verify cache state
   - **HTTP client calls**: Set up WireMock stubs, call the service method, verify WireMock received the expected request
4. **Error scenarios**: Test behavior when external service is unavailable or returns errors (WireMock returning 500, timeout simulation)

Write the generated test file to the resolved path.

### Step 13: Supplement Existing Test File

**This step only applies when a test file already exists at the resolved path (from Step 9).**

1. Read both the source class and the existing test file.
2. Extract all public method names (or endpoint mappings) from the source class.
3. For each public method, check if it is already covered in the existing test file using these signals:
   - **High confidence**: Method name appears in a `@Nested` class name (e.g., `class FindByStatus` covers `findByStatus`)
   - **High confidence**: Method is called on the test subject instance inside a `@Test` method
   - **Medium confidence**: Method name is a substring of a test method name
4. For methods that are NOT covered:
   - Generate new `@Nested` classes with test methods following all the rules above
   - Append them at the end of the test class (before the closing brace)
   - Add any new imports needed
5. **Never** modify, reorder, or duplicate existing test methods.
6. If all methods are already covered:
   > "All public methods in `{ClassName}` already have integration test coverage in `{TestClassName}`."
   Make no changes.

---

## Additional Resources

- For a complete Spring Boot repository input/output example, see [examples/spring-boot-repository.md](examples/spring-boot-repository.md)
- For a Quarkus controller example, see [examples/quarkus-controller.md](examples/quarkus-controller.md)
- For a Micronaut service example, see [examples/micronaut-service.md](examples/micronaut-service.md)

---

Now generate the integration test class for the file at: `$ARGUMENTS`
