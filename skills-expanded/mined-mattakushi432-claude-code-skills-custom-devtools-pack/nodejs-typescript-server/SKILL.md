---
name: nodejs-typescript-server
description: "When to activate: Express with TypeScript, middleware patterns, REST API design, error handling, OpenAPI, JWT auth, rate limiting"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: engineering
  language: typescript
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---

# Node.js TypeScript Server Patterns

## Project Structure
```
src/
├── index.ts               # Entry: create app, start server
├── app.ts                 # Express factory: middlewares, routes
├── config/
│   └── env.ts             # Zod-validated env
├── middleware/
│   ├── auth.ts            # JWT auth
│   ├── rateLimit.ts
│   └── errorHandler.ts
├── routes/
│   └── v1/
│       ├── index.ts
│       └── users.ts
├── services/
│   └── userService.ts
├── repositories/
│   └── userRepository.ts
├── types/
│   └── express.d.ts       # Request augmentation
└── lib/
    └── logger.ts          # Pino
```

## App Factory
```ts
// src/app.ts
import express from 'express'
import helmet from 'helmet'
import cors from 'cors'
import { json } from 'express'
import { v1Router } from './routes/v1'
import { errorHandler } from './middleware/errorHandler'
import { notFoundHandler } from './middleware/notFoundHandler'

export function createApp() {
  const app = express()

  app.use(helmet())
  app.use(cors({ origin: process.env.CORS_ORIGIN, credentials: true }))
  app.use(json({ limit: '1mb' }))

  app.get('/health', (_req, res) => res.json({ status: 'ok', ts: Date.now() }))
  app.use('/api/v1', v1Router)

  app.use(notFoundHandler)
  app.use(errorHandler)

  return app
}
```

## Auth Middleware (JWT)
```ts
// middleware/auth.ts
import { Request, Response, NextFunction } from 'express'
import jwt from 'jsonwebtoken'
import { env } from '../config/env'

interface TokenPayload { sub: string; role: string; iat: number; exp: number }

declare module 'express' {
  interface Request { user?: TokenPayload }
}

export function authenticate(req: Request, res: Response, next: NextFunction) {
  const header = req.headers.authorization
  if (!header?.startsWith('Bearer ')) {
    return res.status(401).json({ error: 'Missing token' })
  }
  try {
    const token   = header.slice(7)
    req.user = jwt.verify(token, env.JWT_SECRET) as TokenPayload
    next()
  } catch {
    res.status(401).json({ error: 'Invalid token' })
  }
}

export function authorize(...roles: string[]) {
  return (req: Request, res: Response, next: NextFunction) => {
    if (!req.user || !roles.includes(req.user.role)) {
      return res.status(403).json({ error: 'Forbidden' })
    }
    next()
  }
}
```

## Error Handler
```ts
// middleware/errorHandler.ts
import { Request, Response, NextFunction } from 'express'
import { ZodError } from 'zod'
import { logger } from '../lib/logger'

export class AppError extends Error {
  constructor(
    public status: number,
    message: string,
    public details?: unknown
  ) { super(message) }
}

export function errorHandler(
  err: unknown,
  _req: Request,
  res: Response,
  _next: NextFunction
) {
  if (err instanceof ZodError) {
    return res.status(422).json({
      error: 'Validation failed',
      details: err.flatten(),
    })
  }

  if (err instanceof AppError) {
    return res.status(err.status).json({
      error: err.message,
      ...(err.details ? { details: err.details } : {}),
    })
  }

  logger.error(err, 'Unhandled error')
  res.status(500).json({ error: 'Internal server error' })
}
```

## Route Handler Pattern
```ts
// routes/v1/users.ts
import { Router } from 'express'
import { z } from 'zod'
import { authenticate } from '../../middleware/auth'
import { userService } from '../../services/userService'
import { AppError } from '../../middleware/errorHandler'

const router = Router()

const CreateUserSchema = z.object({
  name:  z.string().min(1).max(100),
  email: z.string().email(),
})

router.get('/', authenticate, async (req, res, next) => {
  try {
    const { page = 1, limit = 20 } = req.query
    const result = await userService.list({ page: Number(page), limit: Number(limit) })
    res.json(result)
  } catch (err) { next(err) }
})

router.post('/', async (req, res, next) => {
  try {
    const data = CreateUserSchema.parse(req.body)
    const user = await userService.create(data)
    res.status(201).json(user)
  } catch (err) { next(err) }
})

router.get('/:id', authenticate, async (req, res, next) => {
  try {
    const user = await userService.getById(req.params.id)
    if (!user) throw new AppError(404, 'User not found')
    res.json(user)
  } catch (err) { next(err) }
})

export { router as usersRouter }
```

## Rate Limiting
```ts
import rateLimit from 'express-rate-limit'
import RedisStore from 'rate-limit-redis'

export const apiLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,  // 15 min
  max: 100,
  standardHeaders: true,
  legacyHeaders: false,
  store: new RedisStore({ client: redisClient }),
  keyGenerator: (req) => req.user?.sub ?? req.ip ?? 'unknown',
  handler: (_req, res) => res.status(429).json({ error: 'Too many requests' }),
})

export const strictLimiter = rateLimit({
  windowMs: 60_000,
  max: 5,
  message: { error: 'Too many attempts, try again in 1 minute' },
})
```

## Logger (Pino)
```ts
// lib/logger.ts
import pino from 'pino'

export const logger = pino({
  level: process.env.LOG_LEVEL ?? 'info',
  ...(process.env.NODE_ENV !== 'production' && {
    transport: { target: 'pino-pretty', options: { colorize: true } },
  }),
  redact: ['req.headers.authorization', '*.password', '*.token'],
})
```
