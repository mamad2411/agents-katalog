---
applyTo: "**/*.astro"
---

# Astro Patterns

**Priority summary — apply these first:**

1. Default to SSR-only (no `client:*` directive) and static rendering (`prerender: true`).
2. Use `client:*` directives only for components requiring user input or dynamic updates.
3. Use `try/catch` with typed errors for all data fetching in frontmatter.
4. Validate content collection schemas with Zod.
5. Prefer native HTML elements and CSS capabilities before adding JavaScript.

## Native-First Interactions

- Prefer native elements such as `<button>`, `<dialog>`, `<details>`, `<summary>`, `<input>`, and `<form>` before custom JavaScript behavior.
- Prefer CSS states and platform features before JS for presentation and interaction polish.
- Add JavaScript only for behavior that native HTML and CSS cannot provide.

## Partial Hydration (Component Islands)

Use `client:*` directives only when the component requires user input or dynamic updates based on user actions (e.g., click handlers, form controls, state that changes in response to user events):

| Directive | When to Use |
|---|---|
| `client:load` | Above-the-fold interactive |
| `client:visible` | Below-the-fold interactive |
| `client:idle` | Non-critical, deferred |

```astro
<Counter client:visible count={0} />
```

Default to no directive (SSR-only) for static content.

## Rendering Modes

- Default to static (`prerender: true`) for maximum performance.
- Use on-demand rendering (`prerender: false`) only for routes that require dynamic data per request.

## Data Fetching

Prefer `try/catch` with typed errors in the frontmatter:

```astro
---
let data: Item[] = [];
try {
  const res = await fetch('/api/items');
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  data = (await res.json()) as Item[];
} catch (err: unknown) {
  if (err instanceof Error) console.error(err.message);
}
---
```

## Server Actions

Use `defineAction()` for type-safe form handling:

```ts
// src/actions/example.ts
import { z } from 'astro/zod';
import { defineAction, ActionError } from 'astro:actions';

export const submit = defineAction({
  accept: 'form',
  input: z.object({ email: z.string().email() }),
  handler: async (input) => {
    // handler logic
    return { success: true };
  },
});

// src/actions/index.ts
export const server = { submit };
```

## API Routes

```ts
// src/pages/api/items.ts
import type { APIRoute } from 'astro';

export const GET: APIRoute = async () => {
  try {
    const items = await getItems();
    return new Response(JSON.stringify(items), {
      headers: { 'Content-Type': 'application/json' },
    });
  } catch (err: unknown) {
    return new Response('Internal Server Error', { status: 500 });
  }
};
```

## Content Collections

Validate schemas with Zod in `src/content/config.ts`:

```ts
import { defineCollection, z } from 'astro:content';
export const collections = {
  blog: defineCollection({
    type: 'content',
    schema: z.object({ title: z.string(), publishDate: z.date() }),
  }),
};
```

## Live Content Collections (Astro 6+)

For content that must update at request time without a rebuild:

```ts
// src/live.config.ts
import { defineLiveCollection } from 'astro:content';
import { z } from 'astro/zod';
export const collections = {
  updates: defineLiveCollection({
    loader: myLoader(),
    schema: z.object({ slug: z.string(), title: z.string() }),
  }),
};
```

## Fonts API (Astro 6+)

Configure in `astro.config.mjs`, then use `<Font>` in layout:

```ts
// astro.config.mjs
import { defineConfig, fontProviders } from 'astro/config';
export default defineConfig({
  fonts: [{ name: 'Roboto', cssVariable: '--font-roboto', provider: fontProviders.fontsource() }],
});
```

```astro
---
import { Font } from 'astro:assets';
---
<Font cssVariable="--font-roboto" preload />
```
