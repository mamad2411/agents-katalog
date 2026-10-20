---
description: Run Next.js Security and Middleware Check
globs: ['**/middleware.ts', '**/actions.ts', '**/*.action.ts', 'src/app/actions/**/*.ts']
---

# Next.js: Security & Middleware Constraints

<audit_rules>

- You MUST verify that Server Actions (`use server`) are NEVER used for GET (read) operations, as they cannot be cached and use POST requests. Use Server Components for reads.
- You MUST ensure every Server Action validates its input using a schema validation library like Zod BEFORE processing the request.
- You MUST verify authorization inside Server Actions to ensure the user has permission to perform the mutation (e.g., `if (post.authorId !== user.id) throw new Error(...)`).
- You MUST ensure Server Actions return minimal Data Transfer Objects (DTOs) and NEVER leak internal fields (like password hashes).
- You MUST verify `middleware.ts` runs on the Edge runtime. It MUST NOT use Node.js modules (`fs`, `crypto`, DB ORMs like Prisma). Use Web Crypto API instead.
- You MUST ensure `middleware.ts` includes a matcher config to exclude static files (`_next/static`, `images`, `favicon`).
  </audit_rules>

<example_good>

```typescript
// src/app/actions.ts
'use server'
import { z } from 'zod'
import { getSession } from '@/lib/auth'

const DeletePostSchema = z.object({ id: z.string() })

export async function deletePost(formData: FormData) {
  const session = await getSession()
  if (!session) throw new Error('Unauthorized')

  const parsed = DeletePostSchema.parse({ id: formData.get('id') })

  // Verify ownership
  const post = await db.post.findUnique({ where: { id: parsed.id } })
  if (post.authorId !== session.user.id) throw new Error('Forbidden')

  await db.post.delete({ where: { id: parsed.id } })
}
```

</example_good>

<example_bad>

```typescript
// src/app/actions.ts
'use server'
// BAD: Missing input validation and authorization checks
export async function deletePost(id: string) {
  await db.post.delete({ where: { id } })
}
```

</example_bad>
