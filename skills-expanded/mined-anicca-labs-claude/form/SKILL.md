---
name: form
description: Generate a type-safe form from a zod schema using react-hook-form, @hookform/resolvers, and Tailwind-styled field components. Use when building any user input form — login, invites, settings, billing details.
argument-hint: "<feature_or_schema_description>"
---

Generate a validated form for `$ARGUMENTS`.

## Steps

1. **Check existing components** — look in `src/components/` for existing field primitives (`FormField`, `Input`, `Select`) before creating new ones

2. **Define the zod schema** — write a `z.object()` schema in a dedicated `<feature>.schema.ts` file; derive the TypeScript type with `z.infer`. The same schema is reused server-side (server action / route handler) to parse the submitted payload — client validation is UX, server parsing is the security layer

3. **Wire the form** — use `useForm<FormValues>` with `zodResolver(schema)` and explicit `defaultValues` for every field; the form component is `"use client"`

4. **Render with `register`** — native inputs on the web use `{...register('field')}`; reach for `Controller` only for non-native controls (custom select, date picker, rich text)

5. **Handle submission** — `handleSubmit(onSubmit)` where `onSubmit` receives the fully-typed payload and calls the mutation/server action; use `setError("root", ...)` for server-returned errors and render it below the submit button

6. **Type-check** — run `tsc --noEmit` and fix all errors before reporting done

## Canonical output shape

```ts
// <feature>.schema.ts
import { z } from 'zod';
export const inviteSchema = z.object({
  email: z.string().email(),
  role: z.enum(['admin', 'member']),
});
export type InviteFormValues = z.infer<typeof inviteSchema>;
```

```tsx
// <Feature>Form.tsx
'use client';
import { zodResolver } from '@hookform/resolvers/zod';
import { useForm } from 'react-hook-form';
import { inviteSchema, type InviteFormValues } from './invite.schema';

const InviteForm = ({ onSuccess }: { onSuccess: () => void }) => {
  const { register, handleSubmit, setError, formState: { errors, isSubmitting } } =
    useForm<InviteFormValues>({
      resolver: zodResolver(inviteSchema),
      defaultValues: { email: '', role: 'member' },
    });

  const onSubmit = async (data: InviteFormValues) => { /* mutation / server action */ };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col gap-4" noValidate>
      <FormField label="Email" error={errors.email?.message}>
        <input
          type="email"
          {...register('email')}
          aria-invalid={!!errors.email}
          className="w-full rounded-md border border-border-subtle px-3 py-2 aria-[invalid=true]:border-red-500"
        />
      </FormField>

      {errors.root ? <p className="text-sm text-red-600">{errors.root.message}</p> : null}

      <button type="submit" disabled={isSubmitting} className="rounded-md bg-brand px-4 py-2 text-white disabled:opacity-40">
        {isSubmitting ? 'Sending…' : 'Send invite'}
      </button>
    </form>
  );
};

export { InviteForm };
```

The `FormField` wrapper owns the label + inline error slot — each field displays its own error directly below it; never a single shared error at the bottom of the form (the one exception: `errors.root` for server/network errors, below the submit button).

```tsx
// src/components/FormField.tsx
const FormField = ({ label, error, children }: { label: string; error?: string; children: ReactNode }) => (
  <label className="flex flex-col gap-1">
    <span className="text-sm font-medium text-text-secondary">{label}</span>
    {children}
    {error ? <span className="text-sm text-red-600">{error}</span> : null}
  </label>
);
```

## Rules

- Schema in a separate file when reused across pages or on the server
- `defaultValues` must cover every field — no uncontrolled → controlled warnings
- Never use `.optional()` to silence TS errors — fix the type at the source
- Always `<form onSubmit={handleSubmit(...)}>` with a `type="submit"` button — Enter-to-submit and browser semantics come free; `noValidate` so zod owns validation, not the browser
- Accessibility is part of done: inputs wrapped in (or referenced by) a `<label>`, `aria-invalid` on erroring fields
- Never suppress `react-hooks/exhaustive-deps` — fix the dependency
- Run `tsc --noEmit` after generation; zero errors before reporting done
