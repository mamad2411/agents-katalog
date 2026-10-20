---
name: zod-schema-type-inference-chain
version: "1.0"
description: >
  Zod v4 schema definition patterns with the Type Inference Chain for absolute type safety.
  PROACTIVELY activate for: (1) defining Zod schemas as single source of truth, (2) using z.infer for type generation, (3) implementing safe parsing with safeParse.
  Triggers: "zod", "schema", "z.infer"
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

# Zod Schema Type Inference Chain

## The Type Inference Chain Pattern (CRITICAL)

The **Type Inference Chain** is the foundational pattern for all state and form management:

```
Zod Schema (single source of truth)
    |
z.infer<typeof schema> (generate TypeScript type)
    |
useForm<Type>() (type-safe form)
    |
Zustand Store<Type> (type-safe state)
```

This pattern ensures **absolute type safety** across your entire data layer by maintaining **one single source of truth**: the Zod schema.

### Why This Pattern is Critical

**Problem Without Type Inference Chain**:
```typescript
// BAD: Multiple sources of truth
interface UserData {           // Manual type definition
  email: string;
  age: number;
}

const userSchema = z.object({  // Zod schema
  email: z.string().email(),
  age: z.number().min(18),
});

// These can drift out of sync!
```

**Solution With Type Inference Chain**:
```typescript
// GOOD: Single source of truth
const userSchema = z.object({
  email: z.string().email('Invalid email'),
  age: z.number().min(18, 'Must be 18+'),
});

// Type is automatically inferred from schema
type UserData = z.infer<typeof userSchema>;

// Now the schema and type are ALWAYS in sync!
```

## Schema Definition Patterns

### Basic Object Schema

```typescript
import { z } from 'zod';

const userSchema = z.object({
  // String with validations
  username: z.string()
    .min(3, 'Username must be at least 3 characters')
    .max(20, 'Username must be at most 20 characters')
    .regex(/^[a-zA-Z0-9_]+$/, 'Only letters, numbers, and underscores'),

  // Email validation
  email: z.string().email('Invalid email address'),

  // Number with range
  age: z.number()
    .int('Must be a whole number')
    .min(18, 'Must be 18 or older')
    .max(120, 'Invalid age'),

  // Optional field
  middleName: z.string().optional(),

  // Nullable field
  nickname: z.string().nullable(),

  // Enum
  role: z.enum(['user', 'admin', 'moderator']),

  // Boolean
  isActive: z.boolean(),

  // Array
  tags: z.array(z.string())
    .min(1, 'At least one tag required')
    .max(5, 'Maximum 5 tags'),
});

// Infer TypeScript type
type User = z.infer<typeof userSchema>;
```

### Nested Object Schema

```typescript
const addressSchema = z.object({
  street: z.string().min(1, 'Street required'),
  city: z.string().min(1, 'City required'),
  state: z.string().length(2, 'Use 2-letter state code'),
  zipCode: z.string().regex(/^\d{5}$/, 'Must be 5 digits'),
});

const userWithAddressSchema = z.object({
  name: z.string(),
  email: z.string().email(),
  address: addressSchema, // Nested object
});

type UserWithAddress = z.infer<typeof userWithAddressSchema>;
```

## Schema Composition and Reusability

### Using .extend()

```typescript
const baseUserSchema = z.object({
  id: z.string().uuid(),
  email: z.string().email(),
});

// Add more fields to base schema
const fullUserSchema = baseUserSchema.extend({
  name: z.string(),
  age: z.number(),
  role: z.enum(['user', 'admin']),
});

type FullUser = z.infer<typeof fullUserSchema>;
```

### Using .pick() and .omit()

```typescript
const userSchema = z.object({
  id: z.string(),
  email: z.string().email(),
  password: z.string(),
  name: z.string(),
});

// Pick only specific fields
const loginSchema = userSchema.pick({
  email: true,
  password: true,
});
// { email: string; password: string; }

// Omit specific fields
const publicUserSchema = userSchema.omit({
  password: true,
});
// { id: string; email: string; name: string; }
```

## Cross-Field Validation with .refine()

### Password Confirmation

```typescript
const passwordSchema = z.object({
  password: z.string()
    .min(8, 'Password must be at least 8 characters'),
  confirmPassword: z.string(),
}).refine((data) => data.password === data.confirmPassword, {
  message: 'Passwords do not match',
  path: ['confirmPassword'], // Error appears on confirmPassword field
});

type PasswordForm = z.infer<typeof passwordSchema>;
```

### Conditional Validation

```typescript
const shippingSchema = z.object({
  shippingMethod: z.enum(['pickup', 'delivery']),
  address: z.string().optional(),
}).refine(
  (data) => {
    // If delivery is selected, address is required
    if (data.shippingMethod === 'delivery') {
      return data.address && data.address.length > 0;
    }
    return true;
  },
  {
    message: 'Address required for delivery',
    path: ['address'],
  }
);
```

## Safe Error Handling with .safeParse()

### Basic Safe Parsing

```typescript
const userSchema = z.object({
  email: z.string().email(),
  age: z.number().min(18),
});

// Unsafe data from user input or API
const userData = {
  email: 'invalid-email',
  age: 15,
};

// Use safeParse for validation
const result = userSchema.safeParse(userData);

if (!result.success) {
  // Validation failed - handle errors
  const formatted = result.error.format();
  console.log(formatted.email?._errors); // ["Invalid email address"]
  console.log(formatted.age?._errors); // ["Must be 18 or older"]

  // Get flat errors
  const flat = result.error.flatten();
  console.log(flat.fieldErrors);
  // {
  //   email: ["Invalid email address"],
  //   age: ["Must be 18 or older"]
  // }
} else {
  // Validation succeeded - use validated data
  const validUser = result.data; // Fully typed!
}
```

## Anti-Patterns (DO NOT DO)

### Manually Defining Types

```typescript
// WRONG: Manual type separate from schema
interface UserData {
  email: string;
  age: number;
}

const userSchema = z.object({
  email: z.string().email(),
  age: z.number(),
});

// Problem: These can drift out of sync!
```

**Correct:**
```typescript
const userSchema = z.object({
  email: z.string().email(),
  age: z.number(),
});

type UserData = z.infer<typeof userSchema>; // Always in sync!
```

### Using .parse() Without Try/Catch

```typescript
// WRONG: Throws unhandled exception on invalid data
const user = userSchema.parse(untrustedData);
```

**Correct:**
```typescript
const result = userSchema.safeParse(untrustedData);
if (!result.success) {
  // Handle error
} else {
  const user = result.data;
}
```

## Summary

The **zod-schema-type-inference-chain** skill establishes the foundational pattern:

1. **Define Zod schema** - Single source of truth for data structure and validation
2. **Infer TypeScript type** - Use `z.infer<typeof schema>` to generate type
3. **Use in forms** - Pass type to `useForm<Type>({ resolver: zodResolver(schema) })`
4. **Use in stores** - Pass type to Zustand store interface
5. **Validate safely** - Use `.safeParse()` for all external data

---

**Related Skills**: `rhf-zod-schema-integration`, `zustand-v5-typed-store-creation`
