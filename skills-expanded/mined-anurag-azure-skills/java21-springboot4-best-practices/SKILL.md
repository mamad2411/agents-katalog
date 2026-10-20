---
name: "java21-springboot4-best-practices"
description: "Java 21 LTS and Spring Boot 4.0.5+ coding guidelines and best practices for microservices development with modern language features, virtual threads, and production-ready patterns"
version: 2
created: "2026-06-08"
updated: "2026-06-08"
---
## When to Use
Use when developing Java microservices with JDK 21 and Spring Boot 4.x. Apply when writing new code, conducting code reviews, refactoring legacy code, or establishing team coding standards. Essential for greenfield projects or modernization efforts targeting modern Java capabilities.

## Procedure
1. **Use Java 21 Records for DTOs**: Implement all Data Transfer Objects as immutable Records instead of traditional classes. Records provide automatic equals(), hashCode(), toString(), and are inherently thread-safe. ALWAYS add @JsonProperty to ALL fields for JSON serialization. Example: `public record CustomerRequest(@JsonProperty("name") String name, @JsonProperty("email") String email, @JsonProperty("birthDate") LocalDate birthDate) {}`

2. **Pattern Matching with Switch Expressions**: Leverage enhanced switch expressions and pattern matching for cleaner, more readable code. Use sealed types with exhaustive switch for type-safe polymorphism. Example: `return switch(status) { case PENDING -> processPending(); case APPROVED -> processApproved(); default -> throw new IllegalStateException(); }`

3. **Virtual Threads for I/O Operations**: Enable virtual threads in Spring Boot to improve scalability for I/O-bound workloads without reactive programming complexity. Configure `spring.threads.virtual.enabled=true` in application.properties. Use for REST controllers, database access, external API calls. NEVER use synchronized blocks with virtual threads as it pins carrier threads

4. **Constructor Injection with Final Fields**: Always use constructor-based dependency injection with final fields for immutability. Enables better testability and prevents null pointer exceptions. Make all injected dependencies private final. NEVER use field injection (@Autowired on fields). Example: `public class OrderService { private final OrderRepository repository; public OrderService(OrderRepository repository) { this.repository = repository; } }`

5. **Text Blocks for Multi-line Strings**: Use text blocks (triple quotes) for SQL queries, JSON templates, or any multi-line string content. Improves readability and maintainability. Example: `String query = \"\"\"SELECT * FROM orders WHERE tenant_id = :tenantId AND status = :status\"\"\";`

6. **Sequenced Collections**: Use new SequencedCollection, SequencedSet, SequencedMap interfaces when order matters. Methods like getFirst(), getLast(), reversed() provide cleaner API than legacy workarounds. Available in Java 21 standard library

7. **Sealed Classes for Domain Modeling**: Use sealed classes to restrict inheritance hierarchy and enable exhaustive pattern matching. Example: `public sealed interface PaymentMethod permits CreditCard, DebitCard, BankTransfer {}`. Enhances type safety and makes all possible subtypes explicit

8. **MapStruct for DTO Mapping**: Use MapStruct for compile-time DTO-Entity mapping. Generates performant mapping code at compile time. NEVER write manual mapping boilerplate. Example: `@Mapper(componentModel = "spring") public interface CustomerMapper { CustomerResponse toResponse(Customer entity); Customer toEntity(CustomerRequest request); }`

9. **Immutability by Default**: Make fields final where possible. Prefer java.util.Optional over null returns (but don't store Optional fields). Use Records for pure data carriers. Initialize collection fields as empty lists, NEVER null. Return unmodifiableList() from API methods

10. **Generics Best Practices**: Never use raw types. Use bounded wildcards (? extends / ? super) to model covariance/contravariance. SuppressWarnings only around minimal scope with explanatory comment. Follow PECS principle (Producer Extends, Consumer Super)

11. **Exception Handling Best Practices**: Create custom exception hierarchy. Use @ControllerAdvice/@RestControllerAdvice for global exception handling. NEVER expose stack traces in API responses. Always include correlation/trace IDs in error responses. Throw checked exceptions only for recoverable conditions. Wrap/translate low-level exceptions (SQLException → OrderRepositoryException). Use try-with-resources for resource management

12. **Validation with Jakarta Bean Validation**: Use @Valid, @NotNull, @NotBlank, @Size, @Pattern annotations on DTOs. Create custom validators for complex business rules. Validate at controller layer before processing. Use @Validated for method-level validation

13. **Async Processing with @Async**: Use @Async annotation for non-blocking operations. Configure proper thread pool using @EnableAsync and TaskExecutor bean. Return CompletableFuture for async results. NEVER block on futures in virtual thread contexts

14. **Testing with JUnit 5**: Use JUnit 5 Jupiter API - @Test, @ParameterizedTest, @RepeatedTest. Use @ExtendWith(MockitoExtension.class) for unit tests. Use @SpringBootTest for integration tests. Enable parallel execution with junit.jupiter.execution.parallel.enabled=true. Use @WebMvcTest for controller slice tests. Use @DataJpaTest with Testcontainers for repository tests. NEVER use JUnit 4 or vintage engine

15. **Logging with SLF4J + Log4j2**: Use SLF4J façade with Log4j2 implementation (NEVER Logback). Exclude logback-classic from ALL dependencies. Use parameterized logging to avoid string concatenation. Log at appropriate levels (trace, debug, info, warn, error). Use MDC for structured logging. Use JsonTemplateLayout for JSON output. Enable async logging with LMAX Disruptor. Declare loggers as `private static final Logger log = LoggerFactory.getLogger(MyClass.class)` or use @Slf4j Lombok annotation

16. **Observability with Micrometer**: Use Micrometer for metrics, Spring Boot Actuator for health checks, and OpenTelemetry for distributed tracing. Expose /actuator/health, /actuator/metrics endpoints. Configure management.tracing.sampling.probability: 1.0 for full tracing. Protect actuator endpoints with authentication in production

17. **Spring Boot 4 Configuration**: Use profile-specific YAML files (application-dev.yml, application-qat.yml, application-prod.yml). Externalize all secrets via Azure Key Vault or environment variables using ${ENV_VAR:default} placeholders. NEVER hardcode credentials, URLs, or tenant IDs. Use @ConfigurationProperties for type-safe configuration

18. **JPA & Persistence Best Practices**: NEVER use @Data on @Entity classes - use @Getter/@Setter and manual equals()/hashCode() on @Id field. ALWAYS use FetchType.LAZY on relationships with explicit fetch joins. Use @Transactional(readOnly = true) on read methods. Use @Transactional on write methods. NEVER expose entities in REST responses - use DTOs. Use Spring Data JPA with specifications for complex queries

19. **Security Best Practices**: Use prepared statements/parameter binding to avoid SQL injection. Validate all external input with Bean Validation. Enable compiler warnings –Xlint:all. Use TLS 1.2+. Use Azure Managed Identity for authentication. Implement RBAC with @PreAuthorize. NEVER log passwords or tokens. Use char[] for passwords, not String

20. **Maven Build Configuration**: Use Maven Wrapper (mvnw) with pinned JAR. Parent POM: spring-boot-starter-parent 4.0.6. Use dependency management for version control. Configure compiler plugin with release=21. Use maven-enforcer-plugin to forbid dynamic versions and duplicate classes. Quality gates: SpotBugs, PMD, JaCoCo (90% threshold), OWASP Dependency-Check. NEVER skip tests in CI

21. **Code Quality Standards**: Follow 4-space indents (never tabs), 100-120 chars per line. Use PascalCase for classes/enums/interfaces, camelCase for methods/variables, ALL_CAPS for constants. Use reverse-DNS lowercase singular packages (com.foo.payment). NEVER leave dead code, TODOs, or commented functional code. Remove unused imports. Ensure files end with trailing newline

22. **Concurrency Best Practices**: Use java.util.concurrent higher-level constructs and CompletableFuture. Avoid synchronized on public objects. Use immutable message objects across threads. ThreadLocal MUST be removed with remove() to prevent leaks. Use virtual threads for I/O-bound workloads, traditional pools for CPU-bound

23. **Performance Optimization**: Measure before optimizing with JMH micro-benchmarks. Use StringBuilder for manual string loops (not + in loops). Cache expensive reflection or regex results. Prefer primitive collections (HPPC, fastutil) when profiling shows benefit. Buffer all I/O. Make Charset explicit (StandardCharsets.UTF_8)

24. **Documentation Standards**: Public APIs need Javadoc with examples. Keep README in project root with purpose, build, run, contribute sections. Document design decisions in ADRs. Use @Operation and @ApiResponse for OpenAPI documentation
## Pitfalls
- Do NOT use field injection (@Autowired on fields) - use constructor injection for better testability and immutability
- Avoid using traditional classes when Records are appropriate - Records are immutable and thread-safe by design
- Do NOT use old-style switch statements with fall-through cases - use switch expressions for clarity and type safety
- Never enable virtual threads without testing - while they improve I/O scalability, CPU-bound tasks may not benefit and could degrade performance
- Avoid mixing reactive (WebFlux) and non-reactive (Spring MVC) patterns - stick to one model consistently
- Do NOT use string concatenation for complex strings - use text blocks or string templates (preview) for readability
- Never catch Exception or Throwable broadly - catch specific exceptions and handle them appropriately
- Avoid using null - use Optional<T> for potentially absent values and validate inputs with Bean Validation
- Do NOT create mutable DTOs - use Records or classes with final fields only
- Never hard-code configuration values - use @ConfigurationProperties or @Value with externalized configuration
- Avoid synchronous blocking calls in virtual threads unnecessarily - virtual threads help with blocking I/O, but non-blocking alternatives may still be better for some scenarios
- Do NOT use preview features in production without careful consideration - they may change in future Java versions
- Never skip integration tests - unit tests alone are insufficient for Spring Boot applications with complex dependencies
- Avoid using reflection when pattern matching provides a cleaner solution
- Do NOT ignore compiler warnings about unchecked operations or deprecation - address them proactively

## Verification
1. Verify Java version is 21 LTS: run `java -version` and confirm output shows 'openjdk version "21"' or 'java version "21"'
2. Check Spring Boot version is 4.x: verify pom.xml or build.gradle contains spring-boot-starter-parent version 4.0.5 or higher
3. Confirm all DTOs are implemented as Records with proper immutability (no setters, all fields final)
4. Validate constructor injection is used throughout - search for @Autowired on fields (should find none in new code)
5. Check virtual threads are enabled: verify application.properties contains `spring.threads.virtual.enabled=true`
6. Confirm JUnit 5 is used: verify test dependencies include junit-jupiter (not junit 4), and tests use @Test from org.junit.jupiter.api
7. Validate MapStruct is configured: check pom.xml includes mapstruct dependency and annotation processor configuration
8. Check code coverage meets threshold: run `mvn clean test jacoco:report` and verify coverage is >= 90%
9. Confirm pattern matching is used instead of instanceof chains - code review for modern switch expressions
10. Validate Bean Validation is active: check DTOs have @Valid annotations and constraints like @NotNull, @NotBlank
11. Verify exception handling includes correlation/trace IDs and never exposes stack traces in responses
12. Check Actuator endpoints are exposed and secured: access /actuator/health to verify health check functionality
13. Confirm no preview features are used in production code unless explicitly enabled and documented
14. Validate thread pool configuration for @Async operations is properly sized for workload
15. Run static analysis: execute `mvn checkstyle:check` to ensure code style compliance