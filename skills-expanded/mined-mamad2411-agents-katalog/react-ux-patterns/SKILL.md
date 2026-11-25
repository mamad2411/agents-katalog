---
name: react-ux-patterns
description: React and Next.js specific UX patterns including state management, data fetching, and component patterns
license: MIT
---

# React UX Best Practices

## Loading States

### Suspense Pattern
```tsx
import { Suspense } from 'react';

<Suspense fallback={<Skeleton />}>
  <DataComponent />
</Suspense>
```

### Query Hook Pattern
```tsx
const { data, isLoading, error } = useQuery({
  queryKey: ['items'],
  queryFn: fetchItems,
});

if (isLoading) return <Skeleton />;
if (error) return <ErrorState error={error} onRetry={refetch} />;
return <ItemList items={data} />;
```

### Deferred Loading
```tsx
import { useDeferredValue } from 'react';

function SearchResults({ query }) {
  const deferredQuery = useDeferredValue(query);
  const isStale = query !== deferredQuery;
  
  return (
    <div style={{ opacity: isStale ? 0.7 : 1 }}>
      <Results query={deferredQuery} />
    </div>
  );
}
```

## Form Patterns

### Controlled Form with Validation
```tsx
import { useForm } from 'react-hook-form';

function ContactForm() {
  const { 
    register, 
    handleSubmit, 
    formState: { errors, isSubmitting } 
  } = useForm();

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <label htmlFor="email">Email</label>
      <input
        id="email"
        type="email"
        aria-invalid={errors.email ? 'true' : 'false'}
        aria-describedby={errors.email ? 'email-error' : undefined}
        {...register('email', { 
          required: 'Email is required',
          pattern: {
            value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
            message: 'Invalid email address'
          }
        })}
      />
      {errors.email && (
        <span id="email-error" role="alert">
          {errors.email.message}
        </span>
      )}
      
      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Sending...' : 'Submit'}
      </button>
    </form>
  );
}
```

### Validation Timing
| Event | Use Case |
|-------|----------|
| onChange | Real-time feedback (debounce 300ms+) |
| onBlur | Field-level validation on exit |
| onSubmit | Final validation before submission |

## Optimistic Updates

### With React Query
```tsx
const mutation = useMutation({
  mutationFn: updateItem,
  onMutate: async (newData) => {
    await queryClient.cancelQueries({ queryKey: ['items'] });
    const previous = queryClient.getQueryData(['items']);
    
    queryClient.setQueryData(['items'], (old) =>
      old.map((item) =>
        item.id === newData.id ? { ...item, ...newData } : item
      )
    );
    
    return { previous };
  },
  onError: (err, newData, context) => {
    queryClient.setQueryData(['items'], context.previous);
    toast.error('Failed to update');
  },
  onSettled: () => {
    queryClient.invalidateQueries({ queryKey: ['items'] });
  },
});
```

### Use Cases for Optimistic UI
- Toggle states (like, bookmark, follow)
- Simple text edits
- Reordering items
- Adding/removing from lists

### Avoid Optimistic UI When
- Complex server validation required
- Financial transactions
- Irreversible actions
- Multi-step processes

## Focus Management

### Modal Focus Trap
```tsx
import { useRef, useEffect } from 'react';

function Modal({ isOpen, onClose, children }) {
  const modalRef = useRef(null);
  const previousFocus = useRef(null);

  useEffect(() => {
    if (isOpen) {
      previousFocus.current = document.activeElement;
      modalRef.current?.focus();
    }
    return () => {
      previousFocus.current?.focus();
    };
  }, [isOpen]);

  return isOpen ? (
    <div
      ref={modalRef}
      role="dialog"
      aria-modal="true"
      tabIndex={-1}
      onKeyDown={(e) => e.key === 'Escape' && onClose()}
    >
      {children}
    </div>
  ) : null;
}
```

### Skip Link
```tsx
function SkipLink() {
  return (
    <a
      href="#main-content"
      className="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4"
    >
      Skip to main content
    </a>
  );
}
```

## Announcements for Screen Readers

### Live Region Hook
```tsx
import { useState, useCallback } from 'react';

function useAnnounce() {
  const [message, setMessage] = useState('');

  const announce = useCallback((text, priority = 'polite') => {
    setMessage('');
    setTimeout(() => setMessage(text), 100);
  }, []);

  const Announcer = () => (
    <div
      role="status"
      aria-live="polite"
      aria-atomic="true"
      className="sr-only"
    >
      {message}
    </div>
  );

  return { announce, Announcer };
}
```

## Error Boundaries

### Functional Error Boundary
```tsx
import { ErrorBoundary } from 'react-error-boundary';

function ErrorFallback({ error, resetErrorBoundary }) {
  return (
    <div role="alert">
      <h2>Something went wrong</h2>
      <pre>{error.message}</pre>
      <button onClick={resetErrorBoundary}>Try again</button>
    </div>
  );
}

<ErrorBoundary
  FallbackComponent={ErrorFallback}
  onReset={() => queryClient.clear()}
>
  <App />
</ErrorBoundary>
```

## Performance UX

### Code Splitting
```tsx
import { lazy, Suspense } from 'react';

const HeavyComponent = lazy(() => import('./HeavyComponent'));

function App() {
  return (
    <Suspense fallback={<Skeleton />}>
      <HeavyComponent />
    </Suspense>
  );
}
```

### Image Optimization (Next.js)
```tsx
import Image from 'next/image';

<Image
  src="/hero.jpg"
  alt="Hero image description"
  width={1200}
  height={600}
  priority={isAboveFold}
  placeholder="blur"
  blurDataURL={blurPlaceholder}
/>
```

### Virtualization for Long Lists
```tsx
import { useVirtualizer } from '@tanstack/react-virtual';

function VirtualList({ items }) {
  const parentRef = useRef(null);
  
  const virtualizer = useVirtualizer({
    count: items.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 50,
  });

  return (
    <div ref={parentRef} style={{ height: '400px', overflow: 'auto' }}>
      <div style={{ height: virtualizer.getTotalSize() }}>
        {virtualizer.getVirtualItems().map((virtualRow) => (
          <div
            key={virtualRow.key}
            style={{
              position: 'absolute',
              top: virtualRow.start,
              height: virtualRow.size,
            }}
          >
            {items[virtualRow.index]}
          </div>
        ))}
      </div>
    </div>
  );
}
```

## Reduced Motion Support

```tsx
function AnimatedComponent() {
  const prefersReducedMotion = useMediaQuery(
    '(prefers-reduced-motion: reduce)'
  );

  return (
    <motion.div
      animate={{ x: 100 }}
      transition={{
        duration: prefersReducedMotion ? 0 : 0.3,
      }}
    />
  );
}
```

### CSS Approach
```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

## Page Layout Patterns

### Consistent Page Layout Component
```tsx
interface PageLayoutProps {
  title: string;
  subtitle?: string;
  backLink?: string | { href: string; label: string };
  headerContent?: React.ReactNode;  // Action buttons
  maxWidth?: 'default' | 'narrow' | 'wide' | 'full';
  children: React.ReactNode;
}

function PageLayout({ title, subtitle, backLink, headerContent, maxWidth = 'default', children }: PageLayoutProps) {
  return (
    <div className="min-h-screen bg-surface-deep p-6">
      <div className={`mx-auto ${maxWidthClasses[maxWidth]}`}>
        {/* Back navigation */}
        {backLink && (
          <Link href={typeof backLink === 'string' ? backLink : backLink.href}>
            <span className="inline-flex items-center text-text-secondary hover:text-accent mb-6">
              <ArrowLeftIcon className="w-4 h-4 mr-2" />
              {typeof backLink === 'string' ? 'Back' : backLink.label}
            </span>
          </Link>
        )}

        {/* Header with title and actions */}
        <div className="flex flex-wrap items-start justify-between gap-4 mb-8">
          <div>
            <h1 className="text-3xl font-bold text-white mb-2">{title}</h1>
            {subtitle && <p className="text-text-secondary">{subtitle}</p>}
          </div>
          {headerContent}
        </div>

        {children}
      </div>
    </div>
  );
}
```

### Page States Components
```tsx
// Loading state
function PageLoading({ message = 'Loading...' }) {
  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="text-center">
        <Spinner className="w-12 h-12 mx-auto mb-4" />
        <p className="text-text-secondary">{message}</p>
      </div>
    </div>
  );
}

// Error state
function PageError({ title, message, backLink, backLabel }) {
  return (
    <div className="min-h-screen flex items-center justify-center p-8">
      <div className="bg-red-900/20 border border-red-600/30 rounded-xl p-8 max-w-md text-center">
        <h2 className="text-xl font-semibold text-red-400 mb-2">{title}</h2>
        <p className="text-text-secondary mb-6">{message}</p>
        {backLink && <Link href={backLink}>{backLabel}</Link>}
      </div>
    </div>
  );
}

// Empty state
function EmptyState({ icon, title, message, action }) {
  return (
    <div className="bg-surface-raised/30 rounded-lg p-8 text-center border border-dashed border-border">
      {icon && <div className="mb-3">{icon}</div>}
      <p className="font-medium">{title}</p>
      {message && <p className="text-sm mt-1 text-text-secondary">{message}</p>}
      {action && <div className="mt-4">{action}</div>}
    </div>
  );
}
```

## Tab Navigation Patterns

### URL-Synced Tabs
```tsx
type TabId = 'overview' | 'career' | 'settings';

function TabbedPage() {
  const router = useRouter();
  const { id, tab: queryTab } = router.query;
  const [activeTab, setActiveTab] = useState<TabId>('overview');

  // Sync tab from URL
  useEffect(() => {
    if (queryTab && isValidTab(queryTab)) {
      setActiveTab(queryTab as TabId);
    }
  }, [queryTab]);

  // Update URL when tab changes (shallow routing)
  const handleTabChange = useCallback((tab: TabId) => {
    setActiveTab(tab);
    const url = tab === 'overview' 
      ? `/items/${id}` 
      : `/items/${id}?tab=${tab}`;
    router.replace(url, undefined, { shallow: true });
  }, [id, router]);

  return (
    <div>
      {/* Tab bar */}
      <div className="flex gap-1 border-b border-border mb-6">
        {['overview', 'career', 'settings'].map((tab) => (
          <button
            key={tab}
            onClick={() => handleTabChange(tab as TabId)}
            className={`px-4 py-2.5 text-sm font-medium relative ${
              activeTab === tab ? 'text-accent' : 'text-text-secondary hover:text-white'
            }`}
          >
            {tab.charAt(0).toUpperCase() + tab.slice(1)}
            {activeTab === tab && (
              <span className="absolute bottom-0 left-0 right-0 h-0.5 bg-accent" />
            )}
          </button>
        ))}
      </div>

      {/* Tab content */}
      {activeTab === 'overview' && <OverviewTab />}
      {activeTab === 'career' && <CareerTab />}
      {activeTab === 'settings' && <SettingsTab />}
    </div>
  );
}
```

### Multi-Unit Tab Manager (Complex)
```tsx
// For workspaces with multiple editable items (like an IDE)
interface TabInfo {
  id: string;
  label: string;
  isDirty: boolean;
}

function useTabManager() {
  const [tabs, setTabs] = useState<TabInfo[]>([]);
  const [activeTabId, setActiveTabId] = useState<string | null>(null);

  const openTab = (id: string, label: string) => {
    if (!tabs.find(t => t.id === id)) {
      setTabs(prev => [...prev, { id, label, isDirty: false }]);
    }
    setActiveTabId(id);
  };

  const closeTab = (id: string) => {
    const tab = tabs.find(t => t.id === id);
    if (tab?.isDirty && !confirm('Unsaved changes. Close anyway?')) return;
    
    setTabs(prev => prev.filter(t => t.id !== id));
    if (activeTabId === id) {
      setActiveTabId(tabs[0]?.id || null);
    }
  };

  return { tabs, activeTabId, openTab, closeTab, setActiveTabId };
}
```

## Modal Patterns

### Confirmation Modal with Loading
```tsx
interface DeleteConfirmModalProps {
  itemName: string;
  isOpen: boolean;
  isDeleting: boolean;
  onConfirm: () => void;
  onCancel: () => void;
}

function DeleteConfirmModal({ itemName, isOpen, isDeleting, onConfirm, onCancel }: DeleteConfirmModalProps) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      {/* Backdrop - clicking closes (unless deleting) */}
      <div
        className="absolute inset-0 bg-black/70 backdrop-blur-sm"
        onClick={!isDeleting ? onCancel : undefined}
      />

      {/* Modal content */}
      <div className="relative bg-surface-base border border-border rounded-xl p-6 max-w-md w-full shadow-2xl">
        <div className="text-center">
          {/* Warning icon */}
          <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-red-900/30 flex items-center justify-center">
            <WarningIcon className="w-8 h-8 text-red-400" />
          </div>

          <h3 className="text-xl font-bold text-white mb-2">Delete Item?</h3>
          <p className="text-text-secondary mb-6">
            Are you sure you want to permanently delete{' '}
            <span className="text-accent font-semibold">{itemName}</span>?
            This action cannot be undone.
          </p>

          <div className="flex items-center justify-center gap-3">
            <Button variant="ghost" onClick={onCancel} disabled={isDeleting}>
              Cancel
            </Button>
            <Button
              variant="danger"
              onClick={onConfirm}
              isLoading={isDeleting}
            >
              Delete
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}
```

### Edit Modal with Form Reset
```tsx
function EditModal({ item, isOpen, onSave, onCancel, isSaving }) {
  const [formData, setFormData] = useState({ name: '', description: '' });

  // Reset form when item changes
  useEffect(() => {
    if (item) {
      setFormData({ name: item.name, description: item.description || '' });
    }
  }, [item]);

  if (!isOpen) return null;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (formData.name.trim()) {
      onSave(formData);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      <div className="absolute inset-0 bg-black/70" onClick={!isSaving ? onCancel : undefined} />
      <div className="relative bg-surface-base rounded-xl p-6 max-w-md w-full">
        <h3 className="text-xl font-bold mb-4">Edit Item</h3>
        
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1.5">Name *</label>
            <input
              type="text"
              value={formData.name}
              onChange={(e) => setFormData(prev => ({ ...prev, name: e.target.value }))}
              className="w-full px-4 py-2.5 bg-surface-raised border border-border rounded-lg"
              required
              autoFocus
            />
          </div>

          <div className="flex justify-end gap-3 pt-4">
            <Button type="button" variant="ghost" onClick={onCancel} disabled={isSaving}>
              Cancel
            </Button>
            <Button type="submit" variant="primary" isLoading={isSaving}>
              Save Changes
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
}
```

## List Page Pattern

### Standard List Page Structure
```tsx
function ListPage() {
  const [items, setItems] = useState([]);
  const [filters, setFilters] = useState({ search: '', status: '' });
  const [isLoading, setIsLoading] = useState(true);

  // Filtered items (memoized)
  const filteredItems = useMemo(() => {
    return items.filter(item => {
      if (filters.search && !item.name.toLowerCase().includes(filters.search.toLowerCase())) {
        return false;
      }
      if (filters.status && item.status !== filters.status) {
        return false;
      }
      return true;
    });
  }, [items, filters]);

  if (isLoading) return <PageLoading message="Loading items..." />;

  return (
    <PageLayout
      title="Items"
      subtitle={`Manage your ${items.length} items`}
      headerContent={
        <Button variant="primary" onClick={handleCreate}>
          <PlusIcon className="w-4 h-4 mr-2" />
          Create Item
        </Button>
      }
    >
      {/* Filters Card */}
      <Card className="mb-6">
        <div className="flex flex-col sm:flex-row gap-4">
          <div className="flex-1">
            <Input
              type="text"
              placeholder="Search..."
              value={filters.search}
              onChange={(e) => setFilters(prev => ({ ...prev, search: e.target.value }))}
            />
          </div>
          <Select
            value={filters.status}
            onChange={(e) => setFilters(prev => ({ ...prev, status: e.target.value }))}
            options={statusOptions}
          />
        </div>

        {/* Results count */}
        <div className="mt-4 text-sm text-text-secondary">
          Showing {filteredItems.length} of {items.length} items
          {filters.search && <span className="text-accent ml-1">(filtered)</span>}
        </div>
      </Card>

      {/* Items Grid or Table */}
      {filteredItems.length === 0 ? (
        <EmptyState
          icon={<EmptyIcon />}
          title={filters.search ? 'No items match your search' : 'No items yet'}
          message={filters.search ? 'Try adjusting your filters' : 'Create your first item'}
          action={!filters.search && <Button onClick={handleCreate}>Create Item</Button>}
        />
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filteredItems.map(item => (
            <ItemCard key={item.id} item={item} onClick={() => handleClick(item)} />
          ))}
        </div>
      )}
    </PageLayout>
  );
}
```

## Detail Page Pattern

### Standard Detail Page Structure
```tsx
function DetailPage() {
  const router = useRouter();
  const { id } = router.query;
  
  const [item, setItem] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);

  if (isLoading) return <PageLoading message="Loading..." />;
  if (!item) return <PageError title="Not Found" message="Item not found" backLink="/items" />;

  return (
    <PageLayout
      title={item.name}
      subtitle={item.description}
      backLink="/items"
      backLabel="Back to Items"
      headerContent={
        <div className="flex items-center gap-3">
          <Button variant="secondary" size="sm" onClick={() => setIsEditModalOpen(true)}>
            <EditIcon className="w-4 h-4 mr-2" />
            Edit
          </Button>
          <Button
            variant="ghost"
            size="sm"
            onClick={() => setIsDeleteModalOpen(true)}
            className="text-red-400 hover:bg-red-900/20"
          >
            <TrashIcon className="w-4 h-4 mr-2" />
            Delete
          </Button>
        </div>
      }
    >
      {/* Detail content - typically multi-column on desktop */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-1 space-y-6">
          <InfoCard item={item} />
          <StatsCard item={item} />
        </div>
        <div className="lg:col-span-2">
          <MainContentCard item={item} />
        </div>
      </div>

      {/* Modals */}
      <DeleteConfirmModal
        itemName={item.name}
        isOpen={isDeleteModalOpen}
        onConfirm={handleDelete}
        onCancel={() => setIsDeleteModalOpen(false)}
      />
      <EditModal
        item={item}
        isOpen={isEditModalOpen}
        onSave={handleSave}
        onCancel={() => setIsEditModalOpen(false)}
      />
    </PageLayout>
  );
}
```
