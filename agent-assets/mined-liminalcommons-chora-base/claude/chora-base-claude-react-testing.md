---
sap_id: SAP-021
version: 1.0.0
status: active
last_updated: 2025-11-05
type: reference
audience: claude_code
complexity: intermediate
estimated_reading_time: 8
progressive_loading:
  phase_1: "lines 1-180"   # Quick Start + Core Workflows
  phase_2: "lines 181-300" # Advanced Patterns
  phase_3: "full"          # Complete including tips and pitfalls
phase_1_token_estimate: 3500
phase_2_token_estimate: 7000
phase_3_token_estimate: 9500
---

# React Testing & Quality (SAP-021) - Claude-Specific Awareness

**SAP ID**: SAP-021
**Claude Compatibility**: Sonnet 4.5+
**Last Updated**: 2025-11-05

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

This CLAUDE.md provides: Claude Code-specific workflows using Bash (testing), Write (test files), Read (verification).

---

## Quick Start for Claude

This file provides **Claude Code-specific patterns** for React testing with Vitest and React Testing Library.

### First-Time Session

1. Read [AGENTS.md](AGENTS.md) for generic React testing workflows
2. Use this file for Claude Code tool integration (Bash for running tests, Write for test files, Read for verification)
3. Always check if project has existing test setup before installing

### Test Running Commands

```bash
# Run all tests
Bash: pnpm test

# Run specific test file
Bash: pnpm test Button.test.tsx

# Run with coverage
Bash: pnpm test --coverage

# Run in watch mode
Bash: pnpm test --watch

# Run with UI
Bash: pnpm test --ui
```

---

## Claude Code React Testing Workflows

### Workflow 1: Installing Testing Infrastructure with Bash and Write

```markdown
User: "Setup React testing with Vitest"

Claude (Phase 1: Install Dependencies - 0-10k tokens):
1. Install testing packages:
   Bash: pnpm add -D vitest @vitest/ui @vitejs/plugin-react @testing-library/react @testing-library/jest-dom @testing-library/user-event msw@2 jsdom

Claude (Phase 2: Create Config Files - 10-30k tokens):
2. Create Vitest config:
   Write vitest.config.ts
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
         exclude: ['node_modules/', '**/*.test.{ts,tsx}', 'src/test/**'],
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

3. Create test directory:
   Bash: mkdir -p src/test/mocks

4. Create test setup file:
   Write src/test/setup-tests.ts
   ```typescript
   import '@testing-library/jest-dom'
   import { cleanup } from '@testing-library/react'
   import { afterEach, beforeAll, afterAll } from 'vitest'
   import { server } from './mocks/server'

   beforeAll(() => server.listen({ onUnhandledRequest: 'error' }))
   afterEach(() => {
     server.resetHandlers()
     cleanup()
   })
   afterAll(() => server.close())

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

5. Create MSW handlers:
   Write src/test/mocks/handlers.ts
   ```typescript
   import { http, HttpResponse } from 'msw'

   export const handlers = [
     http.get('/api/users', () => {
       return HttpResponse.json([
         { id: 1, name: 'Alice', email: 'alice@example.com' },
         { id: 2, name: 'Bob', email: 'bob@example.com' },
       ])
     }),
   ]
   ```

6. Create MSW server:
   Write src/test/mocks/server.ts
   ```typescript
   import { setupServer } from 'msw/node'
   import { handlers } from './handlers'

   export const server = setupServer(...handlers)
   ```

Claude (Phase 3: Update package.json - 30-40k tokens):
7. Read current package.json:
   Read package.json

8. Add test scripts:
   Edit package.json
   # Add scripts section with test commands

9. Verify installation:
   Bash: pnpm test --version

Claude (response to user):
"✅ React testing infrastructure installed!

**Installed**:
- Vitest 4.0.x (4x faster than Jest)
- React Testing Library 16.x
- MSW 2.x (API mocking)
- @testing-library/user-event 14.x

**Configuration**:
- vitest.config.ts - Vitest config with coverage thresholds (80%)
- src/test/setup-tests.ts - Test setup with MSW
- src/test/mocks/ - MSW handlers for API mocking

**Run tests**:
```bash
pnpm test              # Run all tests
pnpm test --coverage   # With coverage report
pnpm test --ui         # Visual test UI
```

**Next steps**:
1. Write first component test
2. Add MSW handlers for your API endpoints
3. Configure coverage thresholds for CI/CD"

Result: Complete testing infrastructure installed and configured
```

---

### Workflow 2: Writing Component Test with Write

```markdown
User: "Write a test for the Button component"

Claude (Phase 1: Read Component - 0-10k tokens):
1. Read Button component to understand interface:
   Read src/components/ui/Button.tsx

Claude (Phase 2: Write Test - 10-25k tokens):
2. Create test file:
   Write src/components/ui/Button.test.tsx
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

Claude (Phase 3: Run Test - 25-35k tokens):
3. Run test to verify:
   Bash: pnpm test Button.test.tsx

4. Check coverage:
   Bash: pnpm test Button.test.tsx --coverage

Claude (response to user):
"✅ Button component test created and passing!

**Test coverage**:
- Rendering with text ✅
- onClick handler ✅
- Disabled state ✅
- Variant styles ✅

**Test results**:
```
✓ Button (4 tests)
  ✓ renders with correct text
  ✓ calls onClick handler when clicked
  ✓ is disabled when disabled prop is true
  ✓ applies variant styles

Coverage: 95% statements, 90% branches
```

**Best practices applied**:
- ✅ Use getByRole for accessibility
- ✅ Test user behavior, not implementation
- ✅ Use userEvent for realistic interactions
- ✅ Mock functions with vi.fn()"

Result: Component test written and passing
```

---

### Workflow 3: Writing Integration Test with MSW

```markdown
User: "Test the UserList component that fetches users from API"

Claude (Phase 1: Read Component - 0-10k tokens):
1. Read UserList component:
   Read src/features/users/UserList.tsx

Claude (Phase 2: Check MSW Handlers - 10-20k tokens):
2. Check if MSW handler exists:
   Read src/test/mocks/handlers.ts

3. If handler missing, add it:
   Edit src/test/mocks/handlers.ts
   # Add http.get('/api/users', ...) handler

Claude (Phase 3: Write Integration Test - 20-40k tokens):
4. Create integration test:
   Write src/features/users/UserList.test.tsx
   ```typescript
   import { render, screen, waitFor } from '@testing-library/react'
   import { userEvent } from '@testing-library/user-event'
   import { describe, it, expect } from 'vitest'
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

       expect(screen.getByText(/loading/i)).toBeInTheDocument()

       await waitFor(() => {
         expect(screen.getByText(/alice/i)).toBeInTheDocument()
         expect(screen.getByText(/bob/i)).toBeInTheDocument()
       })

       expect(screen.queryByText(/loading/i)).not.toBeInTheDocument()
     })

     it('handles API errors', async () => {
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

       await waitFor(() => {
         expect(screen.getByText(/alice/i)).toBeInTheDocument()
       })

       await user.click(screen.getByRole('button', { name: /refresh/i }))

       expect(screen.getByText(/loading/i)).toBeInTheDocument()

       await waitFor(() => {
         expect(screen.getByText(/alice/i)).toBeInTheDocument()
       })
     })
   })
   ```

5. Run integration test:
   Bash: pnpm test UserList.test.tsx

Claude (response to user):
"✅ Integration test for UserList created and passing!

**Test scenarios**:
- Fetches and displays users from API ✅
- Handles API errors gracefully ✅
- Refetches users on refresh ✅

**Test results**:
```
✓ UserList Integration (3 tests)
  ✓ displays users from API
  ✓ handles API errors
  ✓ refetches users when refresh button clicked

Duration: 850ms
```

**Integration test benefits**:
- Tests real user flow (loading → data → interactions)
- Uses MSW for realistic API mocking
- Tests with providers (TanStack Query)
- Higher confidence than unit tests"

Result: Integration test written with API mocking
```

---

## Claude-Specific Tips

### Tip 1: Always Read Component Before Writing Test

**Pattern**:
```markdown
# Before writing test:
Read src/components/ui/Button.tsx
# Understand props, variants, behavior

# Then write test:
Write src/components/ui/Button.test.tsx
```

**Why**: Understand component interface before testing

---

### Tip 2: Use Bash to Run Tests Immediately After Writing

**Pattern**:
```markdown
# After writing test file:
Write src/components/Button.test.tsx

# Immediately run test:
Bash: pnpm test Button.test.tsx

# Verify it passes, then check coverage:
Bash: pnpm test Button.test.tsx --coverage
```

**Why**: Catch errors early, verify test passes

---

### Tip 3: Check for Existing MSW Handlers Before Adding

**Pattern**:
```markdown
# Before adding MSW handler:
Read src/test/mocks/handlers.ts
# Check if endpoint already mocked

# If missing, use Edit to add:
Edit src/test/mocks/handlers.ts
# Add new handler to handlers array
```

**Why**: Avoid duplicate handlers, reuse existing mocks

---

### Tip 4: Use Write for New Tests, Edit for Updating

**Pattern**:
```markdown
# New test file → Write:
Write src/components/Button.test.tsx

# Add test case to existing file → Edit:
Edit src/components/Button.test.tsx
# old_string: Last test case
# new_string: Last test case + new test case
```

**Why**: Write for new files, Edit for modifications

---

### Tip 5: Run Coverage to Verify Test Completeness

**Pattern**:
```markdown
# After writing tests:
Bash: pnpm test Button.test.tsx --coverage

# Check coverage output:
# Coverage: 95% statements, 90% branches, 85% lines

# If coverage low, add missing test cases
```

**Why**: Ensure comprehensive test coverage

---

## Common Pitfalls for Claude Code

### Pitfall 1: Not Running Tests After Writing Them

**Problem**: Write test but don't verify it passes

**Fix**: Always run tests immediately

```markdown
# ❌ BAD: Write test without running
Write Button.test.tsx

# ✅ GOOD: Write and verify
Write Button.test.tsx
Bash: pnpm test Button.test.tsx
```

**Why**: Catch syntax errors and test failures early

---

### Pitfall 2: Forgetting to Wrap with Providers in Integration Tests

**Problem**: Integration test fails because missing QueryProvider

**Fix**: Always include renderWithProviders helper

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

### Pitfall 3: Not Checking if MSW Handler Already Exists

**Problem**: Add duplicate MSW handler, causes conflicts

**Fix**: Read handlers file first

```markdown
# Before adding handler:
Read src/test/mocks/handlers.ts

# Then add if missing:
Edit src/test/mocks/handlers.ts
```

**Why**: Avoid duplicate handlers, reuse existing mocks

---

### Pitfall 4: Using fireEvent Instead of userEvent

**Problem**: Use fireEvent which doesn't simulate real user interactions

**Fix**: Always use userEvent

```typescript
// ❌ BAD: fireEvent (low-level)
fireEvent.click(button)

// ✅ GOOD: userEvent (realistic)
const user = userEvent.setup()
await user.click(button)
```

**Why**: userEvent simulates realistic interactions (focus, blur, keyboard)

---

### Pitfall 5: Not Using waitFor for Async Operations

**Problem**: Test fails because data not loaded yet

**Fix**: Use waitFor

```typescript
// ❌ BAD: No wait
expect(screen.getByText(/alice/i)).toBeInTheDocument()

// ✅ GOOD: Wait for async
await waitFor(() => {
  expect(screen.getByText(/alice/i)).toBeInTheDocument()
})
```

**Why**: API calls are async, need to wait for DOM updates

---

## Support & Resources

**SAP-021 Documentation**:
- [AGENTS.md](AGENTS.md) - Generic React testing workflows
- [Capability Charter](capability-charter.md) - React testing problem and scope
- [Protocol Spec](protocol-spec.md) - Technical contracts and patterns
- [Awareness Guide](awareness-guide.md) - Detailed workflows
- [Adoption Blueprint](adoption-blueprint.md) - Installation guide
- [Ledger](ledger.md) - Adoption tracking

**External Resources**:
- [Vitest Docs](https://vitest.dev)
- [React Testing Library Docs](https://testing-library.com/react)
- [MSW v2 Docs](https://mswjs.io)

**Related SAPs**:
- [SAP-020 (react-foundation)](../react-foundation/) - React project setup
- [SAP-022 (react-linting)](../react-linting/) - Linting and formatting
- [SAP-023 (react-state-management)](../react-state-management/) - State patterns

---

## Version History

- **1.0.0** (2025-11-05): Initial CLAUDE.md for SAP-021
  - 3 workflows: Installing Testing Infrastructure with Bash/Write, Writing Component Test with Write, Writing Integration Test with MSW
  - Tool patterns: Bash for running tests, Write for new test files, Read for component understanding, Edit for updates
  - 5 Claude-specific tips, 5 common pitfalls
  - Focus on test-driven workflow with immediate verification

---

**Next Steps**:
1. Read [AGENTS.md](AGENTS.md) for generic React testing workflows
2. Review [protocol-spec.md](protocol-spec.md) for technical contracts
3. Check [adoption-blueprint.md](adoption-blueprint.md) for installation
4. Install: `pnpm add -D vitest @testing-library/react msw@2`
