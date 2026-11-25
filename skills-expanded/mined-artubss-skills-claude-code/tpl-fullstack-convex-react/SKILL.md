---
name: tpl-fullstack-convex-react
description: Template do pack (fullstack/08-convex-react.md). Orienta o agente em stacks fullstack e arquitetura ponta a ponta alinhado a esse contexto.
metadata:
  version: 1.0.0
  source_template: fullstack/08-convex-react.md
  generated_by: install_pack_templates_as_claude_skills
---

# PROJECT: Convex + React 19 + Clerk Auth

Skill gerado a partir do pack `templates-claude-code`. Arquivo de origem: `fullstack/08-convex-react.md`. Use como baseline e adapte ao projeto antes de mudancas grandes.

## Conteudo do template

## STACK
- **Backend:** Convex (functions, DB, storage, scheduled jobs)
- **Frontend:** React 19 + TypeScript + Vite 6
- **Auth:** Clerk (JWT integration with Convex)
- **Styling:** Tailwind CSS v3 + shadcn/ui
- **Language:** TypeScript 5.x (strict)
- **Real-time:** Convex reactive query subscriptions (built-in)
- **Testing:** Vitest + convex-test

---

## PROJECT STRUCTURE
```
convex/
├── _generated/
│   ├── api.d.ts                 # Auto-generated, never edit
│   └── dataModel.d.ts
├── schema.ts                    # Table definitions
├── auth.config.ts               # Clerk JWT config
├── functions/
│   ├── users.ts                 # user queries/mutations
│   ├── posts.ts                 # post queries/mutations/actions
│   └── files.ts                 # Storage actions
└── _utils/
    ├── helpers.ts               # Shared Convex helpers
    └── pagination.ts
src/
├── main.tsx                     # ClerkProvider + ConvexProvider
├── App.tsx
├── api/
│   └── convex.ts                # Typed Convex client re-exports
├── hooks/
│   ├── useCurrentUser.ts
│   └── usePaginatedPosts.ts
├── pages/
│   ├── Login.tsx
│   └── Dashboard.tsx
├── components/
│   ├── PostCard.tsx
│   └── CreatePostForm.tsx
└── types.ts
package.json
vite.config.ts
```

---

## ARCHITECTURE RULES
1. **Convex functions are the only backend** — no REST API; all data operations are Convex `query`, `mutation`, or `action`.
2. **`query` = reactive** — every component subscribing to a `useQuery` auto-updates when data changes server-side.
3. **`mutation` is transactional** — all DB writes inside a single mutation run atomically; never split across two mutations for consistency.
4. **`action` for external calls** — any function calling `fetch`, external APIs, or running non-DB logic uses `action`; actions are NOT transactional.
5. **Clerk JWT validates every call** — `ctx.auth.getUserIdentity()` required in every authenticated function.
6. **Optimistic updates for perceived performance** — `useMutation` with `optimisticUpdate` for instant UI feedback.
7. **Schema is the source of truth** — always update `convex/schema.ts` before writing a new function that accesses a new field.

---

## CONVEX SCHEMA

```typescript
// convex/schema.ts
import { defineSchema, defineTable } from 'convex/server'
import { v } from 'convex/values'

export default defineSchema({
  users: defineTable({
    clerkId:   v.string(),
    email:     v.string(),
    name:      v.string(),
    imageUrl:  v.optional(v.string()),
    role:      v.union(v.literal('user'), v.literal('admin')),
  })
  .index('by_clerk_id', ['clerkId'])
  .index('by_email',    ['email']),

  posts: defineTable({
    title:     v.string(),
    body:      v.string(),
    authorId:  v.id('users'),
    published: v.boolean(),
    imageId:   v.optional(v.id('_storage')),
  })
  .index('by_author',    ['authorId'])
  .index('by_published', ['published']),

  likes: defineTable({
    postId: v.id('posts'),
    userId: v.id('users'),
  })
  .index('by_post_and_user', ['postId', 'userId']),
})
```

---

## QUERY / MUTATION / ACTION

```typescript
// convex/functions/posts.ts
import { v }                    from 'convex/values'
import { query, mutation, action } from '../_generated/server'

// Reactive query — any client subscribed auto-updates on data change
export const list = query({
  args: { limit: v.optional(v.number()) },
  handler: async (ctx, { limit = 20 }) => {
    return ctx.db.query('posts')
      .withIndex('by_published', q => q.eq('published', true))
      .order('desc')
      .take(limit)
  },
})

export const create = mutation({
  args: { title: v.string(), body: v.string() },
  handler: async (ctx, args) => {
    const identity = await ctx.auth.getUserIdentity()
    if (!identity) throw new Error('Unauthorized')

    const user = await ctx.db
      .query('users')
      .withIndex('by_clerk_id', q => q.eq('clerkId', identity.subject))
      .first()
    if (!user) throw new Error('User not found')

    return ctx.db.insert('posts', {
      title:     args.title,
      body:      args.body,
      authorId:  user._id,
      published: false,
    })
  },
})

export const deletePost = mutation({
  args: { postId: v.id('posts') },
  handler: async (ctx, { postId }) => {
    const identity = await ctx.auth.getUserIdentity()
    if (!identity) throw new Error('Unauthorized')
    const post = await ctx.db.get(postId)
    if (!post) throw new Error('Post not found')
    const user = await ctx.db.query('users').withIndex('by_clerk_id', q => q.eq('clerkId', identity.subject)).first()
    if (post.authorId !== user?._id) throw new Error('Forbidden')
    if (post.imageId) await ctx.storage.delete(post.imageId)
    await ctx.db.delete(postId)
  },
})

// Action: external API call (NOT transactional)
export const generateSummary = action({
  args: { postId: v.id('posts') },
  handler: async (ctx, { postId }) => {
    const post = await ctx.runQuery(api.functions.posts.getById, { postId })
    const response = await fetch('https://api.openai.com/v1/chat/completions', {
      method: 'POST',
      headers: { Authorization: `Bearer ${process.env.OPENAI_KEY}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({ model: 'gpt-5.4-mini', messages: [{ role: 'user', content: `Summarize: ${post?.body}` }] }),
    })
    const data = await response.json()
    const summary = data.choices[0].message.content
    await ctx.runMutation(api.functions.posts.updateSummary, { postId, summary })
    return summary
  },
})
```

---

## REACT INTEGRATION + OPTIMISTIC UPDATES

```tsx
// src/main.tsx
import { ClerkProvider, useAuth }  from '@clerk/clerk-react'
import { ConvexProviderWithClerk } from 'convex/react-clerk'
import { ConvexReactClient }       from 'convex/react'
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'

const convex = new ConvexReactClient(import.meta.env.VITE_CONVEX_URL)

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <ClerkProvider publishableKey={import.meta.env.VITE_CLERK_PUBLISHABLE_KEY}>
      <ConvexProviderWithClerk client={convex} useAuth={useAuth}>
        <App />
      </ConvexProviderWithClerk>
    </ClerkProvider>
  </React.StrictMode>
)

// src/components/PostList.tsx
import { useQuery, useMutation }  from 'convex/react'
import { api }                    from '../../convex/_generated/api'
import type { Id }                from '../../convex/_generated/dataModel'

export function PostList() {
  // Reactive — auto-refreshes when posts change on server
  const posts = useQuery(api.functions.posts.list, { limit: 20 })

  const deletePost = useMutation(api.functions.posts.deletePost)
    .withOptimisticUpdate((localStore, { postId }) => {
      const current = localStore.getQuery(api.functions.posts.list, { limit: 20 })
      if (current) {
        localStore.setQuery(
          api.functions.posts.list,
          { limit: 20 },
          current.filter(p => p._id !== postId)
        )
      }
    })

  if (!posts) return <p>Loading...</p>

  return (
    <ul>
      {posts.map(post => (
        <li key={post._id} className="flex justify-between p-2">
          <span>{post.title}</span>
          <button
            onClick={() => deletePost({ postId: post._id as Id<'posts'> })}
            className="text-red-500"
          >
            Delete
          </button>
        </li>
      ))}
    </ul>
  )
}
```

---

## FILE STORAGE

```typescript
// convex/functions/files.ts
import { mutation, action } from '../_generated/server'
import { v }                from 'convex/values'

// Step 1: Client calls this to get an upload URL
export const generateUploadUrl = mutation({
  handler: async (ctx) => {
    const identity = await ctx.auth.getUserIdentity()
    if (!identity) throw new Error('Unauthorized')
    return ctx.storage.generateUploadUrl()
  },
})

// Step 2: Client uploads to URL, gets storageId; then calls this
export const savePostImage = mutation({
  args: { postId: v.id('posts'), storageId: v.id('_storage') },
  handler: async (ctx, { postId, storageId }) => {
    return ctx.db.patch(postId, { imageId: storageId })
  },
})

// src/components/ImageUpload.tsx
async function uploadImage(file: File, postId: string) {
  const uploadUrl = await convex.mutation(api.functions.files.generateUploadUrl, {})
  const result = await fetch(uploadUrl, { method: 'POST', headers: { 'Content-Type': file.type }, body: file })
  const { storageId } = await result.json()
  await convex.mutation(api.functions.files.savePostImage, { postId, storageId })
}
```

---

## ROUTING TABLE (Function → Action)

| Function | Type | Auth | Action |
|----------|------|------|--------|
| `posts.list` | query | No | Reactive published post list |
| `posts.getById` | query | No | Single post (reactive) |
| `posts.create` | mutation | Yes | Insert post atomically |
| `posts.update` | mutation | Yes (owner) | Update fields |
| `posts.deletePost` | mutation | Yes (owner) | Delete + clean storage |
| `posts.generateSummary` | action | Yes | Call OpenAI API |
| `users.getCurrentUser` | query | Yes | Get authenticated user |
| `users.upsert` | mutation | Yes | Sync Clerk user to Convex |
| `files.generateUploadUrl` | mutation | Yes | Presigned upload URL |
| `files.savePostImage` | mutation | Yes | Link storage to post |

---

## QUALITY GATES
- [ ] `npx convex dev` — zero TypeScript errors in `convex/` functions
- [ ] `tsc --noEmit` — zero errors in `src/`
- [ ] All mutations check `ctx.auth.getUserIdentity()` before DB writes
- [ ] `useQuery` results handle `undefined` (loading state) gracefully
- [ ] Optimistic updates revert on mutation error
- [ ] `convex/schema.ts` has indexes for all query patterns used
- [ ] Actions validated — no direct DB writes in `action` (use `runMutation`)
- [ ] `npx convex deploy` — deployment succeeds without warnings

---

## FORBIDDEN
- ❌ Direct DB writes in `action` — use `ctx.runMutation()` instead
- ❌ `useQuery` result used without null check (it's `undefined` while loading)
- ❌ Secrets (API keys) in `convex/` code committed to git — use `npx convex env set`
- ❌ Unindexed queries in `query` handlers that scan full tables
- ❌ Mutations that call `fetch()` — that's what `action` is for
- ❌ `_generated/` files edited manually — fully auto-generated
- ❌ Multiple `ConvexReactClient` instances — one at app root only
- ❌ Auth bypass: `ctx.db.query()` before identity check in protected mutations
