---
name: node-express-expert
description: "Build production Node.js applications with Express. Covers middleware architecture, authentication, validation, error handling, testing, and performance."
category: backend
tags: [node, express, javascript, api, middleware]
complexity: advanced
risk: low
compatibility: [claude-code, antigravity, gemini-cli, cursor, copilot, codex-cli, autohand, kiro]
source: antigravity-official
version: "1.0.0"
date_added: "2026-07-10"
last_updated: "2026-07-10"
---

# Node.js Express Expert

## Purpose
Build robust, scalable Node.js applications with Express following production-grade patterns.

## Application Architecture

### 1️⃣ Enterprise Express Setup
```typescript
// src/app.ts
import express from 'express';
import helmet from 'helmet';
import cors from 'cors';
import compression from 'compression';
import rateLimit from 'express-rate-limit';
import { requestId } from './middleware/requestId';
import { requestLogger } from './middleware/logger';
import { errorHandler } from './middleware/errorHandler';
import { router } from './routes';

const app = express();

// Security
app.use(helmet());
app.use(cors({ origin: process.env.CORS_ORIGIN?.split(','), credentials: true }));
app.disable('x-powered-by');

// Performance
app.use(compression());

// Rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100,
  standardHeaders: true,
  legacyHeaders: false,
  keyGenerator: (req) => req.user?.id ?? req.ip ?? 'unknown',
});
app.use('/api', limiter);

// Parsing
app.use(express.json({ limit: '10kb' }));
app.use(express.urlencoded({ extended: true, limit: '10kb' }));

// Request tracking
app.use(requestId);
app.use(requestLogger);

// Routes
app.use('/api/v1', router);
app.get('/health', (req, res) => res.json({ status: 'ok' }));

// 404
app.use((req, res) => res.status(404).json({ message: `Route ${req.method} ${req.path} not found` }));

// Error handler (must be last)
app.use(errorHandler);

export { app };
```

### 2️⃣ Middleware Patterns
```typescript
// Request ID middleware
export const requestId = (req: Request, res: Response, next: NextFunction) => {
  req.id = crypto.randomUUID();
  res.setHeader('X-Request-Id', req.id);
  next();
};

// Async wrapper (eliminates try-catch boilerplate)
export const asyncHandler = (fn: RequestHandler) => 
  (req: Request, res: Response, next: NextFunction) =>
    Promise.resolve(fn(req, res, next)).catch(next);

// Usage
router.get('/posts', asyncHandler(async (req, res) => {
  const posts = await PostService.findAll(req.query);
  res.json({ data: posts });
}));

// Input validation with Zod
import { z } from 'zod';

const createPostSchema = z.object({
  body: z.object({
    title: z.string().min(3).max(255),
    body: z.string().min(100),
    tags: z.array(z.string()).max(5).optional(),
  }),
});

export const validate = (schema: z.AnyZodObject) =>
  asyncHandler(async (req, res, next) => {
    await schema.parseAsync({ body: req.body, query: req.query, params: req.params });
    next();
  });
```

### 3️⃣ Service Layer
```typescript
// src/services/PostService.ts
export class PostService {
  constructor(
    private readonly postRepo: PostRepository,
    private readonly cacheService: CacheService,
    private readonly eventBus: EventBus,
  ) {}

  async findAll(query: PostQuery): Promise<PaginatedResult<Post>> {
    const cacheKey = `posts:${JSON.stringify(query)}`;
    
    return this.cacheService.remember(cacheKey, 300, () =>
      this.postRepo.findAll(query)
    );
  }

  async create(data: CreatePostDto, authorId: string): Promise<Post> {
    const post = await this.postRepo.create({ ...data, authorId });
    await this.eventBus.publish('post.created', { postId: post.id, authorId });
    return post;
  }
}
```

### 4️⃣ Testing with Supertest
```typescript
// tests/posts.test.ts
describe('POST /api/v1/posts', () => {
  it('creates a post when authenticated', async () => {
    const token = generateTestToken({ userId: 'user-1' });
    
    const response = await request(app)
      .post('/api/v1/posts')
      .set('Authorization', `Bearer ${token}`)
      .send({ title: 'Test Post', body: 'x'.repeat(100) });
    
    expect(response.status).toBe(201);
    expect(response.body.data.title).toBe('Test Post');
  });
});
```

## Outputs
1. Express app structure with all middleware
2. Request lifecycle management
3. Service layer and repository pattern
4. Authentication middleware
5. Validation with Zod
6. Test setup with Supertest
