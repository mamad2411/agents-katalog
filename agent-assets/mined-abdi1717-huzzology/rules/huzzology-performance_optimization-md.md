---
description: 
globs: 
alwaysApply: false
---
# Next.js Performance Optimization

- **Development Speed Optimization**
  - Use `npm run dev:fast` (with environment flags) for rapid development iterations
  - Configure `.npmrc` with development-focused optimizations
  - Optimize `tsconfig.json` with performance-focused watch options
  - Use the cache cleaning script (`npm run clean`) when encountering strange compilation errors

- **Configuration Best Practices**
  - Remove unsupported or deprecated experimental features from `next.config.js`
  - Use only well-tested, supported features specific to your Next.js version
  - Follow the pattern: `reactStrictMode: false` for development, `true` for production
  - Optimize image formats with `images.formats: ['image/avif', 'image/webp']`

- **Code Splitting**
  - Use dynamic imports with the `lazyImport` utility function from `lib/utils.ts`
  - Split large components, especially on route-specific pages
  - Follow the pattern:
  ```typescript
  const HeavyComponent = lazyImport(
    () => import('@/components/heavy-component'),
    { ssr: false, displayName: 'HeavyComponent' }
  );
  ```

- **Context Provider Optimization**
  - Load context providers only when needed by specific routes
  - Wrap route-specific providers in dynamic imports
  - Keep common providers in shared layouts
  - Avoid deep provider nesting with composition where possible

- **ShadCN UI Component Rules**
  - Follow this pattern for selects with "All" options (avoid empty string values):
  ```tsx
  <Select value={filter} onValueChange={setFilter}>
    <SelectContent>
      {/* ✅ DO: Use a non-empty string like "all" */}
      <SelectItem value="all">All Items</SelectItem>
      
      {/* ❌ DON'T: Use empty string values */}
      <SelectItem value="">All Items</SelectItem>
    </SelectContent>
  </Select>
  ```
  - Match state handling for these components:
  ```tsx
  const [filter, setFilter] = useState('all');
  
  // Filter logic using the value
  const filtered = useMemo(() => {
    return items.filter(item => 
      filter === 'all' ? true : item.category === filter
    );
  }, [items, filter]);
  ```

- **Bundle Size Reduction**
  - Use proper dynamic imports with the `{ ssr: false }` option for client-only components
  - Include only necessary Tailwind CSS classes
  - Avoid unnecessary dependencies, especially for basic UI needs already covered by ShadCN
  - Use `next/image` for automatic size optimization and WebP/AVIF conversion

- **Preventing Unnecessary Re-renders**
  - Memoize expensive components with `React.memo`
  - Memoize complex calculations with `useMemo`
  - Memoize callback functions with `useCallback`
  - Use optimized state management: prefer `useState` + `useCallback` + context over Redux for most needs

- **Diagnostics & Troubleshooting**
  - Check for "deoptimized the styling of X" warnings (normal for large dependencies)
  - Use browser devtools Network tab to identify slow-loading assets
  - For component performance, use React DevTools Profiler
  - If app remains slow after optimizations, check for memory leaks using Chrome performance tools
