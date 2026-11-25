---
name: test-vitest
description: Use this skill when writing or fixing unit tests with Vitest (TypeScript/JavaScript).
---

# Vitest Testing Skill

Vitest is the recommended test framework for TypeScript/JavaScript projects using Vite. It provides Jest-compatible APIs with first-class ESM support.

## Detection

Vitest is in use when:
- `package.json` devDependencies includes `vitest`
- A `vitest.config.ts` or `vitest.config.js` exists
- Test files use `.spec.ts` or `.test.ts` extensions with `import { describe, it, expect } from 'vitest'`

## File Structure

```
src/
  foo.ts                  # production file
  foo.spec.ts             # test file (co-located)
  # OR
  __tests__/
    foo.test.ts           # alternative location
```

Place test files co-located with production files unless the project uses a separate `__tests__/` directory — match the existing convention.

## Basic Test Structure

```typescript
import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest'
import { myFunction } from './myModule'

describe('myModule', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  describe('myFunction', () => {
    it('should return expected value for valid input', () => {
      // Arrange
      const input = 'hello'

      // Build
      const result = myFunction(input)

      // Assert
      expect(result).toBe('HELLO')
    })

    it('should throw for invalid input', () => {
      expect(() => myFunction(null)).toThrow('Input must not be null')
    })
  })
})
```

## Mocking

### Mock a module
```typescript
vi.mock('./dependency', () => ({
  fetchData: vi.fn().mockResolvedValue({ id: 1, name: 'test' }),
}))
```

### Mock a function
```typescript
const mockFn = vi.fn().mockReturnValue(42)
const mockAsync = vi.fn().mockResolvedValue({ ok: true })
const mockRejected = vi.fn().mockRejectedValue(new Error('fail'))
```

### Spy on a method
```typescript
const spy = vi.spyOn(obj, 'method').mockReturnValue('mocked')
```

### Reset mocks between tests
```typescript
beforeEach(() => {
  vi.clearAllMocks()    // clear call history
  vi.resetAllMocks()    // clear call history + reset implementations
  vi.restoreAllMocks()  // restore original implementations
})
```

## Async Tests

```typescript
it('should resolve promise', async () => {
  const result = await someAsyncFunction()
  expect(result).toEqual({ success: true })
})

it('should reject promise', async () => {
  await expect(someAsyncFunction()).rejects.toThrow('error message')
})
```

## Common Assertions

```typescript
expect(value).toBe(42)                     // strict equality
expect(value).toEqual({ a: 1 })            // deep equality
expect(value).toBeNull()
expect(value).toBeUndefined()
expect(value).toBeTruthy()
expect(value).toBeFalsy()
expect(array).toHaveLength(3)
expect(array).toContain('item')
expect(object).toHaveProperty('key', 'value')
expect(fn).toHaveBeenCalledWith('arg')
expect(fn).toHaveBeenCalledTimes(2)
expect(fn).not.toHaveBeenCalled()
```

## Running Tests

```bash
# Run all tests once
npx vitest run

# Run with coverage
npx vitest run --coverage

# Run specific file
npx vitest run src/foo.spec.ts

# Watch mode (development)
npx vitest
```

## Coverage

Vitest uses `@vitest/coverage-v8` or `@vitest/coverage-istanbul`. Configure in `vitest.config.ts`:

```typescript
export default defineConfig({
  test: {
    coverage: {
      provider: 'v8',
      reporter: ['text', 'lcov'],
      exclude: ['**/*.spec.ts', '**/*.test.ts', '**/node_modules/**'],
    },
  },
})
```

Run with: `npx vitest run --coverage`

## Common Pitfalls

- Always call `vi.clearAllMocks()` in `beforeEach` to prevent test pollution
- Use `vi.mock()` at the top level of the file (not inside `describe`/`it` blocks) — Vitest hoists mock calls
- For ESM modules, prefer `vi.mock()` with factory functions over `jest.spyOn` patterns
- When mocking the same module across multiple test files, each file gets its own isolated mock
