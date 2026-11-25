---
name: fp-toolkit
description: Consolidated toolkit for fp. Covers fp-ts-react, fp-ts-errors, fp-ts-pragmatic
---
# Fp Toolkit

## Core Capabilities
# Fp Toolkit

# Functional Programming in React

Practical patterns for React apps. No jargon, just code that works.

## When to Use This Skill

- When building React apps with fp-ts for type-safe state management
- When handling loading/error/success states in data fetching
- When implementing form validation with error accumulation
- When using React 18/19 or Next.js 14/15 with functional patterns

---

## Quick Reference

| Pattern | Use When |
|---------|----------|
| `Option` | Value might be missing (user not loaded yet) |
| `Either` | Operation might fail (form validation) |
| `TaskEither` | Async operation might fail (API calls) |
| `RemoteData` | Need to show loading/error/success states |
| `pipe` | Chaining multiple transformations |

---

## 1. State with Option (Maybe It's There, Maybe Not)

Use `Option` instead of `null | undefined` for clearer intent.

### Basic Pattern

```typescript
import { useState } from 'react'
import * as O from 'fp-ts/Option'
import { pipe } from 'fp-ts/function'

interface User {
  id: string
  name: string
  email: string
}

function UserProfile() {
  // Option says "this might not exist yet"
  const [user, setUser] = useState<O.Option<User>>(O.none)

  const handleLogin = (userData: User) => {
    setUser(O.some(userData))
  }

  const handleLogout = () => {
    setUser(O.none)
  }

  return pipe(
    user,
    O.match(
      // When there's no user
      () => <button onClick={() => handleLogin({ id: '1', name: 'Alice', email: 'alice@example.com' })}>
        Log In
      </button>,
      // When there's a user
      (u) => (
        <div>
          <p>Welcome, {u.name}!</p>
          <button onClick={handleLogout}>Log Out</button>
        </div>
      )
    )
  )
}
```

### Chaining Optional Values

```typescript
import * as O from 'fp-ts/Option'
import { pipe } from 'fp-ts/function'

interface Profile {
  user: O.Option<{
    name: string
    settings: O.Option<{
      theme: string
    }>
  }>
}

function getTheme(profile: Profile): string {
  return pipe(
    profile.user,
    O.flatMap(u => u.settings),
    O.map(s => s.theme),
    O.getOrElse(() => 'light') // default
  )
}
```

---

## 2. Form Validation with Either

Either is perfect for validation: `Left` = errors, `Right` = valid data.

### Simple Form Validation

```typescript
import * as E from 'fp-ts/Either'
import * as A from 'fp-ts/Array'
import { pipe } from 'fp-ts/function'

// Validation functions return Either<ErrorMessage, ValidValue>
const validateEmail = (email: string): E.Either<string, string> =>
  email.includes('@')
    ? E.right(email)
    : E.left('Invalid email address')

const validatePassword = (password: string): E.Either<string, string> =>
  password.length >= 8
    ? E.right(password)
    : E.left('Password must be at least 8 characters')

const validateName = (name: string): E.Either<string, string> =>
  name.trim().length > 0
    ? E.right(name.trim())
    : E.left('Name is required')
```

### Collecting All Errors (Not Just First One)

```typescript
import * as E from 'fp-ts/Either'
import { sequenceS } from 'fp-ts/Apply'
import { getSemigroup } from 'fp-ts/NonEmptyArray'
import { pipe } from 'fp-ts/function'

// This collects ALL errors, not just the first one
const validateAll = sequenceS(E.getApplicativeValidation(getSemigroup<string>()))

interface SignupForm {
  name: string
  email: string
  password: string
}

interface ValidatedForm {
  name: string
  email: string
  password: string
}

function validateForm(form: SignupForm): E.Either<string[], ValidatedForm> {
  return pipe(
    validateAll({
      name: pipe(validateName(form.name), E.mapLeft(e => [e])),
      email: pipe(validateEmail(form.email), E.mapLeft(e => [e])),
      password: pipe(validatePassword(form.password), E.mapLeft(e => [e])),
    })
  )
}

// Usage in component
function SignupForm() {
  const [form, setForm] = useState({ name: '', email: '', password: '' })
  const [errors, setErrors] = useState<string[]>([])

  const handleSubmit = () => {
    pipe(
      validateForm(form),
      E.match(
        (errs) => setErrors(errs),     // Show all errors
        (valid) => {
          setErrors([])
          submitToServer(valid)         // Submit valid data
        }
      )
    )
  }

  return (
    <form onSubmit={e => { e.preventDefault(); handleSubmit() }}>
      <input
        value={form.name}
        onChange={e => setForm(f => ({ ...f, name: e.target.value }))}
        placeholder="Name"
      />
      <input
        value={form.email}
        onChange={e => setForm(f => ({ ...f, email: e.target.value }))}
        placeholder="Email"
      />
      <input
        type="password"
        value={form.password}
        onChange={e => setForm(f => ({ ...f, password: e.target.value }))}
        placeholder="Password"
      />

      {errors.length > 0 && (
        <ul style={{ color: 'red' }}>
          {errors.map((err, i) => <li key={i}>{err}</li>)}
        </ul>
      )}

      <button type="submit">Sign Up</button>
    </form>
  )
}
```

### Field-Level Errors (Better UX)

```typescript
type FieldErrors = Partial<Record<keyof SignupForm, string>>

function validateFormWithFieldErrors(form: SignupForm): E.Either<FieldErrors, ValidatedForm> {
  const errors: FieldErrors = {}

  pipe(validateName(form.name), E.mapLeft(e => { errors.name = e }))
  pipe(validateEmail(form.email), E.mapLeft(e => { errors.email = e }))
  pipe(validatePassword(form.password), E.mapLeft(e => { errors.password = e }))

  return Object.keys(errors).length > 0
    ? E.left(errors)
    : E.right({ name: form.name.trim(), email: form.email, password: form.password })
}

// In component
{errors.email && <span className="error">{errors.email}</span>}
```

---

## 3. Data Fetching with TaskEither

TaskEither = async operation that might fail. Perfect for API calls.

### Basic Fetch Hook

```typescript
import { useState, useEffect } from 'react'
import * as TE from 'fp-ts/TaskEither'
import * as E from 'fp-ts/Either'
import { pipe } from 'fp-ts/function'

// Wrap fetch in TaskEither
const fetchJson = <T>(url: string): TE.TaskEither<Error, T> =>
  TE.tryCatch(
    async () => {
      const res = await fetch(url)
      if (!res.ok) throw new Error(`HTTP ${res.status}`)
      return res.json()
    },
    (err) => err instanceof Error ? err : new Error(String(err))
  )

// Custom hook
function useFetch<T>(url: string) {
  const [data, setData] = useState<T | null>(null)
  const [error, setError] = useState<Error | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    setLoading(true)
    setError(null)

    pipe(
      fetchJson<T>(url),
      TE.match(
        (err) => {
          setError(err)
          setLoading(false)
        },
        (result) => {
          setData(result)
          setLoading(false)
        }
      )
    )()
  }, [url])

  return { data, error, loading }
}

// Usage
function UserList() {
  const { data, error, loading } = useFetch<User[]>('/api/users')

  if (loading) return <div>Loading...</div>
  if (error) return <div>Error: {error.message}</div>
  return (
    <ul>
      {data?.map(user => <li key={user.id}>{user.name}</li>)}
    </ul>
  )
}
```

### Chaining API Calls

```typescript
// Fetch user, then fetch their posts
const fetchUserWithPosts = (userId: string) => pipe(
  fetchJson<User>(`/api/users/${userId}`),
  TE.flatMap(user => pipe(
    fetchJson<Post[]>(`/api/users/${userId}/posts`),
    TE.map(posts => ({ ...user, posts }))
  ))
)
```

### Parallel API Calls

```typescript
import { sequenceT } from 'fp-ts/Apply'

// Fetch multiple things at once
const fetchDashboardData = () => pipe(
  sequenceT(TE.ApplyPar)(
    fetchJson<User>('/api/user'),
    fetchJson<Stats>('/api/stats'),
    fetchJson<Notifications[]>('/api/notifications')
  ),
  TE.map(([user, stats, notifications]) => ({
    user,
    stats,
    notifications
  }))
)
```

---

## 4. RemoteData Pattern (The Right Way to Handle Async State)

Stop using `{ data, loading, error }` booleans. Use a proper state machine.

### The Pattern

```typescript
// RemoteData has exactly 4 states - no impossible combinations
type RemoteData<E, A> =
  | { _tag: 'NotAsked' }                    // Haven't started yet
  | { _tag: 'Loading' }                     // In progress
  | { _tag: 'Failure'; error: E }           // Failed
  | { _tag: 'Success'; data: A }            // Got it!

// Constructors
const notAsked = <E, A>(): RemoteData<E, A> => ({ _tag: 'NotAsked' })
const loading = <E, A>(): RemoteData<E, A> => ({ _tag: 'Loading' })
const failure = <E, A>(error: E): RemoteData<E, A> => ({ _tag: 'Failure', error })
const success = <E, A>(data: A): RemoteData<E, A> => ({ _tag: 'Success', data })

// Pattern match all states
function fold<E, A, R>(
  rd: RemoteData<E, A>,
  onNotAsked: () => R,
  onLoading: () => R,
  onFailure: (e: E) => R,
  onSuccess: (a: A) => R
): R {
  switch (rd._tag) {
    case 'NotAsked': return onNotAsked()
    case 'Loading': return onLoading()
    case 'Failure': return onFailure(rd.error)
    case 'Success': return onSuccess(rd.data)
  }
}
```

### Hook with RemoteData

```typescript
function useRemoteData<T>(fetchFn: () => Promise<T>) {
  const [state, setState] = useState<RemoteData<Error, T>>(notAsked())

  const execute = async () => {
    setState(loading())
    try {
      const data = await fetchFn()
      setState(success(data))
    } catch (err) {
      setState(failure(err instanceof Error ? err : new Error(String(err))))
    }
  }

  return { state, execute }
}

// Usage
function UserProfile({ userId }: { userId: string }) {
  const { state, execute } = useRemoteData(() =>
    fetch(`/api/users/${userId}`).then(r => r.json())
  )

  useEffect(() => { execute() }, [userId])

  return fold(
    state,
    () => <button onClick={execute}>Load User</button>,
    () => <Spinner />,
    (err) => <ErrorMessage message={err.message} onRetry={execute} />,
    (user) => <UserCard user={user} />
  )
}
```

### Why RemoteData Beats Booleans

```typescript
// ❌ BAD: Impossible states are possible
interface BadState {
  data: User | null
  loading: boolean
  error: Error | null
}
// Can have: { data: user, loading: true, error: someError } - what does that mean?!

// ✅ GOOD: Only valid states exist
type GoodState = RemoteData<Error, User>
// Can only be: NotAsked | Loading | Failure | Success
```

---

## 5. Referential Stability (Preventing Re-renders)

fp-ts values like `O.some(1)` create new objects each render. React sees them as "changed".

### The Problem

```typescript
// ❌ BAD: Creates new Option every render
function BadComponent() {
  const [value, setValue] = useState(O.some(1))

  useEffect(() => {
    // This runs EVERY render because O.some(1) !== O.some(1)
    console.log('value changed')
  }, [value])
}
```

### Solution 1: useMemo

```typescript
// ✅ GOOD: Memoize Option creation
function GoodComponent() {
  const [rawValue, setRawValue] = useState<number | null>(1)

  const value = useMemo(
    () => O.fromNullable(rawValue),
    [rawValue]  // Only recreate when rawValue changes
  )

  useEffect(() => {
    // Now this only runs when rawValue actually changes
    console.log('value changed')
  }, [rawValue])  // Depend on raw value, not Option
}
```

### Solution 2: fp-ts-react-stable-hooks

```bash
npm install fp-ts-react-stable-hooks
```

```typescript
import { useStableO, useStableEffect } from 'fp-ts-react-stable-hooks'
import * as O from 'fp-ts/Option'
import * as Eq from 'fp-ts/Eq'

function StableComponent() {
  // Uses fp-ts equality instead of reference equality
  const [value, setValue] = useStableO(O.some(1))

  // Effect that understands Option equality
  useStableEffect(
    () => { console.log('value changed') },
    [value],
    Eq.tuple(O.getEq(Eq.eqNumber))  // Custom equality
  )
}
```

---

## 6. Dependency Injection with Context

Use ReaderTaskEither for testable components with injected dependencies.

### Setup Dependencies

```typescript
import * as RTE from 'fp-ts/ReaderTaskEither'
import { pipe } from 'fp-ts/function'
import { createContext, useContext, ReactNode } from 'react'

// Define what services your app needs
interface AppDependencies {
  api: {
    getUser: (id: string) => Promise<User>
    updateUser: (id: string, data: Partial<User>) => Promise<User>
  }
  analytics: {
    track: (event: string, data?: object) => void
  }
}

// Create context
const DepsContext = createContext<AppDependencies | null>(null)

// Provider
function AppProvider({ deps, children }: { deps: AppDependencies; children: ReactNode }) {
  return <DepsContext.Provider value={deps}>{children}</DepsContext.Provider>
}

// Hook to use dependencies
function useDeps(): AppDependencies {
  const deps = useContext(DepsContext)
  if (!deps) throw new Error('Missing AppProvider')
  return deps
}
```

### Use in Components

```typescript
function UserProfile({ userId }: { userId: string }) {
  const { api, analytics } = useDeps()
  const [user, setUser] = useState<RemoteData<Error, User>>(notAsked())

  useEffect(() => {
    setUser(loading())
    api.getUser(userId)
      .then(u => {
        setUser(success(u))
        analytics.track('user_viewed', { userId })
      })
      .catch(e => setUser(failure(e)))
  }, [userId, api, analytics])

  // render...
}
```

### Testing with Mock Dependencies

```typescript
const mockDeps: AppDependencies = {
  api: {
    getUser: jest.fn().mockResolvedValue({ id: '1', name: 'Test User' }),
    updateUser: jest.fn().mockResolvedValue({ id: '1', name: 'Updated' }),
  },
  analytics: {
    track: jest.fn(),
  },
}

test('loads user on mount', async () => {
  render(
    <AppProvider deps={mockDeps}>
      <UserProfile userId="1" />
    </AppProvider>
  )

  await screen.findByText('Test User')
  expect(mockDeps.api.getUser).toHaveBeenCalledWith('1')
})
```

---

## 7. React 19 Patterns

### use() for Promises (React 19+)

```typescript
import { use, Suspense } from 'react'

// Instead of useEffect + useState for data fetching
function UserProfile({ userPromise }: { userPromise: Promise<User> }) {
  const user = use(userPromise)  // Suspends until resolved
  return <div>{user.name}</div>
}

// Parent provides the promise
function App() {
  const userPromise = fetchUser('1')  // Start fetching immediately

  return (
    <Suspense fallback={<Spinner />}>
      <UserProfile userPromise={userPromise} />
    </Suspense>
  )
}
```

### useActionState for Forms (React 19+)

```typescript
import { useActionState } from 'react'
import * as E from 'fp-ts/Either'

interface FormState {
  errors: string[]
  success: boolean
}

async function submitForm(
  prevState: FormState,
  formData: FormData
): Promise<FormState> {
  const data = {
    email: formData.get('email') as string,
    password: formData.get('password') as string,
  }

  // Use Either for validation
  const result = pipe(
    validateForm(data),
    E.match(
      (errors) => ({ errors, success: false }),
      async (valid) => {
        await saveToServer(valid)
        return { errors: [], success: true }
      }
    )
  )

  return result
}

function SignupForm() {
  const [state, formAction, isPending] = useActionState(submitForm, {
    errors: [],
    success: false
  })

  return (
    <form action={formAction}>
      <input name="email" type="email" />
      <input name="password" type="password" />

      {state.errors.map(e => <p key={e} className="error">{e}</p>)}

      <button disabled={isPending}>
        {isPending ? 'Submitting...' : 'Sign Up'}
      </button>
    </form>
  )
}
```

### useOptimistic for Instant Feedback (React 19+)

```typescript
import { useOptimistic } from 'react'

function TodoList({ todos }: { todos: Todo[] }) {
  const [optimisticTodos, addOptimisticTodo] = useOptimistic(
    todos,
    (state, newTodo: Todo) => [...state, { ...newTodo, pending: true }]
  )

  const addTodo = async (text: string) => {
    const newTodo = { id: crypto.randomUUID(), text, done: false }

    // Immediately show in UI
    addOptimisticTodo(newTodo)

    // Actually save (will reconcile when done)
    await saveTodo(newTodo)
  }

  return (
    <ul>
      {optimisticTodos.map(todo => (
        <li key={todo.id} style={{ opacity: todo.pending ? 0.5 : 1 }}>
          {todo.text}
        </li>
      ))}
    </ul>
  )
}
```

---

## 8. Common Patterns Cheat Sheet

### Render Based on Option

```typescript
// Pattern 1: match
pipe(
  maybeUser,
  O.match(
    () => <LoginButton />,
    (user) => <UserMenu user={user} />
  )
)

// Pattern 2: fold (same as match)
O.fold(
  () => <LoginButton />,
  (user) => <UserMenu user={user} />
)(maybeUser)

// Pattern 3: getOrElse for simple defaults
const name = pipe(
  maybeUser,
  O.map(u => u.name),
  O.getOrElse(() => 'Guest')
)
```

### Render Based on Either

```typescript
pipe(
  validationResult,
  E.match(
    (errors) => <ErrorList errors={errors} />,
    (data) => <SuccessMessage data={data} />
  )
)
```

### Safe Array Rendering

```typescript
import * as A from 'fp-ts/Array'

// Get first item safely
const firstUser = pipe(
  users,
  A.head,
  O.map(user => <Featured user={user} />),
  O.getOrElse(() => <NoFeaturedUser />)
)

// Find specific item
const adminUser = pipe(
  users,
  A.findFirst(u => u.role === 'admin'),
  O.map(admin => <AdminBadge user={admin} />),
  O.toNullable  // or O.getOrElse(() => null)
)
```

### Conditional Props

```typescript
// Add props only if value exists
const modalProps = {
  isOpen: true,
  ...pipe(
    maybeTitle,
    O.map(title => ({ title })),
    O.getOrElse(() => ({}))
  )
}
```

---

## When to Use What

| Situation | Use |
|-----------|-----|
| Value might not exist | `Option<T>` |
| Operation might fail (sync) | `Either<E, A>` |
| Async operation might fail | `TaskEither<E, A>` |
| Need loading/error/success UI | `RemoteData<E, A>` |
| Form with multiple validations | `Either` with validation applicative |
| Dependency injection | Context + `ReaderTaskEither` |
| Prevent re-renders with fp-ts | `useMemo` or `fp-ts-react-stable-hooks` |

---

## Libraries

- **[fp-ts](https://github.com/gcanti/fp-ts)** - Core library
- **[fp-ts-react-stable-hooks](https://github.com/mblink/fp-ts-react-stable-hooks)** - Stable hooks
- **[@devexperts/remote-data-ts](https://github.com/devexperts/remote-data-ts)** - RemoteData
- **[io-ts](https://github.com/gcanti/io-ts)** - Runtime type validation
- **[zod](https://github.com/colinhacks/zod)** - Schema validation (works great with fp-ts)

---

# Practical Error Handling with fp-ts

This skill teaches you how to handle errors without try/catch spaghetti. No academic jargon - just practical patterns for real problems.

## When to Use This Skill

- When you want type-safe error handling in TypeScript
- When replacing try/catch with Either and TaskEither patterns
- When building APIs or services that need explicit error types
- When accumulating multiple validation errors

The core idea: **Errors are just data**. Instead of throwing them into the void and hoping someone catches them, return them as values that TypeScript can track.

---

## 1. Stop Throwing Everywhere

### The Problem with Exceptions

Exceptions are invisible in your types. They break the contract between functions.

```typescript
// What this function signature promises:
function getUser(id: string): User

// What it actually does:
function getUser(id: string): User {
  if (!id) throw new Error('ID required')
  const user = db.find(id)
  if (!user) throw new Error('User not found')
  return user
}

// The caller has no idea this can fail
const user = getUser(id) // Might explode!
```

You end up with code like this:

```typescript
// MESSY: try/catch everywhere
function processOrder(orderId: string) {
  let order
  try {
    order = getOrder(orderId)
  } catch (e) {
    console.error('Failed to get order')
    return null
  }

  let user
  try {
    user = getUser(order.userId)
  } catch (e) {
    console.error('Failed to get user')
    return null
  }

  let payment
  try {
    payment = chargeCard(user.cardId, order.total)
  } catch (e) {
    console.error('Payment failed')
    return null
  }

  return { order, user, payment }
}
```

### The Solution: Return Errors as Values

```typescript
import * as E from 'fp-ts/Either'
import { pipe } from 'fp-ts/function'

// Now TypeScript KNOWS this can fail
function getUser(id: string): E.Either<string, User> {
  if (!id) return E.left('ID required')
  const user = db.find(id)
  if (!user) return E.left('User not found')
  return E.right(user)
}

// The caller is forced to handle both cases
const result = getUser(id)
// result is Either<string, User> - error OR success, never both
```

---

## 2. The Result Pattern (Either)

`Either<E, A>` is simple: it holds either an error (`E`) or a value (`A`).

- `Left` = error case
- `Right` = success case (think "right" as in "correct")

```typescript
import * as E from 'fp-ts/Either'

// Creating values
const success = E.right(42)           // Right(42)
const failure = E.left('Oops')        // Left('Oops')

// Checking what you have
if (E.isRight(result)) {
  console.log(result.right) // The success value
} else {
  console.log(result.left)  // The error
}

// Better: pattern match with fold
const message = pipe(
  result,
  E.fold(
    (error) => `Failed: ${error}`,
    (value) => `Got: ${value}`
  )
)
```

### Converting Throwing Code to Either

```typescript
// Wrap any throwing function with tryCatch
const parseJSON = (json: string): E.Either<Error, unknown> =>
  E.tryCatch(
    () => JSON.parse(json),
    (e) => (e instanceof Error ? e : new Error(String(e)))
  )

parseJSON('{"valid": true}')  // Right({ valid: true })
parseJSON('not json')          // Left(SyntaxError: ...)

// For functions you'll reuse, use tryCatchK
const safeParseJSON = E.tryCatchK(
  JSON.parse,
  (e) => (e instanceof Error ? e : new Error(String(e)))
)
```

### Common Either Operations

```typescript
import * as E from 'fp-ts/Either'
import { pipe } from 'fp-ts/function'

// Transform the success value
const doubled = pipe(
  E.right(21),
  E.map(n => n * 2)
) // Right(42)

// Transform the error
const betterError = pipe(
  E.left('bad'),
  E.mapLeft(e => `Error: ${e}`)
) // Left('Error: bad')

// Provide a default for errors
const value = pipe(
  E.left('failed'),
  E.getOrElse(() => 0)
) // 0

// Convert nullable to Either
const fromNullable = E.fromNullable('not found')
fromNullable(user)  // Right(user) if exists, Left('not found') if null/undefined
```

---

## 3. Chaining Operations That Might Fail

The real power comes from chaining. Each step can fail, but you write it as a clean pipeline.

### Before: Nested Try/Catch Hell

```typescript
// MESSY: Each step can fail, nested try/catch everywhere
function processUserOrder(userId: string, productId: string): Result | null {
  let user
  try {
    user = getUser(userId)
  } catch (e) {
    logError('User fetch failed', e)
    return null
  }

  if (!user.isActive) {
    logError('User not active')
    return null
  }

  let product
  try {
    product = getProduct(productId)
  } catch (e) {
    logError('Product fetch failed', e)
    return null
  }

  if (product.stock < 1) {
    logError('Out of stock')
    return null
  }

  let order
  try {
    order = createOrder(user, product)
  } catch (e) {
    logError('Order creation failed', e)
    return null
  }

  return order
}
```

### After: Clean Chain with Either

```typescript
import * as E from 'fp-ts/Either'
import { pipe } from 'fp-ts/function'

// Each function returns Either<Error, T>
const getUser = (id: string): E.Either<string, User> => { ... }
const getProduct = (id: string): E.Either<string, Product> => { ... }
const createOrder = (user: User, product: Product): E.Either<string, Order> => { ... }

// Chain them together - first error stops the chain
const processUserOrder = (userId: string, productId: string): E.Either<string, Order> =>
  pipe(
    getUser(userId),
    E.filterOrElse(
      user => user.isActive,
      () => 'User not active'
    ),
    E.chain(user =>
      pipe(
        getProduct(productId),
        E.filterOrElse(
          product => product.stock >= 1,
          () => 'Out of stock'
        ),
        E.chain(product => createOrder(user, product))
      )
    )
  )

// Or use Do notation for cleaner access to intermediate values
const processUserOrder = (userId: string, productId: string): E.Either<string, Order> =>
  pipe(
    E.Do,
    E.bind('user', () => getUser(userId)),
    E.filterOrElse(
      ({ user }) => user.isActive,
      () => 'User not active'
    ),
    E.bind('product', () => getProduct(productId)),
    E.filterOrElse(
      ({ product }) => product.stock >= 1,
      () => 'Out of stock'
    ),
    E.chain(({ user, product }) => createOrder(user, product))
  )
```

### Different Error Types? Use chainW

```typescript
type ValidationError = { type: 'validation'; message: string }
type DbError = { type: 'db'; message: string }

const validateInput = (id: string): E.Either<ValidationError, string> => { ... }
const fetchFromDb = (id: string): E.Either<DbError, User> => { ... }

// chainW (W = "wider") automatically unions the error types
const process = (id: string): E.Either<ValidationError | DbError, User> =>
  pipe(
    validateInput(id),
    E.chainW(validId => fetchFromDb(validId))
  )
```

---

## 4. Collecting Multiple Errors

Sometimes you want ALL errors, not just the first one. Form validation is the classic example.

### Before: Collecting Errors Manually

```typescript
// MESSY: Manual error accumulation
function validateForm(form: FormData): { valid: boolean; errors: string[] } {
  const errors: string[] = []

  if (!form.email) {
    errors.push('Email required')
  } else if (!form.email.includes('@')) {
    errors.push('Invalid email')
  }

  if (!form.password) {
    errors.push('Password required')
  } else if (form.password.length < 8) {
    errors.push('Password too short')
  }

  if (!form.age) {
    errors.push('Age required')
  } else if (form.age < 18) {
    errors.push('Must be 18+')
  }

  return { valid: errors.length === 0, errors }
}
```

### After: Validation with Error Accumulation

```typescript
import * as E from 'fp-ts/Either'
import * as NEA from 'fp-ts/NonEmptyArray'
import { sequenceS } from 'fp-ts/Apply'
import { pipe } from 'fp-ts/function'

// Errors as a NonEmptyArray (always at least one)
type Errors = NEA.NonEmptyArray<string>

// Create the applicative that accumulates errors
const validation = E.getApplicativeValidation(NEA.getSemigroup<string>())

// Validators that return Either<Errors, T>
const validateEmail = (email: string): E.Either<Errors, string> =>
  !email ? E.left(NEA.of('Email required'))
  : !email.includes('@') ? E.left(NEA.of('Invalid email'))
  : E.right(email)

const validatePassword = (password: string): E.Either<Errors, string> =>
  !password ? E.left(NEA.of('Password required'))
  : password.length < 8 ? E.left(NEA.of('Password too short'))
  : E.right(password)

const validateAge = (age: number | undefined): E.Either<Errors, number> =>
  age === undefined ? E.left(NEA.of('Age required'))
  : age < 18 ? E.left(NEA.of('Must be 18+'))
  : E.right(age)

// Combine all validations - collects ALL errors
const validateForm = (form: FormData) =>
  sequenceS(validation)({
    email: validateEmail(form.email),
    password: validatePassword(form.password),
    age: validateAge(form.age)
  })

// Usage
validateForm({ email: '', password: '123', age: 15 })
// Left(['Email required', 'Password too short', 'Must be 18+'])

validateForm({ email: 'a@b.com', password: 'longpassword', age: 25 })
// Right({ email: 'a@b.com', password: 'longpassword', age: 25 })
```

### Field-Level Errors for Forms

```typescript
interface FieldError {
  field: string
  message: string
}

type FormErrors = NEA.NonEmptyArray<FieldError>

const fieldError = (field: string, message: string): FormErrors =>
  NEA.of({ field, message })

const formValidation = E.getApplicativeValidation(NEA.getSemigroup<FieldError>())

// Now errors know which field they belong to
const validateEmail = (email: string): E.Either<FormErrors, string> =>
  !email ? E.left(fieldError('email', 'Required'))
  : !email.includes('@') ? E.left(fieldError('email', 'Invalid format'))
  : E.right(email)

// Easy to display in UI
const getFieldError = (errors: FormErrors, field: string): string | undefined =>
  errors.find(e => e.field === field)?.message
```

---

## 5. Async Operations (TaskEither)

For async operations that can fail, use `TaskEither`. It's like `Either` but for promises.

- `TaskEither<E, A>` = a function that returns `Promise<Either<E, A>>`
- Lazy: nothing runs until you execute it

```typescript
import * as TE from 'fp-ts/TaskEither'
import { pipe } from 'fp-ts/function'

// Wrap any async operation
const fetchUser = (id: string): TE.TaskEither<Error, User> =>
  TE.tryCatch(
    () => fetch(`/api/users/${id}`).then(r => r.json()),
    (e) => (e instanceof Error ? e : new Error(String(e)))
  )

// Chain async operations - just like Either
const getUserPosts = (userId: string): TE.TaskEither<Error, Post[]> =>
  pipe(
    fetchUser(userId),
    TE.chain(user => fetchPosts(user.id))
  )

// Execute when ready
const result = await getUserPosts('123')() // Returns Either<Error, Post[]>
```

### Before: Promise Chain with Error Handling

```typescript
// MESSY: try/catch mixed with promise chains
async function loadDashboard(userId: string) {
  try {
    const user = await fetchUser(userId)
    if (!user) throw new Error('User not found')

    let posts, notifications, settings
    try {
      [posts, notifications, settings] = await Promise.all([
        fetchPosts(user.id),
        fetchNotifications(user.id),
        fetchSettings(user.id)
      ])
    } catch (e) {
      // Which one failed? Who knows!
      console.error('Failed to load data', e)
      return null
    }

    return { user, posts, notifications, settings }
  } catch (e) {
    console.error('Failed to load user', e)
    return null
  }
}
```

### After: Clean TaskEither Pipeline

```typescript
import * as TE from 'fp-ts/TaskEither'
import { sequenceS } from 'fp-ts/Apply'
import { pipe } from 'fp-ts/function'

const loadDashboard = (userId: string) =>
  pipe(
    fetchUser(userId),
    TE.chain(user =>
      pipe(
        // Parallel fetch with sequenceS
        sequenceS(TE.ApplyPar)({
          posts: fetchPosts(user.id),
          notifications: fetchNotifications(user.id),
          settings: fetchSettings(user.id)
        }),
        TE.map(data => ({ user, ...data }))
      )
    )
  )

// Execute and handle both cases
pipe(
  loadDashboard('123'),
  TE.fold(
    (error) => T.of(renderError(error)),
    (data) => T.of(renderDashboard(data))
  )
)()
```

### Retry Failed Operations

```typescript
import * as T from 'fp-ts/Task'
import * as TE from 'fp-ts/TaskEither'
import { pipe } from 'fp-ts/function'

const retry = <E, A>(
  task: TE.TaskEither<E, A>,
  attempts: number,
  delayMs: number
): TE.TaskEither<E, A> =>
  pipe(
    task,
    TE.orElse((error) =>
      attempts > 1
        ? pipe(
            T.delay(delayMs)(T.of(undefined)),
            T.chain(() => retry(task, attempts - 1, delayMs * 2))
          )
        : TE.left(error)
    )
  )

// Retry up to 3 times with exponential backoff
const fetchWithRetry = retry(fetchUser('123'), 3, 1000)
```

### Fallback to Alternative

```typescript
// Try cache first, fall back to API
const getUserData = (id: string) =>
  pipe(
    fetchFromCache(id),
    TE.orElse(() => fetchFromApi(id)),
    TE.orElse(() => TE.right(defaultUser)) // Last resort default
  )
```

---

## 6. Converting Between Patterns

Real codebases have throwing functions, nullable values, and promises. Here's how to work with them.

### From Nullable to Either

```typescript
import * as E from 'fp-ts/Either'
import * as O from 'fp-ts/Option'

// Direct conversion
const user = users.find(u => u.id === id) // User | undefined
const result = E.fromNullable('User not found')(user)

// From Option
const maybeUser: O.Option<User> = O.fromNullable(user)
const eitherUser = pipe(
  maybeUser,
  E.fromOption(() => 'User not found')
)
```

### From Throwing Function to Either

```typescript
// Wrap at the boundary
const safeParse = <T>(schema: ZodSchema<T>) => (data: unknown): E.Either<ZodError, T> =>
  E.tryCatch(
    () => schema.parse(data),
    (e) => e as ZodError
  )

// Use throughout your code
const parseUser = safeParse(UserSchema)
const result = parseUser(rawData) // Either<ZodError, User>
```

### From Promise to TaskEither

```typescript
import * as TE from 'fp-ts/TaskEither'

// Wrap external async functions
const fetchJson = <T>(url: string): TE.TaskEither<Error, T> =>
  TE.tryCatch(
    () => fetch(url).then(r => r.json()),
    (e) => new Error(`Fetch failed: ${e}`)
  )

// Wrap axios, prisma, any async library
const getUserFromDb = (id: string): TE.TaskEither<DbError, User> =>
  TE.tryCatch(
    () => prisma.user.findUniqueOrThrow({ where: { id } }),
    (e) => ({ code: 'DB_ERROR', cause: e })
  )
```

### Back to Promise (Escape Hatch)

Sometimes you need a plain Promise for external APIs.

```typescript
import * as TE from 'fp-ts/TaskEither'
import * as E from 'fp-ts/Either'

const myTaskEither: TE.TaskEither<Error, User> = fetchUser('123')

// Option 1: Get the Either (preserves both cases)
const either: E.Either<Error, User> = await myTaskEither()

// Option 2: Throw on error (for legacy code)
const toThrowingPromise = <E, A>(te: TE.TaskEither<E, A>): Promise<A> =>
  te().then(E.fold(
    (error) => Promise.reject(error),
    (value) => Promise.resolve(value)
  ))

const user = await toThrowingPromise(fetchUser('123')) // Throws if Left

// Option 3: Default on error
const user = await pipe(
  fetchUser('123'),
  TE.getOrElse(() => T.of(defaultUser))
)()
```

---

## Real Scenarios

### Parse User Input Safely

```typescript
interface ParsedInput {
  id: number
  name: string
  tags: string[]
}

const parseInput = (raw: unknown): E.Either<string, ParsedInput> =>
  pipe(
    E.Do,
    E.bind('obj', () =>
      typeof raw === 'object' && raw !== null
        ? E.right(raw as Record<string, unknown>)
        : E.left('Input must be an object')
    ),
    E.bind('id', ({ obj }) =>
      typeof obj.id === 'number'
        ? E.right(obj.id)
        : E.left('id must be a number')
    ),
    E.bind('name', ({ obj }) =>
      typeof obj.name === 'string' && obj.name.length > 0
        ? E.right(obj.name)
        : E.left('name must be a non-empty string')
    ),
    E.bind('tags', ({ obj }) =>
      Array.isArray(obj.tags) && obj.tags.every(t => typeof t === 'string')
        ? E.right(obj.tags as string[])
        : E.left('tags must be an array of strings')
    ),
    E.map(({ id, name, tags }) => ({ id, name, tags }))
  )

// Usage
parseInput({ id: 1, name: 'test', tags: ['a', 'b'] })
// Right({ id: 1, name: 'test', tags: ['a', 'b'] })

parseInput({ id: 'wrong', name: '', tags: null })
// Left('id must be a number')
```

### API Call with Full Error Handling

```typescript
interface ApiError {
  code: string
  message: string
  status?: number
}

const createApiError = (message: string, code = 'UNKNOWN', status?: number): ApiError =>
  ({ code, message, status })

const fetchWithErrorHandling = <T>(url: string): TE.TaskEither<ApiError, T> =>
  pipe(
    TE.tryCatch(
      () => fetch(url),
      () => createApiError('Network error', 'NETWORK')
    ),
    TE.chain(response =>
      response.ok
        ? TE.tryCatch(
            () => response.json() as Promise<T>,
            () => createApiError('Invalid JSON', 'PARSE')
          )
        : TE.left(createApiError(
            `HTTP ${response.status}`,
            response.status === 404 ? 'NOT_FOUND' : 'HTTP_ERROR',
            response.status
          ))
    )
  )

// Usage with pattern matching on error codes
const handleUserFetch = (userId: string) =>
  pipe(
    fetchWithErrorHandling<User>(`/api/users/${userId}`),
    TE.fold(
      (error) => {
        switch (error.code) {
          case 'NOT_FOUND': return T.of(showNotFoundPage())
          case 'NETWORK': return T.of(showOfflineMessage())
          default: return T.of(showGenericError(error.message))
        }
      },
      (user) => T.of(showUserProfile(user))
    )
  )
```

### Process List Where Some Items Might Fail

```typescript
import * as A from 'fp-ts/Array'
import * as E from 'fp-ts/Either'
import { pipe } from 'fp-ts/function'

interface ProcessResult<T> {
  successes: T[]
  failures: Array<{ item: unknown; error: string }>
}

// Process all, collect successes and failures separately
const processAllCollectErrors = <T, R>(
  items: T[],
  process: (item: T) => E.Either<string, R>
): ProcessResult<R> => {
  const results = items.map((item, index) =>
    pipe(
      process(item),
      E.mapLeft(error => ({ item, error, index }))
    )
  )

  return {
    successes: pipe(results, A.filterMap(E.toOption)),
    failures: pipe(
      results,
      A.filterMap(r => E.isLeft(r) ? O.some(r.left) : O.none)
    )
  }
}

// Usage
const parseNumbers = (inputs: string[]) =>
  processAllCollectErrors(inputs, input => {
    const n = parseInt(input, 10)
    return isNaN(n) ? E.left(`Invalid number: ${input}`) : E.right(n)
  })

parseNumbers(['1', 'abc', '3', 'def'])
// {
//   successes: [1, 3],
//   failures: [
//     { item: 'abc', error: 'Invalid number: abc', index: 1 },
//     { item: 'def', error: 'Invalid number: def', index: 3 }
//   ]
// }
```

### Bulk Operations with Partial Success

```typescript
import * as TE from 'fp-ts/TaskEither'
import * as T from 'fp-ts/Task'
import { pipe } from 'fp-ts/function'

interface BulkResult<T> {
  succeeded: T[]
  failed: Array<{ id: string; error: string }>
}

const bulkProcess = <T>(
  ids: string[],
  process: (id: string) => TE.TaskEither<string, T>
): T.Task<BulkResult<T>> =>
  pipe(
    ids,
    A.map(id =>
      pipe(
        process(id),
        TE.fold(
          (error) => T.of({ type: 'failed' as const, id, error }),
          (result) => T.of({ type: 'succeeded' as const, result })
        )
      )
    ),
    T.sequenceArray,
    T.map(results => ({
      succeeded: results
        .filter((r): r is { type: 'succeeded'; result: T } => r.type === 'succeeded')
        .map(r => r.result),
      failed: results
        .filter((r): r is { type: 'failed'; id: string; error: string } => r.type === 'failed')
        .map(({ id, error }) => ({ id, error }))
    }))
  )

// Usage
const deleteUsers = (userIds: string[]) =>
  bulkProcess(userIds, id =>
    pipe(
      deleteUser(id),
      TE.mapLeft(e => e.message)
    )
  )

// All operations run, you get a report of what worked and what didn't
```

---

## Quick Reference

| Pattern | Use When | Example |
|---------|----------|---------|
| `E.right(value)` | Creating a success | `E.right(42)` |
| `E.left(error)` | Creating a failure | `E.left('not found')` |
| `E.tryCatch(fn, onError)` | Wrapping throwing code | `E.tryCatch(() => JSON.parse(s), toError)` |
| `E.fromNullable(error)` | Converting nullable | `E.fromNullable('missing')(maybeValue)` |
| `E.map(fn)` | Transform success | `pipe(result, E.map(x => x * 2))` |
| `E.mapLeft(fn)` | Transform error | `pipe(result, E.mapLeft(addContext))` |
| `E.chain(fn)` | Chain operations | `pipe(getA(), E.chain(a => getB(a.id)))` |
| `E.chainW(fn)` | Chain with different error type | `pipe(validate(), E.chainW(save))` |
| `E.fold(onError, onSuccess)` | Handle both cases | `E.fold(showError, showData)` |
| `E.getOrElse(onError)` | Extract with default | `E.getOrElse(() => 0)` |
| `E.filterOrElse(pred, onFalse)` | Validate with error | `E.filterOrElse(x => x > 0, () => 'must be positive')` |
| `sequenceS(validation)({...})` | Collect all errors | Form validation |

### TaskEither Equivalents

All Either operations have TaskEither equivalents:
- `TE.right`, `TE.left`, `TE.tryCatch`
- `TE.map`, `TE.mapLeft`, `TE.chain`, `TE.chainW`
- `TE.fold`, `TE.getOrElse`, `TE.filterOrElse`
- `TE.orElse` for fallbacks

---

## Summary

1. **Return errors as values** - Use Either/TaskEither instead of throwing
2. **Chain with confidence** - `chain` stops at first error automatically
3. **Collect all errors when needed** - Use validation applicative for forms
4. **Wrap at boundaries** - Convert throwing/Promise code at the edges
5. **Match at the end** - Use `fold` to handle both cases when you're ready to act

The payoff: TypeScript tracks your errors, no more forgotten try/catch, clear control flow, and composable error handling.

---

# Pragmatic Functional Programming

**Read this first.** This guide cuts through the academic jargon and shows you what actually matters. No category theory. No abstract nonsense. Just patterns that make your code better.

## When to Use This Skill

- When starting with fp-ts and need practical guidance
- When writing TypeScript code that handles nullable values, errors, or async operations
- When you want cleaner, more maintainable functional code without the academic overhead
- When refactoring imperative code to functional style

## The Golden Rule

> **If functional programming makes your code harder to read, don't use it.**

FP is a tool, not a religion. Use it when it helps. Skip it when it doesn't.

---

## The 80/20 of FP

These five patterns give you most of the benefits. Master these before exploring anything else.

### 1. Pipe: Chain Operations Clearly

Instead of nesting function calls or creating intermediate variables, chain operations in reading order.

```typescript
import { pipe } from 'fp-ts/function'

// Before: Hard to read (inside-out)
const result = format(validate(parse(input)))

// Before: Too many variables
const parsed = parse(input)
const validated = validate(parsed)
const result = format(validated)

// After: Clear, linear flow
const result = pipe(
  input,
  parse,
  validate,
  format
)
```

**When to use pipe:**
- 3+ transformations on the same data
- You find yourself naming throwaway variables
- Logic reads better top-to-bottom

**When to skip pipe:**
- Just 1-2 operations (direct call is fine)
- The operations don't naturally chain

### 2. Option: Handle Missing Values Without null Checks

Stop writing `if (x !== null && x !== undefined)` everywhere.

```typescript
import * as O from 'fp-ts/Option'
import { pipe } from 'fp-ts/function'

// Before: Defensive null checking
function getUserCity(user: User | null): string {
  if (user === null) return 'Unknown'
  if (user.address === null) return 'Unknown'
  if (user.address.city === null) return 'Unknown'
  return user.address.city
}

// After: Chain through potential missing values
const getUserCity = (user: User | null): string =>
  pipe(
    O.fromNullable(user),
    O.flatMap(u => O.fromNullable(u.address)),
    O.flatMap(a => O.fromNullable(a.city)),
    O.getOrElse(() => 'Unknown')
  )
```

**Plain language translation:**
- `O.fromNullable(x)` = "wrap this value, treating null/undefined as 'nothing'"
- `O.flatMap(fn)` = "if we have something, apply this function"
- `O.getOrElse(() => default)` = "unwrap, or use this default if nothing"

### 3. Either: Make Errors Explicit

Stop throwing exceptions for expected failures. Return errors as values.

```typescript
import * as E from 'fp-ts/Either'
import { pipe } from 'fp-ts/function'

// Before: Hidden failure mode
function parseAge(input: string): number {
  const age = parseInt(input, 10)
  if (isNaN(age)) throw new Error('Invalid age')
  if (age < 0) throw new Error('Age cannot be negative')
  return age
}

// After: Errors are visible in the type
function parseAge(input: string): E.Either<string, number> {
  const age = parseInt(input, 10)
  if (isNaN(age)) return E.left('Invalid age')
  if (age < 0) return E.left('Age cannot be negative')
  return E.right(age)
}

// Using it
const result = parseAge(userInput)
if (E.isRight(result)) {
  console.log(`Age is ${result.right}`)
} else {
  console.log(`Error: ${result.left}`)
}
```

**Plain language translation:**
- `E.right(value)` = "success with this value"
- `E.left(error)` = "failure with this error"
- `E.isRight(x)` = "did it succeed?"

### 4. Map: Transform Without Unpacking

Transform values inside containers without extracting them first.

```typescript
import * as O from 'fp-ts/Option'
import * as E from 'fp-ts/Either'
import * as A from 'fp-ts/Array'
import { pipe } from 'fp-ts/function'

// Transform inside Option
const maybeUser: O.Option<User> = O.some({ name: 'Alice', age: 30 })
const maybeName: O.Option<string> = pipe(
  maybeUser,
  O.map(user => user.name)
)

// Transform inside Either
const result: E.Either<Error, number> = E.right(5)
const doubled: E.Either<Error, number> = pipe(
  result,
  E.map(n => n * 2)
)

// Transform arrays (same concept!)
const numbers = [1, 2, 3]
const doubled = pipe(
  numbers,
  A.map(n => n * 2)
)
```

### 5. FlatMap: Chain Operations That Might Fail

When each step might fail, chain them together.

```typescript
import * as E from 'fp-ts/Either'
import { pipe } from 'fp-ts/function'

const parseJSON = (s: string): E.Either<string, unknown> =>
  E.tryCatch(() => JSON.parse(s), () => 'Invalid JSON')

const extractEmail = (data: unknown): E.Either<string, string> => {
  if (typeof data === 'object' && data !== null && 'email' in data) {
    return E.right((data as { email: string }).email)
  }
  return E.left('No email field')
}

const validateEmail = (email: string): E.Either<string, string> =>
  email.includes('@') ? E.right(email) : E.left('Invalid email format')

// Chain all steps - if any fails, the whole thing fails
const getValidEmail = (input: string): E.Either<string, string> =>
  pipe(
    parseJSON(input),
    E.flatMap(extractEmail),
    E.flatMap(validateEmail)
  )

// Success path: Right('user@example.com')
// Any failure: Left('specific error message')
```

**Plain language:** `flatMap` means "if this succeeded, try the next thing"

---

## When NOT to Use FP

Functional programming is not always the answer. Here's when to keep it simple.

### Simple Null Checks

```typescript
// Just use optional chaining - it's built into the language
const city = user?.address?.city ?? 'Unknown'

// DON'T overcomplicate it
const city = pipe(
  O.fromNullable(user),
  O.flatMap(u => O.fromNullable(u.address)),
  O.flatMap(a => O.fromNullable(a.city)),
  O.getOrElse(() => 'Unknown')
)
```

### Simple Loops

```typescript
// A for loop is fine when you need early exit or complex logic
function findFirst(items: Item[], predicate: (i: Item) => boolean): Item | null {
  for (const item of items) {
    if (predicate(item)) return item
  }
  return null
}

// DON'T force FP when it doesn't help
const result = pipe(
  items,
  A.findFirst(predicate),
  O.toNullable
)
```

### Performance-Critical Code

```typescript
// For hot paths, imperative is faster (no intermediate arrays)
function sumLarge(numbers: number[]): number {
  let sum = 0
  for (let i = 0; i < numbers.length; i++) {
    sum += numbers[i]
  }
  return sum
}

// fp-ts creates intermediate structures
const sum = pipe(numbers, A.reduce(0, (acc, n) => acc + n))
```

### When Your Team Doesn't Know FP

If you're the only one who can read the code, it's not good code.

```typescript
// If your team knows this pattern
async function getUser(id: string): Promise<User | null> {
  try {
    const response = await fetch(`/api/users/${id}`)
    if (!response.ok) return null
    return await response.json()
  } catch {
    return null
  }
}

// Don't force this on them
const getUser = (id: string): TE.TaskEither<Error, User> =>
  pipe(
    TE.tryCatch(() => fetch(`/api/users/${id}`), E.toError),
    TE.flatMap(r => r.ok ? TE.right(r) : TE.left(new Error('Not found'))),
    TE.flatMap(r => TE.tryCatch(() => r.json(), E.toError))
  )
```

---

## Quick Wins: Easy Changes That Improve Code Today

### 1. Replace Nested Ternaries with pipe + fold

```typescript
// Before: Nested ternary nightmare
const message = user === null
  ? 'No user'
  : user.isAdmin
    ? `Admin: ${user.name}`
    : `User: ${user.name}`

// After: Clear case handling
const message = pipe(
  O.fromNullable(user),
  O.fold(
    () => 'No user',
    (u) => u.isAdmin ? `Admin: ${u.name}` : `User: ${u.name}`
  )
)
```

### 2. Replace try-catch with tryCatch

```typescript
// Before: try-catch everywhere
let config
try {
  config = JSON.parse(rawConfig)
} catch {
  config = defaultConfig
}

// After: One-liner
const config = pipe(
  E.tryCatch(() => JSON.parse(rawConfig), () => 'parse error'),
  E.getOrElse(() => defaultConfig)
)
```

### 3. Replace undefined Returns with Option

```typescript
// Before: Caller might forget to check
function findUser(id: string): User | undefined {
  return users.find(u => u.id === id)
}

// After: Type forces caller to handle missing case
function findUser(id: string): O.Option<User> {
  return O.fromNullable(users.find(u => u.id === id))
}
```

### 4. Replace Error Strings with Typed Errors

```typescript
// Before: Just strings
function validate(data: unknown): E.Either<string, User> {
  // ...
  return E.left('validation failed')
}

// After: Structured errors
type ValidationError = {
  field: string
  message: string
}

function validate(data: unknown): E.Either<ValidationError, User> {
  // ...
  return E.left({ field: 'email', message: 'Invalid format' })
}
```

### 5. Use const Assertions for Error Types

```typescript
// Create specific error types without classes
const NotFound = (id: string) => ({ _tag: 'NotFound' as const, id })
const Unauthorized = { _tag: 'Unauthorized' as const }
const ValidationFailed = (errors: string[]) =>
  ({ _tag: 'ValidationFailed' as const, errors })

type AppError =
  | ReturnType<typeof NotFound>
  | typeof Unauthorized
  | ReturnType<typeof ValidationFailed>

// Now you can pattern match
const handleError = (error: AppError): string => {
  switch (error._tag) {
    case 'NotFound': return `Item ${error.id} not found`
    case 'Unauthorized': return 'Please log in'
    case 'ValidationFailed': return error.errors.join(', ')
  }
}
```

---

## Common Refactors: Before and After

### Callback Hell to Pipe

```typescript
// Before
fetchUser(id, (user) => {
  if (!user) return handleNoUser()
  fetchPosts(user.id, (posts) => {
    if (!posts) return handleNoPosts()
    fetchComments(posts[0].id, (comments) => {
      render(user, posts, comments)
    })
  })
})

// After (with TaskEither for async)
import * as TE from 'fp-ts/TaskEither'

const loadData = (id: string) =>
  pipe(
    fetchUser(id),
    TE.flatMap(user => pipe(
      fetchPosts(user.id),
      TE.map(posts => ({ user, posts }))
    )),
    TE.flatMap(({ user, posts }) => pipe(
      fetchComments(posts[0].id),
      TE.map(comments => ({ user, posts, comments }))
    ))
  )

// Execute
const result = await loadData('123')()
pipe(
  result,
  E.fold(handleError, ({ user, posts, comments }) => render(user, posts, comments))
)
```

### Multiple null Checks to Option Chain

```typescript
// Before
function getManagerEmail(employee: Employee): string | null {
  if (!employee.department) return null
  if (!employee.department.manager) return null
  if (!employee.department.manager.email) return null
  return employee.department.manager.email
}

// After
const getManagerEmail = (employee: Employee): O.Option<string> =>
  pipe(
    O.fromNullable(employee.department),
    O.flatMap(d => O.fromNullable(d.manager)),
    O.flatMap(m => O.fromNullable(m.email))
  )

// Use it
pipe(
  getManagerEmail(employee),
  O.fold(
    () => sendToDefault(),
    (email) => sendTo(email)
  )
)
```

### Validation with Multiple Checks

```typescript
// Before: Throws on first error
function validateUser(data: unknown): User {
  if (!data || typeof data !== 'object') throw new Error('Must be object')
  const obj = data as Record<string, unknown>
  if (typeof obj.email !== 'string') throw new Error('Email required')
  if (!obj.email.includes('@')) throw new Error('Invalid email')
  if (typeof obj.age !== 'number') throw new Error('Age required')
  if (obj.age < 0) throw new Error('Age must be positive')
  return obj as User
}

// After: Returns first error, type-safe
const validateUser = (data: unknown): E.Either<string, User> =>
  pipe(
    E.Do,
    E.bind('obj', () =>
      typeof data === 'object' && data !== null
        ? E.right(data as Record<string, unknown>)
        : E.left('Must be object')
    ),
    E.bind('email', ({ obj }) =>
      typeof obj.email === 'string' && obj.email.includes('@')
        ? E.right(obj.email)
        : E.left('Valid email required')
    ),
    E.bind('age', ({ obj }) =>
      typeof obj.age === 'number' && obj.age >= 0
        ? E.right(obj.age)
        : E.left('Valid age required')
    ),
    E.map(({ email, age }) => ({ email, age }))
  )
```

### Promise Chain to TaskEither

```typescript
// Before
async function processOrder(orderId: string): Promise<Receipt> {
  const order = await fetchOrder(orderId)
  if (!order) throw new Error('Order not found')

  const validated = await validateOrder(order)
  if (!validated.success) throw new Error(validated.error)

  const payment = await processPayment(validated.order)
  if (!payment.success) throw new Error('Payment failed')

  return generateReceipt(payment)
}

// After
const processOrder = (orderId: string): TE.TaskEither<string, Receipt> =>
  pipe(
    fetchOrderTE(orderId),
    TE.flatMap(order =>
      order ? TE.right(order) : TE.left('Order not found')
    ),
    TE.flatMap(validateOrderTE),
    TE.flatMap(processPaymentTE),
    TE.map(generateReceipt)
  )
```

---

## The Readability Rule

Before using any FP pattern, ask: **"Would a junior developer understand this?"**

### Too Clever (Avoid)

```typescript
const result = pipe(
  data,
  A.filter(flow(prop('status'), equals('active'))),
  A.map(flow(prop('value'), multiply(2))),
  A.reduce(monoid.concat, monoid.empty),
  O.fromPredicate(gt(threshold))
)
```

### Just Right (Prefer)

```typescript
const activeItems = data.filter(item => item.status === 'active')
const doubledValues = activeItems.map(item => item.value * 2)
const total = doubledValues.reduce((sum, val) => sum + val, 0)
const result = total > threshold ? O.some(total) : O.none
```

### The Middle Ground (Often Best)

```typescript
const result = pipe(
  data,
  A.filter(item => item.status === 'active'),
  A.map(item => item.value * 2),
  A.reduce(0, (sum, val) => sum + val),
  total => total > threshold ? O.some(total) : O.none
)
```

---

## Cheat Sheet

| What you want | Plain language | fp-ts |
|--------------|----------------|-------|
| Handle null/undefined | "Wrap this nullable" | `O.fromNullable(x)` |
| Default for missing | "Use this if nothing" | `O.getOrElse(() => default)` |
| Transform if present | "If something, change it" | `O.map(fn)` |
| Chain nullable operations | "If something, try this" | `O.flatMap(fn)` |
| Return success | "Worked, here's the value" | `E.right(value)` |
| Return failure | "Failed, here's why" | `E.left(error)` |
| Wrap throwing function | "Try this, catch errors" | `E.tryCatch(fn, onError)` |
| Handle both cases | "Do this for error, that for success" | `E.fold(onLeft, onRight)` |
| Chain operations | "Then do this, then that" | `pipe(x, fn1, fn2, fn3)` |

---

## When to Level Up

Once comfortable with these patterns, explore:

1. **TaskEither** - Async operations that can fail (replaces Promise + try/catch)
2. **Validation** - Collect ALL errors instead of stopping at first
3. **Reader** - Dependency injection without classes
4. **Do notation** - Cleaner syntax for multiple bindings

But don't rush. The basics here will handle 80% of real-world scenarios. Get comfortable with these before adding more tools to your belt.

---

## Summary

1. **Use pipe** for 3+ operations
2. **Use Option** for nullable chains
3. **Use Either** for operations that can fail
4. **Use map** to transform wrapped values
5. **Use flatMap** to chain operations that might fail
6. **Skip FP** when it hurts readability
7. **Keep it simple** - if your team can't read it, it's not good code

---
