# Vitest Skill

You are writing tests with Vitest. Apply these conventions.

## Test Structure

- Use `describe` for grouping related tests; use `it` (or `test`) for individual cases.
- Follow Arrange-Act-Assert (AAA) — keep each test focused on a single behavior.
- Write test descriptions that read as specifications: `it('returns 404 when user is not found')`.
- Colocate test files next to source files (`foo.test.ts`) or put them in a `tests/` directory — be consistent.

## Assertions

- Use Vitest's built-in `expect` with chainable matchers: `.toBe()`, `.toEqual()`, `.toMatchObject()`, `.rejects.toThrow()`.
- Use `toEqual` for deep equality of objects/arrays; use `toBe` only for primitive equality and reference checks.
- Use `toMatchInlineSnapshot()` or `toMatchSnapshot()` for complex output — update with `vitest --update-snapshots`.

## Mocking

- Mock modules with `vi.mock('module-name')` at the top of the file — Vitest hoists these automatically.
- Mock individual functions with `vi.fn()` or `vi.spyOn(object, 'method')`.
- Restore mocks after each test: use `vi.restoreAllMocks()` in `afterEach`, or set `restoreMocks: true` in config.
- Stub globals with `vi.stubGlobal('fetch', vi.fn())` — note that `vi.stubGlobal` is not hoisted.
- Use `vi.useFakeTimers()` to control `setTimeout`, `setInterval`, and `Date`.

## Async Tests

- Always `await` promises in tests — unawaited rejections may be silently swallowed.
- Use `await expect(fn()).rejects.toThrow('message')` for expected rejections.
- Use `vi.runAllTimersAsync()` with fake timers to drain the async queue.

## Setup & Teardown

- Use `beforeEach` / `afterEach` for per-test setup/teardown.
- Use `beforeAll` / `afterAll` for expensive shared setup (database connections, temp servers).
- Clean up temp files and resources in `afterEach` — tests must be side-effect-free.

## Configuration (vitest.config.ts)

```ts
export default defineConfig({
  test: {
    globals: true,          // no need to import describe/it/expect
    environment: 'node',    // or 'jsdom' for DOM tests
    coverage: { provider: 'v8', reporter: ['text', 'lcov'] },
  },
});
```
