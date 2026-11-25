---
name: node-express-api
description: >
  Express.js API design patterns including middleware, error handling,
  validation, authentication, and project structure. Use this skill when
  building or maintaining REST APIs with Node.js and Express. Covers
  production-ready patterns for routing, security, and request handling.
license: MIT
metadata:
  author: skillbox
  version: "1.0"
  category: backend
  tags: node, express, api, rest, backend
---

# Express.js API Design

## Project Structure

Organize by feature/domain, not by technical role.

```
src/
  app.ts                # Express app setup, global middleware
  server.ts             # HTTP server startup, graceful shutdown
  config/
    index.ts            # Environment config with validation
  middleware/
    errorHandler.ts     # Central error handler
    authenticate.ts     # Auth middleware
    validate.ts         # Request validation middleware
  features/
    users/
      users.router.ts
      users.controller.ts
      users.service.ts
      users.model.ts
      users.schema.ts   # Zod/Joi validation schemas
    posts/
      posts.router.ts
      ...
  lib/
    db.ts               # Database connection
    logger.ts           # Logger instance
  types/
    index.ts            # Shared TypeScript types
```

## Router and Controller Pattern

Separate routing from business logic. The router defines routes, the controller handles HTTP concerns, the service contains business logic.

```typescript
// features/users/users.router.ts
import { Router } from 'express';
import { UsersController } from './users.controller';
import { authenticate } from '../../middleware/authenticate';
import { validate } from '../../middleware/validate';
import { createUserSchema, updateUserSchema } from './users.schema';

const router = Router();
const controller = new UsersController();

router.get('/', authenticate, controller.list);
router.get('/:id', authenticate, controller.getById);
router.post('/', authenticate, validate(createUserSchema), controller.create);
router.patch('/:id', authenticate, validate(updateUserSchema), controller.update);
router.delete('/:id', authenticate, controller.delete);

export { router as usersRouter };
```

Controllers should be thin -- extract and pass data to services, then format the response:

```typescript
class UsersController {
  async create(req: Request, res: Response, next: NextFunction) {
    try {
      const user = await usersService.create(req.body);
      res.status(201).json({ data: user });
    } catch (error) {
      next(error);
    }
  }
}
```

## Error Handling

Create a centralized error handler. Never let errors silently fail.

```typescript
// Custom error classes
class AppError extends Error {
  constructor(
    public statusCode: number,
    public message: string,
    public code?: string,
    public isOperational = true
  ) {
    super(message);
  }
}

class NotFoundError extends AppError {
  constructor(resource: string) {
    super(404, `${resource} not found`, 'NOT_FOUND');
  }
}

class ValidationError extends AppError {
  constructor(message: string) {
    super(400, message, 'VALIDATION_ERROR');
  }
}
```

Register the error handler as the last middleware:

```typescript
// middleware/errorHandler.ts
function errorHandler(err: Error, req: Request, res: Response, next: NextFunction) {
  if (err instanceof AppError) {
    return res.status(err.statusCode).json({
      error: { message: err.message, code: err.code },
    });
  }

  logger.error('Unhandled error', { error: err, path: req.path });
  res.status(500).json({
    error: { message: 'Internal server error', code: 'INTERNAL_ERROR' },
  });
}
```

- Always call `next(error)` in route handlers instead of sending error responses directly.
- Handle async errors by wrapping handlers or using `express-async-errors`.
- Log unhandled errors with context (request path, user ID, trace ID).

## Request Validation

Validate all incoming data at the boundary using Zod.

```typescript
// middleware/validate.ts
import { ZodSchema } from 'zod';

function validate(schema: ZodSchema) {
  return (req: Request, res: Response, next: NextFunction) => {
    const result = schema.safeParse({
      body: req.body,
      query: req.query,
      params: req.params,
    });
    if (!result.success) {
      return next(new ValidationError(result.error.issues));
    }
    req.body = result.data.body;
    req.query = result.data.query;
    req.params = result.data.params;
    next();
  };
}
```

- Validate body, query params, and path params.
- Strip unknown fields using `.strip()` to prevent mass assignment.
- Define schemas alongside their feature modules.

## Middleware Best Practices

- Apply middleware in order: body parser, CORS, request ID, logger, auth, routes, error handler.
- Use `helmet()` for security headers.
- Use `cors()` with explicit origin configuration, never `*` in production.
- Add a request ID middleware for tracing: attach `req.id = crypto.randomUUID()`.
- Use `express.json({ limit: '10kb' })` to prevent large payload attacks.
- Implement rate limiting with `express-rate-limit` on public endpoints.

## Response Format

Return consistent JSON responses:

```typescript
// Success
{ "data": { ... } }
{ "data": [...], "pagination": { "page": 1, "limit": 20, "total": 100 } }

// Error
{ "error": { "message": "User not found", "code": "NOT_FOUND" } }
```

- Use HTTP status codes correctly: 200 (OK), 201 (Created), 204 (No Content), 400 (Bad Request), 401 (Unauthorized), 403 (Forbidden), 404 (Not Found), 409 (Conflict), 422 (Unprocessable Entity), 500 (Internal Error).
- Return 204 with no body for successful deletions.
- Include pagination metadata for list endpoints.

## Security

- Never expose stack traces in production error responses.
- Sanitize user input to prevent NoSQL injection when using MongoDB.
- Use parameterized queries to prevent SQL injection.
- Hash passwords with `bcrypt` (cost factor 12+) or `argon2`.
- Store secrets in environment variables, never in code.
- Validate and sanitize file uploads: check MIME type, limit size, rename files.

## Graceful Shutdown

```typescript
const server = app.listen(PORT, () => logger.info(`Listening on ${PORT}`));

process.on('SIGTERM', () => {
  logger.info('SIGTERM received, shutting down gracefully');
  server.close(() => {
    db.disconnect();
    process.exit(0);
  });
});
```

## Environment Configuration

Validate all environment variables at startup using Zod. Fail fast if required config is missing.

```typescript
const envSchema = z.object({
  NODE_ENV: z.enum(['development', 'production', 'test']),
  PORT: z.coerce.number().default(3000),
  DATABASE_URL: z.string().url(),
  JWT_SECRET: z.string().min(32),
});

export const env = envSchema.parse(process.env);
```
