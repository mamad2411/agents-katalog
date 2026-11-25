---
name: "svelte"
description: "SvelteKit: file-based routing, server/client load functions, form actions, stores, Cloudflare Workers deployment, component patterns"
---

# SvelteKit Skill

## When to activate
- Building a SvelteKit application (full-stack or static)
- Writing Svelte components (reactive declarations, stores, animations)
- Setting up server load functions and form actions
- Deploying SvelteKit to Cloudflare Workers or Vercel
- Choosing between SvelteKit and Next.js for a project

## When NOT to use
- React ecosystem projects — use the React skill
- When your team is all React and switching would be costly
- Complex enterprise apps where Next.js ecosystem support matters more

## Instructions

### Project setup

```bash
npm create svelte@latest my-app
# Options: SvelteKit demo / Skeleton / Library
# TypeScript: Yes
# ESLint + Prettier: Yes

npm install
npm run dev
```

### File structure

```
src/
├── routes/
│   ├── +layout.svelte        # root layout
│   ├── +layout.server.ts     # root server load
│   ├── +page.svelte          # / route
│   ├── +page.server.ts       # server load + actions for /
│   ├── blog/
│   │   ├── +page.svelte      # /blog
│   │   └── [slug]/
│   │       ├── +page.svelte  # /blog/[slug]
│   │       └── +page.server.ts
│   └── api/
│       └── users/
│           └── +server.ts    # API endpoint
├── lib/
│   ├── components/
│   ├── stores/
│   └── utils/
└── app.html                  # HTML shell
```

### Svelte components

```svelte
<!-- Counter.svelte -->
<script lang="ts">
  // Reactive declarations
  let count = $state(0)               // Svelte 5: runes
  let doubled = $derived(count * 2)  // computed

  // Or Svelte 4 style:
  // let count = 0
  // $: doubled = count * 2

  function increment() { count++ }
</script>

<button onclick={increment}>
  Count: {count} (doubled: {doubled})
</button>
```

### Server load functions

```typescript
// src/routes/blog/[slug]/+page.server.ts
import type { PageServerLoad } from './$types'
import { error } from '@sveltejs/kit'

export const load: PageServerLoad = async ({ params, locals }) => {
  const post = await db.posts.findBySlug(params.slug)
  if (!post) error(404, 'Post not found')

  return {
    post,
    // Only expose what the page needs — don't return sensitive data
  }
}
```

```svelte
<!-- src/routes/blog/[slug]/+page.svelte -->
<script lang="ts">
  import type { PageData } from './$types'
  let { data }: { data: PageData } = $props()
</script>

<article>
  <h1>{data.post.title}</h1>
  <div>{@html data.post.content}</div>
</article>
```

### Form actions (mutations)

```typescript
// src/routes/contact/+page.server.ts
import type { Actions } from './$types'
import { fail, redirect } from '@sveltejs/kit'
import { z } from 'zod'

const schema = z.object({
  email: z.string().email(),
  message: z.string().min(10),
})

export const actions: Actions = {
  default: async ({ request }) => {
    const data = Object.fromEntries(await request.formData())
    const parsed = schema.safeParse(data)

    if (!parsed.success) {
      return fail(422, { errors: parsed.error.flatten(), values: data })
    }

    await sendEmail(parsed.data)
    redirect(303, '/thank-you')
  },
}
```

```svelte
<!-- src/routes/contact/+page.svelte -->
<script lang="ts">
  import { enhance } from '$app/forms'
  let { form } = $props()
</script>

<form method="POST" use:enhance>
  <input name="email" type="email" />
  {#if form?.errors?.fieldErrors?.email}
    <p class="error">{form.errors.fieldErrors.email}</p>
  {/if}
  <textarea name="message"></textarea>
  <button type="submit">Send</button>
</form>
```

### Stores (shared state)

```typescript
// src/lib/stores/cart.ts
import { writable, derived } from 'svelte/store'

interface CartItem { id: string; name: string; price: number; qty: number }

function createCart() {
  const { subscribe, update, set } = writable<CartItem[]>([])

  return {
    subscribe,
    addItem: (item: CartItem) => update(items => {
      const existing = items.find(i => i.id === item.id)
      if (existing) {
        return items.map(i => i.id === item.id ? { ...i, qty: i.qty + 1 } : i)
      }
      return [...items, { ...item, qty: 1 }]
    }),
    removeItem: (id: string) => update(items => items.filter(i => i.id !== id)),
    clear: () => set([]),
  }
}

export const cart = createCart()
export const cartTotal = derived(cart, $cart =>
  $cart.reduce((sum, item) => sum + item.price * item.qty, 0)
)
```

### API endpoints

```typescript
// src/routes/api/users/+server.ts
import type { RequestHandler } from './$types'
import { json } from '@sveltejs/kit'

export const GET: RequestHandler = async ({ url, locals }) => {
  if (!locals.session) return json({ error: 'Unauthorized' }, { status: 401 })

  const page = parseInt(url.searchParams.get('page') ?? '1')
  const users = await db.users.findMany({ skip: (page - 1) * 20, take: 20 })
  return json({ users })
}

export const POST: RequestHandler = async ({ request, locals }) => {
  const body = await request.json()
  const user = await db.users.create({ data: body })
  return json(user, { status: 201 })
}
```

### Cloudflare Workers deployment

```bash
npm install -D @sveltejs/adapter-cloudflare
```

```typescript
// svelte.config.js
import adapter from '@sveltejs/adapter-cloudflare'
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte'

export default {
  preprocess: vitePreprocess(),
  kit: {
    adapter: adapter({ routes: { include: ['/*'], exclude: ['<all>'] } }),
  },
}
```

```typescript
// src/hooks.server.ts — access Cloudflare bindings
import type { Handle } from '@sveltejs/kit'

export const handle: Handle = async ({ event, resolve }) => {
  // Access KV, R2, D1 from Cloudflare Workers
  const { env } = event.platform ?? {}
  event.locals.kv = env?.MY_KV

  return resolve(event)
}
```

## Example

**User:** Build a SvelteKit app with authentication (using locals), a protected dashboard, a contact form with server-side validation, and deployment to Cloudflare Pages.

**Expected output:**
- `src/hooks.server.ts` — session validation from cookie, set `locals.user`
- `src/routes/dashboard/+layout.server.ts` — redirect to /login if no user
- `src/routes/contact/+page.server.ts` — form action with Zod validation + fail()
- `svelte.config.js` — Cloudflare adapter
- `src/routes/+layout.svelte` — nav with `$page.data.user` check

---
