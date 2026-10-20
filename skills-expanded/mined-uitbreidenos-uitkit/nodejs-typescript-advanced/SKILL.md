---
name: "typescript-advanced"
description: "Advanced TypeScript: generics, conditional types, mapped types, template literals, utility types, type guards, discriminated unions at scale"
---

# TypeScript Advanced Skill

## When to activate
- Designing a type-safe API or SDK where generics are essential
- Writing utility types to eliminate type duplication
- Narrowing types with discriminated unions and type guards
- Getting TypeScript to infer types rather than annotating manually
- Debugging complex type errors in generic code
- Building a type-safe event system, state machine, or plugin architecture

## When NOT to use
- Basic TypeScript with simple types — the TypeScript rules skill covers that
- When `any` is genuinely the right answer (rare, but it happens at external API boundaries)
- Over-engineering types for simple internal code — readability > type cleverness

## Instructions

### Generics — make types work for you

```typescript
// Generic function — type inferred from argument
function first<T>(arr: T[]): T | undefined {
  return arr[0]
}
const n = first([1, 2, 3])    // n: number | undefined ✅
const s = first(['a', 'b'])   // s: string | undefined ✅

// Constrained generics
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key]
}
const user = { id: 1, name: 'Alice' }
const name = getProperty(user, 'name')  // name: string ✅
// getProperty(user, 'missing')          // ❌ compile error

// Default type parameter
type ApiResponse<T = unknown> = {
  data: T
  status: number
  message: string
}
```

### Discriminated unions — the foundation of safe state

```typescript
// Each variant has a unique literal 'type' field
type LoadingState = { status: 'loading' }
type SuccessState<T> = { status: 'success'; data: T }
type ErrorState = { status: 'error'; error: Error; retryable: boolean }

type AsyncState<T> = LoadingState | SuccessState<T> | ErrorState

function renderState<T>(state: AsyncState<T>) {
  switch (state.status) {
    case 'loading': return <Spinner />
    case 'success': return <Data data={state.data} />  // state.data available ✅
    case 'error':   return <Error error={state.error} retryable={state.retryable} />
    default: {
      const _exhaustive: never = state  // compile error if a case is missing
      throw new Error(`Unhandled: ${_exhaustive}`)
    }
  }
}
```

### Type guards — runtime narrowing with type safety

```typescript
// User-defined type guard
function isUser(value: unknown): value is User {
  return (
    typeof value === 'object' &&
    value !== null &&
    'id' in value &&
    'email' in value &&
    typeof (value as User).email === 'string'
  )
}

// Assertion function (throws if not the expected type)
function assertUser(value: unknown): asserts value is User {
  if (!isUser(value)) throw new TypeError(`Expected User, got ${typeof value}`)
}

// Usage
const data = await fetchUser()
if (isUser(data)) {
  console.log(data.email)  // data: User ✅
}

assertUser(data)
console.log(data.email)    // data: User ✅ (throws before this line if not a User)
```

### Utility types — avoid repeating yourself

```typescript
type User = {
  id: number
  email: string
  name: string
  passwordHash: string
  createdAt: Date
}

// Omit sensitive fields
type PublicUser = Omit<User, 'passwordHash'>

// All fields optional (for PATCH endpoints)
type UpdateUserRequest = Partial<Pick<User, 'email' | 'name'>>

// Required subset
type CreateUserRequest = Required<Pick<User, 'email' | 'name'>>

// Read-only
type ReadonlyUser = Readonly<User>

// From a function's return type
async function fetchUser(id: number) {
  return db.user.findUnique({ where: { id } })
}
type FetchedUser = Awaited<ReturnType<typeof fetchUser>>

// From a function's parameters
type FetchUserParams = Parameters<typeof fetchUser>[0]  // number
```

### Conditional types

```typescript
// IsArray<T> — true if T is an array
type IsArray<T> = T extends unknown[] ? true : false
type A = IsArray<string[]>  // true
type B = IsArray<string>    // false

// Unwrap array element type
type ElementType<T> = T extends (infer E)[] ? E : T
type C = ElementType<string[]>  // string
type D = ElementType<string>    // string (not an array, returns T)

// NonNullable equivalent (built-in, shown for learning)
type StrictNonNullable<T> = T extends null | undefined ? never : T
type E = StrictNonNullable<string | null | undefined>  // string

// Conditional on object structure
type HasId<T> = T extends { id: unknown } ? true : false
```

### Mapped types — transform object shapes

```typescript
// Make all values nullable
type Nullable<T> = { [K in keyof T]: T[K] | null }

// Make all values async
type Asyncify<T> = { [K in keyof T]: T[K] extends (...args: infer A) => infer R
  ? (...args: A) => Promise<R>
  : T[K]
}

// Filter keys by value type
type PickByValue<T, V> = {
  [K in keyof T as T[K] extends V ? K : never]: T[K]
}
type OnlyStrings = PickByValue<{ a: string; b: number; c: string }, string>
// { a: string; c: string }

// Create a Record from a union
type Status = 'pending' | 'active' | 'inactive'
type StatusConfig = Record<Status, { label: string; color: string }>
```

### Template literal types

```typescript
// Generate all CSS-style size variants
type Size = 'sm' | 'md' | 'lg'
type Color = 'primary' | 'secondary'
type ButtonVariant = `${Color}-${Size}`
// 'primary-sm' | 'primary-md' | 'primary-lg' | 'secondary-sm' | ...

// Extract route params
type ExtractRouteParams<T extends string> =
  T extends `${string}:${infer Param}/${infer Rest}`
    ? Param | ExtractRouteParams<`/${Rest}`>
    : T extends `${string}:${infer Param}`
    ? Param
    : never

type Params = ExtractRouteParams<'/users/:userId/posts/:postId'>
// 'userId' | 'postId'

// Type-safe event system
type EventMap = {
  'user:created': { userId: string; email: string }
  'user:deleted': { userId: string }
  'order:placed': { orderId: string; total: number }
}

type EventName = keyof EventMap

function emit<E extends EventName>(event: E, payload: EventMap[E]): void {
  // ...
}

emit('user:created', { userId: '1', email: 'a@b.com' })  // ✅
emit('user:created', { userId: '1' })                     // ❌ missing email
```

### Infer — extract types from other types

```typescript
// Extract the resolved type of a Promise
type Awaited<T> = T extends Promise<infer U> ? U : T

// Extract function return type
type ReturnType<T extends (...args: any) => any> =
  T extends (...args: any) => infer R ? R : never

// Extract constructor parameters
type ConstructorParams<T extends abstract new (...args: any) => any> =
  T extends abstract new (...args: infer P) => any ? P : never

// Extract array element type
type ArrayElement<T extends readonly unknown[]> =
  T extends readonly (infer E)[] ? E : never

type Nums = ArrayElement<number[]>  // number
```

### `satisfies` operator (TS 4.9+)

```typescript
type Config = {
  port: number
  host: string
  features: Record<string, boolean>
}

// satisfies checks the type but preserves the literal type
const config = {
  port: 3000,
  host: 'localhost',
  features: { dark_mode: true, beta: false },
} satisfies Config

// port is still 3000 (not widened to number)
config.port.toFixed(0)             // ✅ still a number method
config.features.dark_mode          // ✅ TypeScript knows this key exists
config.features.nonexistent        // ❌ compile error
```

## Example

**User:** Build a type-safe API client where the request and response types are inferred from a route definition object, with no manual type annotations at call sites.

**Expected output:**
```typescript
type Routes = {
  'GET /users': { response: User[] }
  'GET /users/:id': { params: { id: string }; response: User }
  'POST /users': { body: CreateUserRequest; response: User }
}

// Calling apiClient.get('/users') → infers response: User[]
// Calling apiClient.get('/users/:id', { params: { id: '1' } }) → infers User
// apiClient.get('/unknown') → compile error
```

---
