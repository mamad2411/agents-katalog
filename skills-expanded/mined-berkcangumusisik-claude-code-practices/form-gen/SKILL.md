---
name: form-gen
description: Generates a form component with validation, error messages, and submit handling
argument-hint: <form-description>
user-invocable: true
allowed-tools: Read Glob Edit
effort: medium
---

## Generate Form

Form description: **$ARGUMENTS**

1. Detect form library:
```bash
cat package.json | grep -E '"react-hook-form"|"formik"|"react-final-form"|"@tanstack/form"'
cat package.json | grep -E '"zod"|"yup"|"joi"'
```

2. Read an existing form component to match patterns.

3. Generate the form with:
   - Field definitions based on description
   - Zod/Yup validation schema
   - Inline error messages (accessible - `aria-describedby`)
   - Loading state on submit
   - Success/error feedback
   - Proper `name` attributes for autofill
   - `autocomplete` hints where applicable

4. TypeScript types for form values and submit handler.

5. Example output for a login form:
```tsx
const loginSchema = z.object({
  email: z.string().email('Invalid email'),
  password: z.string().min(8, 'At least 8 characters'),
})

export function LoginForm({ onSubmit }: LoginFormProps) {
  const form = useForm({ resolver: zodResolver(loginSchema) })
  // ...
}
```

6. Place in the components directory following project conventions.
