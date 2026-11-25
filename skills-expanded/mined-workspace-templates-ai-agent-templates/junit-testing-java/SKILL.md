---
name: junit-testing-java
description: Writes JUnit 5 tests with parameterized cases and Mockito used carefully, avoiding static mocking, over-stubbing and tests tied to implementation.
---

# JUnit 5 and Mockito testing

Test behavior through the public API. Mock only what is slow, external or nondeterministic.

## Steps

1. Use JUnit 5 (`org.junit.jupiter`). One class per unit under test, named `OrderServiceTest`, tests named for behavior: `rejectsOrderWithoutItems()`. Use `@Nested` to group by scenario and `@DisplayName` where the name needs prose.
2. Build objects with small test builders or factory methods. Prefer constructor injection so the test needs no reflection or Spring context. Use `@SpringBootTest` only for wiring tests, and slice annotations (`@DataJpaTest`, `@WebMvcTest`) for the rest.
3. Cover many cases with `@ParameterizedTest` and `@CsvSource`, `@MethodSource` or `@EnumSource`. Give cases names with `name = "{index}: {0}"`.
4. Assertions: AssertJ (`assertThat(result).isEqualTo(...)`) when available. Use `assertThrows` and check the message or type. Group related checks with `assertAll`.
5. Mockito: `@ExtendWith(MockitoExtension.class)` for strict stubs, `@Mock` for outside collaborators, `verify` only when the call is the outcome (sent email, published event). Use `ArgumentCaptor` to inspect arguments.
6. Replace time and randomness with an injected `Clock` or `Supplier`.

## Rules

- Never use `mockStatic` or `mockConstruct` to dodge a design problem; wrap the static call in an interface and inject it.
- Never mock value objects, collections or the class under test.
- No `Thread.sleep`; use Awaitility.
- Remove unnecessary stubbings that strict mode reports.

## Report

Tests added, any design change suggested to avoid static mocking, and the result of `mvn test` or `gradle test`.
