---
name: validation-input-sanitization
description: Implement comprehensive input validation and sanitization patterns. Use when validating user input, sanitizing data, or when the user asks about validation, input sanitization, data validation, or schema validation.
---

# Validation & Input Sanitization

Implement comprehensive validation and sanitization to ensure data integrity and security.

## Validation Strategies

### Schema-Based Validation

**Using Zod:**

```typescript
import { z } from "zod";

// Define schema
const createUserSchema = z.object({
  email: z.string().email("Invalid email format"),
  password: z
    .string()
    .min(8, "Password must be at least 8 characters")
    .regex(/[A-Z]/, "Password must contain uppercase letter")
    .regex(/[a-z]/, "Password must contain lowercase letter")
    .regex(/[0-9]/, "Password must contain number"),
  name: z.string().min(1, "Name is required").max(100),
  age: z.number().int().min(0).max(150).optional(),
  role: z.enum(["admin", "user", "guest"]).default("user"),
});

// Validate
function validateCreateUser(data: unknown) {
  try {
    return createUserSchema.parse(data);
  } catch (error) {
    if (error instanceof z.ZodError) {
      const errors: Record<string, string[]> = {};
      error.errors.forEach((err) => {
        const path = err.path.join(".");
        if (!errors[path]) errors[path] = [];
        errors[path].push(err.message);
      });
      throw new ValidationError("Validation failed", errors);
    }
    throw error;
  }
}
```

**Using Joi:**

```typescript
import Joi from "joi";

const createUserSchema = Joi.object({
  email: Joi.string().email().required(),
  password: Joi.string().min(8).required(),
  name: Joi.string().min(1).max(100).required(),
  age: Joi.number().integer().min(0).max(150).optional(),
  role: Joi.string().valid("admin", "user", "guest").default("user"),
});

function validateCreateUser(data: unknown) {
  const { error, value } = createUserSchema.validate(data, {
    abortEarly: false,
  });

  if (error) {
    const errors: Record<string, string[]> = {};
    error.details.forEach((detail) => {
      const path = detail.path.join(".");
      if (!errors[path]) errors[path] = [];
      errors[path].push(detail.message);
    });
    throw new ValidationError("Validation failed", errors);
  }

  return value;
}
```

### Custom Validators

```typescript
// Custom validation functions
const validators = {
  email: (value: string): boolean => {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
  },

  strongPassword: (value: string): boolean => {
    return /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/.test(
      value,
    );
  },

  phoneNumber: (value: string): boolean => {
    return /^\+?[1-9]\d{1,14}$/.test(value);
  },

  url: (value: string): boolean => {
    try {
      new URL(value);
      return true;
    } catch {
      return false;
    }
  },
};

// Usage in schema
const schema = z.object({
  email: z.string().refine(validators.email, "Invalid email format"),
  password: z.string().refine(validators.strongPassword, "Password too weak"),
});
```

## Input Sanitization

### HTML Sanitization

```typescript
import DOMPurify from "isomorphic-dompurify";

// Sanitize HTML content
function sanitizeHtml(html: string): string {
  return DOMPurify.sanitize(html, {
    ALLOWED_TAGS: ["b", "i", "em", "strong", "a", "p", "br"],
    ALLOWED_ATTR: ["href"],
  });
}

// Remove all HTML
function stripHtml(html: string): string {
  return DOMPurify.sanitize(html, { ALLOWED_TAGS: [] });
}
```

### String Sanitization

```typescript
function sanitizeString(input: string): string {
  return input
    .trim() // Remove leading/trailing whitespace
    .replace(/[<>]/g, "") // Remove HTML brackets
    .replace(/[^\w\s-]/g, "") // Remove special characters (keep alphanumeric, spaces, hyphens)
    .substring(0, 1000); // Limit length
}

// Sanitize for SQL (though ORM handles this)
function sanitizeForSql(input: string): string {
  return input.replace(/['";\\]/g, ""); // Remove SQL special characters
}
```

### Number Sanitization

```typescript
function sanitizeNumber(input: unknown): number | null {
  if (typeof input === "number") {
    return isNaN(input) ? null : input;
  }

  if (typeof input === "string") {
    const parsed = parseFloat(input);
    return isNaN(parsed) ? null : parsed;
  }

  return null;
}

// Integer sanitization
function sanitizeInteger(input: unknown): number | null {
  const num = sanitizeNumber(input);
  return num !== null ? Math.floor(num) : null;
}
```

## Validation Middleware

### Express Validation Middleware

```typescript
import { Request, Response, NextFunction } from "express";

export const validate = (schema: {
  body?: z.ZodSchema;
  query?: z.ZodSchema;
  params?: z.ZodSchema;
}) => {
  return (req: Request, res: Response, next: NextFunction): void => {
    const errors: Record<string, string[]> = {};

    // Validate body
    if (schema.body) {
      try {
        req.body = schema.body.parse(req.body);
      } catch (error) {
        if (error instanceof z.ZodError) {
          error.errors.forEach((err) => {
            const path = `body.${err.path.join(".")}`;
            if (!errors[path]) errors[path] = [];
            errors[path].push(err.message);
          });
        }
      }
    }

    // Validate query
    if (schema.query) {
      try {
        req.query = schema.query.parse(req.query);
      } catch (error) {
        if (error instanceof z.ZodError) {
          error.errors.forEach((err) => {
            const path = `query.${err.path.join(".")}`;
            if (!errors[path]) errors[path] = [];
            errors[path].push(err.message);
          });
        }
      }
    }

    // Validate params
    if (schema.params) {
      try {
        req.params = schema.params.parse(req.params);
      } catch (error) {
        if (error instanceof z.ZodError) {
          error.errors.forEach((err) => {
            const path = `params.${err.path.join(".")}`;
            if (!errors[path]) errors[path] = [];
            errors[path].push(err.message);
          });
        }
      }
    }

    if (Object.keys(errors).length > 0) {
      return res.status(400).json({
        error: {
          message: "Validation failed",
          code: "VALIDATION_ERROR",
          errors,
        },
      });
    }

    next();
  };
};

// Usage
router.post(
  "/users",
  validate({
    body: createUserSchema,
  }),
  createUser,
);
```

## Type Coercion

### Safe Type Coercion

```typescript
function coerceToNumber(value: unknown): number | null {
  if (typeof value === "number") return value;
  if (typeof value === "string") {
    const parsed = parseFloat(value);
    return isNaN(parsed) ? null : parsed;
  }
  return null;
}

function coerceToBoolean(value: unknown): boolean {
  if (typeof value === "boolean") return value;
  if (typeof value === "string") {
    return value.toLowerCase() === "true" || value === "1";
  }
  if (typeof value === "number") return value !== 0;
  return false;
}

function coerceToDate(value: unknown): Date | null {
  if (value instanceof Date) return value;
  if (typeof value === "string" || typeof value === "number") {
    const date = new Date(value);
    return isNaN(date.getTime()) ? null : date;
  }
  return null;
}
```

## Validation Best Practices

### 1. Validate Early

```typescript
// ✅ Good - Validate at API boundary
router.post("/users", validate({ body: createUserSchema }), createUser);

// ❌ Bad - Validate deep in business logic
async function createUser(data: any) {
  // ... business logic ...
  if (!data.email) throw new Error("Email required"); // Too late
}
```

### 2. Validate All Inputs

```typescript
// Validate body, query, params, headers
router.get(
  "/users/:id",
  validate({
    params: z.object({ id: z.string().uuid() }),
    query: z.object({
      include: z.string().optional(),
      fields: z.string().optional(),
    }),
  }),
  getUser,
);
```

### 3. Provide Clear Error Messages

```typescript
// ✅ Good - Specific error messages
z.string().email("Please provide a valid email address");
z.string().min(8, "Password must be at least 8 characters long");

// ❌ Bad - Generic error messages
z.string().email("Invalid");
z.string().min(8, "Error");
```

### 4. Sanitize Before Validation

```typescript
function sanitizeAndValidate(data: unknown, schema: z.ZodSchema) {
  // Sanitize first
  const sanitized = sanitizeInput(data);

  // Then validate
  return schema.parse(sanitized);
}
```

### 5. Use Type-Safe Validation

```typescript
// ✅ Good - Type inference from schema
const schema = z.object({
  email: z.string().email(),
  age: z.number().int(),
});

type UserInput = z.infer<typeof schema>; // Automatically typed
```

## Common Validation Patterns

### Email Validation

```typescript
const emailSchema = z.string().email("Invalid email format");

// Or custom
const emailSchema = z
  .string()
  .refine(
    (email) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email),
    "Invalid email format",
  );
```

### Password Validation

```typescript
const passwordSchema = z
  .string()
  .min(8, "Password must be at least 8 characters")
  .regex(/[A-Z]/, "Password must contain uppercase letter")
  .regex(/[a-z]/, "Password must contain lowercase letter")
  .regex(/[0-9]/, "Password must contain number")
  .regex(/[@$!%*?&]/, "Password must contain special character");
```

### URL Validation

```typescript
const urlSchema = z.string().url("Invalid URL format");

// Or custom
const urlSchema = z.string().refine((url) => {
  try {
    new URL(url);
    return true;
  } catch {
    return false;
  }
}, "Invalid URL format");
```

### Date Validation

```typescript
const dateSchema = z.string().datetime("Invalid date format");

// Or custom
const dateSchema = z
  .string()
  .refine((date) => !isNaN(Date.parse(date)), "Invalid date format");
```

## When Validating Input

1. **Validate at boundaries** - API endpoints, function inputs
2. **Use schema validation** - Zod, Joi, or similar
3. **Sanitize before validating** - Clean input first
4. **Provide clear error messages** - Help users fix issues
5. **Validate all inputs** - Body, query, params, headers
6. **Use type-safe schemas** - Leverage TypeScript inference
7. **Validate early** - Fail fast at API boundary
8. **Sanitize outputs** - When displaying user input
9. **Use custom validators** - For complex validation rules
10. **Test validation** - Ensure all cases are covered
