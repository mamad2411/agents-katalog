---
name: test-jest
description: Use this skill when writing or fixing unit tests with Jest (TypeScript/JavaScript).
---

# Jest Testing Skill

Jest is a widely-used JavaScript testing framework with built-in mocking, assertions, and coverage support.

## Detection

Jest is in use when:
- `package.json` devDependencies includes `jest` or `ts-jest` or `@types/jest`
- A `jest.config.js`, `jest.config.ts`, or `jest.config.json` exists
- Test files use `.spec.ts`, `.test.ts`, `.spec.js`, or `.test.js` extensions
- `package.json` has a `"jest"` configuration key

## File Structure

```
src/
  foo.ts                  # production file
  foo.spec.ts             # test file (co-located)
  # OR
  __tests__/
    foo.test.ts           # alternative location
```

Match the existing project convention.

## Basic Test Structure

```typescript
import { myFunction } from './myModule'

describe('myModule', () => {
  beforeEach(() => {
    jest.clearAllMocks()
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
jest.mock('./dependency', () => ({
  fetchData: jest.fn().mockResolvedValue({ id: 1, name: 'test' }),
}))
```

### Mock a function
```typescript
const mockFn = jest.fn().mockReturnValue(42)
const mockAsync = jest.fn().mockResolvedValue({ ok: true })
const mockRejected = jest.fn().mockRejectedValue(new Error('fail'))
```

### Spy on a method
```typescript
const spy = jest.spyOn(obj, 'method').mockReturnValue('mocked')
```

### Auto mock
```typescript
jest.mock('./heavyModule')  // auto-mocks all exports
```

### Reset mocks between tests
```typescript
beforeEach(() => {
  jest.clearAllMocks()    // clear call counts and instances
  jest.resetAllMocks()    // clear + reset implementations to undefined
  jest.restoreAllMocks()  // restore jest.spyOn originals
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

// With done callback (legacy)
it('legacy callback test', (done) => {
  fetchData((data) => {
    expect(data).toBe('ok')
    done()
  })
})
```

## Timers

```typescript
jest.useFakeTimers()

it('should debounce', () => {
  const fn = jest.fn()
  debounce(fn, 500)()
  jest.advanceTimersByTime(500)
  expect(fn).toHaveBeenCalledTimes(1)
})

afterEach(() => jest.useRealTimers())
```

## Common Assertions

```typescript
expect(value).toBe(42)                     // strict equality (Object.is)
expect(value).toEqual({ a: 1 })            // deep equality
expect(value).toStrictEqual({ a: 1 })      // deep + checks undefined properties
expect(value).toBeNull()
expect(value).toBeUndefined()
expect(value).toBeDefined()
expect(value).toBeTruthy()
expect(value).toBeFalsy()
expect(array).toHaveLength(3)
expect(array).toContain('item')
expect(object).toHaveProperty('key', 'value')
expect(fn).toHaveBeenCalledWith('arg')
expect(fn).toHaveBeenCalledTimes(2)
expect(fn).toHaveBeenNthCalledWith(1, 'first arg')
expect(fn).not.toHaveBeenCalled()
expect(value).toMatchSnapshot()
expect(value).toMatchInlineSnapshot(`"expected"`)
```

## TypeScript Setup

With `ts-jest`:
```json
// jest.config.json
{
  "preset": "ts-jest",
  "testEnvironment": "node",
  "roots": ["<rootDir>/src"]
}
```

With `@swc/jest` (faster):
```json
{
  "transform": {
    "^.+\.(t|j)s$": "@swc/jest"
  }
}
```

## Running Tests

```bash
# Run all tests
npx jest

# Run with coverage
npx jest --coverage

# Run specific file
npx jest src/foo.spec.ts

# Run tests matching pattern
npx jest --testNamePattern="myFunction"

# Watch mode
npx jest --watch
```

## Coverage

Configure in `jest.config.js`:
```javascript
module.exports = {
  collectCoverageFrom: ['src/**/*.ts', '!src/**/*.spec.ts'],
  coverageThreshold: {
    global: { lines: 80 }
  }
}
```

## Common Pitfalls

- `jest.mock()` is hoisted to the top of the file by Babel/Jest — don't rely on variable initialization order
- Use `jest.fn()` over raw functions for spying — raw functions can't be tracked
- `toEqual` does deep equality; `toBe` uses `Object.is` (like `===`) — use `toEqual` for objects/arrays
- Clear mocks in `beforeEach` to prevent test pollution across test cases
- For TypeScript, ensure `@types/jest` is installed or use `import type { jest } from '@jest/globals'`
