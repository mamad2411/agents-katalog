---
name: "spring-boot-4-test-stabilization"
description: "Test isolation patterns, mock strategies, and troubleshooting guide for Spring Boot 4.x unit and integration tests. Eliminates unnecessary database dependencies, fixes mocking issues, and achieves fast, reliable test execution."
version: 1
created: "2026-06-09"
updated: "2026-06-09"
---
## When to Use
Use when tests are flaky, slow, or failing due to mocking issues, database dependencies, or Spring context problems. Apply when migrating from JUnit 4 to JUnit 5, or from @MockBean to @MockitoBean. Essential for achieving 90%+ test coverage with fast, isolated unit tests and targeted integration tests.

## Procedure
1. STEP 1: Classify Test Types - Identify test purpose: UNIT (single class, all dependencies mocked), SLICE (controller/repository layer with minimal Spring context), INTEGRATION (full Spring context with real or embedded DB). Unit tests should be 70-80% of total, slice tests 15-20%, integration tests 5-10%. Unit tests use @ExtendWith(MockitoExtension.class), slice tests use @WebMvcTest/@DataJpaTest, integration tests use @SpringBootTest
2. STEP 2: Configure Unit Tests (No Spring Context) - Annotate test class with @ExtendWith(MockitoExtension.class) ONLY (no @SpringBootTest). Use @Mock for dependencies, @InjectMocks for class under test. Mock ALL external dependencies (repositories, Feign clients, cache services). Use BDD-style mocking: given(mock.method()).willReturn(value). Use AssertJ assertions: assertThat(actual).isEqualTo(expected). Verify interactions with then(mock).should().method(). NO database, NO Spring beans, NO application context
3. STEP 3: Configure Controller Slice Tests - Use @WebMvcTest(ControllerClass.class) to test controller layer only. Use @MockitoBean (NOT @MockBean) to mock service layer dependencies. Inject MockMvc to simulate HTTP requests. Example: mockMvc.perform(post('/api/v1/resource').contentType(APPLICATION_JSON).content(json)).andExpect(status().isOk()). Verify request validation (@Valid) triggers errors. Mock TenantContextHolder if used. NO database access in controller tests
4. STEP 4: Configure Repository Slice Tests - Use @DataJpaTest for repository layer tests. Add @AutoConfigureTestDatabase(replace = Replace.NONE) to use Testcontainers or H2. Use Testcontainers for PostgreSQL integration tests: @Testcontainers + @Container with PostgreSQLContainer. Alternatively use H2 in-memory for simple CRUD tests. Load test data with @Sql scripts or programmatic inserts. Verify queries return expected results. Test custom @Query methods. NO service layer or controller dependencies
5. STEP 5: Eliminate Database Dependencies from Unit Tests - NEVER use @SpringBootTest for service layer unit tests. Mock repository layer with @Mock instead of real database. Use Mockito to return test data: given(repository.findById(1L)).willReturn(Optional.of(entity)). Test business logic in isolation without database. Verify repository method calls with then(repository).should().save(any()). If service uses @Transactional, ignore it in unit tests (transaction behavior tested in integration tests only)
6. STEP 6: Fix Common Mocking Issues - 'UnnecessaryStubbingException': Remove unused given() stubs or add lenient() for optional mocks. 'No qualifying bean': Add @MockitoBean for missing dependencies in slice tests. 'NullPointerException in mock': Verify given() returns non-null (use Optional.of() or mock objects). 'ArgumentMatcher error': Use eq() for literal values mixed with matchers. 'Wrong method signature': Verify mock method signature exactly matches real method (types, parameter order). Use @Captor ArgumentCaptor for complex verification
7. STEP 7: Configure Test Properties - Create src/test/resources/application-test.yml with minimal config. Disable unnecessary features: spring.autoconfigure.exclude for DataSource if not needed. Set logging.level.root=WARN to reduce noise. Use H2 or Testcontainers for database tests. Mock external APIs (Feign clients) with WireMock or @MockitoBean. Set spring.jpa.hibernate.ddl-auto=create-drop for test DB. Override cache config to use simple in-memory cache
8. STEP 8: Parallel Test Execution - Enable parallel execution in pom.xml: junit.jupiter.execution.parallel.enabled=true, mode.default=concurrent, mode.classes.default=concurrent. Ensure tests are isolated (no shared state). Use @TestInstance(Lifecycle.PER_CLASS) if setup is expensive. Disable parallel execution for integration tests if they share database state. Configure maven-surefire-plugin with forkCount=1C (one fork per CPU core)
9. STEP 9: JaCoCo Configuration and Coverage - Configure JaCoCo plugin in pom.xml with 90% threshold. Exclude DTOs, constants, exceptions, configuration classes from coverage: **/dto/**, **/model/**, **/exception/**, **/*Application.class. Run mvn clean test jacoco:report to generate report. Check target/site/jacoco/index.html for coverage details. Focus on service layer (100% target) and controller layer (90% target). Use @Generated to exclude auto-generated code from coverage
10. STEP 10: Migration from JUnit 4 to JUnit 5 - Replace @RunWith(SpringRunner.class) with @ExtendWith(SpringExtension.class) or @SpringBootTest. Replace @RunWith(MockitoJUnitRunner.class) with @ExtendWith(MockitoExtension.class). Replace org.junit.Test with org.junit.jupiter.api.Test. Replace @Before/@After with @BeforeEach/@AfterEach. Replace assertEquals with assertThat().isEqualTo(). Add junit-vintage-engine to exclusions in pom.xml. Use @ParameterizedTest for data-driven tests

## Pitfalls
- DO NOT use @SpringBootTest for unit tests - it loads full Spring context and is slow (use @ExtendWith(MockitoExtention.class) instead)
- DO NOT use @MockBean in Spring Boot 4.x - use @MockitoBean instead (Spring Boot 4.x deprecates @MockBean)
- DO NOT mix unit and integration test annotations - use EITHER @ExtendWith(MockitoExtension.class) OR @SpringBootTest, not both
- DO NOT access real database in unit tests - mock repositories and cache services instead
- DO NOT use Testcontainers for unit tests - only for integration/repository tests (Testcontainers is slow)
- DO NOT forget to mock TenantContextHolder or other ThreadLocal utilities - they return null in tests without setup
- DO NOT leave unused mocks - Mockito throws UnnecessaryStubbingException for stubs that are never verified
- DO NOT use assertEquals from JUnit - use AssertJ assertThat().isEqualTo() for better error messages
- DO NOT test transaction behavior in unit tests - @Transactional is ignored without Spring context
- DO NOT share state between tests - each test should be independent and isolated
- DO NOT use @BeforeAll without @TestInstance(Lifecycle.PER_CLASS) - setup runs once per class, not per test
- DO NOT enable parallel execution without ensuring tests are thread-safe and isolated
- DO NOT exclude service layer from JaCoCo - target 100% service coverage, exclude only DTOs/models/constants
- DO NOT use H2 for complex PostgreSQL-specific queries - use Testcontainers with PostgreSQL image for accurate testing
- DO NOT mock final classes without mockito-inline dependency - add mockito-inline for final class mocking

## Verification
1. Verify unit tests run without Spring context: check no @SpringBootTest annotation, only @ExtendWith(MockitoExtension.class)
2. Confirm all unit tests use @Mock and @InjectMocks with BDD-style given/then
3. Run 'mvn clean test' and verify all tests pass with execution time < 30 seconds for unit tests
4. Check controller tests use @WebMvcTest and @MockitoBean (not real database)
5. Verify repository tests use @DataJpaTest with Testcontainers or H2
6. Confirm JaCoCo report shows >= 90% coverage with proper exclusions (mvn jacoco:report)
7. Validate no UnnecessaryStubbingException warnings in test output
8. Check test isolation: run tests in random order or parallel mode without failures
9. Verify JUnit 5 is used: all tests use org.junit.jupiter.api.Test (not org.junit.Test)
10. Confirm no junit-vintage-engine in dependencies (check mvn dependency:tree)
11. Validate test naming follows pattern: methodName_scenario_expectedBehavior with @DisplayName
12. Check application-test.yml exists with minimal configuration for fast startup