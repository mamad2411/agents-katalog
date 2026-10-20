---
description: Run TypeScript Strictness and Error Boundary Checks
globs: ['**/*.ts', '**/*.tsx', 'tsconfig.json']
---

# Code Quality: TypeScript & Error Boundaries

<audit_rules>

- You MUST enforce strict TypeScript settings. Verify `strict: true` and `noImplicitAny: true` in `tsconfig.json`.
- You MUST flag any explicit or implicit `any` types. Using `any` is STRICTLY PROHIBITED; use `unknown` or define a proper interface if the shape is dynamic.
- You MUST verify that type assertions (e.g., `as User`) are avoided unless absolutely necessary (like when dealing with raw DOM APIs). Prefer Zod runtime validation.
- You MUST enforce null safety. Use optional chaining (`?.`) and nullish coalescing (`??`) correctly.
- You MUST ensure all React application segments are wrapped in proper Error Boundaries (`error.tsx` in Next.js) to prevent the entire app from crashing on unhandled exceptions.
- You MUST verify that Promises are properly awaited or caught. Avoid floating promises.
  </audit_rules>

<example_good>

```typescript
import { z } from 'zod'

const UserSchema = z.object({ id: z.string(), name: z.string() })
type User = z.infer<typeof UserSchema>

export async function fetchUser(data: unknown): Promise<User | null> {
  try {
    // Runtime validation instead of type assertion
    const user = UserSchema.parse(data)
    return user
  } catch (error) {
    console.error('Validation failed', error)
    return null
  }
}
```

</example_good>

<example_bad>

```typescript
// BAD: Using 'any' and type assertions
export async function fetchUser(data: any) {
  // CRITICAL: Type assertion bypasses type checking
  const user = data as User
  return user
}
```

</example_bad>
