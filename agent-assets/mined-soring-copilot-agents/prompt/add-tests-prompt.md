---
name: add-tests
description: Generate comprehensive tests for an existing file or module
agent: tester
model: GPT-5.1-Codex
tools:
  - editFiles
  - createFile
  - codebase
  - search
  - usages
  - runTests
  - testFailure
  - problems
  - runInTerminal
---

# Generate Tests

## Target: ${input:target:File path or module to test (e.g., "backend/app/services/user_service.py")}

Analyze the target code and generate a comprehensive test suite.

### Steps

1. **Read the target file** — Understand all public functions, classes, and their signatures
2. **Trace dependencies** — Identify what needs to be mocked (database, external APIs, other services)
3. **Map existing tests** — Check if tests already exist; extend rather than duplicate
4. **Write tests** covering:
   - ✅ Happy path for every public function
   - ❌ Error conditions (invalid input, not found, unauthorized)
   - 🔲 Edge cases (empty input, boundary values, null/None)
   - 🔐 Security cases (injection attempts, auth bypass, data leakage)
   - ⚡ Async behavior (if applicable)
5. **Run the tests** — Execute with `#runTests` and fix any failures
6. **Verify coverage** — Check that all critical code paths are exercised

### Conventions

- **Python**: pytest + pytest-asyncio, `httpx.AsyncClient` for API tests, fixtures in `conftest.py`
- **Vue**: Vitest + Vue Testing Library, `userEvent` for interactions
- **React**: Vitest + React Testing Library, `msw` for API mocking

Place test files adjacent to source: `module.py` → `tests/test_module.py`, `Component.vue` → `__tests__/Component.test.ts`
