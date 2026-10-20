---
name: kb-testing-patterns
description: Stack-agnostic universal testing principles across the 3-layer pyramid in this repo — AAA structure, FIRST properties, mocking strategy decisions, RTL component rules (role queries, userEvent over fireEvent, anti-shallow), fixture/factory/builder data patterns, and common anti-patterns. Use when writing or reviewing tests or deciding what to mock.
last-verified: 2026-04-23
---

# Testing Patterns

> Universal principles for the 3-layer pyramid used in this repo: **Unit / Component / E2E** (per `SK.md §4.2`).
> For E2E / Playwright / browser testing → see `sk-e2e`.
> For the repo's concrete Server Action + Drizzle test patterns (factory-function mocks, `createChain()`) → see `kb-testing-nextjs` (portable) + `sk-testing-nextjs` (kit-shipped infra).

---

## 1. Testing Pyramid

```
        /\          E2E (Few — expensive, slow)
       /  \         Critical user flows only
      /----\
     /      \       Component (Some)
    /--------\      RTL + userEvent, single-component interaction
   /          \
  /------------\    Unit (Many — fast, cheap)
                    Functions, logic, server actions (with mocks)
```

| Layer         | Tool                  | Scope                                              | Speed          |
| ------------- | --------------------- | -------------------------------------------------- | -------------- |
| **Unit**      | Vitest / Jest         | Pure functions, logic, server actions w/ mocked DB | <50ms          |
| **Component** | React Testing Library | Single component + interaction                     | <200ms         |
| **E2E**       | Playwright            | Full user flows across pages, real DB, auth/RBAC   | 3-30s per spec |

> 🧭 **This repo's pyramid has 3 layers (per `SK.md §4.2`), not 4.** "Integration"-style concerns (server actions exercising DB code) are covered at the **Unit** tier using factory-function mocks to Drizzle — see `kb-testing-nextjs` for the pattern. Real-DB integration is reserved for **E2E** via the isolated Neon branch in `scripts/tools/e2e-runner.ts` (see `sk-e2e`).

---

## 2. AAA Pattern

| Step        | Purpose                 |
| ----------- | ----------------------- |
| **Arrange** | Set up test data        |
| **Act**     | Execute code under test |
| **Assert**  | Verify outcome          |

```ts
test('totalWithTax adds 16% IVA', () => {
  // Arrange
  const subtotal = 100;

  // Act
  const result = totalWithTax(subtotal);

  // Assert
  expect(result).toBe(116);
});
```

---

## 3. Test Type Selection

| Type          | Best For                                       | Speed         |
| ------------- | ---------------------------------------------- | ------------- |
| **Unit**      | Pure functions, logic, server actions w/ mocks | Fast (<50ms)  |
| **Component** | UI behavior in isolation (RTL)                 | Fast (<200ms) |
| **E2E**       | Critical user flows, real DB, auth/RBAC        | Slow          |

---

## 4. Unit Test Principles

### Good Unit Tests (FIRST)

| Principle         | Meaning                |
| ----------------- | ---------------------- |
| **F**ast          | < 100ms each           |
| **I**solated      | No external deps       |
| **R**epeatable    | Same result always     |
| **S**elf-checking | No manual verification |
| **T**imely        | Written with code      |

### What to Unit Test

| Test           | Don't Test       |
| -------------- | ---------------- |
| Business logic | Framework code   |
| Edge cases     | Third-party libs |
| Error handling | Simple getters   |

---

## 5. Component Test Principles (RTL)

### 🔴 When component tests are MANDATORY

> Issues that touch **interactive components** MUST ship with an RTL component test. No exceptions for:
>
> - `onClick` / `onChange` / `onSubmit` handlers
> - Conditional rendering based on state/props
> - Form validation UI
> - Accessible interactions (keyboard, ARIA)
>
> **Purely presentational components** (no handlers, no state) can skip — but state that explicitly.

### Key rules

- **Test behavior, not implementation.** Assert against visible DOM / a11y tree, not internal state.
- **Use `@testing-library/user-event`** over `fireEvent` for realistic interactions.
- **Query by role first** (`getByRole`), then label, then text. `getByTestId` only when no semantic option.
- **Shallow test anti-pattern:** `expect(Component).toBeDefined()` catches zero bugs. Avoid.
- **Cleanup between tests:** `afterEach(cleanup)` in setup file — otherwise DOM accumulates across tests.

### Minimal template

```tsx
import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

import { MyComponent } from '@/components/MyComponent';

describe('MyComponent', () => {
  it('triggers handler on click', async () => {
    const user = userEvent.setup();
    const handler = vi.fn();

    render(<MyComponent onAction={handler}>Label</MyComponent>);
    await user.click(screen.getByRole('button', { name: 'Label' }));

    expect(handler).toHaveBeenCalledTimes(1);
  });
});
```

---

## 6. Server-action / "integration-style" unit tests

> In this repo, server actions are tested at the **Unit** tier using factory-function mocks to Drizzle and `@/lib/auth` — not real DB. Real-DB exercise happens in E2E. See `kb-testing-nextjs` for the concrete pattern (`vi.mock('@/lib/auth', () => ({ auth: () => mockSession }))`, `createChain()` helper, schema-module mocks, `ActionResult` assertions).

### What to cover at this tier

| Area              | Focus                                           |
| ----------------- | ----------------------------------------------- |
| Server actions    | Input validation → DB call shape → side effects |
| Auth/RBAC gates   | Unauthorized path returns expected error shape  |
| External services | Contract mocks (email, push, etc.)              |

### Setup discipline

| Phase        | Action                                                     |
| ------------ | ---------------------------------------------------------- |
| `beforeEach` | Reset mocks (`vi.resetAllMocks()` or per-mock `mockReset`) |
| `afterEach`  | Clear any module-level state                               |

---

## 7. Mocking Principles

### When to Mock

| Mock            | Don't Mock          |
| --------------- | ------------------- |
| External APIs   | The code under test |
| Database (unit) | Simple dependencies |
| Time/random     | Pure functions      |
| Network         | In-memory stores    |

### Mock Types

| Type | Use                       |
| ---- | ------------------------- |
| Stub | Return fixed values       |
| Spy  | Track calls               |
| Mock | Set expectations          |
| Fake | Simplified implementation |

---

## 8. Test Organization

### Naming

| Pattern         | Example                       |
| --------------- | ----------------------------- |
| Should behavior | "should return error when..." |
| When condition  | "when user not found..."      |
| Given-when-then | "given X, when Y, then Z"     |

### Grouping

| Level      | Use                 |
| ---------- | ------------------- |
| describe   | Group related tests |
| it/test    | Individual case     |
| beforeEach | Common setup        |

---

## 9. Test Data

### Strategies

| Approach  | Use                    |
| --------- | ---------------------- |
| Factories | Generate test data     |
| Fixtures  | Predefined datasets    |
| Builders  | Fluent object creation |

### Principles

- Use realistic data
- Randomize non-essential values (faker)
- Share common fixtures
- Keep data minimal

---

## 10. Best Practices

| Practice            | Why                  |
| ------------------- | -------------------- |
| One assert per test | Clear failure reason |
| Independent tests   | No order dependency  |
| Fast tests          | Run frequently       |
| Descriptive names   | Self-documenting     |
| Clean up            | Avoid side effects   |

---

## 11. Anti-Patterns

| ❌ Don't                               | ✅ Do                      |
| -------------------------------------- | -------------------------- |
| Test implementation                    | Test behavior              |
| Duplicate test code                    | Use factories              |
| Complex test setup                     | Simplify or split          |
| Ignore flaky tests                     | Fix root cause             |
| Skip cleanup                           | Reset state                |
| `expect(X).toBeDefined()` as real test | Assert observable behavior |

---

> **Remember:** Tests are documentation. If someone can't understand what the code does from the tests, rewrite them.

---

_Cross-reference: `sk-e2e` for E2E, Playwright, stability rules, and RBAC verification patterns. `kb-testing-nextjs` (portable) + `sk-testing-nextjs` (kit-shipped infra) for Next.js server actions + Drizzle-typed factories + real-DB integration tests._
