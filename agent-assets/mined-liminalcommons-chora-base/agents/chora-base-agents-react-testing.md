---
sap_id: SAP-021
version: 1.0.0
status: active
last_updated: 2025-11-05
type: reference
audience: agents
complexity: intermediate
estimated_reading_time: 10
progressive_loading:
  phase_1: "lines 1-220"   # Quick Reference + Core Workflows
  phase_2: "lines 221-420" # Advanced Testing Patterns
  phase_3: "full"          # Complete including best practices
phase_1_token_estimate: 4500
phase_2_token_estimate: 9000
phase_3_token_estimate: 11500
---

# React Testing & Quality (SAP-021) - Agent Awareness

**SAP ID**: SAP-021
**Last Updated**: 2025-11-05
**Audience**: Generic AI Coding Agents

---

## 📖 Quick Reference

**New to SAP-021?** → Read **[README.md](README.md)** first (10-min read)

The README provides:
- 🚀 **Quick Start** - 3-minute setup (Vitest + RTL + MSW installation) with complete test suite
- 📚 **Time Savings** - 85% setup time reduction (30 min vs manual), 4x faster than Jest, 60-80% more bugs caught
- 🎯 **React Testing Library** - Accessible queries, user event simulation, async testing patterns
- 🔧 **MSW v2 API Mocking** - Network-level mocking with http handlers for API testing
- 📊 **Coverage Thresholds** - 80% lines/functions, 75% branches with v8 provider
- 🔗 **Integration** - Works with SAP-020 (Foundation), SAP-022 (Linting), SAP-023 (State), SAP-005 (CI/CD), SAP-039 (E2E)

This AGENTS.md provides: Agent-specific patterns for React testing workflows.

---

## Quick Reference

### When to Use

**Use React Testing (SAP-021) when**:
- Adding tests to React projects from SAP-020
- Setting up testing infrastructure (Vitest, React Testing Library)
- Writing component, hook, and integration tests
- Implementing API mocking with MSW v2
- Configuring test coverage thresholds for CI/CD
- Establishing testing standards for React teams

**Don't use when**:
- Need E2E testing only (use Playwright/Cypress - future SAP-027)
- Testing React Native apps (different patterns)
- Working with React <18 (older Testing Library patterns)
- Need visual regression testing (use Percy/Chromatic)
- Testing non-React projects (use language-specific testing SAPs)

### Key Technology Versions

| Technology | Version | Why This Version |
|------------|---------|------------------|
| **Vitest** | 4.0.x | 4x faster than Jest, ESM-first, native TS |
| **React Testing Library** | 16.x | Accessibility-first queries, React 19 compat |
| **MSW** | 2.x | Service Worker-based API mocking |
| **user-event** | 14.x | Realistic user interaction simulation |
| **@testing-library/jest-dom** | 6.x | Custom matchers (toBeInTheDocument, etc.) |

### Testing Philosophy (Testing Trophy)

```
        /\       E2E (10-20%) [Future: SAP-027]
       /  \
      /____\     Integration (50-60%) ← HIGHEST ROI
     /      \
    /________\   Unit (20-30%)
   /__________\
Static Analysis (100% - TypeScript, ESLint)
```

**SAP-021 Focus**: Integration (50-60%) + Unit (20-30%)

---

## User Signal Patterns

### Testing Setup Operations

| User Says | Formal Action | Tool/Command | Notes |
|-----------|---------------|--------------|-------|
| "setup React testing" | install_testing_infrastructure() | Vitest + RTL + MSW | Full stack |
| "add Vitest" | install_vitest() | pnpm add -D vitest | Test framework |
| "configure testing" | configure_vitest() | vitest.config.ts | Config file |
| "setup MSW" | install_msw() | pnpm add -D msw@2 | API mocking |
| "run tests" | run_test_suite() | pnpm test | Execute tests |

### Test Writing Operations

| User Says | Formal Action | Tool/Command | Notes |
|-----------|---------------|--------------|-------|
| "test component" | write_component_test() | RTL render + queries | User behavior |
| "test hook" | write_hook_test() | renderHook() | Custom hooks |
| "test API integration" | write_integration_test() | MSW handlers | With mocking |
| "mock API" | create_msw_handler() | http.get(), http.post() | MSW v2 |
| "check coverage" | generate_coverage() | pnpm test --coverage | Coverage report |

### Common Variations

**Setup Requests**:
- "setup testing" / "add tests" / "configure Vitest" → install_testing_infrastructure()
- "setup mocking" / "add MSW" / "mock APIs" → install_msw()

**Test Writing**:
- "test component" / "write component test" / "add component tests" → write_component_test()
- "test hook" / "test custom hook" / "add hook tests" → write_hook_test()

---

## Common Workflows

### Workflow 1: Install Testing Infrastructure (10-20 minutes)

**User signal**: "Setup React testing", "Add Vitest and React Testing Library", "Configure testing"

**Purpose**: Install and configure comprehensive testing stack (Vitest, RTL, MSW)

**Steps**:
1. Install testing dependencies:
   ```bash
   pnpm add -D vitest @vitest/ui @vitejs/plugin-react
   pnpm add -D @testing-library/react @testing-library/jest-dom @testing-library/user-event
   pnpm add -D msw@2
   pnpm add -D jsdom
   ```

2. Create Vitest configuration (`vitest.config.ts`):
   ```typescript
   import { defineConfig } from 'vitest/config'
   import react from '@vitejs/plugin-react'
   import path from 'path'

   export default defineConfig({
     plugins: [react()],
     test: {
       environment: 'jsdom',
       globals: true,
       setupFiles: ['./src/test/setup-tests.ts'],
       coverage: {
         provider: 'v8',
         reporter: ['text', 'json', 'html'],
         exclude: [
           'node_modules/',
           '**/*.test.{ts,tsx}',
           'src/test/**',
         ],
         thresholds: {
           lines: 80,
           functions: 80,
           branches: 75,
           statements: 80,
         },
       },
     },
     resolve: {
       alias: {
         '@': path.resolve(__dirname, './src'),
       },
     },
   })
   ```

3. Create test setup file (`src/test/setup-tests.ts`):
   ```typescript
   import '@testing-library/jest-dom'
   import { cleanup } from '@testing-library/react'
   import { afterEach } from 'vitest'

   // Cleanup after each test
   afterEach(() => {
     cleanup()
   })

   // Mock window.matchMedia
   Object.defineProperty(window, 'matchMedia', {
     writable: true,
     value: vi.fn().mockImplementation(query => ({
       matches: false,
       media: query,
       onchange: null,
       addListener: vi.fn(),
       removeListener: vi.fn(),
       addEventListener: vi.fn(),
       removeEventListener: vi.fn(),
       dispatchEvent: vi.fn(),
     })),
   })
   ```

4. Add test scripts to package.json:
   ```json
   {
     "scripts": {
       "test": "vitest",
       "test:ui": "vitest --ui",
       "test:coverage": "vitest --coverage",
       "test:run": "vitest run"
     }
   }
   ```

5. Verify installation:
   ```bash
   pnpm test --version
   # Expected: Vitest 4.0.x
   ```

**Expected outcome**: Complete testing infrastructure ready, Vitest configured with coverage thresholds

**Time saved**: 3-5 hours (manual setup) → 10-20 minutes (SAP-021 guided)

---

### Workflow 2: Write Component Test (5-10 minutes)

**User signal**: "Test component", "Write component test", "Add tests for Button component"

**Purpose**: Write integration test for React component using React Testing Library

**Steps**:
1. Create test file (`src/components/ui/Button.test.tsx`):
   ```typescript
   import { render, screen } from '@testing-library/react'
   import { userEvent } from '@testing-library/user-event'
   import { describe, it, expect, vi } from 'vitest'
   import { Button } from './Button'

   describe('Button', () => {
     it('renders with correct text', () => {
       render(<Button>Click me</Button>)
       expect(screen.getByRole('button', { name: /click me/i })).toBeInTheDocument()
     })

     it('calls onClick handler when clicked', async () => {
       const user = userEvent.setup()
       const handleClick = vi.fn()
       render(<Button onClick={handleClick}>Click me</Button>)

       await user.click(screen.getByRole('button', { name: /click me/i }))

       expect(handleClick).toHaveBeenCalledTimes(1)
     })

     it('is disabled when disabled prop is true', () => {
       render(<Button disabled>Disabled</Button>)
       expect(screen.getByRole('button', { name: /disabled/i })).toBeDisabled()
     })

     it('applies variant styles', () => {
       render(<Button variant="primary">Primary</Button>)
       const button = screen.getByRole('button', { name: /primary/i })
       expect(button).toHaveClass('variant-primary')
     })
   })
   ```

2. Run test:
   ```bash
   pnpm test Button.test.tsx
   ```

3. Check coverage:
   ```bash
   pnpm test --coverage Button.test.tsx
   ```

**Expected outcome**: Component test passing, covering user behavior

**Best practices applied**:
- ✅ Use `getByRole` for accessible queries
- ✅ Test user interactions with `userEvent`
- ✅ Test behavior, not implementation
- ✅ Mock functions with `vi.fn()`

---

### Workflow 3: Write Hook Test (5-10 minutes)

**User signal**: "Test hook", "Test custom hook", "Write hook test"

**Purpose**: Test custom React hook with renderHook

**Steps**:
1. Create hook test file (`src/hooks/useCounter.test.ts`):
   ```typescript
   import { renderHook, act } from '@testing-library/react'
   import { describe, it, expect } from 'vitest'
   import { useCounter } from './useCounter'

   describe('useCounter', () => {
     it('initializes with default value', () => {
       const { result } = renderHook(() => useCounter())
       expect(result.current.count).toBe(0)
     })

     it('initializes with custom value', () => {
       const { result } = renderHook(() => useCounter(10))
       expect(result.current.count).toBe(10)
     })

     it('increments count', () => {
       const { result } = renderHook(() => useCounter())

       act(() => {
         result.current.increment()
       })

       expect(result.current.count).toBe(1)
     })

     it('decrements count', () => {
       const { result } = renderHook(() => useCounter(5))

       act(() => {
         result.current.decrement()
       })

       expect(result.current.count).toBe(4)
     })

     it('resets count to initial value', () => {
       const { result } = renderHook(() => useCounter(10))

       act(() => {
         result.current.increment()
         result.current.increment()
         result.current.reset()
       })

       expect(result.current.count).toBe(10)
     })
   })
   ```

2. Run hook test:
   ```bash
   pnpm test useCounter.test.ts
   ```

**Expected outcome**: Hook test passing, covering all hook operations

---

### Workflow 4: Setup MSW for API Mocking (15-25 minutes)

**User signal**: "Setup MSW", "Mock APIs", "Add API mocking"

**Purpose**: Configure Mock Service Worker v2 for API mocking in tests

**Steps**:
1. Install MSW:
   ```bash
   pnpm add -D msw@2
   ```

2. Initialize MSW:
   ```bash
   pnpm dlx msw@2 init public/ --save
   ```

3. Create MSW handlers (`src/test/mocks/handlers.ts`):
   ```typescript
   import { http, HttpResponse } from 'msw'

   export const handlers = [
     // GET /api/users
     http.get('/api/users', () => {
       return HttpResponse.json([
         { id: 1, name: 'Alice', email: 'alice@example.com' },
         { id: 2, name: 'Bob', email: 'bob@example.com' },
       ])
     }),

     // POST /api/users
     http.post('/api/users', async ({ request }) => {
       const newUser = await request.json()
       return HttpResponse.json(
         { id: 3, ...newUser },
         { status: 201 }
       )
     }),

     // GET /api/users/:id
     http.get('/api/users/:id', ({ params }) => {
       const { id } = params
       return HttpResponse.json({
         id: Number(id),
         name: 'Alice',
         email: 'alice@example.com',
       })
     }),

     // Error handler
     http.get('/api/error', () => {
       return HttpResponse.json(
         { message: 'Internal Server Error' },
         { status: 500 }
       )
     }),
   ]
   ```

4. Create MSW server (`src/test/mocks/server.ts`):
   ```typescript
   import { setupServer } from 'msw/node'
   import { handlers } from './handlers'

   export const server = setupServer(...handlers)
   ```

5. Setup MSW in test setup (`src/test/setup-tests.ts`):
   ```typescript
   import '@testing-library/jest-dom'
   import { cleanup } from '@testing-library/react'
   import { afterEach, beforeAll, afterAll } from 'vitest'
   import { server } from './mocks/server'

   // Start MSW server before all tests
   beforeAll(() => server.listen({ onUnhandledRequest: 'error' }))

   // Reset handlers after each test
   afterEach(() => {
     server.resetHandlers()
     cleanup()
   })

   // Close MSW server after all tests
   afterAll(() => server.close())
   ```

6. Test with MSW:
   ```typescript
   import { render, screen, waitFor } from '@testing-library/react'
   import { describe, it, expect } from 'vitest'
   import { UserList } from './UserList'

   describe('UserList', () => {
     it('fetches and displays users', async () => {
       render(<UserList />)

       await waitFor(() => {
         expect(screen.getByText(/alice/i)).toBeInTheDocument()
         expect(screen.getByText(/bob/i)).toBeInTheDocument()
       })
     })
   })
   ```

**Expected outcome**: MSW configured, API requests mocked in tests

---

### Workflow 5: Write Integration Test with API Mocking (10-20 minutes)

**User signal**: "Test API integration", "Write integration test", "Test component with API"

**Purpose**: Write integration test for component that fetches data from API

**Steps**:
1. Create integration test (`src/features/users/UserList.test.tsx`):
   ```typescript
   import { render, screen, waitFor } from '@testing-library/react'
   import { userEvent } from '@testing-library/user-event'
   import { describe, it, expect, beforeEach } from 'vitest'
   import { http, HttpResponse } from 'msw'
   import { server } from '@/test/mocks/server'
   import { UserList } from './UserList'
   import { QueryProvider } from '@/components/providers/query-provider'

   function renderWithProviders(ui: React.ReactElement) {
     return render(<QueryProvider>{ui}</QueryProvider>)
   }

   describe('UserList Integration', () => {
     it('displays users from API', async () => {
       renderWithProviders(<UserList />)

       // Initially shows loading state
       expect(screen.getByText(/loading/i)).toBeInTheDocument()

       // After API response, shows users
       await waitFor(() => {
         expect(screen.getByText(/alice/i)).toBeInTheDocument()
         expect(screen.getByText(/bob/i)).toBeInTheDocument()
       })

       // Loading state removed
       expect(screen.queryByText(/loading/i)).not.toBeInTheDocument()
     })

     it('handles API errors', async () => {
       // Override handler for this test
       server.use(
         http.get('/api/users', () => {
           return HttpResponse.json(
             { message: 'Server Error' },
             { status: 500 }
           )
         })
       )

       renderWithProviders(<UserList />)

       await waitFor(() => {
         expect(screen.getByText(/error loading users/i)).toBeInTheDocument()
       })
     })

     it('refetches users when refresh button clicked', async () => {
       const user = userEvent.setup()
       renderWithProviders(<UserList />)

       // Wait for initial load
       await waitFor(() => {
         expect(screen.getByText(/alice/i)).toBeInTheDocument()
       })

       // Click refresh button
       await user.click(screen.getByRole('button', { name: /refresh/i }))

       // Should show loading state again
       expect(screen.getByText(/loading/i)).toBeInTheDocument()

       // Then show users again
       await waitFor(() => {
         expect(screen.getByText(/alice/i)).toBeInTheDocument()
       })
     })
   })
   ```

2. Run integration test:
   ```bash
   pnpm test UserList.test.tsx
   ```

**Expected outcome**: Integration test passing, testing full user flow with API

**Integration test benefits**:
- Tests real user scenarios
- Catches integration bugs
- Higher confidence than unit tests
- 50-60% of test suite should be integration

---

## Best Practices

### Practice 1: Use Integration Tests Over Unit Tests

**Pattern**:
```typescript
// ✅ GOOD: Integration test (50-60% of tests)
it('fetches and displays users', async () => {
  render(<UserList />)
  await waitFor(() => {
    expect(screen.getByText(/alice/i)).toBeInTheDocument()
  })
})

// ⚠️ OK: Unit test (20-30% of tests)
it('formats user name', () => {
  expect(formatUserName({ first: 'John', last: 'Doe' })).toBe('John Doe')
})
```

**Why**: Integration tests provide higher ROI, catch more bugs

---

### Practice 2: Use Accessible Queries (getByRole First)

**Pattern**:
```typescript
// ✅ BEST: getByRole (accessible)
screen.getByRole('button', { name: /submit/i })
screen.getByRole('textbox', { name: /email/i })

// ⚠️ OK: getByLabelText (forms)
screen.getByLabelText(/email/i)

// ❌ LAST RESORT: getByTestId
screen.getByTestId('submit-btn')
```

**Why**: Accessible queries ensure components work with screen readers

---

### Practice 3: Use userEvent Over fireEvent

**Pattern**:
```typescript
// ✅ GOOD: userEvent (realistic)
const user = userEvent.setup()
await user.click(button)
await user.type(input, 'hello')

// ❌ BAD: fireEvent (low-level)
fireEvent.click(button)
fireEvent.change(input, { target: { value: 'hello' } })
```

**Why**: userEvent simulates realistic user interactions (focus, blur, keyboard events)

---

### Practice 4: Mock APIs with MSW, Not axios.mock

**Pattern**:
```typescript
// ✅ GOOD: MSW (network-level mocking)
http.get('/api/users', () => {
  return HttpResponse.json([...])
})

// ❌ BAD: axios mock (implementation coupling)
axios.get = vi.fn().mockResolvedValue({ data: [...] })
```

**Why**: MSW mocks at network level, works with any HTTP client

---

### Practice 5: Set Coverage Thresholds in Config

**Pattern**:
```typescript
// vitest.config.ts
coverage: {
  thresholds: {
    lines: 80,
    functions: 80,
    branches: 75,
    statements: 80,
  },
}
```

**Why**: Enforces minimum coverage, prevents coverage regression

---

## Common Pitfalls

### Pitfall 1: Testing Implementation Details

**Problem**: Test internal state instead of user behavior

**Fix**: Test what user sees/does

```typescript
// ❌ BAD: Tests implementation
expect(wrapper.state('count')).toBe(1)

// ✅ GOOD: Tests user-visible behavior
expect(screen.getByText(/count: 1/i)).toBeInTheDocument()
```

**Why**: Implementation can change, user behavior stays same

---

### Pitfall 2: Using getByTestId Instead of getByRole

**Problem**: Use data-testid everywhere

**Fix**: Use accessible queries

```typescript
// ❌ BAD: data-testid (not accessible)
screen.getByTestId('submit-btn')

// ✅ GOOD: getByRole (accessible)
screen.getByRole('button', { name: /submit/i })
```

**Why**: Accessible queries improve component accessibility

---

### Pitfall 3: Not Cleaning Up After Tests

**Problem**: Tests affect each other, flaky results

**Fix**: Always cleanup

```typescript
// In setup-tests.ts
afterEach(() => {
  cleanup()
  server.resetHandlers()
})
```

**Why**: Clean state for each test, no cross-test pollution

---

### Pitfall 4: Forgetting to Wait for Async Updates

**Problem**: Test fails because data not loaded yet

**Fix**: Use waitFor

```typescript
// ❌ BAD: Doesn't wait for async
expect(screen.getByText(/alice/i)).toBeInTheDocument()

// ✅ GOOD: Waits for async update
await waitFor(() => {
  expect(screen.getByText(/alice/i)).toBeInTheDocument()
})
```

**Why**: API calls are async, need to wait for DOM updates

---

### Pitfall 5: Not Wrapping Components with Providers

**Problem**: Test fails because missing TanStack Query provider

**Fix**: Wrap with providers

```typescript
// ❌ BAD: Missing provider
render(<UserList />)

// ✅ GOOD: Wrapped with provider
function renderWithProviders(ui: React.ReactElement) {
  return render(<QueryProvider>{ui}</QueryProvider>)
}
renderWithProviders(<UserList />)
```

**Why**: Many components depend on context providers

---

## Integration with Other SAPs

### SAP-020 (react-foundation)
- React project structure and TypeScript configuration
- Integration: SAP-021 adds testing to SAP-020 projects

### SAP-022 (react-linting)
- ESLint configuration including testing-library plugin
- Integration: SAP-022 enforces testing best practices via linting

### SAP-023 (react-state-management)
- TanStack Query and Zustand testing patterns
- Integration: SAP-021 provides test utilities for state management

### SAP-024 (react-styling)
- Testing styled components
- Integration: SAP-021 tests style application, not CSS specifics

### SAP-025 (react-performance)
- Performance testing patterns
- Integration: SAP-021 baseline, SAP-025 adds performance tests

---

## Support & Resources

**SAP-021 Documentation**:
- [Capability Charter](capability-charter.md) - React testing problem and scope
- [Protocol Spec](protocol-spec.md) - Technical contracts and patterns
- [Awareness Guide](awareness-guide.md) - Detailed workflows
- [Adoption Blueprint](adoption-blueprint.md) - Installation guide
- [Ledger](ledger.md) - Adoption tracking

**External Resources**:
- [Vitest Docs](https://vitest.dev)
- [React Testing Library Docs](https://testing-library.com/react)
- [MSW v2 Docs](https://mswjs.io)
- [Kent C. Dodds Testing Blog](https://kentcdodds.com/blog/common-mistakes-with-react-testing-library)

**Related SAPs**:
- [SAP-020 (react-foundation)](../react-foundation/) - React project setup
- [SAP-022 (react-linting)](../react-linting/) - Linting and formatting
- [SAP-023 (react-state-management)](../react-state-management/) - State patterns
- [SAP-027 (react-e2e-testing)](../react-e2e-testing/) - Future E2E testing SAP

---

## Version History

- **1.0.0** (2025-11-05): Initial AGENTS.md for SAP-021
  - 5 workflows: Install Testing Infrastructure, Write Component Test, Write Hook Test, Setup MSW for API Mocking, Write Integration Test with API Mocking
  - 2 user signal pattern tables (Testing Setup Operations with 5 signals, Test Writing Operations with 5 signals)
  - 5 best practices, 5 common pitfalls
  - Integration with SAP-020, SAP-022, SAP-023, SAP-024, SAP-025

---

**Next Steps**:
1. Read [CLAUDE.md](CLAUDE.md) for Claude Code-specific patterns
2. Review [protocol-spec.md](protocol-spec.md) for technical contracts
3. Check [adoption-blueprint.md](adoption-blueprint.md) for installation
4. Install: `pnpm add -D vitest @testing-library/react msw@2`
