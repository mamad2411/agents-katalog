---
name: form-validation
description: |
  Form building and validation patterns. Apply for any user input form — registration,
  checkout, settings, admin panels. Covers React Hook Form + Zod, field components,
  async validation, multi-step forms, and UX best practices.
---

# Form Validation — React Hook Form + Zod

## Schema-First Approach
```typescript
import { z } from 'zod';

// Define schema first — single source of truth
const RegisterSchema = z.object({
  name: z.string().min(2, 'Name must be at least 2 characters').max(100),
  email: z.string().email('Enter a valid email address'),
  phone: z.string().regex(/^\+998[0-9]{9}$/, 'Enter valid UZ phone: +998XXXXXXXXX'),
  password: z.string()
    .min(8, 'Password must be at least 8 characters')
    .regex(/[A-Z]/, 'Must contain at least one uppercase letter')
    .regex(/[0-9]/, 'Must contain at least one number'),
  confirmPassword: z.string(),
}).refine(data => data.password === data.confirmPassword, {
  message: "Passwords don't match",
  path: ['confirmPassword'],
});

type RegisterFormData = z.infer<typeof RegisterSchema>;
```

## Form Implementation
```tsx
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';

function RegisterForm() {
  const form = useForm<RegisterFormData>({
    resolver: zodResolver(RegisterSchema),
    defaultValues: { name: '', email: '', phone: '+998', password: '', confirmPassword: '' },
    mode: 'onBlur',    // Validate on blur (not on every keystroke)
  });

  const onSubmit = async (data: RegisterFormData) => {
    try {
      await api.auth.register(data);
      navigate('/dashboard');
    } catch (err) {
      // Server-side errors → set field errors
      if (err.code === 'EMAIL_TAKEN') {
        form.setError('email', { message: 'This email is already registered' });
      } else {
        form.setError('root', { message: 'Registration failed. Please try again.' });
      }
    }
  };

  return (
    <form onSubmit={form.handleSubmit(onSubmit)} noValidate>
      <FormField
        label="Full Name"
        error={form.formState.errors.name?.message}
        {...form.register('name')}
      />
      <FormField
        label="Email"
        type="email"
        error={form.formState.errors.email?.message}
        {...form.register('email')}
      />
      
      {form.formState.errors.root && (
        <Alert variant="error">{form.formState.errors.root.message}</Alert>
      )}
      
      <Button type="submit" isLoading={form.formState.isSubmitting}>
        Create Account
      </Button>
    </form>
  );
}
```

## Reusable FormField Component
```tsx
interface FormFieldProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label: string;
  error?: string;
  hint?: string;
}

const FormField = forwardRef<HTMLInputElement, FormFieldProps>(
  ({ label, error, hint, id, ...props }, ref) => {
    const fieldId = id || label.toLowerCase().replace(/\s+/g, '-');
    return (
      <div className="form-field">
        <label htmlFor={fieldId} className="form-label">{label}</label>
        <input
          ref={ref}
          id={fieldId}
          aria-invalid={!!error}
          aria-describedby={error ? `${fieldId}-error` : hint ? `${fieldId}-hint` : undefined}
          className={cn('form-input', error && 'form-input--error')}
          {...props}
        />
        {hint && !error && <p id={`${fieldId}-hint`} className="form-hint">{hint}</p>}
        {error && <p id={`${fieldId}-error`} role="alert" className="form-error">{error}</p>}
      </div>
    );
  }
);
```

## Async Validation
```typescript
// Debounced server-side validation (e.g., check username availability)
const usernameSchema = z.string().min(3).refine(
  async (username) => {
    const res = await api.users.checkUsername(username);
    return res.available;
  },
  { message: 'Username is already taken' }
);

// In form: mode: 'onBlur' prevents too-frequent API calls
```
