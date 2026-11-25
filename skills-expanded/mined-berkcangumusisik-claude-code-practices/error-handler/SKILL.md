---
name: error-handler
description: Creates a centralized error handling system with typed errors and proper HTTP responses
user-invocable: true
allowed-tools: Read Glob Edit
effort: medium
---

## Generate Error Handling System

1. Check existing error handling:
```bash
grep -rn "catch\|try\|throw\|Error(" src/ --include="*.ts" -l | head -10
grep -rn "class.*Error" src/ --include="*.ts" | head -10
```

2. Generate typed error classes:
```ts
export class AppError extends Error {
  constructor(
    message: string,
    public readonly statusCode: number,
    public readonly code: string,
    public readonly isOperational = true,
  ) {
    super(message)
    this.name = this.constructor.name
  }
}

export class NotFoundError extends AppError {
  constructor(resource: string) {
    super(`${resource} not found`, 404, 'NOT_FOUND')
  }
}

export class ValidationError extends AppError {
  constructor(details: ZodIssue[]) {
    super('Validation failed', 400, 'VALIDATION_ERROR')
  }
}

export class UnauthorizedError extends AppError {
  constructor() { super('Unauthorized', 401, 'UNAUTHORIZED') }
}
```

3. Generate global error handler middleware.

4. Add `Result<T, E>` type for functions that can fail without throwing.

5. Replace generic `try/catch` blocks with typed errors throughout the codebase.
