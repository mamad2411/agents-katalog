---
name: test-driven-development
description: Testing discipline that adapts to user tier and task type. Rigorous RED-GREEN-REFACTOR for critical code. Invisible testing for Builder-tier users. Pragmatic skip for trivial changes. The goal is confidence that the code works, not ceremony.
invoke_when: Use when writing any production code, adding features, fixing bugs, or refactoring. Adapts approach based on user tier and task type.
---

# Test-Driven Development

## The Iron Rule

**NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST** — for code that matters.

This rule applies absolutely to: business logic, authentication, payments, data mutations, API endpoints, and calculations. No exceptions, no matter who's asking or how small the change seems.

For everything else, the approach adapts to the situation.

---

## Tier-Adapted Testing Modes

### Invisible TDD (Builder-Tier Users)

Builder-tier users care that things work, not how you verified they work. When working with Builder-tier users:

**Do this:**
- Write tests. Always write tests for anything meaningful.
- Run them. Make sure they pass.
- Report results in outcome language: "I built the payment flow and verified it works correctly — handles successful charges, declined cards, and network errors."
- If something breaks, say: "I found an issue with how refunds were handled and fixed it."

**Don't do this:**
- "I wrote 3 failing tests to establish the RED state..."
- "Achieved GREEN state on all test cases..."
- "Now entering the REFACTOR phase..."
- "Test coverage is at 87.3% across 12 test suites..."

The tests still exist. The discipline still happens. The user just doesn't need a play-by-play of your testing methodology. They need to know their product works.

**How to report:**
| Instead of | Say |
|-----------|-----|
| "Wrote 5 unit tests for the auth module" | "Built the login system and verified it handles email/password, Google sign-in, and invalid credentials correctly" |
| "RED: 3 failing tests for payment processing" | "Working on the payment flow now" |
| "All 12 tests passing, 94% coverage" | "Payment processing is working — tested with successful charges, declines, and edge cases" |
| "Added regression test for bug #234" | "Fixed the bug and made sure it won't come back" |

### Pragmatic TDD (Quick Fixes, Any Tier)

Some changes don't need formal TDD. Applying RED-GREEN-REFACTOR to a CSS color change is like wearing a hard hat to check the mailbox.

**Skip formal TDD for:**
- CSS and styling changes (spacing, colors, fonts, layout tweaks)
- Copy and text updates (labels, messages, placeholder text)
- Configuration changes (env vars, feature flags, build config)
- Simple UI tweaks (reordering elements, showing/hiding existing components)
- Static content updates (about pages, marketing copy)
- Dependency version bumps (with no API changes)

**Instead, verify these by:**
- Building the project (confirms no syntax errors)
- Visually checking the result when possible
- Running the existing test suite (confirms nothing broke)

**But NEVER skip tests for "quick fixes" that touch:**
- Authentication or authorization logic
- Payment or billing code
- Database queries or migrations
- API request/response handling
- Business rules or calculations
- Data validation or sanitization

A "quick" auth fix without tests is how breaches happen.

### Full TDD (Engineer-Tier Users, All Critical Code)

The complete RED-GREEN-REFACTOR cycle. Engineer-tier users appreciate and expect this rigor.

#### RED: Write a Failing Test
1. Decide what the code should DO (not how it should work internally)
2. Write a test that asserts the expected behavior
3. Run the test — it MUST fail
4. If it passes, your test is wrong or the feature already exists

#### GREEN: Make It Pass
1. Write the MINIMUM code to make the test pass
2. Do not write elegant code — write working code
3. Do not add features the test doesn't require
4. Run the test — it MUST pass

#### REFACTOR: Clean Up
1. Now that it works, make it clean
2. Extract common patterns, improve naming, simplify logic
3. Run tests after EVERY refactor step — they must still pass
4. If tests break during refactoring, your refactor changed behavior — undo it

---

## What ALWAYS Gets Tests Regardless of Tier

No matter who the user is or how small the task seems, these ALWAYS get tested:

### Auth Flows
- Login with valid credentials succeeds
- Login with invalid credentials fails with appropriate error
- Session expiry is handled correctly
- Protected routes reject unauthenticated requests
- Role-based access controls are enforced
- Password reset flow works end-to-end
- OAuth callback handling works correctly

### Payment Processing
- Successful charge processes correctly
- Declined card is handled gracefully
- Webhook signature verification works
- Refund flow processes correctly
- Subscription creation, update, and cancellation work
- Price calculation is accurate (tax, discounts, currency)
- Idempotency keys prevent duplicate charges

### Data Mutations
- Create operations validate required fields
- Update operations don't overwrite unrelated fields
- Delete operations handle cascading correctly
- Concurrent writes don't cause data corruption
- Invalid data is rejected with clear errors
- Database transactions roll back on failure

### API Endpoints
- Correct status codes for success and error cases
- Request validation rejects malformed input
- Response shape matches the contract
- Rate limiting works (if applicable)
- Authentication is enforced on protected endpoints
- Pagination works correctly

### Business Calculations
- Pricing calculations are accurate
- Rounding is handled correctly (especially for currency)
- Edge cases: zero amounts, negative values, overflow
- Time zone handling is correct
- Unit conversions are accurate

---

## Testing Anti-Patterns to Avoid

1. **Testing implementation, not behavior** — test WHAT it does, not HOW it does it
2. **Mocking everything** — mocks that diverge from reality give false confidence
3. **Testing the framework** — don't test that React renders a div
4. **No assertions** — a test without assertions is not a test
5. **Flaky tests** — fix or delete; a flaky test is worse than no test
6. **Testing trivial getters/setters** — this adds maintenance, not confidence
7. **Ceremonial tests** — writing tests to hit a coverage number rather than to verify behavior

## Test Infrastructure Setup (Do This First)

Before writing any test, ensure the test infrastructure exists:

### TypeScript/JavaScript
1. Install vitest if not present: `npm install -D vitest @vitest/coverage-v8`
2. Add scripts to package.json:
   ```json
   "test": "vitest run",
   "test:watch": "vitest",
   "test:coverage": "vitest run --coverage"
   ```
3. If supertest is needed for API tests: `npm install -D supertest @types/supertest`

### Python
1. Install pytest if not present: `pip install pytest pytest-cov`
2. Add pytest.ini or pyproject.toml config with coverage settings

### Go
1. Use stdlib `testing` — no install needed
2. Run with: `go test -cover ./...`

This is a one-time setup. Do it on the FIRST test, not every test.

## TypeScript-Specific Rules

- **NEVER use `catch (err: any)`** — use `catch (err: unknown)` and narrow:
  ```typescript
  catch (err: unknown) {
    if (err instanceof Error) {
      // handle Error
    }
    throw err;
  }
  ```
- **NEVER use `: any` in test files either** — tests should be as strictly typed as production code

## Integration with Architecture Spec

Read `architecture.md` to determine:
- Which testing framework to use (Jest, Vitest, pytest, Go testing, etc.)
- Where test files should live (co-located, `__tests__/`, `tests/`)
- Naming conventions for test files
- Coverage thresholds (if specified)

Follow whatever the architecture spec says. If it doesn't specify, default to Vitest for TypeScript, pytest for Python, stdlib testing for Go.

---

## Rationalization Pressure Test

These are excuses you might generate to skip testing. Each one is wrong.

| Rationalization | Why It's Wrong | What To Do Instead |
|----------------|---------------|-------------------|
| "This change is too small to test" | Small changes cause big bugs. A one-line auth fix without tests is how breaches happen | If it's small, the test is small too — write it |
| "I'll add tests later" | Later never comes. Untested code breeds more untested code | Write the test FIRST. That's what TDD means |
| "The test would be trivial" | If it's trivial, it takes 30 seconds. If it's not trivial, you definitely need it | Write the "trivial" test and move on |
| "Testing this would require too much setup" | Complex test setup signals complex code that needs testing the most | Simplify the code or invest in test fixtures. Either way, test it |
| "The user didn't ask for tests" | Production code gets tests. That's not optional. Your human partner is paying for working software | Write tests. Report results, not methodology |
| "This is just a prototype" | Shipworthy exists to prevent prototypes from becoming unmaintainable production code | Test the prototype. It's faster than debugging it later |
| "I can verify this manually" | Manual verification misses edge cases and regressions. Run the command | Write an automated test. Run it. Trust the output |
| "The existing tests already cover this" | If they do, adding one more is cheap insurance. If they don't, you need it | Check coverage. If covered, great. If not, add a test |
