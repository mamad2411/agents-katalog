---
name: react-patterns-advanced
description: "When to activate: render props, HOC, headless components, suspense, concurrent mode, portals, forwardRef, imperative handles"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: engineering
  language: typescript
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---

# React Advanced Patterns

## Render Props
```tsx
interface RenderProps<T> {
  data: T
  loading: boolean
  error: Error | null
  refetch: () => void
}

function DataProvider<T>({
  url,
  children,
}: {
  url: string
  children: (props: RenderProps<T>) => React.ReactNode
}) {
  const [data, setData] = useState<T | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<Error | null>(null)

  const fetch_ = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const res = await fetch(url)
      setData(await res.json())
    } catch (e) {
      setError(e instanceof Error ? e : new Error(String(e)))
    } finally {
      setLoading(false)
    }
  }, [url])

  useEffect(() => { fetch_() }, [fetch_])

  return <>{children({ data: data as T, loading, error, refetch: fetch_ })}</>
}

// Usage
<DataProvider<User[]> url="/api/users">
  {({ data, loading }) => loading ? <Spinner /> : <UserList users={data} />}
</DataProvider>
```

## Higher-Order Components (sparingly — prefer hooks)
```tsx
function withAuth<P extends { user: User }>(
  Component: React.ComponentType<P>
): React.ComponentType<Omit<P, 'user'>> {
  return function AuthenticatedComponent(props: Omit<P, 'user'>) {
    const user = useAuth()
    if (!user) return <Navigate to="/login" />
    return <Component {...(props as P)} user={user} />
  }
}

const ProtectedDashboard = withAuth(Dashboard)
```

## forwardRef + useImperativeHandle
```tsx
interface DialogHandle {
  open:  () => void
  close: () => void
  isOpen: boolean
}

const Dialog = forwardRef<DialogHandle, { children: ReactNode }>(
  function Dialog({ children }, ref) {
    const [isOpen, setIsOpen] = useState(false)

    useImperativeHandle(ref, () => ({
      open:   () => setIsOpen(true),
      close:  () => setIsOpen(false),
      isOpen,
    }), [isOpen])

    if (!isOpen) return null
    return createPortal(
      <div role="dialog" aria-modal>
        {children}
        <button onClick={() => setIsOpen(false)}>Close</button>
      </div>,
      document.body
    )
  }
)

// Usage
function App() {
  const dialogRef = useRef<DialogHandle>(null)
  return (
    <>
      <button onClick={() => dialogRef.current?.open()}>Open</button>
      <Dialog ref={dialogRef}>
        <p>Dialog content</p>
      </Dialog>
    </>
  )
}
```

## Controlled / Uncontrolled Pattern (shared component)
```tsx
function useControllableState<T>(
  controlled: T | undefined,
  onChange: ((v: T) => void) | undefined,
  defaultValue: T
) {
  const [internal, setInternal] = useState(defaultValue)
  const isControlled = controlled !== undefined
  const value = isControlled ? controlled : internal

  const setValue = useCallback((v: T) => {
    if (!isControlled) setInternal(v)
    onChange?.(v)
  }, [isControlled, onChange])

  return [value, setValue] as const
}

// Component works both controlled and uncontrolled
function Select({
  value: controlledValue,
  defaultValue = '',
  onChange,
  options,
}: SelectProps) {
  const [value, setValue] = useControllableState(controlledValue, onChange, defaultValue)
  // ...
}
```

## Suspense Patterns
```tsx
// Suspense with error recovery
function AsyncSection({ children }: { children: ReactNode }) {
  const [key, setKey] = useState(0)
  return (
    <ErrorBoundary
      key={key}
      fallback={
        <div>
          <p>Failed to load</p>
          <button onClick={() => setKey(k => k + 1)}>Retry</button>
        </div>
      }
    >
      <Suspense fallback={<Skeleton />}>{children}</Suspense>
    </ErrorBoundary>
  )
}

// use() hook (React 19)
function UserProfile({ id }: { id: string }) {
  const user = use(fetchUser(id))  // suspends; must be stable promise
  return <div>{user.name}</div>
}
```

## Context Selectors (avoid full re-renders)
```tsx
// When context value is large, split or use useSyncExternalStore
function createContextSelector<T>(context: React.Context<T>) {
  return function useSelector<S>(selector: (v: T) => S): S {
    const ctx = useContext(context)
    const [, force] = useReducer(x => x + 1, 0)
    const ref = useRef(selector(ctx))

    useEffect(() => {
      const next = selector(ctx)
      if (!Object.is(ref.current, next)) {
        ref.current = next
        force()
      }
    })

    return ref.current
  }
}
```

## Children Utilities
```tsx
// Iterate typed children
import { Children, isValidElement, cloneElement } from 'react'

function RadioGroup({ children, name }: { children: ReactNode; name: string }) {
  return (
    <fieldset>
      {Children.map(children, child => {
        if (isValidElement<{ name?: string }>(child)) {
          return cloneElement(child, { name })
        }
        return child
      })}
    </fieldset>
  )
}
```
