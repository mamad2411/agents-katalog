---
name: nextjs-server-components
description: Default to React Server Components; use 'use client' only at leaf interactive nodes
---

# Next.js Server Components

React Server Components (RSC) are the default in the Next.js App Router (stable since Next.js 13.4). Every component in `app/` is a Server Component unless explicitly marked otherwise.

## Rules

- **Do not add `'use client'` unless required.** A component needs `'use client'` only if it uses browser APIs (`window`, `document`, `localStorage`), React hooks (`useState`, `useEffect`, `useRef`), or event handlers (`onClick`, `onChange`).
- **Push `'use client'` to the leaves.** If only a small interactive part of a large component tree needs client-side behavior, extract that part into a separate file and mark only that file.
- **Never mark a layout or a page `'use client'`** unless every single child also needs to be a Client Component — layouts and pages should stay on the server.
- **Pass Server Component output as `children` props** into Client Components instead of importing Server Components inside Client Components (which is not supported).

## Examples

```tsx
// BAD — entire page becomes a Client Component for one button
'use client'
export default function ProductPage({ product }) {
  const [count, setCount] = useState(0)
  return (
    <main>
      <h1>{product.name}</h1>  {/* could have been a Server Component */}
      <button onClick={() => setCount(c => c + 1)}>{count}</button>
    </main>
  )
}

// GOOD — only the interactive leaf is a Client Component
// components/AddToCartButton.tsx
'use client'
export function AddToCartButton() {
  const [count, setCount] = useState(0)
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>
}

// app/products/[id]/page.tsx — stays a Server Component
import { AddToCartButton } from '@/components/AddToCartButton'
export default async function ProductPage({ params }) {
  const product = await fetchProduct(params.id)
  return (
    <main>
      <h1>{product.name}</h1>
      <AddToCartButton />
    </main>
  )
}
```
