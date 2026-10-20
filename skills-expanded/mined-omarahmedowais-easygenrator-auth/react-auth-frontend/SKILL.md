---
name: react-auth-frontend
description: >-
  Conventions for the React + TypeScript frontend: feature folders, the apiFetch client and
  in-memory token, AuthProvider and route guards, react-hook-form + zod forms, and the
  Tailwind/shadcn-style UI primitives. Use whenever adding or changing a page, form, API call,
  route or component under frontend/.
---

# React auth frontend conventions

## Structure

```
src/api/            client.ts (apiFetch + refreshSession), session.ts (in-memory token), errors.ts, types.ts
src/features/<f>/   api.ts, schemas.ts, components/, pages/, routes/ (guards)
src/components/ui/  primitives (button, input, label, form-field). Style with tokens, not raw colors
src/app/            providers.tsx (QueryClient, AuthProvider, Toaster), router.tsx (route table)
```

Use the `@/` alias for imports across folders.

## Data and auth

- **All HTTP goes through `apiFetch`.** It adds the Bearer token and `credentials: 'include'`, handles 401 with a single-flight refresh (cross-tab Web Lock) plus one replay, and throws `ApiError`.
- Auth endpoints pass `skipRefresh: true`.
- **Tokens never touch localStorage/sessionStorage.** The session is restored on load from the refresh cookie (`AuthProvider` calls `authApi.refresh()`).
- Read auth state with `useAuth()` (`state.status` is `loading | authenticated | unauthenticated`).
- Server data uses TanStack Query (`useQuery({ queryKey: [...], queryFn })`). Sign-out clears the cache.
- Protect routes by nesting them under `<RequireAuth />`. Sign-in/up pages go under `<RedirectIfAuthenticated />`.

## Forms

```tsx
const form = useForm<Values>({ resolver: zodResolver(schema), mode: 'onTouched', defaultValues });
// field
<FormField label="Email" error={errors.email?.message}><Input {...register('email')} /></FormField>
// server errors
catch (e) { if (isApiError(e) && e.status === 409) setError('email', {...}); else setError('root', { message: errorMessage(e) }); }
```

- Schemas live in `features/<f>/schemas.ts`. Validation rules mirror `backend/src/common/validation/auth-rules.ts`, so change both together.
- `FormField` wires `id`, `aria-invalid` and `aria-describedby`. Don't hand-roll labels.
- Submit buttons use `loading={isSubmitting}`. Forms use `noValidate` so zod owns the messages.

## UI

- Tailwind v4 with tokens in `styles.css` (`bg-card`, `text-muted-foreground`, `border-border`, `text-destructive`, …). Dark mode follows the OS.
- Icons come from `lucide-react` with `aria-hidden` when decorative. Toasts use `sonner`.
- Layouts must work at 360px wide.
