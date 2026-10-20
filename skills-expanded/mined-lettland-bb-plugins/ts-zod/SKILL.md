---
name: ts-zod
description: Use when validating data at TypeScript boundaries with Zod — parse-don't-validate, infer types from schemas, refinements, transforms, error handling.
metadata:
  added: 2026-05-18
  last_reviewed: 2026-05-18
  type: language
  languages: [typescript]
  status: active
  invokes_shell: false
  shell_reviewed: "valksor 2026-05-17"
  related: [typescript, react]
---

# TS Zod

**Iron Law: parse, don't validate. The schema is the source of truth — infer the TypeScript type from it, never write a parallel `interface`. Validate at every untrusted boundary (HTTP, form, env, localStorage).**

**Version**: this skill targets **Zod v4** (released mid-2025). Differences from v3 that are NOT covered here:

- `z.record(z.string(), z.unknown())` → in v4, `z.record(z.unknown())` (single-arg; key defaults to string)
- `ZodError.format()` / `.flatten()` shapes shifted; `.issues` is now the primary error path
- Bundle size dropped ~7× (now ~7KB tree-shaken) — re-evaluate the Valibot tradeoff if bundle size was your reason
- For schema-compat with v3, `import { z } from "zod/v4"` is the explicit shim during migration

## Why Zod (vs Yup / Valibot / ArkType)

| Library     | Verdict                                                                               |
| ----------- | ------------------------------------------------------------------------------------- |
| **Zod**     | mature, huge ecosystem (RHF, tRPC, OpenAPI), inferred types — **default**             |
| **Valibot** | ~10x smaller bundle (tree-shakable), Zod-similar API; pick when bundle size dominates |
| **ArkType** | type-syntax schemas for unions, 100x faster than Zod at runtime; smaller ecosystem    |
| **Yup**     | older, weaker types, more weight; skip for new projects                               |
| **io-ts**   | functional, very correct, steep learning curve                                        |

## Schema → type

```ts
import { z } from "zod";

const UserSchema = z.object({
  id: z.string().uuid(),
  email: z.string().email(),
  age: z.number().int().min(0).max(150),
  role: z.enum(["admin", "user", "guest"]),
  createdAt: z.coerce.date(), // parses string → Date
  metadata: z.record(z.unknown()).optional(), // v4 single-arg; v3 was z.record(z.string(), z.unknown())
});

export type User = z.infer<typeof UserSchema>; // ← the source of truth
```

**Never write `interface User { id: string; ... }` next to the schema.** They drift. `z.infer<typeof X>` is the contract.

## Parse, don't validate

```ts
// WRONG — checks then casts; type system trusts you
if (isValidUser(data)) {
  const user = data as User;
}

// RIGHT — parse returns typed value or throws
const user = UserSchema.parse(data); // throws ZodError

// RIGHT — safeParse returns discriminated result
const result = UserSchema.safeParse(data);
if (!result.success) return { errors: result.error.flatten() };
const user = result.data; // narrowed to User
```

`safeParse` everywhere user input enters: API request bodies, form submits, URL query, localStorage reads, env vars at boot.

## Refinements + custom validators

```ts
const PasswordSchema = z
  .string()
  .min(12, "at least 12 chars")
  .refine((s) => /[A-Z]/.test(s), "needs uppercase")
  .refine((s) => /[0-9]/.test(s), "needs digit");

const SignupSchema = z
  .object({
    password: PasswordSchema,
    confirm: z.string(),
  })
  .refine((d) => d.password === d.confirm, {
    message: "passwords don't match",
    path: ["confirm"], // attach error to specific field
  });
```

`refine` for one-field rules; cross-field rules at the object level with `path` so the error lands on the right input.

## Transforms — clean data on parse

```ts
const TrimmedEmail = z.string().trim().toLowerCase().email();
const ParsedQuery = z.object({
  limit: z.coerce.number().int().min(1).max(100).default(20),
  cursor: z.string().optional(),
});

// from URLSearchParams — all strings
const q = ParsedQuery.parse(Object.fromEntries(new URLSearchParams(location.search)));
// q.limit is `number`, not `string`
```

`z.coerce.*` for URL/form data (everything is a string). `.default()` for optional fields with fallback. `.transform()` for arbitrary post-parse shaping (e.g., normalize phone numbers).

## Error formatting

```ts
const r = UserSchema.safeParse(input);
if (!r.success) {
  // .flatten() — { formErrors: [], fieldErrors: { email: [...], age: [...] } }
  return Response.json({ errors: r.error.flatten().fieldErrors }, { status: 400 });

  // .format() — nested tree mirroring the schema shape
  // r.error.format();

  // .issues — raw array, full detail
  // r.error.issues;
}
```

For HTTP APIs use `.flatten()`. For React Hook Form, use `@hookform/resolvers/zod` — handles it for you.

## React Hook Form integration

```ts
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";

const SignupSchema = z.object({
  email: z.string().email(),
  password: z.string().min(12),
});

function SignupForm() {
  const { register, handleSubmit, formState: { errors } } = useForm<z.infer<typeof SignupSchema>>({
    resolver: zodResolver(SignupSchema),
  });
  return <form onSubmit={handleSubmit(onSubmit)}>
    <input {...register("email")} />
    {errors.email && <span>{errors.email.message}</span>}
  </form>;
}
```

## Env var validation at boot

```ts
const Env = z.object({
  NODE_ENV: z.enum(["development", "production", "test"]),
  DATABASE_URL: z.string().url(),
  PORT: z.coerce.number().int().positive().default(3000),
});

export const env = Env.parse(process.env); // throws at startup, not at use-site
```

Fail at boot, not at request 200. Logs name the missing/invalid var explicitly.

## Anti-patterns

- Writing `interface Foo` next to `FooSchema` — they will drift; infer instead
- `z.any()` / `z.unknown()` for "I'll deal with it later" — you won't; tighten now
- Validating already-validated data inside the same trust boundary — wasted CPU
- Ignoring `safeParse` error shape — `result.error` is rich; flatten or format properly
- Throwing `ZodError` to the client raw — exposes schema internals; map to your error shape
- Using `parse` (throws) in hot paths where you could branch — `safeParse` is cheaper than try/catch
- Schema for output shaping (toJSON / serialization) — that's not what Zod is for; use a serializer
- Recompiling schemas in render (`z.object({...}).parse(props)`) — hoist to module scope

## Red flags

| Thought                          | Reality                                                                             |
| -------------------------------- | ----------------------------------------------------------------------------------- |
| "TypeScript already checks this" | TS is compile-time; runtime data from HTTP/storage/forms is untyped at the boundary |
| "I'll add validation later"      | First crash on bad input = scramble                                                 |
| "It's just an internal API"      | Internal APIs become external; validate now or scramble later                       |
| "Just use `as User`"             | That's a lie to the compiler; the bug surfaces three layers deep                    |

## Hand-off

For advanced TS type-level work: `Skill(typescript)`. For form integration patterns: `Skill(react)`. For general TS rules: `Skill(typescript)`.
