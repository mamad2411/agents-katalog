---
name: atdd
description: "ATDD + TDD reference for AI coding agents. Acceptance Test-Driven Development: convert Acceptance Criteria into tests, then implement via Red-Green-Refactor. Two-stream testing (acceptance + unit), anti-pattern guards, dependency-aware test selection, mutation testing verification. Use when implementing any Story with Acceptance Criteria. Use when Dev agent needs to write tests first. Not for manual testing or QA — those are behavioral, not code-level."
---

# ATDD — Acceptance Test-Driven Development for AI Agents

## When to use

- Dev agent implementing a Story with Acceptance Criteria
- Any task where code changes need test coverage
- Setting up test infrastructure in a new project
- Reviewing whether tests actually verify requirements (not just implementation)

## When NOT to use

- QA acceptance testing (behavioral, browser-based — use webapp-testing)
- Code review (use code-review-expert)
- Performance/security testing (use performance-audit / security-pentest)

---

## Core Philosophy

> "AI agents do not need to be told HOW to do TDD; they need to be told WHICH tests to check."
> — TDAD (arxiv 2603.17973, 2026)

> "Without acceptance tests anchoring behavior, AI can willy-nilly plop code around and write unit tests that pass but don't verify the right thing."
> — Uncle Bob / swingerman/atdd

Tests are **executable specifications**, not afterthoughts. They define WHAT the code must do BEFORE the code exists. Two independent streams of tests verify two independent concerns:

| Stream | Source | Verifies | Granularity |
|---|---|---|---|
| **Acceptance tests** | Acceptance Criteria (AC) | Business behavior — does it do what the user needs? | End-to-end per AC checkbox |
| **Unit tests** | Implementation design | Internal correctness — does each function work? | Per function/method |

Both streams must pass. Neither alone is sufficient.

---

## Double Loop Architecture

ATDD operates as two nested TDD loops:

```
OUTER LOOP (acceptance — hours/days):
  Write acceptance test from AC → RED
    INNER LOOP (unit — minutes):
      Write unit test → RED
      Implement → GREEN
      Refactor → GREEN
      (repeat for each function/method)
  Acceptance test → GREEN
  (repeat for each AC checkbox)
```

The outer loop stays RED for much longer — you write ONE acceptance test, then cycle through multiple inner unit-test loops to build up the implementation piece by piece until the acceptance test turns GREEN.

**Key insight**: the outer loop (acceptance test) defines WHAT the system must do. The inner loop (unit tests) defines HOW each piece works. Both are needed — acceptance alone is too coarse, unit alone misses business requirements.

---

## Uncle Bob's Three Laws of TDD

The nano-cycle — follow these on a second-by-second basis:

1. **You must not write production code unless it makes a failing test pass.**
2. **You must not write more of a test than is sufficient to fail** (including compile/parse failure).
3. **You must not write more production code than is sufficient to make the currently failing test pass.**

These laws force tiny, incremental steps. You write ONE assert, see it fail, write ONE line of implementation, see it pass. Then next assert.

---

## FIRST Principles for Tests

Every test you write must satisfy all five:

| Principle | Meaning | Why it matters |
|---|---|---|
| **Fast** | Executes in milliseconds | Slow tests don't get run. Slow = skipped = untested. |
| **Isolated** | No test depends on another | Tests can run in any order, in parallel |
| **Repeatable** | Same result every time, any environment | No flaky tests. No "works on my machine." |
| **Self-validating** | Pass/fail without human inspection | No manual log reading. Assert or fail. |
| **Timely** | Written immediately BEFORE the code | The T in TDD. Not after. Not "later." Now. |

---

## Test Pyramid

```
         /  E2E / Acceptance  \     ~10%  — slow, broad, fragile
        /   Integration tests  \    ~20%  — medium speed, service boundaries
       /     Unit tests         \   ~70%  — fast, isolated, abundant
      /__________________________\
```

| Level | What it tests | Speed | Count | When to write |
|---|---|---|---|---|
| **Unit** | Single function/method in isolation | ms | Many (70%) | Inner TDD loop |
| **Integration** | Two+ components together, API calls, DB queries | 100ms-1s | Some (20%) | When testing boundaries |
| **Acceptance/E2E** | Full user flow, AC checkbox | 1s-10s | Few (10%) | Outer ATDD loop |

**For AI agents**: write unit tests for speed (inner loop), acceptance tests for correctness (outer loop). Skip E2E browser tests — those are QA's job (separate agent).

---

## Test Doubles (when to use each)

| Double | What it does | When to use | When NOT to use |
|---|---|---|---|
| **Dummy** | Fills a parameter slot, never called | Satisfying a required parameter you don't care about | When the parameter affects behavior |
| **Stub** | Returns canned values | Controlling return values for testing specific paths | When you need to verify calls were made |
| **Spy** | Records calls for later inspection | Verifying a method was called with specific args | When you can test via return value instead |
| **Mock** | Pre-programmed expectations, fails if violated | Verifying interaction patterns (event emitted, API called) | When state verification is simpler |
| **Fake** | Working simplified implementation (in-memory DB) | Integration tests needing a fast substitute | In production code |

**Golden rule**: mock EXTERNAL dependencies (HTTP, DB, filesystem, clock). NEVER mock the subject under test. Prefer fakes over mocks (Google's recommendation) — fakes behave like the real thing, mocks verify interactions.

```python
# GOOD — fake external dependency
def test_send_notification(fake_email_service):
    send_welcome(user, email_service=fake_email_service)
    assert fake_email_service.last_sent_to == user.email

# BAD — mocking the thing you're testing
@mock.patch("mymodule.send_welcome")
def test_send_welcome(mock_fn):
    mock_fn.return_value = True
    assert send_welcome(user) == True  # tests the mock, not the code
```

---

## Test Naming and Structure

### Naming convention

Use descriptive names that read as a sentence:

```python
# Pattern: test_{action}_{scenario}_{expected_result}
def test_greet_with_valid_name_returns_greeting():
def test_greet_with_empty_name_raises_value_error():
def test_auth_with_expired_token_returns_401():
```

Or BDD-style (preferred for acceptance tests):

```python
# Pattern: test_{given}_{when}_{then}
def test_given_registered_user_when_login_then_session_created():
def test_given_expired_token_when_refresh_then_new_token_issued():
```

### Structure: Arrange-Act-Assert (= Given-When-Then)

Every test has exactly three sections:

```python
def test_checkout_applies_discount():
    # ARRANGE (Given) — set up preconditions
    cart = Cart(items=[Item("book", price=100)])
    code = DiscountCode("SAVE10", percent=10)

    # ACT (When) — perform the action
    cart.apply_discount(code)

    # ASSERT (Then) — verify the outcome
    assert cart.total == 90
```

**One assert per test** (ideally). Multiple asserts = multiple behaviors = split into multiple tests.

---

## Test Data Patterns

### Factory functions (simplest)

```python
def make_user(**overrides):
    defaults = {"name": "Test User", "email": "test@example.com", "active": True}
    return User(**{**defaults, **overrides})

# Usage: only specify what matters for THIS test
user = make_user(active=False)
```

### Builder pattern (for complex objects)

```python
user = UserBuilder().with_name("Alice").with_role("admin").inactive().build()
```

### Why this matters for AI agents

AI tends to hardcode test data ("magic values"). Use factories instead — they make tests readable (only show what's relevant) and maintainable (change defaults in one place).

---

## Kent Beck's Test Desiderata (12 properties of good tests)

Not all tests need all properties, but trading one away should give a more valuable property in return:

| Property | Meaning |
|---|---|
| **Isolated** | Same result regardless of execution order |
| **Composable** | Run 1 or 1,000,000 — same results |
| **Fast** | Milliseconds, not seconds |
| **Inspiring** | Passing tests give confidence to ship |
| **Writable** | Easy to write (low friction → more tests) |
| **Readable** | Easy to understand what is being tested |
| **Behavioral** | Tests behavior, not implementation |
| **Structure-insensitive** | Survives refactoring |
| **Automated** | No human judgment needed to evaluate |
| **Specific** | Failure pinpoints the exact problem |
| **Deterministic** | Same inputs → same pass/fail every time |
| **Predictive** | Passing tests = code works in production |

**For AI agents**: prioritize **Behavioral**, **Structure-insensitive**, and **Specific**. AI-generated tests often fail on these three — they test implementation (not behavioral), break on refactor (not structure-insensitive), and assert too broadly (not specific).

---

## Implementation Strategies (GREEN phase)

Three strategies for making a failing test pass. Shift between them as confidence changes:

| Strategy | What | When |
|---|---|---|
| **Obvious Implementation** | Type the real solution directly | You know exactly what to write |
| **Fake It ('til you make it)** | Return a hardcoded constant, refactor later | You know the answer but not the path |
| **Triangulation** | Add a second example to force generalization | Exploring unknown territory |

### Flow

```
Start with Obvious Implementation
  → unexpected RED? → switch to Fake It
    → need to generalize? → add another test (Triangulation)
      → pattern emerges → refactor to real implementation
        → confidence returns → back to Obvious Implementation
```

**For AI agents**: AI defaults to Obvious Implementation always. This is fine for simple tasks. For complex algorithms, force Triangulation: write TWO test cases with different values before implementing. This prevents the AI from hardcoding the first test's expected value.

---

## Transformation Priority Premise (TPP)

Uncle Bob's ordering for growing implementation complexity during GREEN phase:

```
{} → nil                  (no code → return nothing)
nil → constant             (return a literal value)
constant → constant+       (return a more complex constant)
constant → scalar          (replace constant with a variable)
statement → statements     (add another line)
unconditional → if         (add a condition)
scalar → collection        (use a list/array)
statement → recursion      (self-referencing)
if → while                 (loop)
collection → stream/map    (higher-order iteration)
expression → function      (extract behavior)
variable → assignment      (mutate state)
```

**Rule**: prefer transformations higher in the list. When a test requires a `while` but you can solve it with an `if` → use `if`. The simpler transformation is always preferred.

**For AI agents**: AI tends to jump straight to the most general solution (loops, recursion). TPP forces incremental growth: first hardcode, then if, then loop. Each step is testable. Each step is verified. Less chance of over-engineering.

---

## Test List Technique

Before touching any code, write a list of all test cases you plan to implement:

```markdown
## Test List for: greet(name, style) → str

Happy paths:
- [ ] casual style returns "Hey {name}!"
- [ ] formal style returns "Good day, {name}."
- [ ] pirate style returns "Ahoy, {name}!"

Edge cases:
- [ ] empty name → ValueError
- [ ] None name → ValueError
- [ ] very long name (1000 chars) → works without truncation
- [ ] name with special characters (emoji, unicode) → works

Error paths:
- [ ] unknown style → ValueError with clear message
- [ ] None style → uses default (casual)
- [ ] empty string style → ValueError

Integration:
- [ ] CLI: --name World → prints greeting to stdout
- [ ] CLI: missing --name → exit code 1 + usage
- [ ] CLI: --style bad → exit code 1 + error message
```

### Why this matters

1. **Problem partitioning** — break the task into small, testable chunks
2. **Coverage planning** — see gaps before writing code
3. **Priority ordering** — start with happy path, then edges, then errors
4. **Living document** — add tests discovered during implementation

**For AI agents**: give Dev the test list in the task description (extracted from AC). Dev checks items off as implemented. This is more effective than "write tests for this function" — it tells the agent WHICH tests to write.

---

## Systematic Edge Case Selection

### Equivalence Partitioning

Group inputs into classes where values behave the same. Test ONE value per class:

```
Input: age (integer, valid range 0-150)
Classes:
  Invalid negative: -1  (representative)
  Valid low boundary: 0  (representative)
  Valid typical: 25      (representative)
  Valid high boundary: 150 (representative)
  Invalid high: 151     (representative)
```

### Boundary Value Analysis

Errors cluster at boundaries. Test: exactly AT, just BELOW, and just ABOVE each boundary:

```
Range [1, 100]:
  Test: 0 (below), 1 (at lower), 2 (above lower)
  Test: 99 (below upper), 100 (at upper), 101 (above upper)
```

### Happy + Unhappy Path Coverage

Every test suite needs BOTH:

| Path type | What it tests | Example |
|---|---|---|
| **Happy path** | Normal expected flow | Valid login → session created |
| **Unhappy path** | Error/exception flow | Wrong password → 401 + error message |
| **Edge case** | Boundary conditions | Password exactly at max length |
| **Destructive** | Malicious/unexpected input | SQL injection in email field |

**For AI agents**: AI defaults to happy-path-only testing. Explicitly require: "for each AC checkbox, write one happy test AND at least one unhappy test."

---

## Characterization Tests (for legacy code)

When working on existing code without tests (common when `/bx:run` picks up a project):

1. **Don't try to understand the code first** — capture its current behavior
2. **Write tests that assert what the code CURRENTLY does** (even if buggy)
3. **These tests protect against unintended changes during refactoring**
4. **Only AFTER characterization tests are green → refactor safely**

```python
# Step 1: Capture current behavior (even if "wrong")
def test_legacy_calculate_tax():
    # We don't know if 0.08 is correct, but that's what the code returns today
    assert calculate_tax(100) == 8.0

# Step 2: Now safe to refactor calculate_tax() — test catches regressions
# Step 3: If 8.0 is wrong, write a NEW test with correct value, see it RED, fix
```

**For AI agents**: when the Story modifies existing untested code, Dev should FIRST write characterization tests (capture current behavior), THEN make changes (TDD on the new behavior). This prevents "fix one thing, break three others."

---

## The ATDD Cycle (step by step)

### Phase 0: UNDERSTAND

Before writing any code or test:

1. **Read the Acceptance Criteria** — every `- [ ]` checkbox is a contract
2. **Read the Story description** — understand WHY, not just WHAT
3. **Identify the scope** — which files will be created/changed?
4. **Check existing tests** — what test infrastructure exists? (`pytest`, `jest`, `go test`?)

If no test infrastructure exists → **set it up first** (see "Bootstrap" section below).

### Phase 1: RED — Write failing tests

Two sub-phases, in this order:

#### 1a. Acceptance tests (from AC)

For EACH `- [ ]` checkbox in AC, write at least one test:

```
AC: "- [ ] POST /api/auth returns 200 for valid credentials"
→ test: test_auth_returns_200_for_valid_credentials()

AC: "- [ ] expired token returns 401 with clear error body"
→ test: test_expired_token_returns_401()
→ test: test_expired_token_error_body_is_descriptive()

AC: "- [ ] unknown email returns 200 (no enumeration)"
→ test: test_unknown_email_returns_200_not_404()
```

**Conversion rules:**

| AC pattern | Test pattern |
|---|---|
| `X returns Y` | Assert response/output equals Y |
| `X with Z should W` | Parameterize: input Z → expect W |
| `X must not Y` | Assert Y does NOT happen (negative test) |
| `X handles Z gracefully` | Test with Z input, assert no crash + meaningful error |
| `validates X` | Test valid input passes + invalid input rejected |
| `≥N% coverage` | Not a test — this is a metric gate, skip |

**Given/When/Then structure** (recommended for readability):

```python
def test_auth_valid_credentials():
    # GIVEN a registered user with valid credentials
    user = create_test_user(email="test@example.com", password="secret")

    # WHEN they POST to /api/auth
    response = client.post("/api/auth", json={"email": user.email, "password": "secret"})

    # THEN they get 200 with a session token
    assert response.status_code == 200
    assert "token" in response.json()
```

#### 1b. Unit tests (from implementation design)

Think about the internal functions you'll need. For each:

- **Happy path** — does it work with good input?
- **Edge cases** — empty input, None, boundary values, max length
- **Error paths** — what should it raise/return on bad input?

```python
def test_greet_casual_style():
    assert greet("Alice", "casual") == "Hey Alice! What's up?"

def test_greet_unknown_style_raises():
    with pytest.raises(ValueError):
        greet("Alice", "unknown")

def test_greet_empty_name():
    # Design decision: should this raise or use default?
    # Test documents the decision.
    with pytest.raises(ValueError):
        greet("", "casual")
```

#### 1c. Run all tests — they MUST fail

```bash
pytest tests/ -v  # or: npm test / go test ./...
```

If ANY test passes → your test is wrong (testing something that already exists, or testing a trivial tautology). Fix the test.

**Anti-pattern guard**: if a test passes without you writing any implementation code, the test is **tautological** — it tests what the code does, not what it should do. Delete it and rewrite.

### Phase 2: GREEN — Minimum implementation

Write the **minimum** code to make ALL tests pass:

1. Start with the simplest failing test
2. Write just enough code to make it pass
3. Run tests → one more green
4. Next failing test → write just enough code
5. Repeat until all green

**Rules:**
- Do NOT write code that isn't driven by a failing test
- Do NOT add features not covered by tests
- Do NOT optimize — that's Phase 3
- Do NOT skip tests — every red must become green

### Phase 3: REFACTOR — Clean up

Now that all tests pass, improve the code:

1. Remove duplication
2. Improve naming
3. Simplify logic
4. Extract helpers if needed

After EVERY refactor step: **run ALL tests**. If any fail → your refactor broke something. Revert and try again.

### Phase 4: VERIFY — Self-check before reporting Done

Before reporting "Done" to Lead:

| Check | How |
|---|---|
| All AC checkboxes have tests? | Count AC items vs test functions |
| All tests pass? | `pytest -v` / `npm test` |
| Linter clean? | `ruff check .` / `eslint .` |
| No tautological tests? | Review: does each test fail if you break the implementation? |
| Coverage ≥80% on new files? | `pytest --cov=. --cov-report=term-missing` |

---

## Anti-Patterns (NEVER do these)

### 1. Tautological tests

```python
# BAD — tests what code does, not what it should do
def test_greet():
    result = greet("Alice", "casual")
    assert result == greet("Alice", "casual")  # always passes!
```

**Fix**: assert against a LITERAL expected value, not against the function output.

### 2. Implementation-coupled tests

```python
# BAD — breaks if you rename internal variable
def test_internals():
    g = Greeter()
    assert g._style_map["casual"] == "Hey {name}!"  # testing private API
```

**Fix**: test through the PUBLIC interface only. Test behavior, not structure.

### 3. One test verifies everything

```python
# BAD — if it fails, you don't know which part broke
def test_everything():
    assert greet("A", "casual") == "Hey A!"
    assert greet("B", "formal") == "Good day, B."
    assert greet("C", "pirate") == "Ahoy, C!"
    assert raises(ValueError, greet, "D", "bad")
```

**Fix**: one behavior per test. Four tests, not one.

### 4. Mocking everything

```python
# BAD — mocking the thing you're testing
@mock.patch("mymodule.greet")
def test_greet(mock_greet):
    mock_greet.return_value = "Hello"
    assert greet("A") == "Hello"  # tests the mock, not the code
```

**Fix**: mock only external dependencies (DB, HTTP, filesystem). Never mock the subject under test.

### 5. Test after implementation

Writing implementation first then generating tests = tests that pass by construction. They verify what the code DOES, not what it SHOULD do. If you later refactor, these tests might still pass even if behavior is broken.

**Fix**: always write the test FIRST. See it fail. Then implement.

### 6. Hardcoded test data without rationale

```python
# BAD — why 42? Why "abc"? Magic values without explanation
def test_process():
    assert process(42, "abc") == 17
```

**Fix**: use descriptive variable names or comments explaining WHY this test data matters.

---

## Dependency-Aware Test Selection

When changing existing code, identify which EXISTING tests are affected:

### Heuristic: find related test files

```bash
# For a changed source file, find its test counterparts:
# Python: src/auth/token.py → tests/test_token.py, tests/auth/test_token.py
# Node:   src/auth/token.ts → src/auth/token.test.ts, __tests__/token.test.ts
# Go:     pkg/auth/token.go → pkg/auth/token_test.go (same package)
# Rust:   src/auth/token.rs → #[cfg(test)] module inside same file
```

### Run affected tests FIRST (fast feedback)

```bash
# Only tests related to changed files — seconds, not minutes
pytest tests/test_token.py tests/test_auth.py -v
```

If these fail → fix before running the full suite.

### Then run FULL suite (regression check)

```bash
pytest tests/ -v  # entire project
```

---

## Bootstrap: Setting Up Test Infrastructure

If the project has NO test framework:

### Python
```bash
# Create virtual environment if none exists
python3 -m venv .venv
.venv/bin/pip install pytest pytest-cov ruff

# Create pyproject.toml
cat > pyproject.toml << 'EOF'
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-v --tb=short"

[tool.ruff]
line-length = 120
EOF

mkdir -p tests
touch tests/__init__.py
```

### Node.js (Jest)
```bash
npm install --save-dev jest @types/jest ts-jest
# Add to package.json: "scripts": { "test": "jest" }
mkdir -p __tests__
```

### Node.js (Vitest)
```bash
npm install --save-dev vitest
# Add to package.json: "scripts": { "test": "vitest run" }
```

### Go
```bash
# Go has built-in testing — no setup needed
# Tests are *_test.go files in the same package
```

---

## Coverage Strategy

### What to measure

**Delta coverage** — coverage on CHANGED files only, not the entire project. A new feature shouldn't be penalized for legacy untested code.

### Thresholds

| Gate | Threshold | Blocks? |
|---|---|---|
| Story branch (dev work) | Target 100%, report actual | No |
| feat → dev (EPIC COMPLETE) | ≥80% per changed file, 0% = block | **Yes** |
| dev → main (release) | ≥80% per changed file, 0% = block | **Yes** |

### Measuring

```bash
# Python
pytest --cov=. --cov-report=json tests/
# Parse coverage.json for per-file line coverage

# Node
npx jest --coverage --coverageReporters=json-summary
# or: npx vitest run --coverage

# Go
go test -coverprofile=cover.out ./...
go tool cover -func=cover.out
```

### What 0% means

A changed source file with 0% coverage = NO tests exist for it AT ALL. This always blocks merge, regardless of other files' coverage. If the file is non-testable (config, migration, CSS), explicitly document why — don't just ignore it.

---

## Mutation Testing (advanced, optional)

Standard coverage tells you "this line was executed during tests." It does NOT tell you "this line is VERIFIED by tests." Mutation testing answers the real question: **if I break this line, does any test fail?**

### When to use

- Before release (part of `/bx:git-release` quality gate)
- When coverage is high (>80%) but you suspect tests are weak
- For critical business logic (payments, auth, data integrity)

### How it works

1. The tool mutates your source code (e.g., changes `>` to `>=`, removes a line, swaps `true`/`false`)
2. Runs your tests against the mutant
3. If tests PASS on the mutant → **the mutant survived** → your tests don't catch that change → gap
4. If tests FAIL → **the mutant was killed** → your tests verify that behavior

### Tools

```bash
# Python
pip install mutmut
mutmut run --paths-to-mutate=src/

# Node
npx stryker run

# Go
go install github.com/zimmski/go-mutesting/cmd/go-mutesting@latest
go-mutesting ./...
```

### Interpreting results

- **Mutation score ≥80%** → tests are strong
- **Mutation score 50-80%** → tests run the code but don't verify it carefully
- **Mutation score <50%** → tests are decorative (high coverage, low value)

---

## Context Isolation (critical for AI agents)

> "When everything runs in one context window, the LLM cannot truly follow TDD. The test writer's detailed analysis bleeds into the implementer's thinking."
> — alexop.dev, 2025

### The Problem

If the same AI context writes tests AND implements code, it **subconsciously designs tests around the implementation it's already planning**. The tests pass by construction — they verify what the code does, not what it should do. This is the #1 reason AI-generated tests have low mutation scores.

### The Solution for Multi-Agent Pipelines

Multi-agent pipelines solve this through isolated Codex subagents:
- **Lead** provides AC → **Dev** writes tests from AC (Phase 1 RED)
- Dev implements (Phase 2 GREEN) in the SAME context — this is acceptable because tests were written FIRST from AC, not from implementation plans
- **Bug Reviewer** (separate agent, fresh context) reviews the tests — catches tautological tests that Dev might have written
- **Test Failure Analyst** (separate agent, fresh context) diagnoses test failures — no implementation bias

For maximum isolation (optional, high-assurance tasks):
- Spawn a separate **Test Writer** subagent that ONLY sees AC + function signatures
- Test Writer sends tests back to Lead
- Lead gives tests to Dev: "here are your failing tests, make them pass"
- Dev never sees WHY these tests were written — pure red-green

### When to use full isolation

- Security-critical code (auth, payments, encryption)
- Complex business rules with many edge cases
- When Dev's tests keep passing from the start (smell: tautological tests)

---

## Property-Based Testing (advanced)

Standard example-based tests check specific inputs → specific outputs. Property-based testing checks **invariants** that must hold for ALL valid inputs.

### When to use

- Pure functions with clear contracts (encode/decode, serialize/deserialize, sort, math)
- Data transformations where roundtrip must be identity
- Parsers, validators, converters
- When you suspect edge cases but don't know which ones

### Pattern

```python
from hypothesis import given, strategies as st

# Property: encoding then decoding always returns original
@given(text=st.text())
def test_roundtrip(text):
    assert decode(encode(text)) == text

# Property: sorting is idempotent
@given(lst=st.lists(st.integers()))
def test_sort_idempotent(lst):
    assert sorted(sorted(lst)) == sorted(lst)

# Property: output is always valid
@given(name=st.text(min_size=1), style=st.sampled_from(["formal", "casual", "pirate"]))
def test_greet_always_contains_name(name, style):
    result = greet(name, style)
    assert name in result
```

### Tools

```bash
# Python
pip install hypothesis
# Use with pytest: just decorate test functions with @given(...)

# Node
npm install fast-check
# import fc from 'fast-check'; fc.assert(fc.property(...))

# Go
// built-in: func FuzzGreet(f *testing.F) { f.Fuzz(func(t *testing.T, name string) { ... }) }
```

### Combining with ATDD

Property-based tests complement (not replace) example-based tests:
- **AC tests** = specific examples ("greet Alice casual → Hey Alice!") — ALWAYS needed
- **Property tests** = invariants ("greet ALWAYS contains the name") — for robust coverage
- **Mutation tests** = verification ("if I break greet, does any test catch it?") — for quality

---

## Spec-Driven Development (SDD)

> "In the future, code will just be specifications. Our tests will be our code."
> — Paul Duvall, 2026

ATDD is the testing discipline within a broader **Spec-Driven Development** approach for AI agents:

```
Acceptance Criteria (spec)
  → Gherkin scenarios (Given/When/Then)
    → Acceptance tests (executable spec)
      → Unit tests (implementation spec)
        → Implementation (code)
```

Each layer is MORE specific than the previous. The spec is the source of truth — code is a derivation.

### For `/bx:run` this means

1. **AC in the tracker or spec** = the source of truth
2. **Dev's acceptance tests** = executable version of that spec (Phase 1a RED)
3. **Dev's unit tests** = implementation-level spec (Phase 1b RED)
4. **Dev's code** = derived from tests, not the other way around

If AC changes → tests change → code changes. Never the reverse.

### Gherkin for complex AC

When AC is complex (multi-step user flows), structure tests as `.feature` files:

```gherkin
Feature: Magic link authentication

  Scenario: Happy path sign-in
    Given a registered user with email "alice@example.com"
    When they request a magic link
    Then they receive an email within 30 seconds
    And the email contains a signed token with 15-min TTL

  Scenario: Expired token
    Given a magic link token older than 15 minutes
    When the user clicks the link
    Then they see a 401 error
    And the error message says "Link expired, request a new one"
```

For simple AC (one-liner criteria), skip Gherkin — plain test functions are sufficient.

---

## Quick Reference Card

```
DOUBLE LOOP:
  OUTER (acceptance, hours):  AC checkbox → acceptance test → RED
    INNER (unit, minutes):    function → unit test → RED → implement → GREEN → refactor
  → acceptance test → GREEN
  → next AC checkbox

THREE LAWS (nano-cycle, seconds):
  1. No production code without a failing test
  2. No more test than sufficient to fail
  3. No more code than sufficient to pass

FIRST PRINCIPLES:
  Fast / Isolated / Repeatable / Self-validating / Timely

TEST PYRAMID:
  10%  Acceptance/E2E (outer loop — from AC)
  20%  Integration (service boundaries, API contracts)
  70%  Unit (inner loop — per function)

TWO STREAMS:
  Acceptance = from AC checkboxes = WHAT (business behavior)
  Unit = from implementation = HOW (internal correctness)

STRUCTURE (every test):
  ARRANGE (Given) → ACT (When) → ASSERT (Then)
  One behavior per test. One assert per test (ideally).

TEST DOUBLES:
  Dummy (fill params) → Stub (canned returns) → Spy (record calls)
  → Mock (verify interactions) → Fake (simplified real)
  ✓ Mock external deps (HTTP, DB, filesystem)
  ✗ NEVER mock the subject under test

ANTI-PATTERNS:
  ✗ Test after implementation (tautological)
  ✗ One test verifies everything (undiagnosable)
  ✗ Mock the subject under test (tests the mock)
  ✗ Magic values without rationale (opaque)
  ✗ Test private APIs (fragile coupling)
  ✗ Implementation-coupled tests (break on refactor)

NAMING:
  test_{action}_{scenario}_{expected_result}
  test_given_{precondition}_when_{action}_then_{outcome}

COVERAGE:
  Target 100% on new code
  Gate at 80% per changed file
  0% = always blocks
  Delta (changed files only), not total project
  Mutation score ≥80% = tests are strong
```

---

## Sources

- [TDAD: Test-Driven Agentic Development (arxiv 2603.17973)](https://arxiv.org/html/2603.17973v2) — agents need targeted test context, not procedural TDD instructions. Regressions reduced 70%.
- [Simon Willison: Red/green TDD - Agentic Engineering Patterns](https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/) — 5 tokens that dramatically improve AI code quality
- [swingerman/atdd: ATDD for Claude Code](https://github.com/swingerman/atdd) — Uncle Bob's two-stream testing (acceptance + unit), Given/When/Then spec generation
- [Paul Duvall: ATDD with AI — Tests as Programming Language](https://www.paulmduvall.com/atdd-driven-ai-development-how-prompting-and-tests-steer-the-code/) — Gherkin .feature files as executable spec, DoubleUp! testbed
- [alexop.dev: Forcing Claude Code to TDD](https://alexop.dev/posts/custom-tdd-workflow-claude-code-vue/) — context isolation via subagents, implementation bleeding anti-pattern
- [Nathan Fox: Taming GenAI Agents with TDD](https://www.nathanfox.net/p/taming-genai-agents-like-claude-code) — CLAUDE.md embedding, incremental tested pieces
- [Martin Fowler: Understanding Spec-Driven Development](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html) — Kiro, spec-kit, Tessl comparison
- [Spec-Driven Development (arxiv 2602.00180)](https://arxiv.org/html/2602.00180v1) — from code to contract in AI-assisted development
- [Meta: LLMs for Mutation Testing at Scale](https://engineering.fb.com/2025/09/30/security/llms-are-the-key-to-mutation-testing-and-better-compliance/) — 73% acceptance rate on LLM-generated mutation tests
- [Atlassian: Automating Mutation Coverage with AI](https://www.atlassian.com/blog/developer/automating-mutation-coverage-with-ai) — pushing projects to 80%+ mutation score
- [Hypothesis: Property-Based Testing for Python](https://github.com/HypothesisWorks/hypothesis) — found bugs in CPython, NumPy
- [Agile Alliance: ATDD](https://agilealliance.org/glossary/atdd/) — three amigos, collaborative requirements definition
- [Agentic Coding Handbook: TDD Workflow](https://tweag.github.io/agentic-coding-handbook/WORKFLOW_TDD/) — describe one behavior at a time through tests
- [Uncle Bob: The Cycles of TDD](https://blog.cleancoder.com/uncle-bob/2014/12/17/TheCyclesOfTDD.html) — nano/micro/milli cycles, Three Laws
- [Uncle Bob: The Three Rules of TDD](http://butunclebob.com/ArticleS.UncleBob.TheThreeRulesOfTdd) — canonical three laws
- [Martin Fowler: Practical Test Pyramid](https://martinfowler.com/articles/practical-test-pyramid.html) — unit/integration/E2E ratio
- [Martin Fowler: Mocks Aren't Stubs](https://martinfowler.com/articles/mocksArentStubs.html) — test doubles taxonomy
- [Martin Fowler: Given When Then](https://martinfowler.com/bliki/GivenWhenThen.html) — BDD naming pattern
- [Samman Coaching: Double-Loop TDD](https://sammancoaching.org/learning_hours/bdd/double_loop_tdd.html) — outer (acceptance) + inner (unit) loops
- [Pact: Consumer-Driven Contract Testing](https://docs.pact.io/) — API contract testing for microservices
- [FIRST Principles](https://medium.com/pragmatic-programmers/unit-tests-are-first-fast-isolated-repeatable-self-verifying-and-timely-a83e8070698e) — Fast, Isolated, Repeatable, Self-validating, Timely
- [Kent Beck: Test Desiderata](https://medium.com/@kentbeck_7670/test-desiderata-94150638a4b3) — 12 properties of good tests
- [TestDesiderata.com](https://testdesiderata.com/) — Kent Beck + Kelly Sutton video explanations
- [Uncle Bob: Transformation Priority Premise](http://blog.cleancoder.com/uncle-bob/2013/05/27/TheTransformationPriorityPremise.html) — ordering code transformations simple → complex
- [Kent Beck: TDD by Example](https://stanislaw.github.io/2016-01-25-notes-on-test-driven-development-by-example-by-kent-beck.html) — Fake It, Obvious Implementation, Triangulation strategies
- [TDD Test List Technique](https://agiledojo.de/2018-12-16-tdd-testlist/) — plan test cases before coding
- [Michael Feathers: Working Effectively with Legacy Code](https://en.wikipedia.org/wiki/Characterization_test) — characterization tests for legacy code
