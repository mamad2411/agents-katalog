---
name: spring-boot-service-design
description: Structures a Spring Boot service into thin controllers, transactional services and typed config, tested with slice tests instead of full context starts.
---

# Spring Boot service design

Thin controllers, transactional services, typed config, sliced tests.

## Steps

1. Package by feature (`orders`, `billing`), not by layer. Inside each: `OrderController`, `OrderService`, `OrderRepository`, DTO records and the entity.
2. Controllers only translate HTTP: bind and validate (`@Valid`, Bean Validation annotations), call one service method, map to a response record. No repository calls, no business rules.
3. Services own the rules and the transaction boundary: `@Transactional` on the public method, `readOnly = true` for queries. Do not annotate controllers or repositories for transactions.
4. Never return JPA entities from controllers. Use Java records as request and response DTOs, mapped explicitly, so a column change never changes the API.
5. Use constructor injection only (one constructor needs no annotation). No field `@Autowired`.
6. Replace scattered `@Value` with `@ConfigurationProperties` on a record, with `@Validated` constraints, so a missing setting stops startup with a clear message.
7. Handle errors in one `@RestControllerAdvice` that maps domain exceptions to ProblemDetail responses.
8. Test by slice: `@WebMvcTest` with `MockMvc` and a mocked service for controllers; `@DataJpaTest` with Testcontainers for repositories; plain JUnit with mocks for services. Keep `@SpringBootTest` for a few end-to-end checks.
9. Guard against lazy loading traps: set `spring.jpa.open-in-view=false` and fetch what a use case needs with explicit queries or `@EntityGraph`.

## Rules

- Never put business logic in a controller or an entity setter chain.
- Never catch `Exception` in a service to hide it.

## Report

Structure created or changed, settings flipped, and tests added with their run time.
