---
name: coding-standards
description: Universal coding standards, best practices, and patterns for TypeScript, JavaScript, React, and Node.js development.
version: 1.0.0
author: opencode
type: skill
category: development
tags:
  - standards
  - best-practices
  - typescript
  - javascript
  - react
  - node
  - api
  - testing
---

# Coding Standards & Best Practices

Universal coding standards applicable across all projects.

## Code Quality Principles

### 1. Readability First
- Code is read more than written
- Clear variable and function names
- Self-documenting code preferred over comments
- Consistent formatting

### 2. KISS (Keep It Simple, Stupid)
- Simplest solution that works
- Avoid over-engineering
- No premature optimization
- Easy to understand > clever code

### 3. DRY (Don't Repeat Yourself)
- Extract common logic into functions
- Create reusable components
- Share utilities across modules
- Avoid copy-paste programming

### 4. YAGNI (You Aren't Gonna Need It)
- Don't build features before they're needed
- Avoid speculative generality
- Add complexity only when required
- Start simple, refactor when needed

## TypeScript/JavaScript Standards

### Variable Naming

```typescript
// GOOD: Descriptive names
const marketSearchQuery = 'election'
const isUserAuthenticated = true
const totalRevenue = 1000

// BAD: Unclear names
const q = 'election'
const flag = true
const x = 1000
```

### Function Naming

```typescript
// GOOD: Verb-noun pattern
async function fetchMarketData(marketId: string): Promise<void> {
  // ...
}

function calculateSimilarity(a: number[], b: number[]): number {
  // ...
  return 0
}

function isValidEmail(email: string): boolean {
  return /.+@.+\..+/.test(email)
}

// BAD: Unclear or noun-only
async function market(id: string): Promise<void> {
  // ...
}

function similarity(a: unknown, b: unknown) {
  // ...
}

function email(e: string) {
  // ...
}
```

### Immutability Pattern (CRITICAL)

```typescript
// ALWAYS use spread operator
const updatedUser = {
  ...user,
  name: 'New Name'
}

const updatedArray = [...items, newItem]

// NEVER mutate directly
user.name = 'New Name'  // BAD
items.push(newItem)     // BAD
```

### Error Handling

```typescript
// GOOD: Comprehensive error handling
export async function fetchData(url: string) {
  try {
    const response = await fetch(url)

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`)
    }

    return await response.json()
  } catch (error) {
    console.error('Fetch failed:', error)
    throw new Error('Failed to fetch data')
  }
}

// BAD: No error handling
export async function fetchDataUnsafe(url: string) {
  const response = await fetch(url)
  return response.json()
}
```

### Async/Await Best Practices

```typescript
// GOOD: Parallel execution when possible
const [users, markets, stats] = await Promise.all([
  fetchUsers(),
  fetchMarkets(),
  fetchStats()
])

// BAD: Sequential when unnecessary
const users = await fetchUsers()
const markets = await fetchMarkets()
const stats = await fetchStats()
```

### Type Safety

```typescript
// GOOD: Proper types
interface Market {
  id: string
  name: string
  status: 'active' | 'resolved' | 'closed'
  created_at: Date
}

export async function getMarket(id: string): Promise<Market> {
  throw new Error('Not implemented')
}

// BAD: Using 'any'
export async function getMarketUnsafe(id: any): Promise<any> {
  throw new Error('Not implemented')
}
```

## React Best Practices

### Component Structure

```typescript
import type { ReactNode } from 'react'

interface ButtonProps {
  children: ReactNode
  onClick: () => void
  disabled?: boolean
  variant?: 'primary' | 'secondary'
}

export function Button({
  children,
  onClick,
  disabled = false,
  variant = 'primary'
}: ButtonProps) {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={`btn btn-${variant}`}
    >
      {children}
    </button>
  )
}

// BAD: No types, unclear structure
export function ButtonUnsafe(props: any) {
  return <button onClick={props.onClick}>{props.children}</button>
}
```

### Custom Hooks

```typescript
import { useEffect, useState } from 'react'

// GOOD: Reusable custom hook
export function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value)

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value)
    }, delay)

    return () => clearTimeout(handler)
  }, [value, delay])

  return debouncedValue
}

// Usage
// const debouncedQuery = useDebounce(searchQuery, 500)
```

### State Management

```typescript
import { useState } from 'react'

// GOOD: Proper state updates
const [count, setCount] = useState(0)

// Functional update for state based on previous state
setCount(prev => prev + 1)

// BAD: Direct state reference
setCount(count + 1)  // Can be stale in async scenarios
```

### Conditional Rendering

```typescript
// GOOD: Clear conditional rendering
{
  isLoading && <Spinner />
}
{
  error && <ErrorMessage error={error} />
}
{
  data && <DataDisplay data={data} />
}

// BAD: Ternary hell
{
  isLoading
    ? <Spinner />
    : error
      ? <ErrorMessage error={error} />
      : data
        ? <DataDisplay data={data} />
        : null
}
```

## API Design Standards

### REST API Conventions

```
GET    /api/markets              # List all markets
GET    /api/markets/:id          # Get specific market
POST   /api/markets              # Create new market
PUT    /api/markets/:id          # Update market (full)
PATCH  /api/markets/:id          # Update market (partial)
DELETE /api/markets/:id          # Delete market

# Query parameters for filtering
GET /api/markets?status=active&limit=10&offset=0
```

### Response Format

```typescript
// GOOD: Consistent response structure
interface ApiResponse<T> {
  success: boolean
  data?: T
  error?: string
  meta?: {
    total: number
    page: number
    limit: number
  }
}
```

### Input Validation

```typescript
import { z } from 'zod'

// GOOD: Schema validation
const CreateMarketSchema = z.object({
  name: z.string().min(1).max(200),
  description: z.string().min(1).max(2000),
  endDate: z.string().datetime(),
  categories: z.array(z.string()).min(1)
})
```

## File Organization

### Project Structure

```
src/
|-- app/
|-- components/
|-- hooks/
|-- lib/
|-- types/
`-- styles/
```

### File Naming

```
components/Button.tsx
hooks/useAuth.ts
lib/formatDate.ts
types/market.types.ts
```

## Comments & Documentation

### When to Comment

```typescript
// GOOD: Explain WHY, not WHAT
// Use exponential backoff to avoid overwhelming the API during outages
const delay = Math.min(1000 * Math.pow(2, retryCount), 30000)
```

### JSDoc for Public APIs

```typescript
/**
 * Searches markets using semantic similarity.
 */
export async function searchMarkets(query: string, limit: number = 10) {
  throw new Error('Not implemented')
}
```

## Performance Best Practices

### Memoization

```typescript
import { useCallback, useMemo } from 'react'
```

### Lazy Loading

```typescript
import { lazy, Suspense } from 'react'
```

### Database Queries

```typescript
// GOOD: Select only needed columns
const { data } = await supabase
  .from('markets')
  .select('id, name, status')
  .limit(10)
```

## Testing Standards

### Test Structure (AAA Pattern)

```typescript
test('calculates similarity correctly', () => {
  // Arrange
  const vector1 = [1, 0, 0]
  const vector2 = [0, 1, 0]

  // Act
  const similarity = calculateCosineSimilarity(vector1, vector2)

  // Assert
  expect(similarity).toBe(0)
})
```

### Test Naming

```typescript
test('returns empty array when no markets match query', () => {
  // ...
})
```

## Code Smell Detection

Watch for these anti-patterns:

### 1. Long Functions
### 2. Deep Nesting
### 3. Magic Numbers

Remember: Code quality is not negotiable. Clear, maintainable code enables rapid development and confident refactoring.
