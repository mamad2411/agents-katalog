---
name: react-component-architecture
description: |
  React 18 component design patterns. Apply when building components, hooks, contexts, or
  compound components. Covers composition patterns, render props, compound components,
  custom hooks extraction, ref forwarding, and component testing with Testing Library.
---

# React Component Architecture

## Component Design Rules
1. Single Responsibility — one component, one purpose
2. Props interface explicit and typed (TypeScript always)
3. No prop drilling beyond 2 levels (use context or Zustand)
4. Prefer composition over configuration
5. Extract custom hooks when logic exceeds 10 lines

## Compound Component Pattern (Complex UI)
```tsx
// Example: Tabs compound component
interface TabsContextValue {
  activeTab: string;
  setActiveTab: (id: string) => void;
}

const TabsContext = createContext<TabsContextValue | null>(null);

function useTabs() {
  const ctx = useContext(TabsContext);
  if (!ctx) throw new Error('useTabs must be used within <Tabs>');
  return ctx;
}

// Root
function Tabs({ defaultTab, children }: { defaultTab: string; children: ReactNode }) {
  const [activeTab, setActiveTab] = useState(defaultTab);
  return (
    <TabsContext.Provider value={{ activeTab, setActiveTab }}>
      <div className="tabs">{children}</div>
    </TabsContext.Provider>
  );
}

// Sub-components
function TabList({ children }: { children: ReactNode }) {
  return <div role="tablist" className="flex border-b">{children}</div>;
}

function Tab({ id, children }: { id: string; children: ReactNode }) {
  const { activeTab, setActiveTab } = useTabs();
  return (
    <button
      role="tab"
      aria-selected={activeTab === id}
      onClick={() => setActiveTab(id)}
      className={cn('tab-btn', activeTab === id && 'tab-btn--active')}
    >
      {children}
    </button>
  );
}

function TabPanel({ id, children }: { id: string; children: ReactNode }) {
  const { activeTab } = useTabs();
  if (activeTab !== id) return null;
  return <div role="tabpanel">{children}</div>;
}

// Attach sub-components
Tabs.List = TabList;
Tabs.Tab = Tab;
Tabs.Panel = TabPanel;

// Usage — reads like English
<Tabs defaultTab="orders">
  <Tabs.List>
    <Tabs.Tab id="orders">Orders</Tabs.Tab>
    <Tabs.Tab id="products">Products</Tabs.Tab>
  </Tabs.List>
  <Tabs.Panel id="orders"><OrdersTable /></Tabs.Panel>
  <Tabs.Panel id="products"><ProductsGrid /></Tabs.Panel>
</Tabs>
```

## Custom Hook Extraction
```tsx
// Extract all stateful logic into named hooks
function useProductSearch(initialQuery = '') {
  const [query, setQuery] = useState(initialQuery);
  const debouncedQuery = useDebounce(query, 300);

  const { data, isLoading, error } = useQuery({
    queryKey: ['products', 'search', debouncedQuery],
    queryFn: () => api.products.search(debouncedQuery),
    enabled: debouncedQuery.length >= 2,
    staleTime: 30_000,
  });

  return {
    query,
    setQuery,
    results: data?.items ?? [],
    isSearching: isLoading && debouncedQuery.length >= 2,
    error,
    hasResults: (data?.total ?? 0) > 0,
  };
}

// Component becomes clean
function ProductSearch() {
  const { query, setQuery, results, isSearching } = useProductSearch();
  return (
    <div>
      <SearchInput value={query} onChange={setQuery} isLoading={isSearching} />
      <SearchResults items={results} />
    </div>
  );
}
```

## Ref Forwarding
```tsx
// For reusable form elements that need ref access
const TextInput = forwardRef<HTMLInputElement, TextInputProps>(
  ({ label, error, ...props }, ref) => (
    <div className="form-field">
      {label && <label className="form-label">{label}</label>}
      <input ref={ref} className={cn('form-input', error && 'form-input--error')} {...props} />
      {error && <p className="form-error">{error}</p>}
    </div>
  )
);
TextInput.displayName = 'TextInput';
```

## Component Testing (Vitest + Testing Library)
```tsx
import { render, screen, userEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';

describe('ProductCard', () => {
  const mockProduct = { id: '1', name: 'Widget Pro', price: 49.99, stock: 5 };

  it('should display product details', () => {
    render(<ProductCard product={mockProduct} />);
    expect(screen.getByText('Widget Pro')).toBeInTheDocument();
    expect(screen.getByText('$49.99')).toBeInTheDocument();
  });

  it('should call onAddToCart when button clicked', async () => {
    const onAddToCart = vi.fn();
    render(<ProductCard product={mockProduct} onAddToCart={onAddToCart} />);
    await userEvent.click(screen.getByRole('button', { name: /add to cart/i }));
    expect(onAddToCart).toHaveBeenCalledWith('1', 1);
  });

  it('should disable add to cart when out of stock', () => {
    const outOfStock = { ...mockProduct, stock: 0 };
    render(<ProductCard product={outOfStock} />);
    expect(screen.getByRole('button', { name: /out of stock/i })).toBeDisabled();
  });
});
```

## Error Boundaries
```tsx
class ErrorBoundary extends Component<
  { children: ReactNode; fallback: ReactNode },
  { hasError: boolean; error: Error | null }
> {
  state = { hasError: false, error: null };

  static getDerivedStateFromError(error: Error) {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, info: ErrorInfo) {
    logger.error('React ErrorBoundary caught', { error, componentStack: info.componentStack });
  }

  render() {
    if (this.state.hasError) return this.props.fallback;
    return this.props.children;
  }
}

// Wrap route-level components
<ErrorBoundary fallback={<ErrorPage />}>
  <Dashboard />
</ErrorBoundary>
```
