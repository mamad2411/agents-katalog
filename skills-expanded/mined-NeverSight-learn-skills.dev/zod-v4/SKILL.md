---
name: zod-v4
description: Use when writing Zod schemas, validating user input, handling Zod errors, or migrating from Zod v3 to v4 patterns.
license: MIT
metadata:
  author: pyyupsk
  version: "1.0"
---

# Zod v4

Patterns for Zod v4 schema definition, validation, and error handling.

## Naming

Schema: `camelCase` + `Schema` suffix. Inferred type: same name without suffix.

```ts
export const userSchema = z.object({
  id: z.string(),
  email: z.string().email(),
  role: z.enum(["admin", "user"]),
});

export type User = z.infer<typeof userSchema>;
```

## `parse` vs `safeParse`

| Method      | When to use                                                                |
| ----------- | -------------------------------------------------------------------------- |
| `parse`     | Trusted data only — env validation, server startup. Throws on failure.     |
| `safeParse` | All user input. Returns `{ success, data, error }`. Compose with `safe()`. |

```ts
async function validateUser(input: unknown) {
  const result = userSchema.safeParse(input);
  if (!result.success)
    return [new Error(z.prettifyError(result.error)), null] as const;
  return [null, result.data] as const;
}
```

## Error Messages — `error` not `message`

```ts
// ❌ v3 style
z.string().min(3, { message: "Too short" });

// ✅ v4
z.string().min(3, { error: "Too short" });
```

## Human-Readable Errors

`z.prettifyError(error)` replaces `error.flatten()` and `error.format()`:

```ts
const result = userSchema.safeParse(input);
if (!result.success) {
  console.error(z.prettifyError(result.error));
}
```

## Merging Schemas — shape spread, not `.merge()`

```ts
// ❌ .merge() is deprecated in v4
const combined = schemaA.merge(schemaB);

// ✅ shape spread
const combined = z.object({ ...schemaA.shape, ...schemaB.shape });
```

## URL Validation

```ts
// ✅ v4 shorthand
z.url();

// equivalent to
z.string().url();
```

## Server Actions Integration

```ts
async function createPost(formData: FormData) {
  "use server";
  const result = createPostSchema.safeParse(Object.fromEntries(formData));
  if (!result.success) return { error: z.prettifyError(result.error) };
  await db.insert(posts).values(result.data);
}
```

## Common Mistakes

- Using `message` instead of `error` in v4 validators — silently ignored
- Using `.merge()` — deprecated, use shape spread
- Using `error.flatten()` or `error.format()` — use `z.prettifyError()` instead
- Using `parse` on user input — always `safeParse` for untrusted data
