---
name: lyra-code-review
description: Pre-merge review gate. One checklist across seven categories with four severity levels and explicit merge consequences for each finding.
compatibility: Read-only git/gh for scope; test runners invoked read-only to confirm coverage claims. Language-agnostic core with TS, Python, and PHP specifics.
---

# lyra-code-review

## What it does

The pre-merge review gate: one pass across seven categories, every finding labeled P0 through P3 with an explicit merge consequence. P0 means data loss, a security breach, a broken build, or a dummy test masquerading as coverage. P1 means missing tests, missing input validation, an N+1 query, or a feature flag without a cleanup plan. P2 means naming issues, dead code, or missing error-path tests. P3 means style and formatting the author may ignore.

---

## The checklist

### 1. Correctness

- Change matches the spec, task, or PR description.
- Edge cases handled: null, empty, zero, boundary, off-by-one, overflow.
- Error paths exercised, not just the happy path. Every `try` has a meaningful `catch`.
- No race conditions in concurrent or async paths.

### 2. Security & data isolation

- Every query in a multi-tenant system filters by tenant. No exceptions.
- Soft-deleted records filtered where applicable.
- Auth guards on every protected route. Input validated via DTOs or schemas (zod, pydantic, form requests) — no raw `req.body` reaching logic.
- No secrets, tokens, or credentials committed, logged, or leaked. All queries parameterized; no string concatenation in SQL or shell.

### 3. Type & language hygiene

- TypeScript: no `any`, no bare `unknown` without a type guard, no `@ts-ignore` without a comment, return types on public functions, no `console.log` in production.
- Python: type hints on public signatures, no `# type: ignore` without a comment, `pydantic` or `@dataclass` for structured data, no bare `except:`, no `print()` in production.
- PHP: `declare(strict_types=1);`, typed properties and return types, no `@phpstan-ignore-line` without justification, no `dump()` or `dd()` in committed code.

### 4. Database safety

- Tenant and soft-delete filters present in every applicable query.
- Projections on large documents — no `SELECT *` when a subset suffices. Indexes exist for the new query patterns.
- No N+1 queries. One query inside a loop is a P1.
- Multi-step mutations wrapped in a transaction. Unwrapped sequential `await db.update()` calls that can leave the DB half-written are a P0.

### 5. Test existence & quality

- Tests exist for every new public method, every behavior change, and every bug fix (with a regression test).
- Tests assert behavior, not implementation. Tests assert real outputs, not `expect(true)`. Tests cover the error path.
- Flip-the-comparison check: if you flipped a `<` to `>` in the production code, would a test go red? If not, the test is a dummy.
- Coverage did not drop. 100% coverage with all-dummy tests is a P0; coverage without assertions is theater.

### 6. Devex regressions

- Env var renames or additions: `.env.example` updated and announced in the PR description. Unannounced is a P1.
- Port or network remaps: README and dependent config updated.
- New mandatory setup scripts: documented in the PR description and setup guide.
- New required build steps: migration note included.

### 7. Feature-flag / gate leaks

- Flag check absent, or only on the UI and not the API handler — P0.
- Flag check in the happy path but absent in the error handler or background job — P0.
- Always-on constants like `const ENABLE_NEW_X = true` bypassing the flag service — P0.
- Flag without a linked issue or TODO for cleanup — P1.

---

## The anti-dummy-test gate

Scan every new or modified test against these six patterns. Any match is a P0.

1. **Tautology** — asserts the language, not the code. Delete the production code and the test still passes.

```ts
test("addition works", () => {
  expect(1 + 1).toBe(2);
});
```

2. **`expect(true)` / always-passing** — proves the function didn't throw, nothing about correctness.

```ts
test("function runs", () => {
  myFunction();
  expect(true).toBe(true);
});
```

3. **Testing the mock** — the mock is the subject of the assertion, not the real code under test.

```ts
const mock = jest.fn().mockReturnValue({ id: 1 });
expect(mock()).toEqual({ id: 1 });
```

4. **No assertions** — the test renders or calls something but never asserts. "It didn't crash" is not a test.

```ts
test('renders', () => { render(<Component />) })
```

5. **Testing implementation, not behavior** — locks in private details and makes refactoring impossible.

```ts
test("uses a Map internally", () => {
  expect((cache as any).store).toBeInstanceOf(Map);
});
```

6. **Catch-all try/catch swallowing failures** — the test passes whether the function works or throws.

```ts
test("works", () => {
  try {
    myFunction();
  } catch (e) {
    /* ignore */
  }
  expect(true).toBe(true);
});
```

---

## The verdict

- Any P0 → block.
- Any P1 → request changes; fix or defer with a linked issue.
- P2 only → approve with notes.
- P3 only → approve.

---

_Part of the [skill collection](../README.md)._