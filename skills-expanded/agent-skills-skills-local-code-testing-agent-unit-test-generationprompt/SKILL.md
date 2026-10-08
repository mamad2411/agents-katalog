---
description: >-
  Guidelines for concise tests of relevant production behavior across
  programming languages, following existing project conventions
---

# Unit Test Generation Prompt

Write concise tests that protect relevant production behavior. Read the implementation and its callers, identify meaningful regressions and plausible failures, and use the smallest useful set of checks. There is no default coverage percentage or test-count goal. Follow explicitly requested targets and applicable required checks without padding the suite with low-value cases.

## Discover and Follow Conventions

Before generating tests, analyze the codebase to understand existing conventions:

- **Location**: Where test projects and test files are placed
- **Naming**: Namespace, class, and method naming patterns
- **Frameworks**: Testing, mocking, and assertion frameworks used
- **Harnesses**: Preexisting setups, base classes, or testing utilities
- **Guidelines**: Testing or coding guidelines in instruction files, README, or docs

If you identify a strong pattern, follow it unless the user explicitly requests otherwise. If no pattern exists and there's no user guidance, use your best judgment.

## Test Generation Requirements

Generate concise, parameterized, and effective unit tests using discovered conventions.

- **Exercise real production code** and assert its outputs, state changes, or required interactions; do not substitute the behavior under test with mocks or copied implementations
- **Choose useful isolation**: mock external dependencies where helpful; use a local integration check when the risk lies at that boundary. Real behavior does not mean live production services
- **Justify cases from the actual flow**: supported inputs, domain rules, observed regressions, reachable boundaries, and plausible dependency failures. Do not invent unreachable states merely to execute a branch
- **Stop at the scoped risks** once relevant checks pass. Broaden only for an explicit goal, applicable requirement, or new evidence of a meaningful gap; do not generate infrastructure solely for coverage metrics

### Key Testing Goals

| Goal                          | Description                                                                                          |
| ----------------------------- | ---------------------------------------------------------------------------------------------------- |
| **Minimal but Comprehensive** | Avoid redundant tests                                                                                |
| **Logical Coverage**          | Focus on meaningful edge cases, domain-specific inputs, boundary values, and bug-revealing scenarios |
| **Core Logic Focus**          | Test positive cases and actual execution logic; avoid low-value tests for language features          |
| **Risk-Based Selection**      | Choose happy paths, errors, and rare reachable boundaries by consequence and relevance, not a quota |
| **Best Practices**            | Use Arrange-Act-Assert pattern and proper naming (`Method_Condition_ExpectedResult`)                 |
| **Buildable & Complete**      | Tests must compile, run, and contain no hallucinated or missed logic                                 |

## Quality over Quantity

When the task specifies particular test scenarios or behaviors to cover:

1. **Cover stated behavior** — use focused checks for the requested, testable requirements; one test may cover several related requirements
2. **Test the actual implementation against its contract** — read the source and callers, and assert intended return values, side effects, or errors rather than copying implementation details into expectations
3. **Prefer fewer focused tests** — skip trivial boilerplate, tests of the language/framework, and mocks asserting their own setup. Small unit tests remain useful when they protect meaningful behavior
4. **Run the relevant tests** — investigate failures against the contract. Fix faulty tests; report or repair production defects within authorized scope, never rewrite a valid expectation just to obtain a pass

## Parameterization

- Prefer parameterized tests (e.g., `[DataRow]`, `[Theory]`, `@pytest.mark.parametrize`) over multiple similar methods
- Combine logically related test cases into a single parameterized method
- Keep separate tests when they explain distinct behavior more clearly; parameterization is a convenience, not a goal

## Analysis Before Generation

Before writing tests:

1. **Trace** the relevant production paths, callers, and existing tests
2. **Establish** expected behavior from the intended contract, actual inputs, and domain rules
3. **Select** regressions and plausible failure modes that a test could catch, including trust-boundary validation and reachable rare cases where consequential
4. **Choose** the smallest useful check and dependency isolation; reuse the existing harness

Do not require exhaustive parameter documentation or a test for every public method. Investigate concurrency, timing, and resource failures when the actual flow makes them relevant.

## Coverage Types

Select relevant cases; do not automatically generate each category for every method.

| Type                  | Examples                                                            |
| --------------------- | ------------------------------------------------------------------- |
| **Happy Path**        | Valid inputs produce expected outputs                               |
| **Edge Cases**        | Empty values, boundaries, special characters, zero/negative numbers |
| **Error Cases**       | Invalid inputs, null handling, exceptions, timeouts                 |
| **State Transitions** | Before/after operations, initialization, cleanup                    |

## Output Requirements

- Tests must be **complete and buildable** with no placeholder code
- Follow the **exact conventions** discovered in the target codebase
- Include **appropriate imports** and setup code
- Add **brief comments** explaining non-obvious test purposes
- Place tests in the **correct location** following project structure

## Build and Verification

- **Scoped builds during development**: Build the specific test project during implementation for faster iteration
- **Relevant verification**: Run the affected tests and applicable required checks. Broaden to a workspace build or wider suite only for affected integrations, failures, or unresolved risks
- **API signature verification**: Before calling any method in test code, verify the exact parameter types, count, and order by reading the source code
- **Project reference validation**: Before writing test code, verify the test project references all source projects the tests will use. Call the `code-testing-extensions` skill and read the language-specific extension file for guidance (e.g., `dotnet.md` for .NET)

## Test Scope Guidelines

- Prefer deterministic unit tests for local logic; use a focused integration check where the relevant risk requires the real dependency boundary
- Avoid live endpoints, credentials, fixed ports, and precise wall-clock timing unless the authorized task needs them. Temporary files or local services can be appropriate when they exercise relevant behavior
- Mock external dependencies only where useful; keep the real production path under test
- Report what executed and what remains unproven. Passing isolated tests do not establish live runtime or deployment behavior
