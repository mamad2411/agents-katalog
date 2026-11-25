---
name: coding-standards
description: Universal coding standards, best practices, and patterns for TypeScript, JavaScript, React, and Go development.
---

# Coding Standards and Best Practices

Universal coding standards applicable to all projects in the Fusion Labs workspace.

## When to Activate

- Writing new code in any language
- Reviewing pull requests
- Refactoring existing code
- Onboarding to a new project

## Code Quality Principles

### 1. Readability First

- Code is read far more often than it is written
- Use clear variable and function names
- Prefer self-documenting code over comments
- Maintain consistent formatting

### 2. KISS (Keep It Simple, Stupid)

- Adopt the simplest solution that works
- Avoid over-engineering
- Avoid premature optimization
- Understandability > cleverness

### 3. DRY (Don't Repeat Yourself)

- Extract common logic into functions
- Create reusable components
- Share utility functions across modules
- Avoid copy-paste programming

### 4. YAGNI (You Aren't Gonna Need It)

- Don't build features you don't yet need
- Avoid speculative generalization
- Add complexity only when required
- Start simple, refactor as needed

## TypeScript/JavaScript Standards

### Variable Naming

```typescript
// ✅ GOOD: Descriptive names
const assetSearchQuery = 'bitcoin'
const isUserAuthenticated = true
const totalPortfolioValue = 50000

// ❌ BAD: Unclear names
const q = 'bitcoin'
const flag = true
const x = 50000
```

### Function Naming

```typescript
// ✅ GOOD: Verb-noun pattern
async function fetchAssetData(assetId: string) { }
function calculatePortfolioValue(assets: Asset[]) { }
function isValidEmail(email: string): boolean { }

// ❌ BAD: Unclear or noun-only
async function asset(id: string) { }
function value(a: any) { }
```

### Immutability Patterns

```typescript
// ✅ ALWAYS use spread operator
const updatedUser = { ...user, name: 'New Name' }
const updatedArray = [...items, newItem]

// ❌ NEVER mutate directly
user.name = 'New Name'  // BAD
items.push(newItem)     // BAD
```

### Error Handling

```typescript
// ✅ GOOD: Comprehensive error handling
async function fetchData(url: string) {
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

// ❌ BAD: No error handling
async function fetchData(url: string) {
  const response = await fetch(url)
  return response.json()
}
```

### Async/Await Best Practices

```typescript
// ✅ GOOD: Parallel execution when possible
const [users, assets, stats] = await Promise.all([
  fetchUsers(),
  fetchAssets(),
  fetchStats()
])

// ❌ BAD: Sequential when unnecessary
const users = await fetchUsers()
const assets = await fetchAssets()
const stats = await fetchStats()
```

### Type Safety

```typescript
// ✅ GOOD: Proper types
interface Asset {
  id: string
  name: string
  ticker: string
  status: 'active' | 'archived'
  value: number
  created_at: Date
}

function getAsset(id: string): Promise<Asset> {
  // Implementation
}

// ❌ BAD: Using 'any'
function getAsset(id: any): Promise<any> {
  // Implementation
}
```

## Go Standards

### Naming Conventions

```go
// Exported names: PascalCase
func GetUser(id string) (*User, error) { }
type AssetService struct { }

// Unexported names: camelCase
func validateInput(input string) error { }
type userRepository struct { }

// Acronyms: Consistent casing
var httpClient *http.Client  // Not httpClient
type JSONResponse struct{}    // Not JsonResponse
```

### Error Messages

```go
// ✅ GOOD: Lowercase, no punctuation, with context
return fmt.Errorf("fetch user %s: %w", id, err)

// ❌ BAD: Capitalized, with punctuation
return fmt.Errorf("Failed to fetch user: %v.", err)
```

## API Design Standards

### REST Conventions

```
GET    /api/assets              # List resources
GET    /api/assets/:id          # Get specific resource
POST   /api/assets              # Create resource
PUT    /api/assets/:id          # Full replace
PATCH  /api/assets/:id          # Partial update
DELETE /api/assets/:id          # Delete resource

# Query parameters for filtering
GET /api/assets?status=active&limit=10&offset=0
```

### Consistent Response Format

```typescript
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

## File Organization

### TypeScript/React Projects

```
src/
├── components/         # React components
│   ├── ui/            # Generic UI components
│   ├── forms/         # Form components
│   └── layouts/       # Layout components
├── hooks/             # Custom React hooks
├── lib/               # Utilities and configs
│   ├── api/           # API clients
│   ├── utils/         # Helper functions
│   └── constants/     # Constants
├── types/             # TypeScript types
└── styles/            # Global styles
```

### File Naming

```
components/Button.tsx          # PascalCase for components
hooks/useAuth.ts               # camelCase with 'use' prefix
lib/formatDate.ts              # camelCase for utilities
types/asset.types.ts           # camelCase with .types suffix
```

## Comments and Documentation

### When to Add Comments

```typescript
// ✅ GOOD: Explain WHY, not WHAT
// Use exponential backoff to avoid overwhelming the API during outages
const delay = Math.min(1000 * Math.pow(2, retryCount), 30000)

// ❌ BAD: Stating the obvious
// Increment counter by 1
count++
```

### JSDoc for Public APIs

```typescript
/**
 * Searches assets using semantic similarity.
 *
 * @param query - Natural language search query
 * @param limit - Maximum number of results (default: 10)
 * @returns Array of assets sorted by relevance
 * @throws {Error} If API fails
 *
 * @example
 * ```typescript
 * const results = await searchAssets('bitcoin', 5)
 * ```
 */
export async function searchAssets(
  query: string,
  limit: number = 10
): Promise<Asset[]> {
  // Implementation
}
```

## Code Smell Detection

### 1. Long Functions

```typescript
// ❌ BAD: Function > 50 lines — split it up
function processData() { /* 100 lines */ }

// ✅ GOOD: Split into smaller functions
function processData() {
  const validated = validateData()
  const transformed = transformData(validated)
  return saveData(transformed)
}
```

### 2. Deep Nesting

```typescript
// ❌ BAD: 5+ levels of nesting
if (user) {
  if (user.isAdmin) {
    if (asset) { /* ... */ }
  }
}

// ✅ GOOD: Early returns
if (!user) return
if (!user.isAdmin) return
if (!asset) return
// Do something
```

### 3. Magic Numbers

```typescript
// ❌ BAD: Unexplained numbers
if (retryCount > 3) { }
setTimeout(callback, 500)

// ✅ GOOD: Named constants
const MAX_RETRIES = 3
const DEBOUNCE_DELAY_MS = 500

if (retryCount > MAX_RETRIES) { }
setTimeout(callback, DEBOUNCE_DELAY_MS)
```

---

**Remember**: Code quality is non-negotiable. Clear, maintainable code enables rapid development and confident refactoring.
