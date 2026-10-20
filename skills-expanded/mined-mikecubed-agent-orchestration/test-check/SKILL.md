---
name: test-check
description: >
  Enforces test quality rules (TEST-1 through TEST-9, plus TEST-BEHAVIOR,
  TEST-NO-MOCK-FOR-PURE, TEST-VACUOUS). Loaded by the conductor for review
  and test operations. Detects weak assertions, insufficient coverage,
  missing property tests, slow unit tests, I/O in unit tests, missing
  boundary conditions, mock-pinned implementation tests, mocks of pure
  core functions, and tests with no meaningful assertion. Complements
  gate-check (which enforces that tests exist and went red→green) by
  enforcing the quality of tests that exist.
version: "1.0.0"
last-reviewed: "2026-03-04"
languages: [typescript, python, go, rust, javascript]
changelog: "../../CHANGELOG.md"
tools: Read, Grep, Glob, Bash
model: opus
permissionMode: default
---

# Test Check — Test Quality Enforcement

Precedence in the overall system: SEC → gate (TEST-PINNED, TEST-RED-FIRST) →
BOUND/PURE/RESULT/TYPED → COMP/IMMUT →
**TEST-1, TEST-2, TEST-6, TEST-BEHAVIOR, TEST-NO-MOCK-FOR-PURE (BLOCK)** →
TEST-VACUOUS, TEST-3..5, TEST-7..9 (WARN/INFO).

---

## Rules

### TEST-1 — No Weak Assertions
**Severity**: BLOCK | **Languages**: * | **Source**: CCC

**What it prohibits**: Assertions that pass without verifying meaningful
behaviour. Weak assertion patterns by language:

| Language | Prohibited | Preferred |
|----------|-----------|-----------|
| TypeScript/JavaScript | `toBeTruthy()`, `toBeFalsy()`, `toBeDefined()` without semantic reason | `toBe(exact)`, `toEqual(structure)`, `toStrictEqual(...)` |
| Python | `assert x` (bare assert), `assertTrue(x)` without message | `assertEqual(a, b)`, `assertRaises(ErrorType, fn)` |
| Go | `if result == nil { t.Fatal(...) }` replacing a table comparison | `if result != expected { t.Errorf("got %v, want %v", ...) }` |
| Rust | `assert!(result.is_some())` | `assert_eq!(result, Some(expected_value))` |

**Exemptions**:
- `toBeDefined()` / `assertIsNotNone()` when the contract is that a value exists
  but its exact type is a separate concern — only if a comment explains the intent
- Existence checks on optional fields returned by mutable external APIs

**Detection**:
1. Grep test files for `toBeTruthy()`, `toBeFalsy()`, `toBeDefined()` with no
   subsequent assertion on the same value
2. Grep Python test files for bare `assert x` (no `==` comparison) or
   `assertTrue(x)` / `assertFalse(x)` on non-boolean expressions
3. Grep Rust test files for `assert!(result.is_some())`, `assert!(result.is_ok())`
   where a `assert_eq!` with the inner value would be more informative

**agent_action**:
1. Cite: `TEST-1 (BLOCK): Weak assertion at {file}:{line}. '{assertion}' does not verify the expected value.`
2. Show the current assertion
3. Propose the specific, value-asserting replacement based on the actual value being tested
4. Example: `expect(result).toBeTruthy()` → `expect(result).toBe('expected-string')`
5. If `--fix`: replace assertion with the specific matcher (requires knowing the expected value from context)
6. If expected value is ambiguous: cite TEST-1 and ask user to specify the expected value before fixing

**Bypass prohibition**: "It's just a smoke test", "I only need to check it doesn't throw"
→ If the behaviour has no verifiable output, the test is incomplete. Add a meaningful
assertion or document as a pending test with a TEST-1 waiver and issue reference.

---

### TEST-2 — Domain Layer Coverage ≥ 90%
**Severity**: BLOCK | **Languages**: * | **Source**: CCC

**What it prohibits**: A domain layer (pure business logic, entities, value
objects, use cases) with line or branch coverage below 90%. Domain code is the
heart of the application and has no infrastructure dependencies — there is no
excuse for low coverage here.

**Domain layer heuristics** (file path patterns):
- `src/domain/`, `domain/`, `core/`, `entities/`, `models/`, `use-cases/`
- Files with zero external I/O imports (no DB, HTTP, file system)

**Detection**:
1. Check if a coverage report exists (e.g., `coverage/lcov.info`, `.coverage`,
   `coverage.out`, `tarpaulin-report.json`)
2. Parse the report for files matching domain path patterns
3. Flag any file below 90% line coverage

**agent_action**:
1. Cite: `TEST-2 (BLOCK): Domain file '{file}' has {pct}% coverage (minimum: 90%).`
2. List uncovered lines/branches from the coverage report
3. Propose: "Write tests for the uncovered paths: {specific_lines}"
4. If no coverage report exists: `TEST-2 (BLOCK): No coverage report found. Run coverage and ensure domain layer reaches 90% before review completes.`
5. Do NOT generate placeholder tests; require meaningful assertions (TEST-1)

---

### TEST-3 — Application Layer Coverage ≥ 80%
**Severity**: WARN | **Languages**: * | **Source**: CCC

**What it prohibits**: Application-layer code (controllers, services, handlers,
repositories) with line or branch coverage below 80%.

**Application layer heuristics** (file path patterns):
- `src/application/`, `services/`, `controllers/`, `handlers/`, `repositories/`
- Files that import both domain types AND infrastructure adapters

**Detection**: Same as TEST-2, applied to application-layer file patterns.

**agent_action**:
1. Cite: `TEST-3 (WARN): Application file '{file}' has {pct}% coverage (target: 80%).`
2. List the highest-impact uncovered paths
3. Propose: "Add integration tests for: {specific_paths}"
4. If `--fix`: generate test stubs (not implementations) referencing the uncovered paths

---

### TEST-4 — Property Tests Required for Entities
**Severity**: WARN | **Languages**: * | **Source**: CCC

**What it prohibits**: Entity or value object types that lack at least one
property-based test verifying their invariants. Example-based tests cannot
exhaustively verify structural invariants — property tests can.

**Applicable to**:
- Entities with validation rules (e.g., `Email`, `Money`, `OrderId`)
- Value objects with mathematical invariants (e.g., commutative addition)
- Serialisation/deserialisation round-trips

**Language tooling**:
- TypeScript/JavaScript: `fast-check`
- Python: `hypothesis`
- Go: `testing/quick` or `rapid`
- Rust: `proptest` or `quickcheck`

**Detection**:
1. Identify entity/value object files (domain layer patterns)
2. Search their test files for property-test function patterns:
   - `fc.property(`, `@given(`, `proptest!`, `quickcheck!`, `rapid.Check(`
3. Flag entities with no property test coverage

**agent_action**:
1. Cite: `TEST-4 (WARN): Entity '{name}' at {file} has no property tests. Invariants are not exhaustively verified.`
2. Identify the key invariants from the entity's validation rules
3. Propose: "Add a property test verifying: {invariant_description}"
4. Show a starter property test scaffold in the detected language

---

### TEST-5 — Unit Tests Must Run Under 100ms Each
**Severity**: WARN | **Languages**: * | **Source**: CCC

**What it prohibits**: Individual unit tests that take longer than 100ms to
execute. Slow unit tests signal hidden I/O, uncontrolled concurrency, or
unnecessary real-time waits. Slow tests are skipped under deadline pressure.

**Note**: This rule applies to **unit tests only** — integration and end-to-end
tests are exempt.

**Unit test heuristics**: Tests that do not spin up servers, connect to databases,
or invoke file system operations. File naming: `*.test.ts`, `*.unit.test.*`,
`test_*.py` (no `@pytest.mark.integration`).

**Detection**:
1. Check if a test timing report is available from the last test run
2. Flag tests exceeding 100ms
3. If no timing data: look for `sleep()`, `time.sleep()`, `asyncio.sleep()`,
   `setTimeout()` inside unit test bodies — these are indicators

**agent_action**:
1. Cite: `TEST-5 (WARN): Unit test '{name}' at {file}:{line} ran in {ms}ms (limit: 100ms).`
2. Identify the cause: sleep, real I/O, large data setup, or CPU-heavy computation
3. Propose: mock the slow dependency or extract the slow path to an integration test
4. If `--fix` and cause is a `sleep(N)`: remove the sleep and use an event-driven assertion

---

### TEST-6 — No I/O in Unit Tests
**Severity**: BLOCK | **Languages**: * | **Source**: CCC

**What it prohibits**: Unit tests that perform real I/O operations:
- File system reads/writes (not mocked)
- Real network requests (HTTP, gRPC, TCP)
- Real database queries (not using an in-memory or test double)
- Environment variable reads that differ between CI and local

**Exemptions**:
- Integration tests (marked with `@pytest.mark.integration`, `//go:build integration`, etc.)
- Tests in `tests/integration/` or `__tests__/integration/` directories

**Detection**:
1. In unit test files, grep for:
   - `fs.readFile`, `fs.writeFile`, `open(`, `os.path`, `pathlib.Path` (outside mocking context)
   - `fetch(`, `axios.`, `httpx.`, `http.Get(`, `reqwest::` (outside mocking context)
   - Real DB connection strings (`postgres://`, `mysql://`, `mongodb://`)
2. Look for absence of mock/spy declarations where I/O calls are used

**agent_action**:
1. Cite: `TEST-6 (BLOCK): Unit test '{test_name}' at {file}:{line} performs real I/O: '{call}'.`
2. Identify: what is being called and what it produces
3. Propose: replace with a mock, fake, or stub using the language's test double facilities
4. Example: `jest.mock('../db/connection')` / `unittest.mock.patch` / `httptest.NewServer`
5. If `--fix`: add the mock wrapper — but DO NOT guess the return value without context

---

### TEST-7 — Boundary Conditions Must Be Tested
**Severity**: WARN | **Languages**: * | **Source**: CCC

**What it prohibits**: Functions with numeric, string, or collection inputs that
lack test cases for boundary values. Boundary conditions are the most common
source of off-by-one errors and null pointer exceptions.

**Required boundary cases** (if the function accepts the type):
| Input type | Required boundary cases |
|-----------|------------------------|
| Integer / float | 0, negative, max int, min int, overflow |
| String | empty string `""`, single character, max-length, unicode |
| List / array | empty list, single element, maximum size |
| Optional / nullable | null / None / nil / Option::None |
| Date / time | epoch, end-of-month, leap day, timezone boundary |

**Detection**:
1. Identify public functions in domain/application layers
2. For each function, check its test file for at least one test using a boundary value
3. Flag functions with only "happy path" tests

**agent_action**:
1. Cite: `TEST-7 (WARN): Function '{name}' at {file}:{line} lacks boundary condition tests.`
2. List the missing boundaries based on the parameter types
3. Propose test cases: "Add tests for: empty list, null input, zero value"
4. If `--fix`: generate the test stubs with the boundary values filled in

---

### TEST-8 — Test-to-Implementation Ratio Monitoring
**Severity**: INFO | **Languages**: * | **Source**: CCC

**What it monitors**: The ratio of test lines to implementation lines. A ratio
below 1:1 does not automatically trigger a violation but indicates the test suite
is likely underpowered relative to the code it covers.

**Target**: ≥ 1:1 (test lines : implementation lines)
**Report threshold**: < 1:1 triggers INFO; no auto-fix; no BLOCK.

**Detection**:
1. Count lines in test files vs non-test source files within the scope
2. Report the ratio

**agent_action**:
1. Report: `TEST-8 (INFO): Test-to-implementation ratio is {ratio}:1 (target: ≥ 1:1).`
2. If ratio is healthy: no action required
3. If ratio < 0.5:1: "Consider adding tests for the most complex or highest-risk modules first."
4. Never block on this metric alone; combine with TEST-2 and TEST-3 coverage data

---

Report schema: see `skills/conductor/shared-contracts.md`.

---

### TEST-9 — Mutation Score (INFO/WARN)

**Severity**: INFO when score is 60–79%; WARN when score is < 60%  
**Applies to**: `test` and `review` operations only (NOT `write` or `refactor` — too expensive)

**What it checks**: Whether the test suite can detect incorrect implementations. A mutation testing
tool introduces small code changes (e.g., flipping `>` to `>=`, removing a return statement) and
checks if at least one test fails. High mutation survival means tests are passing on wrong
implementations.

**Tool detection order** (stop at first available):
1. Stryker: `npx stryker --version 2>/dev/null` (TypeScript/JavaScript)
2. mutmut: `python3 -m mutmut --version 2>/dev/null` (Python)
3. cargo-mutants: `cargo mutants --version 2>/dev/null` (Rust)
4. go-mutesting: `go-mutesting --version 2>/dev/null` (Go)

**If no tool available**: emit INFO: "Install {tool} for mutation score reporting (TEST-9)" and skip.

**When tool is available**: Run with `--timeout 120` (time-boxed at 120 seconds; partial results acceptable).

**Score thresholds**:

| Score | Severity | Message |
|-------|----------|---------|
| ≥ 80% | Pass | No finding |
| 60–79% | INFO | "Mutation score {X}% for {layer}: consider strengthening assertions" |
| < 60% | WARN | "Mutation score {X}% for {layer}: tests pass on wrong implementations — see surviving mutants" |
| Not available | INFO | "Install {tool} for mutation score reporting (TEST-9)" |

**Parse output**:
- Stryker: extract `"Mutation score: XX.XX%"` from stdout
- mutmut: compute `caught / (caught + survived) * 100` from `"X out of Y mutants survived"`
- cargo-mutants: compute `caught / (caught + missed) * 100` from `"X caught, Y missed"`
- go-mutesting: extract `"The mutation score is X.XX"` from stdout

---

### TEST-BEHAVIOR — Tests Assert Outputs, Not Internal Call Sequences
**Severity**: BLOCK | **Languages**: * | **Source**: CCC

**What it prohibits**: Test assertions on internal call sequences, mock call
counts, private fields, or internal state. Tests that observe *how* the
implementation works (rather than *what* it produces) break on every refactor
and signal that the test is pinning the implementation, not the behavior.

**Detection signals**:
- `toHaveBeenCalledTimes(`, `toHaveBeenCalledWith(`, `expect(mock.calls)` (Jest/Vitest)
- `assert_called_with`, `assert_called_once`, `mock.call_args_list` (Python `unittest.mock`)
- `verify(`, `times(`, `inOrder` (Mockito-style)
- Access patterns: `obj._private`, `obj.__private`, reflection used to read private state
- `should have called X N times` in assertion descriptions

**Allowed cases**:
- Asserting on a return value, a typed domain event, or an observable side
  effect (e.g., a row was written to an in-memory adapter)
- Verifying that an *expected* side effect happened via the adapter's public
  surface (count the resulting rows, not the mock calls)
- Mock call assertions when the test is genuinely about a protocol (e.g., the
  adapter must call `bus.publish(event)` exactly once on success) — but
  prefer asserting the resulting state where possible

**agent_action**:
1. Cite: `TEST-BEHAVIOR (BLOCK): Test asserts on internal call sequence or private state at {file}:{line}.`
2. Show the offending assertion.
3. Propose the equivalent assertion on the return value, public field, or
   typed event.
4. If the test is genuinely about a protocol, narrow the assertion to the
   minimal observable contract.

---

### TEST-NO-MOCK-FOR-PURE — Tests of Core Functions Must Not Import Mocking Libraries
**Severity**: BLOCK | **Languages**: * | **Source**: CCC

**What it prohibits**: A test file that exercises a function or type located in
`core/` (per the conductor's Section 14 layer detection) importing a mocking
library. Pure functions need only inputs and outputs — if a test needs to mock
something to exercise a core function, the function is not pure and belongs in
`shell/` (or its dependencies belong in `shell/`).

**Detection**:
1. Resolve the layer of the file under test (per conductor's Section 14).
2. If the file is in `core/`: grep its test file for imports of:
   - JS/TS: `jest`, `vi.mock`, `sinon`, `testdouble`
   - Python: `unittest.mock`, `pytest-mock`, `mock`
   - Go: `gomock`, `testify/mock`
   - Rust: `mockall`, `mockito`
3. Flag any such import.

**agent_action**:
1. Cite: `TEST-NO-MOCK-FOR-PURE (BLOCK): Test of core function '{name}' imports '{lib}' at {file}:{line}.`
2. Diagnose: if a mock is needed, the dependency is impure — it belongs in
   shell, and the function under test should accept its outputs as parameters.
3. Propose: extract the impure dependency to shell; pass its result into the
   pure core function as a parameter; test the pure core function directly
   with literal inputs.

**Bypass prohibition**: "I'm just mocking the clock / RNG / config" → That
function is not pure. Pass the time / seed / config value in as a parameter
instead.

---

### TEST-VACUOUS — Tests Must Have Meaningful Assertions
**Severity**: WARN (default) / BLOCK (with `--deep`) | **Languages**: * | **Source**: CCC

**What it prohibits**: Tests with no assertion, or only truthy/existence
checks that pass on virtually any non-null implementation:
- `expect(result).toBeDefined()` / `assertIsNotNone(result)` as the *only*
  assertion
- `assert result` (Python) without a comparison
- `assert!(result.is_some())` (Rust) without `assert_eq!` on the inner value
- A test function body that calls the function but asserts nothing

**Detection**:
1. Grep test files for test functions whose body contains exactly one
   assertion of the weak forms above.
2. Grep for test functions whose body contains zero assertion calls.
3. Cross-reference with TEST-1 (which BLOCKs weak assertions categorically);
   TEST-VACUOUS adds the "no assertion at all" and "only weak" classes.

**Allowed cases**:
- A type-existence smoke test, *if* a follow-up test in the same file asserts
  on the value (the smoke test is documentation, not the only test).
- Tests explicitly marked as pending or skipped (with `it.skip`, `@pytest.mark.skip`,
  `#[ignore]`) — these don't run.

**agent_action**:
1. Cite: `TEST-VACUOUS (WARN): Test '{name}' at {file}:{line} has no meaningful assertion.`
2. Propose a specific assertion using the value the function actually returns.
3. With `--deep`: upgrade to BLOCK.

This rule pairs with the gate-check's TEST-RED-FIRST: a vacuous test cannot
go red→green, so a red→green confirmation also confirms the test is not
vacuous. TEST-VACUOUS is the static-analysis backstop for sessions where the
red→green record is unavailable.
