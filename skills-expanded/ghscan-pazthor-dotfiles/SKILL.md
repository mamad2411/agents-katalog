# Review the selected Laravel code as a senior software architect

First identify:

1. The responsibility of the code.
2. Business invariants it must protect.
3. Inputs, outputs and side effects.
4. Dependencies and infrastructure concerns.
5. Transaction boundaries.
6. State transitions.
7. Concurrency, idempotency and failure risks.
8. Testing difficulty and cognitive load.

Do not recommend a design pattern merely because one could be used.

First propose the simplest refactor that improves correctness, clarity and
testability.

Only recommend a named pattern when the code has a concrete recurring problem
that the pattern solves.

Evaluate whether any of these are justified:

- Extract Method
- Application Service or Action
- Value Object
- DTO
- Domain Service
- Strategy
- State pattern
- Specification
- Repository abstraction
- Aggregate root
- Domain event
- Factory

For every recommendation:

- explain the specific problem it solves;
- explain why a simpler refactor is insufficient;
- describe the tradeoffs;
- explain which alternatives were rejected;
- preserve existing behavior;
- avoid speculative abstractions;
- do not modify code until the analysis is approved.

Treat Singleton as a lifecycle decision, not a default design improvement.
