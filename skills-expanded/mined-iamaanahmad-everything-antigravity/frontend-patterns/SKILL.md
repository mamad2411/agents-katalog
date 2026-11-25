---
name: frontend-patterns
description: Frontend development patterns for React, Next.js, state management, performance optimization, and UI best practices.
model: gemini-2.0-pro-exp
---

# Frontend Development Patterns

Modern frontend patterns for React, Next.js, and performant user interfaces in Antigravity projects.

## Component Patterns

### Composition Over Inheritance

```typescript
export function Card({ children, variant = 'default' }: { children: React.ReactNode; variant?: string }) {
  return <div className={`card card-${variant}`}>{children}</div>
}

export function CardHeader({ children }: { children: React.ReactNode }) {
  return <div className="card-header">{children}</div>
}
```

### Compound Components

```typescript
const TabsContext = createContext<{ activeTab: string; setActiveTab: (t: string) => void } | undefined>(undefined)

export function Tabs({ children, defaultTab }: { children: React.ReactNode; defaultTab: string }) {
  const [activeTab, setActiveTab] = useState(defaultTab)
  return <TabsContext.Provider value={{ activeTab, setActiveTab }}>{children}</TabsContext.Provider>
}

export function Tab({ id, children }: { id: string; children: React.ReactNode }) {
  const ctx = useContext(TabsContext)
  if (!ctx) throw new Error('Tab must be used within Tabs')
  return <button className={ctx.activeTab === id ? 'active' : ''} onClick={() => ctx.setActiveTab(id)}>{children}</button>
}
```

## Custom Hooks Patterns

### Debounce Hook

```typescript
export function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value)
  useEffect(() => {
    const handler = setTimeout(() => setDebouncedValue(value), delay)
    return () => clearTimeout(handler)
  }, [value, delay])
  return debouncedValue
}
```

### Async Data Fetching Hook

```typescript
export function useQuery<T>(key: string, fetcher: () => Promise<T>, options?: { enabled?: boolean }) {
  const [data, setData] = useState<T | null>(null)
  const [error, setError] = useState<Error | null>(null)
  const [loading, setLoading] = useState(false)

  const refetch = useCallback(async () => {
    setLoading(true)
    try {
      setData(await fetcher())
    } catch (err) {
      setError(err as Error)
    } finally {
      setLoading(false)
    }
  }, [fetcher])

  useEffect(() => {
    if (options?.enabled !== false) refetch()
  }, [key, refetch, options?.enabled])

  return { data, error, loading, refetch }
}
```

### Toggle Hook

```typescript
export function useToggle(initial = false): [boolean, () => void] {
  const [value, setValue] = useState(initial)
  const toggle = useCallback(() => setValue(v => !v), [])
  return [value, toggle]
}
```

## State Management Patterns

### Context + Reducer Pattern

```typescript
type Action =
  | { type: 'SET_ITEMS'; payload: Item[] }
  | { type: 'SET_LOADING'; payload: boolean }

function reducer(state: State, action: Action): State {
  switch (action.type) {
    case 'SET_ITEMS': return { ...state, items: action.payload }
    case 'SET_LOADING': return { ...state, loading: action.payload }
    default: return state
  }
}

export function useAppState() {
  const ctx = useContext(AppContext)
  if (!ctx) throw new Error('useAppState must be used within AppProvider')
  return ctx
}
```

## Performance Optimization

### Memoization

```typescript
// Expensive computation
const sortedItems = useMemo(() => items.sort((a, b) => b.value - a.value), [items])

// Stable callback reference
const handleSearch = useCallback((query: string) => setQuery(query), [])

// Pure component
export const ItemCard = React.memo<ItemCardProps>(({ item }) => (
  <div className="item-card"><h3>{item.name}</h3></div>
))
```

### Code Splitting & Lazy Loading

```typescript
const HeavyChart = lazy(() => import('./HeavyChart'))

export function Dashboard() {
  return (
    <Suspense fallback={<ChartSkeleton />}>
      <HeavyChart data={data} />
    </Suspense>
  )
}
```

### Virtualization for Long Lists

```typescript
import { useVirtualizer } from '@tanstack/react-virtual'

export function VirtualList({ items }: { items: Item[] }) {
  const parentRef = useRef<HTMLDivElement>(null)
  const virtualizer = useVirtualizer({
    count: items.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 100,
    overscan: 5
  })

  return (
    <div ref={parentRef} style={{ height: '600px', overflow: 'auto' }}>
      <div style={{ height: `${virtualizer.getTotalSize()}px`, position: 'relative' }}>
        {virtualizer.getVirtualItems().map(row => (
          <div key={row.index} style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: `${row.size}px`, transform: `translateY(${row.start}px)` }}>
            <ItemCard item={items[row.index]} />
          </div>
        ))}
      </div>
    </div>
  )
}
```

## Form Handling

### Controlled Form with Validation

```typescript
export function CreateForm() {
  const [formData, setFormData] = useState({ name: '', description: '' })
  const [errors, setErrors] = useState<Record<string, string>>({})

  const validate = (): boolean => {
    const newErrors: Record<string, string> = {}
    if (!formData.name.trim()) newErrors.name = 'Name is required'
    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!validate()) return
    await submitForm(formData)
  }

  return (
    <form onSubmit={handleSubmit}>
      <input value={formData.name} onChange={e => setFormData(p => ({ ...p, name: e.target.value }))} />
      {errors.name && <span className="error">{errors.name}</span>}
      <button type="submit">Submit</button>
    </form>
  )
}
```

## Error Boundary Pattern

```typescript
export class ErrorBoundary extends React.Component<
  { children: React.ReactNode },
  { hasError: boolean; error: Error | null }
> {
  state = { hasError: false, error: null }

  static getDerivedStateFromError(error: Error) {
    return { hasError: true, error }
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="error-fallback">
          <h2>Something went wrong</h2>
          <button onClick={() => this.setState({ hasError: false })}>Try again</button>
        </div>
      )
    }
    return this.props.children
  }
}
```

## Accessibility Patterns

### Keyboard Navigation

```typescript
const handleKeyDown = (e: React.KeyboardEvent) => {
  switch (e.key) {
    case 'ArrowDown': e.preventDefault(); setActiveIndex(i => Math.min(i + 1, options.length - 1)); break
    case 'ArrowUp': e.preventDefault(); setActiveIndex(i => Math.max(i - 1, 0)); break
    case 'Enter': e.preventDefault(); onSelect(options[activeIndex]); break
    case 'Escape': setIsOpen(false); break
  }
}
```

**Remember**: Modern frontend patterns enable maintainable, performant user interfaces. Choose patterns that fit your project complexity.
