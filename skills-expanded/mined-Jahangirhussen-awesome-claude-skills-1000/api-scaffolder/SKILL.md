---
name: api-scaffolder
description: >
  Trigger when the user wants to scaffold REST or GraphQL API endpoints, route handlers, controllers, or middleware. Also trigger for adding validation, error handling, authentication guards, or OpenAPI/Swagger docs to existing endpoints.
source:
  repository: armaneker/claude-code-skills
  original_path: saas-builder-kit/skills/api-scaffolder
  original_name: api-scaffolder
status: canonical
---
# API Scaffolder

You are an expert API engineer. Generate production-ready endpoint code with validation, error handling, and auth middleware — not just stubs.

## Workflow

1. **Identify the target framework:**
   - Express / Express + TypeScript
   - Fastify
   - Next.js API Routes (`/pages/api` or `/app/api` with Route Handlers)
   - Hono, Koa, or other (ask user)

2. **Identify the API style:**
   - REST (default)
   - GraphQL (ask for schema/resolvers or SDL-first vs code-first)
   - tRPC (if mentioned)

3. **Identify the resource(s)** — e.g. "users", "orders", "products"

4. **Generate the full CRUD scaffold** unless the user specifies specific operations.

## Output Structure

For each resource, generate these files:

```
src/
  routes/
    users.ts          ← route definitions
  controllers/
    users.controller.ts
  validators/
    users.validator.ts
  middleware/
    auth.middleware.ts
    error.middleware.ts
  types/
    users.types.ts
```

## Express + TypeScript Example

**Route file (`src/routes/users.ts`):**
```typescript
import { Router } from 'express';
import { authenticate } from '../middleware/auth.middleware';
import { validate } from '../middleware/validate.middleware';
import * as controller from '../controllers/users.controller';
import { createUserSchema, updateUserSchema } from '../validators/users.validator';

const router = Router();

router.get('/',    authenticate, controller.list);
router.get('/:id', authenticate, controller.getById);
router.post('/',   authenticate, validate(createUserSchema), controller.create);
router.patch('/:id', authenticate, validate(updateUserSchema), controller.update);
router.delete('/:id', authenticate, controller.remove);

export default router;
```

**Controller (`src/controllers/users.controller.ts`):**
```typescript
import { Request, Response, NextFunction } from 'express';
import { UserService } from '../services/users.service';
import { NotFoundError } from '../errors';

const userService = new UserService();

export const list = async (req: Request, res: Response, next: NextFunction) => {
  try {
    const { page = 1, limit = 20 } = req.query;
    const users = await userService.findAll({ page: Number(page), limit: Number(limit) });
    res.json({ data: users.items, meta: { page, limit, total: users.total } });
  } catch (err) { next(err); }
};

export const getById = async (req: Request, res: Response, next: NextFunction) => {
  try {
    const user = await userService.findById(req.params.id);
    if (!user) throw new NotFoundError('User not found');
    res.json({ data: user });
  } catch (err) { next(err); }
};

export const create = async (req: Request, res: Response, next: NextFunction) => {
  try {
    const user = await userService.create(req.body);
    res.status(201).json({ data: user });
  } catch (err) { next(err); }
};
```

**Validator (`src/validators/users.validator.ts`):**
```typescript
import { z } from 'zod';

export const createUserSchema = z.object({
  body: z.object({
    email: z.string().email(),
    name: z.string().min(1).max(100),
    role: z.enum(['user', 'admin']).default('user'),
  }),
});

export const updateUserSchema = z.object({
  params: z.object({ id: z.string().uuid() }),
  body: z.object({
    name: z.string().min(1).max(100).optional(),
    role: z.enum(['user', 'admin']).optional(),
  }).refine(data => Object.keys(data).length > 0, 'At least one field required'),
});
```

**Global error handler (`src/middleware/error.middleware.ts`):**
```typescript
import { Request, Response, NextFunction } from 'express';
import { ZodError } from 'zod';

export const errorHandler = (err: unknown, req: Request, res: Response, next: NextFunction) => {
  if (err instanceof ZodError) {
    return res.status(400).json({
      error: 'Validation failed',
      details: err.flatten().fieldErrors,
    });
  }
  if (err instanceof AppError) {
    return res.status(err.statusCode).json({ error: err.message });
  }
  console.error(err);
  res.status(500).json({ error: 'Internal server error' });
};
```

## Next.js Route Handlers (App Router)

```typescript
// app/api/users/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { getServerSession } from 'next-auth';
import { authOptions } from '@/lib/auth';
import { createUserSchema } from '@/validators/users.validator';

export async function GET(req: NextRequest) {
  const session = await getServerSession(authOptions);
  if (!session) return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });

  const { searchParams } = new URL(req.url);
  const page = Number(searchParams.get('page') ?? 1);
  // ... fetch logic
  return NextResponse.json({ data: users });
}

export async function POST(req: NextRequest) {
  const session = await getServerSession(authOptions);
  if (!session) return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });

  const body = await req.json();
  const parsed = createUserSchema.safeParse(body);
  if (!parsed.success) {
    return NextResponse.json({ error: 'Validation failed', details: parsed.error.flatten() }, { status: 400 });
  }
  // ... create logic
  return NextResponse.json({ data: user }, { status: 201 });
}
```

## Standard Response Envelope

Always use a consistent response shape:

```typescript
// Success (single)
{ "data": { ... } }

// Success (list)
{ "data": [...], "meta": { "page": 1, "limit": 20, "total": 100 } }

// Error
{ "error": "Human-readable message", "details": { ... } }
```

## Auth Middleware Pattern

```typescript
// src/middleware/auth.middleware.ts
import { Request, Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';

export interface AuthRequest extends Request {
  user?: { id: string; role: string };
}

export const authenticate = (req: AuthRequest, res: Response, next: NextFunction) => {
  const token = req.headers.authorization?.replace('Bearer ', '');
  if (!token) return res.status(401).json({ error: 'No token provided' });

  try {
    req.user = jwt.verify(token, process.env.JWT_SECRET!) as { id: string; role: string };
    next();
  } catch {
    res.status(401).json({ error: 'Invalid token' });
  }
};

export const requireRole = (role: string) => (req: AuthRequest, res: Response, next: NextFunction) => {
  if (req.user?.role !== role) return res.status(403).json({ error: 'Forbidden' });
  next();
};
```

## Common Pitfalls — Avoid These

- **Not validating req.params.id** as UUID before hitting the DB — leads to confusing DB errors
- **Returning stack traces in production** — always sanitize error messages
- **Missing pagination** on list endpoints — add `page` + `limit` from day one
- **Async route handlers without try/catch or asyncHandler wrapper** — unhandled rejections crash Express < 5
- **Storing business logic in controllers** — controllers should be thin; logic goes in services
- **No rate limiting** — add `express-rate-limit` on auth and write endpoints before going to production

## OpenAPI Docs

If the user wants Swagger/OpenAPI docs, add `@asteasolutions/zod-to-openapi` or `swagger-jsdoc`:

```typescript
// Register schema
registry.register('CreateUser', createUserSchema);
registry.registerPath({
  method: 'post', path: '/users', tags: ['Users'],
  request: { body: { content: { 'application/json': { schema: CreateUserSchema } } } },
  responses: { 201: { description: 'Created', content: { 'application/json': { schema: UserSchema } } } },
});
```
