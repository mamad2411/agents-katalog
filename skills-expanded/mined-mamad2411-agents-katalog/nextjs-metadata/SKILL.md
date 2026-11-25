---
name: nextjs-metadata
description: Define metadata/generateMetadata per page; never use <Head> in App Router
---

# Next.js Metadata

In App Router, page metadata is declared via exported `metadata` objects or `generateMetadata` functions at the `page.tsx` / `layout.tsx` level. The `<Head>` component from `next/head` is a Pages Router API — it does nothing in App Router and must not be used.

## Rules

- **Export `metadata`** (static) or **`generateMetadata`** (dynamic/async) from `page.tsx` or `layout.tsx` — never from Client Components.
- **Never import or use `<Head>` from `next/head`** in App Router code. It silently has no effect.
- **Place global metadata in `app/layout.tsx`** and override at the page level — Next.js merges them automatically.
- **Use `generateMetadata` for dynamic routes** where the title/description depend on fetched data.
- **Always include at minimum `title` and `description`** on every page.

## Examples

```tsx
// BAD — Pages Router pattern, does nothing in App Router
import Head from 'next/head'
export default function ProductPage({ product }) {
  return (
    <>
      <Head>
        <title>{product.name}</title>
      </Head>
      <main>...</main>
    </>
  )
}

// GOOD — static metadata
// app/about/page.tsx
import type { Metadata } from 'next'
export const metadata: Metadata = {
  title: 'About Us',
  description: 'Learn more about our company.',
}
export default function AboutPage() { ... }

// GOOD — dynamic metadata from fetched data
// app/products/[id]/page.tsx
import type { Metadata } from 'next'
type ProductPageProps = { params: { id: string } }
export async function generateMetadata({ params }: ProductPageProps): Promise<Metadata> {
  const product = await fetchProduct(params.id)
  return {
    title: product.name,
    description: product.description,
    openGraph: { images: [product.imageUrl] },
  }
}
export default async function ProductPage({ params }: ProductPageProps) { ... }

// GOOD — global defaults in root layout
// app/layout.tsx
export const metadata: Metadata = {
  title: { template: '%s | Acme', default: 'Acme' },
  description: 'The best product in the world.',
}
```
