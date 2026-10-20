---
name: performance-optimization
description: |
  Performance optimization techniques for frontend and backend. Apply when experiencing slow
  queries, high load times, N+1 problems, large bundles, or memory leaks. Covers query optimization,
  N+1 detection, caching layers, frontend bundle splitting, image optimization, and profiling.
---

# Performance Optimization

## Backend Performance

### N+1 Query Detection & Fix
```python
# ❌ N+1 — triggers 1 + N DB queries
orders = Order.objects.all()
for order in orders:
    print(order.user.email)  # New query for each order!

# ✅ select_related — 1 JOIN query (for ForeignKey / OneToOne)
orders = Order.objects.select_related('user', 'user__profile').all()

# ✅ prefetch_related — 2 queries (for ManyToMany / reverse FK)
orders = Order.objects.prefetch_related('items', 'items__product').all()

# Detect N+1 in development:
# pip install django-silk or django-debug-toolbar
# Check: any endpoint making > 10 queries is suspicious
```

### Query Optimization Patterns
```python
# Only fetch needed columns
users = User.objects.values('id', 'email', 'name')  # Not SELECT *

# Use exists() not count() for boolean checks
if Order.objects.filter(user=user, status='pending').exists():  # ✅
if Order.objects.filter(user=user, status='pending').count() > 0:  # ❌

# Bulk operations (not loop inserts)
OrderItem.objects.bulk_create([
    OrderItem(order=order, product_id=p_id, quantity=qty)
    for p_id, qty in items
], batch_size=500)

# Defer heavy text/binary fields not needed immediately
posts = Post.objects.defer('content', 'html_content').all()
```

### Database Connection Pooling
```python
# Django + pgBouncer or django-db-geventpool
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'CONN_MAX_AGE': 60,       # Persistent connections
        'OPTIONS': {'pool_size': 20, 'max_overflow': 30},
    }
}
```

### Response Compression
```python
# Django
MIDDLEWARE = ['django.middleware.gzip.GZipMiddleware', ...]

# FastAPI
from fastapi.middleware.gzip import GZipMiddleware
app.add_middleware(GZipMiddleware, minimum_size=1000)
```

## Frontend Performance

### Code Splitting
```tsx
// Route-level splitting (always)
const Dashboard = lazy(() => import('./pages/Dashboard'));
const AdminPanel = lazy(() => import('./pages/AdminPanel'));

// Component-level splitting for heavy libs
const RichEditor = lazy(() => import('./components/RichEditor'));
const ChartWidget = lazy(() => import('./components/ChartWidget'));

// Wrap with Suspense + skeleton
<Suspense fallback={<DashboardSkeleton />}>
  <Dashboard />
</Suspense>
```

### Image Optimization
```tsx
// Always specify width/height to prevent CLS
<img src={product.image} width={400} height={300} loading="lazy" alt={product.name} />

// Use WebP with fallback
<picture>
  <source srcSet={product.image.webp} type="image/webp" />
  <img src={product.image.jpg} alt={product.name} loading="lazy" />
</picture>

// Next.js: use <Image> component (automatic optimization)
// Vite: use vite-imagetools plugin
```

### React Performance
```tsx
// Virtualize long lists (>100 items)
import { useVirtualizer } from '@tanstack/react-virtual';

// Avoid re-renders: memoize when cost is measurable
const ProcessedData = memo(({ data }: { data: RawData[] }) => {
  const processed = useMemo(() => expensiveTransform(data), [data]);
  return <DataTable rows={processed} />;
});

// Debounce search inputs
const debouncedSearch = useDebounce(searchTerm, 300);

// Avoid anonymous functions in JSX (creates new ref each render)
// ❌ onClick={() => handleClick(item.id)}
// ✅ Create a memoized handler or use data attributes
```

### Bundle Optimization
```typescript
// vite.config.ts
export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          query: ['@tanstack/react-query'],
          motion: ['framer-motion'],
          charts: ['recharts'],
        }
      }
    },
    chunkSizeWarningLimit: 500, // KB
  }
});
```

## Profiling Tools
```bash
# Backend
py-spy top --pid <pid>           # CPU profiling (no code changes needed)
memory_profiler                  # Memory usage per line
django-silk                      # Request/SQL profiling dashboard

# Frontend  
npx vite-bundle-analyzer         # Bundle composition
Chrome DevTools Performance tab  # Runtime profiling
Lighthouse CLI                   # Automated scoring
web-vitals npm package           # Real user monitoring
```
