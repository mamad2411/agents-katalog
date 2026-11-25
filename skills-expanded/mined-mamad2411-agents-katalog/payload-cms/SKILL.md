---
name: "payload-cms"
description: "Payload CMS: TypeScript-first headless CMS, collection schemas, access control, hooks, REST+GraphQL APIs, Next.js App Router integration"
---

# Payload CMS Skill

## When to activate
- Building a Next.js app that needs a content management system
- Setting up typed content collections (blog posts, products, pages)
- Implementing field-level access control (admin only, author can edit own)
- Using Payload's hooks to trigger side effects on document changes
- Migrating from a SaaS CMS (Contentful, Sanity) to a self-hosted solution

## When NOT to use
- Simple static sites with markdown files — use Astro + content collections
- Non-TypeScript projects — Payload is TypeScript-first
- When you need a visual drag-and-drop page builder — use Webflow or Builder.io

## Instructions

### Installation (with Next.js)

```bash
npx create-payload-app@latest my-app
# Template: Website / E-commerce / Blank
# Database: MongoDB / PostgreSQL
# TypeScript: Yes (default)
```

### Collection schema

```typescript
// collections/Posts.ts
import type { CollectionConfig } from 'payload'

export const Posts: CollectionConfig = {
  slug: 'posts',
  admin: {
    useAsTitle: 'title',
    defaultColumns: ['title', 'status', 'author', 'updatedAt'],
  },
  access: {
    read:   () => true,          // public
    create: isAuthenticated,      // logged in
    update: isAuthorOrAdmin,      // own posts or admin
    delete: isAdmin,              // admin only
  },
  fields: [
    { name: 'title',   type: 'text',     required: true },
    { name: 'slug',    type: 'text',     unique: true, admin: { position: 'sidebar' } },
    { name: 'content', type: 'richText', required: true },
    {
      name: 'status',
      type: 'select',
      options: ['draft', 'published'],
      defaultValue: 'draft',
      admin: { position: 'sidebar' },
    },
    {
      name: 'author',
      type: 'relationship',
      relationTo: 'users',
      admin: { position: 'sidebar' },
    },
    {
      name: 'heroImage',
      type: 'upload',
      relationTo: 'media',
    },
    {
      name: 'tags',
      type: 'array',
      fields: [{ name: 'tag', type: 'text' }],
    },
    {
      name: 'seo',
      type: 'group',
      fields: [
        { name: 'title',       type: 'text' },
        { name: 'description', type: 'textarea' },
      ],
    },
  ],
  timestamps: true,
}
```

### Access control helpers

```typescript
// access/isAdmin.ts
import type { AccessArgs } from 'payload'

export const isAdmin = ({ req: { user } }: AccessArgs) =>
  user?.role === 'admin'

export const isAuthenticated = ({ req: { user } }: AccessArgs) =>
  Boolean(user)

export const isAuthorOrAdmin = ({ req: { user } }: AccessArgs) => {
  if (!user) return false
  if (user.role === 'admin') return true
  return { author: { equals: user.id } }  // constraint-based access
}
```

### Hooks — trigger side effects

```typescript
// hooks run before/after document operations
export const Posts: CollectionConfig = {
  // ...
  hooks: {
    beforeChange: [
      async ({ data, operation }) => {
        // Auto-generate slug from title
        if (operation === 'create' && !data.slug) {
          data.slug = data.title
            .toLowerCase()
            .replace(/[^a-z0-9]+/g, '-')
            .replace(/^-|-$/g, '')
        }
        return data
      },
    ],
    afterChange: [
      async ({ doc, operation }) => {
        // Trigger revalidation when post is published
        if (doc.status === 'published') {
          await fetch(`${process.env.NEXT_PUBLIC_APP_URL}/api/revalidate`, {
            method: 'POST',
            headers: { 'x-revalidate-secret': process.env.REVALIDATE_SECRET! },
            body: JSON.stringify({ slug: doc.slug }),
          })
        }
      },
    ],
    afterDelete: [
      async ({ doc }) => {
        // Clean up related content
        await deleteRelatedMedia(doc.heroImage)
      },
    ],
  },
}
```

### payload.config.ts

```typescript
import { buildConfig } from 'payload'
import { mongooseAdapter } from '@payloadcms/db-mongodb'
// or: import { postgresAdapter } from '@payloadcms/db-postgres'
import { lexicalEditor } from '@payloadcms/richtext-lexical'
import { Posts } from './collections/Posts'
import { Media } from './collections/Media'
import { Users } from './collections/Users'

export default buildConfig({
  serverURL: process.env.NEXT_PUBLIC_APP_URL,
  admin: {
    user: Users.slug,
    meta: { titleSuffix: '— My CMS' },
  },
  collections: [Posts, Media, Users],
  db: mongooseAdapter({ url: process.env.MONGODB_URI! }),
  editor: lexicalEditor({}),
  secret: process.env.PAYLOAD_SECRET!,
  typescript: { outputFile: path.resolve(__dirname, 'payload-types.ts') },
})
```

### Next.js App Router integration

```typescript
// app/(app)/blog/[slug]/page.tsx
import { getPayload } from 'payload'
import config from '@payload-config'
import { notFound } from 'next/navigation'

export default async function BlogPost({ params }: { params: { slug: string } }) {
  const payload = await getPayload({ config })

  const { docs } = await payload.find({
    collection: 'posts',
    where: {
      and: [
        { slug:   { equals: params.slug } },
        { status: { equals: 'published' } },
      ],
    },
    depth: 2,  // resolve relationships
  })

  if (!docs[0]) notFound()
  const post = docs[0]

  return (
    <article>
      <h1>{post.title}</h1>
      {/* Render Lexical rich text */}
    </article>
  )
}

export async function generateStaticParams() {
  const payload = await getPayload({ config })
  const { docs } = await payload.find({
    collection: 'posts',
    where: { status: { equals: 'published' } },
    select: { slug: true },
    pagination: false,
  })
  return docs.map(post => ({ slug: post.slug }))
}
```

### Local API vs REST vs GraphQL

```typescript
// Local API (fastest — no HTTP overhead, use in Server Components)
const payload = await getPayload({ config })
const post = await payload.findByID({ collection: 'posts', id })

// REST API (from client or external services)
const res = await fetch(`${process.env.NEXT_PUBLIC_APP_URL}/api/posts?where[status][equals]=published`)
const { docs } = await res.json()

// GraphQL (for complex queries)
const query = `
  query { Posts(where: { status: { equals: published } }) {
    docs { id title slug author { name } }
  }}
`
```

## Example

**User:** Set up Payload CMS for a blog — posts collection with rich text, author relationship, status (draft/published), slug auto-generation, and a Next.js page that fetches published posts server-side.

**Expected output:**
- `collections/Posts.ts` — full collection config with all fields, hooks for slug, afterChange revalidation
- `collections/Users.ts` — role field (admin/editor/author)
- `payload.config.ts` — Postgres adapter, all collections
- `app/(cms)/[[...segments]]/page.tsx` — Payload admin panel route
- `app/(app)/blog/page.tsx` — Server Component using local API
- `payload-types.ts` — generated (run `payload generate:types`)

---
