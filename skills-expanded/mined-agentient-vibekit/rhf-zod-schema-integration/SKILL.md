---
name: rhf-zod-schema-integration
version: "1.0"
description: >
  React Hook Form v7 with zodResolver integration for type-safe validated forms.
  PROACTIVELY activate for: (1) creating forms with useForm and zodResolver, (2) implementing field registration with spread syntax, (3) handling form state and errors.
  Triggers: "react hook form", "useForm", "zodResolver"
group: state-forms
core-integration:
  techniques:
    primary: ["structured_decomposition"]
    secondary: []
  contracts:
    input: "none"
    output: "none"
  patterns: "none"
  rubrics: "none"
---

# React Hook Form + Zod Schema Integration

## The Integration Pattern

React Hook Form v7 + Zod provides fully type-safe, validated forms:

```typescript
'use client'

import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

// 1. Define Zod schema
const schema = z.object({
  email: z.string().email('Invalid email'),
  password: z.string().min(8, 'Minimum 8 characters'),
});

// 2. Infer TypeScript type
type FormData = z.infer<typeof schema>;

// 3. Create form with zodResolver
function MyForm() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<FormData>({
    resolver: zodResolver(schema), // Zod validates automatically
  });

  const onSubmit = (data: FormData) => {
    // data is fully typed and validated!
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register('email')} />
      {errors.email && <p>{errors.email.message}</p>}

      <input type="password" {...register('password')} />
      {errors.password && <p>{errors.password.message}</p>}

      <button type="submit" disabled={isSubmitting}>Submit</button>
    </form>
  );
}
```

## useForm Configuration

```typescript
const {
  register,
  handleSubmit,
  formState,
  reset,
  watch,
  getValues,
  setValue,
  setError,
} = useForm<FormData>({
  // REQUIRED: zodResolver connects Zod to RHF
  resolver: zodResolver(mySchema),

  // Initial values
  defaultValues: {
    email: '',
    password: '',
  },

  // Validation mode
  mode: 'onBlur', // 'onChange' | 'onBlur' | 'onSubmit' | 'onTouched' | 'all'

  // Revalidate mode after first submit
  reValidateMode: 'onChange',
});
```

## Field Registration (v7 Spread Pattern)

```typescript
// CORRECT: v7 spread syntax
<input {...register('fieldName')} />

// This spreads: { name, onChange, onBlur, ref }

// WRONG: v6 ref pattern (deprecated)
<input name="fieldName" ref={register} />
```

### Registration with Type Conversion

```typescript
// Number input
<input
  type="number"
  {...register('age', { valueAsNumber: true })}
/>

// Date input
<input
  type="date"
  {...register('birthDate', { valueAsDate: true })}
/>

// Checkbox
<input
  type="checkbox"
  {...register('acceptTerms')}
/>
```

## Error Handling Patterns

### Field-Level Errors

```typescript
{errors.email && (
  <p className="text-red-500 text-sm mt-1">
    {errors.email.message}
  </p>
)}

// Nested errors
{errors.address?.street && (
  <p>{errors.address.street.message}</p>
)}

// Array errors
{errors.items?.[index]?.name && (
  <p>{errors.items[index]?.name?.message}</p>
)}
```

### Form-Level Errors

```typescript
const onSubmit = async (data: FormData) => {
  try {
    await api.submit(data);
  } catch (error) {
    // Set form-level error
    setError('root', {
      message: 'Submission failed. Please try again.',
    });
  }
};

// Display form error
{errors.root && (
  <div className="bg-red-100 p-3 rounded">
    {errors.root.message}
  </div>
)}
```

## Form State Management

```typescript
const {
  formState: {
    errors,          // Validation errors
    isSubmitting,    // true during async submission
    isSubmitted,     // true after submission attempt
    isDirty,         // true if any field changed from default
    isValid,         // true if no validation errors
    dirtyFields,     // Object of dirty fields
    touchedFields,   // Object of touched fields
  },
} = useForm<FormData>();

// Usage
<button
  type="submit"
  disabled={isSubmitting || !isDirty}
>
  {isSubmitting ? 'Submitting...' : 'Submit'}
</button>
```

## Complete Form Example

```typescript
'use client'

import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

const signupSchema = z.object({
  email: z.string().email('Invalid email address'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
  confirmPassword: z.string(),
}).refine((data) => data.password === data.confirmPassword, {
  message: 'Passwords do not match',
  path: ['confirmPassword'],
});

type SignupFormData = z.infer<typeof signupSchema>;

export function SignupForm() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting, isDirty },
    reset,
    setError,
  } = useForm<SignupFormData>({
    resolver: zodResolver(signupSchema),
    mode: 'onBlur',
    defaultValues: {
      email: '',
      password: '',
      confirmPassword: '',
    },
  });

  const onSubmit = async (data: SignupFormData) => {
    try {
      const response = await fetch('/api/signup', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        const error = await response.json();
        setError('root', { message: error.message });
        return;
      }

      reset();
      alert('Signup successful!');
    } catch (error) {
      setError('root', { message: 'Network error. Please try again.' });
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4 max-w-md">
      {errors.root && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
          {errors.root.message}
        </div>
      )}

      <div>
        <label htmlFor="email" className="block text-sm font-medium mb-1">
          Email
        </label>
        <input
          id="email"
          type="email"
          {...register('email')}
          className="w-full px-3 py-2 border rounded-md"
        />
        {errors.email && (
          <p className="text-red-500 text-sm mt-1">{errors.email.message}</p>
        )}
      </div>

      <div>
        <label htmlFor="password" className="block text-sm font-medium mb-1">
          Password
        </label>
        <input
          id="password"
          type="password"
          {...register('password')}
          className="w-full px-3 py-2 border rounded-md"
        />
        {errors.password && (
          <p className="text-red-500 text-sm mt-1">{errors.password.message}</p>
        )}
      </div>

      <div>
        <label htmlFor="confirmPassword" className="block text-sm font-medium mb-1">
          Confirm Password
        </label>
        <input
          id="confirmPassword"
          type="password"
          {...register('confirmPassword')}
          className="w-full px-3 py-2 border rounded-md"
        />
        {errors.confirmPassword && (
          <p className="text-red-500 text-sm mt-1">{errors.confirmPassword.message}</p>
        )}
      </div>

      <button
        type="submit"
        disabled={isSubmitting || !isDirty}
        className="w-full py-2 px-4 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:bg-gray-400"
      >
        {isSubmitting ? 'Creating account...' : 'Sign Up'}
      </button>
    </form>
  );
}
```

## Anti-Patterns

### Mixing Validation Sources

```typescript
// WRONG: Validation in both Zod and register
const schema = z.object({ email: z.string().email() });
<input {...register('email', { required: 'Required' })} />

// CORRECT: All validation in Zod
const schema = z.object({ email: z.string().email().min(1, 'Required') });
<input {...register('email')} />
```

### Using v6 Registration

```typescript
// WRONG: v6 ref pattern
<input name="email" ref={register} />

// CORRECT: v7 spread pattern
<input {...register('email')} />
```

## Summary

React Hook Form v7 + Zod integration provides:
- Type-safe forms with `z.infer<typeof schema>`
- Automatic validation via `zodResolver`
- v7 spread registration: `{...register('field')}`
- Rich error handling with `errors` object
- Form state management (isSubmitting, isDirty, isValid)
- No validation duplication - Zod is single source of truth

---

**Related Skills**: `zod-schema-type-inference-chain`, `rhf-dynamic-field-arrays`
