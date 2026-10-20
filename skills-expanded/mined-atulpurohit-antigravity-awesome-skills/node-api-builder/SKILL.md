---
name: node-api-builder
description: "Build production-ready Node.js APIs with Express or Fastify. Covers middleware, authentication, validation, error handling, and performance optimization."
category: php-frameworks
tags: ['node', 'express', 'api', 'javascript', 'backend']
complexity: advanced
risk: low
compatibility: [claude-code, antigravity, gemini-cli, cursor, copilot, codex-cli, autohand, kiro]
source: antigravity-official
version: "1.0.0"
date_added: "2026-07-10"
last_updated: "2026-07-10"
---

# Node.js API Builder

## Purpose
Build fast, scalable Node.js APIs with proper architecture, security, validation, and observability.

## Operating Mode
You are a **Node.js backend engineer**. You write clean, modular, tested Node.js code using modern JavaScript/TypeScript patterns.

## Architecture Pattern

### Project Structure
```
src/
├── app.ts              # Express app setup
├── server.ts           # Server entry point
├── config/             # Environment config
├── routes/             # Route definitions
├── controllers/        # Request handlers
├── services/           # Business logic
├── repositories/       # Data access
├── middlewares/        # Custom middleware
├── validators/         # Input validation schemas
├── models/             # Database models
├── utils/              # Utilities
├── types/              # TypeScript types
└── __tests__/          # Tests
```

### Express App Setup
```typescript
// src/app.ts
import express, { Application, Request, Response, NextFunction } from 'express';
import helmet from 'helmet';
import cors from 'cors';
import rateLimit from 'express-rate-limit';
import { json } from 'express';
import { errorHandler } from './middlewares/errorHandler';
import routes from './routes';

const app: Application = express();

// Security middleware
app.use(helmet());
app.use(cors({ origin: process.env.ALLOWED_ORIGINS?.split(',') }));

// Rate limiting
app.use('/api', rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100,
  standardHeaders: true,
  legacyHeaders: false,
}));

// Body parsing
app.use(json({ limit: '10kb' }));

// Routes
app.use('/api/v1', routes);

// Health check
app.get('/health', (req: Request, res: Response) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// 404 handler
app.use((req: Request, res: Response) => {
  res.status(404).json({ message: 'Route not found' });
});

// Global error handler
app.use(errorHandler);

export default app;
```

### Controller Pattern
```typescript
// src/controllers/post.controller.ts
import { Request, Response, NextFunction } from 'express';
import { PostService } from '../services/post.service';
import { createPostSchema } from '../validators/post.validator';

export class PostController {
  constructor(private postService: PostService) {}

  async getPosts(req: Request, res: Response, next: NextFunction): Promise<void> {
    try {
      const { page = 1, limit = 20, status } = req.query;
      const result = await this.postService.findAll({ page: +page, limit: +limit, status: status as string });
      res.json({ data: result.posts, meta: result.pagination });
    } catch (error) {
      next(error);
    }
  }

  async createPost(req: Request, res: Response, next: NextFunction): Promise<void> {
    try {
      const { error, value } = createPostSchema.validate(req.body);
      if (error) throw new ValidationError(error.details[0].message);

      const post = await this.postService.create({ ...value, authorId: req.user!.id });
      res.status(201).json({ data: post });
    } catch (error) {
      next(error);
    }
  }
}
```

### Authentication Middleware
```typescript
// src/middlewares/auth.ts
import jwt from 'jsonwebtoken';

export const authenticate = async (req: Request, res: Response, next: NextFunction) => {
  const token = req.headers.authorization?.split(' ')[1];
  
  if (!token) {
    return res.status(401).json({ message: 'Authentication required' });
  }

  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET!) as JwtPayload;
    req.user = await UserRepository.findById(decoded.userId);
    next();
  } catch {
    res.status(401).json({ message: 'Invalid or expired token' });
  }
};
```

### Error Handling
```typescript
// src/middlewares/errorHandler.ts
export const errorHandler = (error: Error, req: Request, res: Response, next: NextFunction) => {
  console.error(error);

  if (error instanceof ValidationError) {
    return res.status(422).json({ message: error.message, type: 'validation' });
  }
  if (error instanceof NotFoundError) {
    return res.status(404).json({ message: error.message });
  }
  if (error instanceof UnauthorizedError) {
    return res.status(401).json({ message: error.message });
  }

  res.status(500).json({ message: 'Internal server error', requestId: req.id });
};
```

## Outputs
1. Express/Fastify app setup
2. Controller/Service/Repository layers
3. Authentication middleware
4. Input validation schemas (Joi/Zod)
5. Error handling middleware
6. API testing with Jest/Supertest
7. Docker configuration
