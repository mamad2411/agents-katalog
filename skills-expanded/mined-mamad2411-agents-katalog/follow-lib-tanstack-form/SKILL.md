---
name: follow-lib-tanstack-form
description: Use TanStack Form end to end — fields, Standard Schema validation, arrays, async validators, granular reactivity
argument-hint: "[framework] [schema-lib]"
related:
  - follow-lib-tanstack-ecosystem
  - run-typecheck
  - resolve-errors
---

## Goal

Use TanStack Form (v1) fully — headless type-safe forms: fields, Standard Schema validation (Zod/Valibot/ArkType), array fields, async validation, granular subscriptions, composable field components

## Scope

For forms of any size — headless = state/validation only, the UI is yours; adapters: `react-form`, `solid-form`, `vue-form`, `angular-form`, `svelte-form`; libraries like shadcn already have wrappers (re-export patterns per the docs)

- part of TanStack ecosystem — selection/dispatch lives in `/follow-lib-tanstack-ecosystem`

## Execute

### 1. Install

> Goal: install the form package and the framework adapter

```bash
bun add @tanstack/react-form zod   # adapter per framework + the schema lib used
```

### 2. Form Instance

> Goal: create a typed form instance with schema validation

```tsx
const form = useForm({
  defaultValues: { email: '', tags: [] as string[] },  // the type source of truth
  validators: { onSubmit: userSchema },                 // form-level schema
  onSubmit: async ({ value, formApi }) => {
    await api.createUser(value)          // value typed per defaultValues
    formApi.reset()
  },
})
```

### 3. Fields And Validation

> Goal: field render-prop + trigger control

```tsx
<form.Field
  name="email"
  validators={{
    onChange: schema.shape.email,                    // Standard Schema → per-field
    onChangeAsync: async ({ value }) =>
      await isEmailTaken(value) ? 'Email taken' : undefined,
    onChangeAsyncDebounceMs: 300,
  }}
>
  {(field) => (
    <>
      <input value={field.state.value}
        onChange={(e) => field.handleChange(e.target.value)}
        onBlur={field.handleBlur} />
      {field.state.meta.errors.map((err) => <em key={String(err)}>{String(err)}</em>)}
    </>
  )}
</form.Field>
```

- Triggers: `onMount`/`onChange`/`onBlur`/`onSubmit`/`onChangeAsync`/`onBlurAsync`/`onSubmitAsync` + `*AsyncDebounceMs` + `onDynamic`
- `field.state.meta`: `errors`, `isTouched`, `isDirty`, `isValidating`, `errorMap`

### 4. Patterns

> Goal: cover real forms

1. **Array fields**: `mode="array"` + `field.pushValue(v)`/`removeValue(i)`/`swapValues` — dynamic lists (skills, line items)
2. **Granular subscribe**: `<form.Subscribe selector={(s) => s.canSubmit}>` — re-render only the derived slice
3. **Composable fields**: wrap `form.Field` into shared input components via `createFormHook` + `fieldComponents`/`formComponents`
4. **Linked fields**: `listeners` on a field → recompute other fields when the value changes
5. **Server submit errors**: catch in `onSubmit` → map into field errors or a form-level error display
6. **Reset/persist**: `formApi.reset()`, draft autosave via subscribe + storage

### 5. Verify

> Goal: prove submit, validation, and field state work before finishing

1. `/run-typecheck` — field names are typed from defaultValues (a typo trips a compile error)
2. Test validation triggers, async debounce, array ops, submit/reset flow
3. On failure → `/resolve-errors` max 3 rounds

## Rules

- `defaultValues` = the type source — complete for every field, never missing
- Standard Schema validators — don't write regex/manual validators when the schema has one
- Async validators must have debounce — otherwise you spam the server on every keystroke
- Headless = a11y is the app's job: `label htmlFor`, `aria-invalid`, `aria-describedby`, error text link
- Use `form.Subscribe` for derived UI — never subscribe the whole store

## Expected Outcome

- Type-safe forms from field to submit
- Validation (sync/async/schema) + array fields + granular reactivity work
- Composable field components reusable across forms
