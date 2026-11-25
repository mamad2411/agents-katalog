---
name: tpl-situacao-testes-codigo-sem-testes
description: Template do pack (situacao/08-testes-codigo-sem-testes.md). Orienta o agente em tarefas situacionais como debug, seguranca e refactor alinhado a esse contexto.
metadata:
  version: 1.0.0
  source_template: situacao/08-testes-codigo-sem-testes.md
  generated_by: install_pack_templates_as_claude_skills
---

# SITUATION: Writing Tests for Untested Code

Skill gerado a partir do pack `templates-claude-code`. Arquivo de origem: `situacao/08-testes-codigo-sem-testes.md`. Use como baseline e adapte ao projeto antes de mudancas grandes.

## Conteudo do template

## CONTEXT
Use this configuration when a codebase has zero or very few tests and you need to add them — without breaking existing behavior, and without being able to refactor first. The challenge: the code is often not written to be testable (global state, hardwired dependencies, no dependency injection). The goal is to add tests that work with the code as-is, not force an architectural rewrite.

## OBJECTIVES
- Add tests that document and lock down existing behavior (correct or not)
- Identify the highest-risk paths and test those first
- Make the code incrementally more testable without big refactors
- Achieve meaningful coverage without testing trivial code
- Create a safety net that makes future refactoring safe

## APPROACH RULES

1. **Characterization tests first.** Before writing tests that assert what "should" happen, write tests that assert what DOES happen. Run the code, observe output, write a test that captures it. This is the safety net — even if behavior is wrong, you want to know if it changes.

2. **Start at the highest risk, not the lowest complexity.** High risk = code that handles money, auth, data mutation, external integrations. A complex but low-risk rendering function can wait. Test what breaks the most when wrong.

3. **Test the boundary, not the implementation.** Test inputs and outputs. Don't test internal state or private methods. If you have to, the architecture needs to change later.

4. **Identify seams.** A seam is a place where you can substitute behavior without editing code (constructor injection, module mock, env variable). Find all seams before writing tests. If a class has no seams, you'll need to add a minimal one.

5. **One failing test at a time.** When adding tests, add one, make it pass, commit. Don't write 50 tests then try to make them all pass — the feedback loop is too long.

6. **Mock at the outermost boundary.** Mock database connections, HTTP calls, filesystems. Do not mock your own business logic — those are integration tests in disguise.

7. **Coverage targets by risk tier:**
   - Critical (payments, auth, data deletion): 100% line + branch coverage
   - Core business logic: 80%+ coverage
   - Utility functions: 60%+ coverage
   - Simple glue code / configuration: skip or minimal

## ROUTING TABLE

| If you encounter | Then |
|-----------------|------|
| Global mutable state | Wrap in a function or class that can be reset. Add a `reset()` method. Test in isolation. |
| `new SomeService()` inside a function (hardwired dependency) | Pass it as a parameter with a default. This is the minimal seam you need. |
| Database calls in the middle of business logic | Extract DB calls to a Repository interface. Mock the repository in unit tests. |
| HTTP calls in business logic | Extract to a client class. Mock it. Or use `nock`/`msw` to intercept at the HTTP layer. |
| Timer-dependent code (setTimeout, intervals) | Use Jest's fake timers (`jest.useFakeTimers()`) or sinon fake timers. |
| File system operations | Mock `fs` module or use a temp directory with cleanup in `afterEach` |
| Untestable legacy function (500 lines, everything mixed) | Write a characterization test at the top level only. Add TODO comment. Refactor in a separate PR. |
| A function that's never called in tests (0% coverage) | Write a smoke test: does it run without throwing? Then add edge cases. |
| Async code without proper async/await | Convert to async/await first. Then test with async test functions. |
| Third-party library with complex behavior | Test your code's behavior assuming the library works. Use stubs/fakes, not mocks of internals. |

## Test Pyramid Strategy

```
E2E Tests (5%)
  → Cover the most critical user journeys only
  → Slow, flaky if overdone. Use sparingly.

Integration Tests (25%)
  → Test how components work together
  → Use real DB (in-memory or test DB), mock external APIs
  → Example: UserService creates a user and can retrieve it

Unit Tests (70%)
  → Test individual functions/classes in isolation
  → Fast, no I/O, fully mocked dependencies
  → Example: validateEmail() returns false for malformed email
```

## Test Naming Convention

```javascript
// Pattern: [unit] should [expected behavior] when [condition]
describe('AuthService', () => {
  describe('login()', () => {
    it('should return JWT token when credentials are valid', async () => { ... })
    it('should throw UnauthorizedError when password is wrong', async () => { ... })
    it('should throw UnauthorizedError when user does not exist', async () => { ... })
    it('should lock account after 5 failed attempts', async () => { ... })
  })
})
```

## DO NOT

- **DO NOT** mock what you own — mock external dependencies, not your own services in unit tests
- **DO NOT** test private methods directly — if you feel you need to, the class has too many responsibilities
- **DO NOT** write tests that depend on execution order — each test must be independent
- **DO NOT** use `beforeAll` for mutable state — use `beforeEach` so each test starts clean
- **DO NOT** target 100% line coverage across the board — it leads to testing trivial code while missing critical logic
- **DO NOT** write assertions that test the mock itself (`expect(mockFn).toHaveBeenCalled` only)  — test the outcome
- **DO NOT** leave `console.log` in test files — tests should be silent in CI
- **DO NOT** skip flaky tests with `xtest` or `.skip` — fix the flakiness or delete the test

## OUTPUT FORMAT

When adding tests to an existing codebase, produce:

1. **Coverage Report** — before and after, focusing on critical paths
2. **Test inventory** — list of what's tested and what's intentionally not tested
3. **Seams identified** — places where the code was adjusted (minimally) to be testable
4. **Characterization tests list** — tests that capture current behavior (possibly wrong/to be revisited)
5. **Skipped paths** — what was NOT tested and why (complexity, risk, time)

Template for a characterization test comment:
```javascript
// CHARACTERIZATION TEST: Captures current behavior as of 2024-01-15.
// This behavior may not be correct — see issue #123.
// Do not change this test without first verifying the business requirement.
it('should return null when user not found (current behavior)', () => {
  expect(service.getUser(-1)).toBeNull()
})
```

## QUALITY GATES

- [ ] Coverage of critical paths (auth, payments, data mutations) is ≥ 90%
- [ ] Every test is independent: passes when run alone and in any order
- [ ] No test takes more than 200ms (if so, investigate why)
- [ ] No production code was changed to make tests pass (only seams added)
- [ ] All tests are named with the `should [behavior] when [condition]` pattern
- [ ] Test suite runs cleanly in CI with zero flaky failures
- [ ] Characterization tests are marked as such with a comment
- [ ] Coverage report visible in CI output
- [ ] A new developer can understand what a function does by reading its tests
