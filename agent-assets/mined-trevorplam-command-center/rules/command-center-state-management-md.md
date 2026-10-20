---
description: Run Frontend State Management and React Architecture Check
globs: ['src/components/**/*.tsx', 'src/hooks/**/*.ts', 'src/store/**/*.ts']
---

# Frontend: State Management

<audit_rules>

- You MUST prefer URL search parameters for filter/sort/pagination state instead of `useState` so that URLs are shareable.
- You MUST push `useState` as far down the component tree as possible to prevent unnecessary re-renders of parent components.
- You MUST verify that React Context is only used for true global state (like theming or auth). For complex global state, recommend Zustand or Redux.
- You MUST flag prop drilling (passing props through >3 levels of components). Recommend composition or Context instead.
- You MUST ensure side effects in `useEffect` have proper cleanup functions and correct dependency arrays.
  </audit_rules>

<example_good>

```tsx
// Using URL state for shareable filters
import { useSearchParams } from 'next/navigation'

export function ProductList() {
  const searchParams = useSearchParams()
  const category = searchParams.get('category')
  // ... fetch products by category
}
```

</example_good>

<example_bad>

```tsx
// BAD: Using local state for filters makes the URL unshareable
export function ProductList() {
  const [category, setCategory] = useState('all')
  // ...
}
```

</example_bad>
