---
name: react-component-composition
description: Use when structuring React component APIs — composition over inheritance, compound components, render props. Use when a component is growing too many boolean/variant props or children need to share implicit state.
metadata:
  origin: ECC (decomposed from frontend-patterns)
allowed-tools: Read, Edit, Grep, Glob
---

# React component composition patterns

## Composition over inheritance

Split a component into small pieces (`Card`, `CardHeader`, `CardBody`) instead of one component with many flags:

```tsx
export function Card({ children, variant = 'default' }: { children: React.ReactNode; variant?: 'default' | 'outlined' }) {
  return <div className={`card card-${variant}`}>{children}</div>;
}
export function CardHeader({ children }: { children: React.ReactNode }) {
  return <div className="card-header">{children}</div>;
}
// <Card><CardHeader>Title</CardHeader></Card>
```

## Compound components (implicit shared state via Context)

Use when siblings (`Tab`, `TabList`) need to coordinate without prop-drilling:

```tsx
const TabsContext = createContext<{ activeTab: string; setActiveTab: (t: string) => void } | undefined>(undefined);

export function Tabs({ children, defaultTab }: { children: React.ReactNode; defaultTab: string }) {
  const [activeTab, setActiveTab] = useState(defaultTab);
  return <TabsContext.Provider value={{ activeTab, setActiveTab }}>{children}</TabsContext.Provider>;
}
export function Tab({ id, children }: { id: string; children: React.ReactNode }) {
  const ctx = useContext(TabsContext);
  if (!ctx) throw new Error('Tab must be used within Tabs');
  return (
    <button className={ctx.activeTab === id ? 'active' : ''} onClick={() => ctx.setActiveTab(id)}>
      {children}
    </button>
  );
}
```

## Render props

Use when a component owns async/derived state but the caller decides how to render each phase:

```tsx
export function DataLoader<T>({ url, children }: { url: string; children: (data: T | null, loading: boolean, error: Error | null) => React.ReactNode }) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);
  useEffect(() => {
    fetch(url).then((r) => r.json()).then(setData).catch(setError).finally(() => setLoading(false));
  }, [url]);
  return <>{children(data, loading, error)}</>;
}
```

Prefer a custom hook (see `react-custom-hooks`) over render props for new code — render props mainly survive in older codebases or when the "renderer" truly varies per call site.

## When to reach for each

- Two or three visual sub-parts, no shared implicit state → composition.
- Siblings need to read/write one shared piece of state without prop drilling → compound components.
- The consumer needs full control over markup for each async phase → render props (or a hook returning `{data, loading, error}`, see `react-custom-hooks`).
