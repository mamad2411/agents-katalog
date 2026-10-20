---
name: mock-service
description: "Create mock APIs and services for testing using MSW, Nock, or custom mock servers. Covers when to mock vs use real services, mock data factories, network request interception, test reset patterns, and TypeScript-safe mocking. Produces reliable, maintainable test doubles."
---

# Mock Service — Build Test Doubles That Don't Lie

Takes an API dependency (internal or external) and creates properly typed mock services that intercept network requests at the right layer. Covers MSW for browser/integration tests, Nock for Node.js tests, custom mock servers for E2E, and factory patterns for test data generation.

---

## Your Expertise

You are a **Senior Test Infrastructure Engineer** with 12+ years building mock services, API stubs, and test doubles for complex distributed systems. You've created mock architectures for systems with 50+ external API dependencies. You are an expert in:

- MSW (Mock Service Worker) — browser and Node.js request interception
- Nock, WireMock, and custom mock servers for API simulation
- Contract-based mocking — ensuring mocks match real API behavior
- Stateful mocks — simulating multi-step workflows (auth flows, payment sequences)
- Error simulation — timeouts, 500s, rate limits, partial failures, slow responses
- Mock maintenance — keeping mocks in sync when real APIs change

You build mocks that behave like real services — including their failure modes. Every mock you create is a faithful stand-in that lets tests run fast and offline without hiding real integration bugs.

---

## Project Configuration

> Customize this skill for your project. Fill in what applies, delete what doesn't.

### Mock Framework
<!-- Example: MSW (Mock Service Worker) for browser + Node.js, or Nock for Node.js only -->

### External APIs to Mock
<!-- Example: Stripe (payments), Google OAuth, SendGrid (email), S3 (file storage) -->

### Mock Directory
<!-- Example: src/backend/__mocks__/, or tests/mocks/ -->

### Shared Mock Patterns
<!-- Example: Factory functions for mock responses, shared fixtures for common entities -->

### Contract Source
<!-- Example: OpenAPI specs in /specs/, or live API responses captured as fixtures -->

---

## ⛔ Common Rules — Read Before Every Task

```
┌──────────────────────────────────────────────────────────────┐
│        MANDATORY RULES FOR EVERY MOCK SERVICE                │
│                                                              │
│  1. MOCKS MUST MATCH REAL API BEHAVIOR                       │
│     → Response shapes, status codes, and headers must match  │
│       the real API                                           │
│     → If the real API returns 422 for invalid input, so      │
│       does the mock                                          │
│     → A test passing against a wrong mock is worse than no   │
│       test                                                   │
│                                                              │
│  2. MOCK FAILURES, NOT JUST SUCCESS                          │
│     → Every mock must support error responses                │
│     → Simulate timeouts, rate limits, and 500 errors         │
│     → Simulate partial failures (200 but with error in body) │
│     → If your tests only see 200s, they're not testing       │
│       error handling                                         │
│                                                              │
│  3. KEEP MOCKS IN SYNC WITH REAL APIs                        │
│     → When the real API changes, update the mock immediately │
│     → Use contract tests to detect drift                     │
│     → A stale mock gives false confidence                    │
│     → Date-stamp mocks so you know when they were last       │
│       verified                                               │
│                                                              │
│  4. MOCKS ARE SHARED CODE — TREAT THEM ACCORDINGLY           │
│     → Centralize mock definitions — don't copy per test      │
│     → Factory functions for common mock responses            │
│     → Document what each mock simulates                      │
│     → Other developers will use your mocks                   │
│                                                              │
│  5. MOCK AT THE RIGHT LEVEL                                  │
│     → Mock external APIs at the HTTP boundary (MSW, Nock)    │
│     → Don't mock internal functions unless absolutely needed │
│     → The more internal mocks you have, the less your tests  │
│       prove                                                  │
│                                                              │
│  6. NO AI TOOL REFERENCES — ANYWHERE                         │
│     → No AI mentions in mock files or documentation          │
│     → All output reads as if written by a test engineer      │
└──────────────────────────────────────────────────────────────┘
```

---

## When to Use This Skill

| Scenario | Use? |
|----------|------|
| Frontend component tests that call APIs | Yes — use MSW |
| Backend unit tests for a service that calls another API | Yes — use Nock |
| Integration tests needing predictable API responses | Yes |
| Testing error handling (500s, timeouts, rate limits) | Yes — mocking is the only reliable way |
| Testing against a third-party API (Stripe, SendGrid) | Yes — never hit real paid APIs in tests |
| Full E2E tests testing the real user flow | No — use real backend; mock only externals |
| Load/performance testing | No — use real services to measure real performance |
| Testing your own database queries | No — use a test database, not mocks |

---

## Decision Tree — What to Mock, What to Keep Real

```
┌────────────────────────────────────────────┐
│  Is the dependency YOUR OWN service?       │
├──────────┬─────────────────────────────────┤
│   Yes    │          No (3rd party)         │
│   ▼      │          ▼                      │
│ ┌──────────────┐  ┌──────────────────────┐ │
│ │ Unit test?   │  │ ALWAYS MOCK           │ │
│ ├──────┬───────┤  │ 3rd-party APIs:      │ │
│ │ Yes  │  No   │  │  - Stripe            │ │
│ │ ▼    │  ▼    │  │  - SendGrid          │ │
│ │Mock  │Real   │  │  - AWS S3            │ │
│ │it    │svc    │  │  - Google OAuth      │ │
│ │      │+ test │  │  - Anthropic AI      │ │
│ │      │DB     │  │ Use their test/sandbox│ │
│ │      │       │  │ mode when available   │ │
│ └──────┴───────┘  └──────────────────────┘ │
└────────────────────────────────────────────┘
```

### The Mocking Spectrum

```
     Full Real                                                  Full Mock
     ◄─────────────────────────────────────────────────────────────►

     E2E Test           Integration Test         Unit Test
     Real DB            Test DB + Mock externals  Everything mocked
     Real Backend       Real service code         Function isolation
     Real Frontend      Mocked 3rd-party APIs     Mocked dependencies
     Real Browser       In-memory where possible  No I/O

     HIGHEST CONFIDENCE ────────────────────── FASTEST EXECUTION
     SLOWEST EXECUTION  ────────────────────── LOWEST CONFIDENCE
```

---

## Mock Tool Selection

```
┌──────────────────────────────────────────────────────────────┐
│  TOOL           │  LAYER        │  BEST FOR                  │
├──────────────────┼───────────────┼────────────────────────────┤
│  MSW            │  Network      │  Browser tests, React      │
│  (Mock Service  │  (intercepts  │  component tests, Next.js  │
│   Worker)       │  fetch/XHR)   │  integration tests         │
│                 │               │                            │
│  Nock           │  Network      │  Node.js tests, backend    │
│                 │  (intercepts  │  service tests, API client  │
│                 │  http module) │  tests                     │
│                 │               │                            │
│  cy.intercept() │  Network      │  Cypress E2E tests (built  │
│                 │  (proxy)      │  in, no extra library)     │
│                 │               │                            │
│  Jest mocks     │  Module       │  Mocking internal modules, │
│  (jest.mock)    │  (replaces    │  database clients, file    │
│                 │  imports)     │  system                    │
│                 │               │                            │
│  Custom Server  │  Full server  │  E2E tests needing a fake  │
│  (Express)      │  (runs on    │  third-party API           │
│                 │  a port)     │                            │
└──────────────────┴───────────────┴────────────────────────────┘
```

---

## MSW (Mock Service Worker) — Browser & Node

### Setup for React/Next.js Tests

```typescript
// src/mocks/server.ts — for Node.js test environment (Jest/Vitest)
import { setupServer } from 'msw/node'
import { handlers } from './handlers'

export const server = setupServer(...handlers)

// src/mocks/browser.ts — for browser test environment (Storybook, dev)
import { setupWorker } from 'msw/browser'
import { handlers } from './handlers'

export const worker = setupWorker(...handlers)
```

### Handler Structure

```typescript
// src/mocks/handlers/index.ts
import { courseHandlers } from './courses'
import { authHandlers } from './auth'
import { enrollmentHandlers } from './enrollments'

export const handlers = [
  ...authHandlers,
  ...courseHandlers,
  ...enrollmentHandlers,
]
```

```typescript
// src/mocks/handlers/courses.ts
import { http, HttpResponse, delay } from 'msw'
import { courseFactory } from '../factories/course'

const BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3001'

export const courseHandlers = [
  // ─── GET /api/courses ────────────────────────────────
  http.get(`${BASE_URL}/api/courses`, async ({ request }) => {
    const url = new URL(request.url)
    const status = url.searchParams.get('status')
    const page = parseInt(url.searchParams.get('page') || '1')
    const limit = parseInt(url.searchParams.get('limit') || '20')

    // Simulate realistic delay
    await delay(100)

    const courses = courseFactory.buildList(limit, {
      status: status || 'published',
    })

    return HttpResponse.json({
      items: courses,
      total: 47,
      page,
      limit,
      totalPages: 3,
    })
  }),

  // ─── GET /api/courses/:id ───────────────────────────
  http.get(`${BASE_URL}/api/courses/:id`, async ({ params }) => {
    const { id } = params

    if (id === 'not-found-id') {
      return HttpResponse.json(
        { error: 'Course not found' },
        { status: 404 }
      )
    }

    await delay(50)

    return HttpResponse.json(
      courseFactory.build({ id: id as string })
    )
  }),

  // ─── POST /api/courses ──────────────────────────────
  http.post(`${BASE_URL}/api/courses`, async ({ request }) => {
    const body = await request.json() as Record<string, unknown>

    // Validate required fields
    if (!body.title) {
      return HttpResponse.json(
        { error: 'Title is required' },
        { status: 400 }
      )
    }

    await delay(200)

    return HttpResponse.json(
      courseFactory.build({
        title: body.title as string,
        status: 'draft',
      }),
      { status: 201 }
    )
  }),

  // ─── Error scenario handlers ────────────────────────
  // These are used by specific tests that override defaults
  http.get(`${BASE_URL}/api/courses/error-500`, () => {
    return HttpResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    )
  }),
]
```

### Test Setup with MSW

```typescript
// src/tests/setup.ts (for Jest or Vitest)
import { server } from '../mocks/server'

beforeAll(() => {
  // Start MSW server before all tests
  server.listen({
    onUnhandledRequest: 'warn',  // Warn about unhandled requests
  })
})

afterEach(() => {
  // Reset handlers to defaults between tests
  // This is CRITICAL — without it, test overrides leak
  server.resetHandlers()
})

afterAll(() => {
  server.close()
})
```

### Per-Test Handler Overrides

```typescript
import { http, HttpResponse } from 'msw'
import { server } from '../../mocks/server'

describe('Course List', () => {
  it('shows error state when API fails', async () => {
    // Override ONLY for this test — reset in afterEach
    server.use(
      http.get('*/api/courses', () => {
        return HttpResponse.json(
          { error: 'Database connection failed' },
          { status: 500 }
        )
      })
    )

    render(<CourseList />)

    await waitFor(() => {
      expect(screen.getByText('Failed to load courses')).toBeInTheDocument()
    })
  })

  it('shows empty state when no courses', async () => {
    server.use(
      http.get('*/api/courses', () => {
        return HttpResponse.json({
          items: [],
          total: 0,
          page: 1,
          limit: 20,
          totalPages: 0,
        })
      })
    )

    render(<CourseList />)

    await waitFor(() => {
      expect(screen.getByText('No courses found')).toBeInTheDocument()
    })
  })

  it('loads and displays courses', async () => {
    // Uses default handler — no override needed
    render(<CourseList />)

    await waitFor(() => {
      expect(screen.getAllByTestId('course-card')).toHaveLength(20)
    })
  })
})
```

---

## Nock — Node.js HTTP Mocking

### When to Use Nock vs MSW

```
┌──────────────────────────────────────────┐
│  Nock: intercepts Node.js http module    │
│  MSW:  intercepts fetch/XHR in browser   │
│                                          │
│  Use Nock when:                          │
│   - Testing backend services             │
│   - Testing API clients in Node.js       │
│   - Testing middleware                   │
│   - Testing webhook handlers             │
│                                          │
│  Use MSW when:                           │
│   - Testing React/Next.js components     │
│   - Testing browser-side API calls       │
│   - Testing with React Testing Library   │
│   - Storybook mock data                  │
└──────────────────────────────────────────┘
```

### Nock Patterns

```typescript
// tests/services/stripe-service.test.ts
import nock from 'nock'
import { StripeService } from '../../services/stripe'

describe('StripeService', () => {
  const stripeApi = nock('https://api.stripe.com')

  afterEach(() => {
    nock.cleanAll()              // Remove all interceptors
    nock.enableNetConnect()      // Re-enable real HTTP (safety)
  })

  it('creates a customer', async () => {
    stripeApi
      .post('/v1/customers', {
        email: 'user@test.com',
        name: 'Test User',
      })
      .reply(200, {
        id: 'cus_test123',
        email: 'user@test.com',
        name: 'Test User',
        created: 1234567890,
      })

    const service = new StripeService()
    const customer = await service.createCustomer('user@test.com', 'Test User')

    expect(customer.id).toBe('cus_test123')
    expect(stripeApi.isDone()).toBe(true)  // Verify the mock was called
  })

  it('handles Stripe API errors', async () => {
    stripeApi
      .post('/v1/customers')
      .reply(402, {
        error: {
          type: 'card_error',
          message: 'Your card was declined',
        },
      })

    const service = new StripeService()

    await expect(
      service.createCustomer('user@test.com', 'Test User')
    ).rejects.toThrow('Your card was declined')
  })

  it('retries on network timeout', async () => {
    // First call times out
    stripeApi
      .post('/v1/customers')
      .delayConnection(10000)   // Simulate timeout
      .reply(200, {})

    // Second call (retry) succeeds
    stripeApi
      .post('/v1/customers')
      .reply(200, { id: 'cus_retry_success' })

    const service = new StripeService({ timeout: 1000, retries: 1 })
    const customer = await service.createCustomer('user@test.com', 'Test User')

    expect(customer.id).toBe('cus_retry_success')
  })
})
```

---

## Mock Data Factories

### Why Factories Beat Fixtures

```
┌──────────────────────────────────────────────────────────────┐
│  FIXTURES (JSON files)            FACTORIES (Builder funcs)  │
│                                                              │
│  Static data                      Dynamic data               │
│  One shape per file               Infinite variations        │
│  Hard to customize per test       Override any field          │
│  Drift from real schema           Type-checked against schema│
│  Copy-pasted across tests         Single source of truth     │
│  "fixtures/user-admin.json"       userFactory.build({admin:1})│
│  "fixtures/user-learner.json"     userFactory.build({role:..})│
│  "fixtures/user-no-email.json"    userFactory.build({email:0})│
│  = 20 fixture files               = 1 factory function       │
└──────────────────────────────────────────────────────────────┘
```

### Factory Pattern Implementation

```typescript
// src/mocks/factories/base.ts
import { v4 as uuid } from 'uuid'

type FactoryDefinition<T> = {
  [K in keyof T]: T[K] | (() => T[K])
}

export function createFactory<T extends Record<string, unknown>>(
  defaults: FactoryDefinition<T>
) {
  let sequence = 0

  function build(overrides: Partial<T> = {}): T {
    sequence++
    const result = {} as T

    for (const key of Object.keys(defaults) as (keyof T)[]) {
      const defaultValue = defaults[key]
      if (key in overrides) {
        result[key] = overrides[key]!
      } else if (typeof defaultValue === 'function') {
        result[key] = (defaultValue as () => T[keyof T])()
      } else {
        result[key] = defaultValue as T[keyof T]
      }
    }

    return result
  }

  function buildList(count: number, overrides: Partial<T> = {}): T[] {
    return Array.from({ length: count }, () => build(overrides))
  }

  function getSequence() {
    return sequence
  }

  return { build, buildList, getSequence }
}
```

```typescript
// src/mocks/factories/course.ts
import { createFactory } from './base'
import { v4 as uuid } from 'uuid'

interface MockCourse {
  id: string
  title: string
  description: string
  status: string
  category: string
  created_at: string
  updated_at: string
  sections_count: number
  enrolled_count: number
  thumbnail_url: string | null
  created_by: string
}

export const courseFactory = createFactory<MockCourse>({
  id: () => uuid(),
  title: () => `Test Course ${Date.now()}`,
  description: 'A comprehensive course for testing purposes.',
  status: 'published',
  category: 'Engineering',
  created_at: () => new Date().toISOString(),
  updated_at: () => new Date().toISOString(),
  sections_count: 5,
  enrolled_count: 12,
  thumbnail_url: null,
  created_by: () => uuid(),
})

// Usage:
// courseFactory.build()                          → default course
// courseFactory.build({ status: 'draft' })       → draft course
// courseFactory.build({ title: 'My Course' })    → custom title
// courseFactory.buildList(10)                    → 10 courses
// courseFactory.buildList(5, { status: 'draft'}) → 5 draft courses
```

```typescript
// src/mocks/factories/user.ts
import { createFactory } from './base'
import { v4 as uuid } from 'uuid'

interface MockUser {
  id: string
  email: string
  first_name: string
  last_name: string
  role: string
  is_active: boolean
  tenant_id: string
  avatar_url: string | null
  created_at: string
}

let userSeq = 0

export const userFactory = createFactory<MockUser>({
  id: () => uuid(),
  email: () => `user${++userSeq}@test.com`,
  first_name: () => `User`,
  last_name: () => `${userSeq}`,
  role: 'learner',
  is_active: true,
  tenant_id: () => uuid(),
  avatar_url: null,
  created_at: () => new Date().toISOString(),
})
```

---

## Resetting Mocks Between Tests

### The Reset Flow

```
┌──────────┐     beforeEach    ┌──────────┐     Test runs     ┌──────────┐
│  Clean   │ ───────────────▶  │  Fresh   │ ────────────────▶ │  Test    │
│  state   │                   │  mocks   │                    │  adds    │
│          │                   │  applied │                    │  overrides│
└──────────┘                   └──────────┘                    └────┬─────┘
                                                                    │
     ┌──────────────────────────────────────────────────────────────┘
     │  afterEach
     ▼
┌──────────┐
│  Reset   │ → server.resetHandlers()  (MSW)
│  all     │ → nock.cleanAll()         (Nock)
│  mocks   │ → jest.restoreAllMocks()  (Jest)
│          │ → factory sequence reset  (optional)
└──────────┘
```

### Critical Reset Rules

```
┌──────────────────────────────────────────────────────────────┐
│  MOCK RESET RULES — NEVER SKIP                              │
│                                                              │
│  1. ALWAYS reset mocks in afterEach, not afterAll            │
│     → afterAll resets only once after all tests in a file    │
│     → afterEach resets after EACH test — prevents leakage   │
│                                                              │
│  2. Reset ORDER matters:                                     │
│     → First:  server.resetHandlers()  (network mocks)       │
│     → Second: jest.restoreAllMocks()  (module mocks)        │
│     → Third:  cleanup any test data   (DB seeds)            │
│                                                              │
│  3. Use server.use() for per-test overrides                  │
│     → They auto-reset on server.resetHandlers()             │
│     → Never modify the default handlers array directly       │
│                                                              │
│  4. VERIFY mocks were called                                 │
│     → nock.isDone() — were all interceptors consumed?        │
│     → expect(fetchMock).toHaveBeenCalled()                   │
│     → Uncalled mocks = either dead code or wrong URL         │
└──────────────────────────────────────────────────────────────┘
```

---

## Type-Safe Mocking

### Typing Mock Responses

```typescript
// src/types/api.ts — share these between frontend and mock handlers
export interface CourseListResponse {
  items: Course[]
  total: number
  page: number
  limit: number
  totalPages: number
}

export interface Course {
  id: string
  title: string
  description: string
  status: 'draft' | 'published' | 'archived'
  category: string
  created_at: string
}

// src/mocks/handlers/courses.ts
import type { CourseListResponse, Course } from '../../types/api'

http.get('*/api/courses', () => {
  // TypeScript ensures the response matches the real API shape
  const response: CourseListResponse = {
    items: courseFactory.buildList(10),
    total: 10,
    page: 1,
    limit: 20,
    totalPages: 1,
  }
  return HttpResponse.json(response)
})
```

### Typing Jest Mocks

```typescript
// Typed mock for a service
import { EmailService } from '../services/email'

jest.mock('../services/email')

const mockEmailService = jest.mocked(EmailService)

// Now TypeScript knows the shape of the mock
mockEmailService.prototype.send.mockResolvedValue({ messageId: 'test-123' })

// This would be a TypeScript error:
// mockEmailService.prototype.send.mockResolvedValue({ wrong_field: true })
```

---

## Common Mistakes / Anti-Patterns

```
┌──────────────────────────────────────────────────────────────┐
│  ANTI-PATTERN                    │  DO THIS INSTEAD          │
├──────────────────────────────────┼───────────────────────────┤
│  Mocking your own database       │  Use a test database      │
│  Not resetting mocks             │  afterEach → resetHandlers│
│  Fixtures with 500-line JSON     │  Factory functions         │
│  Mocking fetch globally          │  MSW per-handler intercept│
│  Hardcoded UUIDs in mocks        │  Factory-generated UUIDs  │
│  Mock returns don't match schema │  Type-check mock responses│
│  Mocking too deep (internals)    │  Mock at the boundary     │
│  No verification mocks were used │  assert isDone / called   │
│  Same mock data for all tests    │  Customize per scenario   │
│  Mocking in production code      │  Mocks in test files only │
│  Using real 3rd-party APIs       │  Always mock externals    │
│  Not testing error responses     │  Mock 400/500/timeout     │
└──────────────────────────────────┴───────────────────────────┘
```

---

## Tips for Best Results

1. **Mock at the network boundary** — not at the module level. MSW and Nock intercept HTTP, which means your real fetch/axios code runs too
2. **Keep factories close to your API types** — if the API type changes, the factory should break at compile time
3. **Test the error path first** — mocking 500s and timeouts is the most valuable use of mocks because you can't reliably trigger these with real services
4. **Use `onUnhandledRequest: 'error'`** in MSW — this catches any fetch call your handlers don't cover, preventing silent failures
5. **One factory per entity** — `userFactory`, `courseFactory`, `enrollmentFactory`. Never a generic `dataFactory`
6. **Name your mocked scenarios** — `server.use(coursesEmptyState)` is clearer than inline handler definitions
7. **Simulate realistic delays** — `await delay(100)` catches race conditions that instant responses hide
8. **Never mock what you own** — if you control both the client and server, test them together. Mock only third-party boundaries
9. **Verify mock coverage** — if you have 20 handlers but tests only trigger 5, you have dead mock code
10. **Keep mocks in sync with real API** — run contract tests (see contract-test skill) to ensure mocks match reality

<!--
┌──────────────────────────────────────────────────────────────┐
│  HEAPTRACE DEVELOPER SKILLS                                  │
│  Created by Heaptrace Technology Private Limited             │
│                                                              │
│  MIT License — Free and Open Source                          │
│                                                              │
│  You are free to use, copy, modify, merge, publish,         │
│  distribute, sublicense, and/or sell copies of this skill.   │
│  No restrictions. No attribution required.                   │
│                                                              │
│  heaptrace.com | github.com/heaptracetechnology              │
└──────────────────────────────────────────────────────────────┘
-->
