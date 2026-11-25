# Stack

- TanStack Start (Vite-based) + TanStack Router + Query + Form
- Convex (backend, DB, scheduled jobs, file storage, vector search via @convex-dev/rag)
- better-auth via @convex-dev/better-auth
- shadcn/ui (Base UI variant) + Tailwind v4 + hugeicons
- AI SDK v6 (@ai-sdk/openai, @ai-sdk/react, ai)
- Resend for transactional email
- Sentry + PostHog + Vercel Analytics for observability
- Polar (Merchant of Record) for billing via @convex-dev/polar (Stripe adapter stubbed)
- pnpm, oxlint + oxfmt + tsgo for tooling
- Hosted on Vercel

# Sentry

Error collection is automatic and configured in `src/router.tsx`.

Server functions should be instrumented:

```tsx
import * as Sentry from "@sentry/tanstackstart-react";

Sentry.startSpan({ name: "operation name" }, async () => {
  // operation
});
```

# Convex schemas

Use the validator builder `v` from `convex/values`:

- `v.id<TableName>(tableName)`, `v.string()`, `v.number()`, `v.boolean()`, `v.bytes()`
- `v.literal<T>(literal)`, `v.array<T>(element)`, `v.object<T>(fields)`, `v.record<K, V>(keys, values)`
- `v.union<T>(...members)`, `v.optional<T>(value)`, `v.any()`

System fields `_id` and `_creationTime` are auto-added — do not declare them. Indexes
required for non-PK lookups; declare with `.index("name", ["field1", "field2"])`.

Schema docs: https://docs.convex.dev/database/types

# shadcn

This project uses Base UI (not Radix). Install components with:

```bash
pnpm dlx shadcn@latest add <component>
```

For form composition use `FieldGroup` + `Field`. Icons in buttons use `data-icon`.
Use semantic tokens (`bg-primary`, `text-muted-foreground`) — never raw colors.
Use `flex` + `gap-*` — never `space-x-*` / `space-y-*`. Use `size-*` for square dims.

# Imports

`#/*` and `@/*` both resolve to `./src/*`. Prefer `@/` for app code.
