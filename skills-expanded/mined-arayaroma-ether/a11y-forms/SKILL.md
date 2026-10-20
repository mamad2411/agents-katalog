---
name: a11y-forms
description: Use when building or reviewing any form input, select, or textarea in React/Next.js — label connection via htmlFor/id, required-field signaling, and error-message wiring via aria-describedby/aria-invalid. The most commonly flagged a11y issue in code review.
metadata:
  origin: community (decomposed from frontend-a11y)
allowed-tools: Read, Edit, Grep, Glob
---

# Form accessibility

## Label connection

```tsx
// BAD — no association, screen readers can't connect them
<label>Email</label>
<input type="email" />

// GOOD
<label htmlFor="email">Email</label>
<input id="email" type="email" />
```

## Required fields

```tsx
<label htmlFor="email">
  Email <span aria-hidden="true">*</span>
</label>
<input id="email" type="email" required aria-required="true" />
```

The asterisk is `aria-hidden` because it's redundant once `aria-required`/`required` are present —
without them, it would be the only signal and should stay visible to screen readers instead.

## Error messages

```tsx
<input id="email" type="email" aria-describedby="email-error" aria-invalid={!!error} />
{error && (
  <span id="email-error" role="alert">
    {error}
  </span>
)}
```

`aria-describedby` should be `undefined` (not an empty/dangling id) when there's no error —
pointing at a non-existent id is worse than pointing at nothing.

## Complete example

```tsx
export function LoginForm({ onSubmit }: { onSubmit: (email: string, password: string) => void }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errors, setErrors] = useState<{ email?: string; password?: string }>({});

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const newErrors: typeof errors = {};
    if (!email) newErrors.email = 'Email is required';
    if (!password) newErrors.password = 'Password is required';
    if (Object.keys(newErrors).length) return setErrors(newErrors);
    onSubmit(email, password);
  };

  return (
    <form onSubmit={handleSubmit} noValidate>
      <div>
        <label htmlFor="email">
          Email <span aria-hidden="true">*</span>
        </label>
        <input
          id="email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          aria-required="true"
          aria-describedby={errors.email ? 'email-error' : undefined}
          aria-invalid={!!errors.email}
          autoComplete="email"
        />
        {errors.email && <span id="email-error" role="alert">{errors.email}</span>}
      </div>
      <div>
        <label htmlFor="password">
          Password <span aria-hidden="true">*</span>
        </label>
        <input
          id="password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          aria-required="true"
          aria-describedby={errors.password ? 'password-error' : undefined}
          aria-invalid={!!errors.password}
          autoComplete="current-password"
        />
        {errors.password && <span id="password-error" role="alert">{errors.password}</span>}
      </div>
      <button type="submit">Log in</button>
    </form>
  );
}
```

## Anti-patterns

```tsx
// Placeholder is not a label substitute — it disappears on input and isn't reliably announced
<input placeholder="Enter your email" />
```

## Checklist

- [ ] Every `<input>`/`<select>`/`<textarea>` has a `<label htmlFor>` matching its `id`
- [ ] Error text is linked via `aria-describedby` and marked `role="alert"`
- [ ] `aria-invalid` reflects the current validation state, not a hardcoded value
- [ ] No form relies on `placeholder` as its only label

## Related

- `react-forms` — the validation/state-management half of the same form.
- `a11y-semantics-aria` — for non-form ARIA usage (labelledby, live regions, expanded state).
