---
name: testing-mocks
description: Create and structure mocks for tests using createMock, vi.mock, and NestJS DI patterns. USE WHEN writing unit or integration tests with mocked dependencies, when asked about mocking services or repositories, or when setting up test environments with injected dependencies.
license: MIT
---

# Testing Mocks

This skill describes mocking patterns and best practices for creating maintainable, type-safe mocks in this codebase.

## When to Use This Skill

Use when asked to:

- Create mocks for services, repositories, or dependencies
- Mock modules or external libraries
- Set up NestJS test containers with mocked providers
- Configure mock return values or assertions
- Write integration tests with mocked I/O

## Core Principle 1: `createMock<T>()` for All Injectable Classes

Use `@golevelup/ts-vitest`'s `createMock<T>()` to auto-mock any TypeScript class or interface. It returns a fully-typed `DeepMocked<T>` where every method is a `vi.fn()` and properties are recursively mocked. **Never write manual stub objects** — `createMock` stays in sync with the source type automatically.

```ts
import { createMock } from "@golevelup/ts-vitest";
import type { DeepMocked } from "@golevelup/ts-vitest";

const mockService = createMock<MyService>();
```

## Core Principle 2: Declare Services Outside Hook, Instantiate Inside

**Always** declare service variables at the describe block scope using `let`, then populate them inside `beforeAll` or `beforeEach` using `module.get()` or `await module.resolve()`. This ensures services are available to all tests and maintains proper isolation.

```ts
describe(MyService, () => {
  // ✅ Declare services OUTSIDE the hook at describe scope
  let service: MyService;
  let repository: DeepMocked<Repository<MyEntity>>;

  // ✅ Instantiate INSIDE the hook
  beforeAll(async () => {
    const module = await Test.createTestingModule({
      providers: [MyService, /* mocks */],
    }).compile();

    // Retrieve using module.get() or await module.resolve()
    service = module.get(MyService);
    repository = module.get(getRepositoryToken(MyEntity));
  });

  it("uses the service", async () => {
    // ✅ All tests have access to instantiated services
    const result = await service.doWork();
    expect(result).toBeDefined();
  });
});
```

**Why this pattern matters:**

- Services are available to all tests in the describe block
- Proper TypeScript scoping for type inference
- ESLint and type checkers can verify safe access
- Enables configuring mock behavior per test (see Pattern 4)

## Pattern 1: Mocking Services in NestJS DI Tests

Provide mocked services through Nest's testing module using the class as the provider token.

```ts
import { createMock } from "@golevelup/ts-vitest";
import { Test } from "@nestjs/testing";
import { beforeAll, describe, expect, it } from "vitest";

describe(MyCommand, () => {
  let command: MyCommand;
  let mockLoggerService: DeepMocked<LoggerService>;

  beforeAll(async () => {
    const module = await Test.createTestingModule({
      providers: [
        MyCommand,
        { provide: LoggerService, useValue: createMock<LoggerService>() },
        { provide: InputService, useValue: createMock<InputService>() },
      ],
    }).compile();

    command = module.get(MyCommand);
    mockLoggerService = module.get(LoggerService);
  });

  it("logs on initialization", async () => {
    await command.initialize();
    expect(mockLoggerService.log).toHaveBeenCalled();
  });
});
```

**Key points:**

- Put mocks in `providers:[]`, never in `imports:[]`
- Store the mocked instance to configure return values per test
- Use `module.get(ServiceClass)` to retrieve the mock

## Pattern 2: Mocking TypeORM Repositories

Use `getRepositoryToken(Entity)` as the provider token for repository mocks.

```ts
import { createMock } from "@golevelup/ts-vitest";
import { Test } from "@nestjs/testing";
import { getRepositoryToken } from "@nestjs/typeorm";
import type { DeepMocked } from "@golevelup/ts-vitest";
import type { Repository } from "typeorm";

const module = await Test.createTestingModule({
  imports: [LoggerModule],
  providers: [
    MyService,
    {
      provide: getRepositoryToken(MyEntity),
      useValue: createMock<Repository<MyEntity>>() satisfies DeepMocked<Repository<MyEntity>>,
    },
  ],
}).compile();

const repository = module.get(getRepositoryToken(MyEntity)) as DeepMocked<Repository<MyEntity>>;
```

**Required setup:** Each NestJS project's `tsconfig.json` must include:

```json
{
  "compilerOptions": {
    "paths": {
      "@golevelup/ts-vitest": ["./node_modules/@golevelup/ts-vitest/lib/index.d.ts"]
    }
  }
}
```

The `satisfies DeepMocked<T>` annotation prevents ESLint's type-aware rules from flagging safe calls as unsafe.

## Pattern 3: Module-Level Mocking with `vi.mock()`

Mock external modules or third-party libraries using `vi.mock()` at the top of your test file. Use `vi.hoisted()` for functions that need to be created before module import.

```ts
import { beforeEach, describe, expect, it } from "vitest";

// Define mocks before imports
const { mockCommandFactoryRun } = vi.hoisted(() => ({
  mockCommandFactoryRun: vi
    .fn<() => Promise<void>>()
    .mockResolvedValue(undefined),
}));

vi.mock("nest-commander", async (importOriginal) => {
  const importedModule = await importOriginal();
  const actual =
    typeof importedModule === "object" && importedModule !== null
      ? importedModule
      : {};
  return {
    ...actual,
    CommandFactory: {
      run: mockCommandFactoryRun,
    },
  };
});

// Now safe to import the module being tested
import { CaelundasModule } from "./caelundas.module";

describe("bootstrap", () => {
  beforeEach(() => {
    vi.resetModules();
    mockCommandFactoryRun.mockClear();
  });

  it("calls CommandFactory.run on startup", async () => {
    await import("./main");
    expect(mockCommandFactoryRun).toHaveBeenCalledTimes(1);
  });
});
```

**Key points:**

- Use `vi.hoisted()` to create function mocks that must exist before import
- Always return the spread actual module plus your overrides
- Check the module type before spreading: `typeof importedModule === "object" && importedModule !== null`
- Call `vi.resetModules()` in `beforeEach()` to clear module cache between tests

## Pattern 4: Configuring Mock Return Values Per Test

Store mock instances and configure return values in specific test cases.

```ts
let service: MyService;
let repository: DeepMocked<Repository<MyEntity>>;

beforeAll(async () => {
  const module = await Test.createTestingModule({
    providers: [
      MyService,
      {
        provide: getRepositoryToken(MyEntity),
        useValue: createMock<Repository<MyEntity>>(),
      },
    ],
  }).compile();

  service = module.get(MyService);
  repository = module.get(getRepositoryToken(MyEntity));
});

it("returns entity when found", async () => {
  repository.findOneBy.mockResolvedValue(myFixture);
  const result = await service.findOne(1);
  expect(result).toStrictEqual(myFixture);
});

it("returns null when not found", async () => {
  repository.findOneBy.mockResolvedValue(null);
  const result = await service.findOne(999);
  expect(result).toBeNull();
});
```

**Key patterns:**

- Use `mockResolvedValue()` for async methods returning data
- Use `mockRejectedValue()` for error cases
- Use `mockReturnValue()` for synchronous methods
- Reset mocks with `mockClear()` if test contamination occurs

## Pattern 5: Asserting Mock Call Arguments

Verify that mocks were called with expected arguments.

```ts
it("validates configuration on module setup", () => {
  // Mock was already called during module import
  const firstCall = mockForRoot.mock.calls[0] as
    | [{ validate?: (config: unknown) => unknown }]
    | undefined;
  const options = firstCall?.[0];

  expect(options?.isGlobal).toBe(true);
  expect(typeof options?.validate).toBe("function");
  expect(options?.validate?.({})).toStrictEqual({ OUTPUT_DIRECTORY: "./output" });
});
```

**Key patterns:**

- Access call history via `.mock.calls[index]`
- Type the call arguments array explicitly to ensure safety
- Use optional chaining for nested properties
- Verify both the fact of the call and its arguments

## Anti-Patterns to Avoid

❌ **Don't declare services inside the hook:**

```ts
// BAD: Variable scoped to the hook only — not accessible to tests
beforeAll(async () => {
  let command: MyCommand; // ❌ Only accessible here
  const module = await Test.createTestingModule({ ... }).compile();
  command = module.get(MyCommand);
});

it("uses command", () => {
  command.run(); // ❌ ReferenceError: command is not defined
});
```

✅ **Do declare outside, instantiate inside:**

```ts
// GOOD: Declared at describe scope, instantiated in hook
let command: MyCommand;

beforeAll(async () => {
  const module = await Test.createTestingModule({ ... }).compile();
  command = module.get(MyCommand); // ✅ Available to all tests
});

it("uses command", () => {
  command.run(); // ✅ Works
});
```

---

❌ **Don't create manual stub objects:**

```ts
// BAD: High maintenance, goes out of sync with source
const mockService = {
  log: vi.fn(),
  error: vi.fn(),
};
```

✅ **Do use `createMock<T>()`:**

```ts
// GOOD: Automatically stays in sync
const mockService = createMock<LoggerService>();
```

---

❌ **Don't put repository mocks in `imports:`:**

```ts
// BAD: Mocks belong in providers
const module = await Test.createTestingModule({
  imports: [createMock<Repository<MyEntity>>()],
}).compile();
```

✅ **Do use `getRepositoryToken()` in providers:**

```ts
// GOOD: Uses proper DI provider pattern
{
  provide: getRepositoryToken(MyEntity),
  useValue: createMock<Repository<MyEntity>>(),
}
```

---

❌ **Don't forget type annotations for mocks:**

```ts
// BAD: Type checker can't verify safe calls
const repository = module.get(getRepositoryToken(MyEntity));
repository.findOneBy.mockResolvedValue(data); // Unsafe
```

✅ **Do annotate mocks with `DeepMocked<T>`:**

```ts
// GOOD: Type safe and ESLint compliant
const repository = module.get(getRepositoryToken(MyEntity)) as DeepMocked<Repository<MyEntity>>;
repository.findOneBy.mockResolvedValue(data); // Type safe
```

## References

- [Testing Strategy](../../skills/testing-strategy/SKILL.md)
- [@golevelup/ts-vitest docs](https://github.com/golevelup/ts-vitest)
- [Vitest API](https://vitest.dev/api/)
- [NestJS Testing](https://docs.nestjs.com/fundamentals/testing)
