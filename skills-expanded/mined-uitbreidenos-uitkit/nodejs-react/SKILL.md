---
name: "react"
description: "React patterns: hooks, context, performance optimisation, component composition, state management, common anti-patterns"
---

# React Skill

## When to activate
- Designing component architecture for a new feature
- Debugging performance issues (unnecessary re-renders)
- Choosing between local state, context, and external state management
- Writing custom hooks to share logic across components
- Implementing compound components, render props, or other composition patterns
- Migrating class components to function components

## When NOT to use
- Next.js App Router features (Server Components, Server Actions) — use the Next.js skill
- React Native — different platform constraints
- Simple static UI with no state — just write HTML

## Instructions

### State — where to put it

| State type | Where to put it |
|---|---|
| UI state (open/closed, selected tab) | Local `useState` in the component |
| Derived data (filtered list, computed total) | `useMemo` — no state, derive from props/state |
| Shared between sibling components | Lift to common parent |
| Shared across a subtree (theme, auth, locale) | Context |
| Server state (API data) | React Query / SWR |
| Complex client state with many interactions | Zustand / Jotai |

**Default to local state.** Only lift when multiple components need it.

### Custom hooks — the right abstraction

Extract logic into a custom hook when the same stateful logic appears in 2+ components:

```typescript
// hooks/useDebounce.ts
function useDebounce<T>(value: T, delayMs: number): T {
  const [debounced, setDebounced] = useState(value)
  useEffect(() => {
    const timer = setTimeout(() => setDebounced(value), delayMs)
    return () => clearTimeout(timer)
  }, [value, delayMs])
  return debounced
}

// hooks/useLocalStorage.ts
function useLocalStorage<T>(key: string, initialValue: T) {
  const [value, setValue] = useState<T>(() => {
    try {
      const item = window.localStorage.getItem(key)
      return item ? JSON.parse(item) : initialValue
    } catch { return initialValue }
  })

  const setStoredValue = (newValue: T) => {
    setValue(newValue)
    window.localStorage.setItem(key, JSON.stringify(newValue))
  }

  return [value, setStoredValue] as const
}

// hooks/useAsync.ts
function useAsync<T>(fn: () => Promise<T>, deps: unknown[]) {
  const [state, setState] = useState<{
    data: T | null; error: Error | null; loading: boolean
  }>({ data: null, error: null, loading: true })

  useEffect(() => {
    setState(s => ({ ...s, loading: true }))
    fn()
      .then(data => setState({ data, error: null, loading: false }))
      .catch(error => setState({ data: null, error, loading: false }))
  }, deps)

  return state
}
```

### Context — only for truly global data

```typescript
// contexts/AuthContext.tsx
type AuthContextValue = {
  user: User | null
  signIn: (email: string, password: string) => Promise<void>
  signOut: () => Promise<void>
}

const AuthContext = createContext<AuthContextValue | null>(null)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)

  const signIn = async (email: string, password: string) => {
    const user = await api.signIn(email, password)
    setUser(user)
  }

  const signOut = async () => {
    await api.signOut()
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, signIn, signOut }}>
      {children}
    </AuthContext.Provider>
  )
}

// Always guard against missing provider
export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be inside AuthProvider')
  return ctx
}
```

**Context anti-patterns to avoid:**
- Don't put everything in one giant context — split by concern
- Don't put fast-changing values (mouse position, scroll) in context — causes re-renders for all consumers
- Don't use context as a substitute for proper state management at scale

### Performance — fixing unnecessary re-renders

```typescript
// 1. memo — skip re-render if props haven't changed
const UserCard = memo(({ user }: { user: User }) => {
  return <div>{user.name}</div>
})

// 2. useMemo — memoize expensive computations
const sortedItems = useMemo(
  () => [...items].sort((a, b) => a.name.localeCompare(b.name)),
  [items] // only recompute when items changes
)

// 3. useCallback — stable function reference for child props
const handleSubmit = useCallback(async (data: FormData) => {
  await api.submit(data)
  refetch()
}, [refetch]) // stable if refetch is stable

// 4. Lazy loading
const HeavyChart = lazy(() => import('./HeavyChart'))

function Dashboard() {
  return (
    <Suspense fallback={<Skeleton />}>
      <HeavyChart />
    </Suspense>
  )
}
```

**How to find what's re-rendering:**
- React DevTools Profiler → record → click around → see which components render and why
- Add `console.log('render', componentName)` temporarily
- `why-did-you-render` library for detailed re-render reasons

**When NOT to memoize:** memoization has overhead. Only add `memo`/`useMemo`/`useCallback` when you've confirmed a component re-renders too often and it's causing actual slowness.

### Component composition patterns

**Compound components (related components that share state):**
```typescript
// Instead of: <Select value={val} options={opts} onChange={fn} />
// Use compound components for complex UIs:

const SelectContext = createContext<SelectContextValue | null>(null)

function Select({ children, value, onChange }: SelectProps) {
  return (
    <SelectContext.Provider value={{ value, onChange }}>
      <div className="select">{children}</div>
    </SelectContext.Provider>
  )
}

Select.Option = function Option({ value, children }: OptionProps) {
  const ctx = useContext(SelectContext)!
  return (
    <div
      className={ctx.value === value ? 'selected' : ''}
      onClick={() => ctx.onChange(value)}
    >
      {children}
    </div>
  )
}

// Usage:
<Select value={selected} onChange={setSelected}>
  <Select.Option value="a">Option A</Select.Option>
  <Select.Option value="b">Option B</Select.Option>
</Select>
```

**Render props / children as function:**
```typescript
function DataFetcher<T>({ url, children }: {
  url: string
  children: (data: T | null, loading: boolean, error: Error | null) => ReactNode
}) {
  const { data, loading, error } = useAsync(() => fetch(url).then(r => r.json()), [url])
  return <>{children(data, loading, error)}</>
}

// Usage:
<DataFetcher url="/api/users">
  {(users, loading, error) => {
    if (loading) return <Spinner />
    if (error) return <ErrorMessage error={error} />
    return <UserList users={users} />
  }}
</DataFetcher>
```

### Common anti-patterns

**Derived state as state (the most common mistake):**
```typescript
// Bad — fullName is derived, doesn't need state
const [firstName, setFirstName] = useState('')
const [lastName, setLastName] = useState('')
const [fullName, setFullName] = useState('')  // ❌

// Good — derive it
const fullName = `${firstName} ${lastName}`  // ✅ just a variable
```

**useEffect for data that can be computed synchronously:**
```typescript
// Bad — useEffect is async by nature
useEffect(() => {
  setFilteredItems(items.filter(i => i.active))
}, [items])

// Good — useMemo is synchronous, happens during render
const filteredItems = useMemo(
  () => items.filter(i => i.active),
  [items]
)
```

**Stale closures in useEffect:**
```typescript
// Bad — count is captured at the time effect runs
useEffect(() => {
  const interval = setInterval(() => {
    console.log(count) // always logs the initial value!
  }, 1000)
  return () => clearInterval(interval)
}, []) // ❌ missing count in deps

// Good — use a ref for values that change but don't need to trigger re-renders
const countRef = useRef(count)
countRef.current = count  // always up to date

useEffect(() => {
  const interval = setInterval(() => {
    console.log(countRef.current) // always current
  }, 1000)
  return () => clearInterval(interval)
}, []) // ✅ interval only created once
```

### State management with Zustand

```typescript
import { create } from 'zustand'
import { persist } from 'zustand/middleware'

type CartStore = {
  items: CartItem[]
  addItem: (item: CartItem) => void
  removeItem: (id: string) => void
  total: () => number
}

export const useCart = create<CartStore>()(
  persist(
    (set, get) => ({
      items: [],
      addItem: (item) => set(state => ({ items: [...state.items, item] })),
      removeItem: (id) => set(state => ({
        items: state.items.filter(i => i.id !== id)
      })),
      total: () => get().items.reduce((sum, i) => sum + i.price * i.qty, 0),
    }),
    { name: 'cart' } // persists to localStorage
  )
)
```

## Example

**User:** A product filter component re-renders too often and slows down a list of 500 items.

**Expected analysis and fix:**
- Wrap the item component in `memo` — items re-render only when their own props change
- Move filter state up and wrap the filter function in `useCallback`
- Use `useMemo` for the filtered + sorted list computation
- Virtualise the list with `@tanstack/virtual` if still slow after memoisation

---
