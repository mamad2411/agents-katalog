---
name: node-express-pro
description: "Express.js patterns, middleware architecture, error handling, validation, file uploads. Use when building or reviewing Node.js/Express services."
---

# Node Express Pro

## Purpose

Build production-grade Express.js applications with clean middleware architecture, centralized error handling, request validation, and organized routing.

## When to Use

**Use this when:**
- Building or reviewing a REST API with Express.js, including routing, middleware ordering, and controller/service separation
- Setting up a new Node.js backend from scratch that needs a proven project structure and error-handling baseline
- Debugging unhandled promise rejections, missing `next(err)` calls, or inconsistent error response shapes across routes

**Use this ESPECIALLY when:**
- The application has grown beyond a single file and controller logic, business logic, and database calls are tangled together
- Adding file upload endpoints, multipart forms, or streaming responses where Express middleware sequencing is critical
- Hardening an existing service with Helmet, rate limiting, structured logging, and graceful shutdown before a production launch

**Don't skip when:**
- Any new route is added without a validation middleware — raw `req.body` reaching service layer is the top injection vector
- Introducing a background job (Bull, Agenda) that shares the same database layer as the HTTP service
- Changing environment variable handling, because misconfigured env at startup is invisible until the first runtime failure in production

## Core Patterns

### 1. Project Structure

```
src/
  index.js / app.js
  config/
    env.js            ← Environment variables (zod validation)
    database.js
    redis.js
  middleware/
    auth.js
    errorHandler.js
    validate.js
    rateLimiter.js
  routes/
    v1/
      projects.routes.js
      users.routes.js
  controllers/
    projects.controller.js
  services/
    projects.service.js
  models/
    project.model.js   ← Prisma / Sequelize / Mongoose
  validators/
    project.validator.js
  utils/
    AppError.js        ← Custom error class
    logger.js
    pagination.js
  jobs/
    email.job.js       ← Bull / Agenda
  tests/
    projects.test.js
  prisma/               ← Prisma schema + migrations
```

### 2. App Factory

```javascript
// app.js
const express = require('express')
const cors = require('cors')
const helmet = require('helmet')

function createApp() {
  const app = express()

  // Global middleware (order matters)
  app.use(helmet())
  app.use(cors({ origin: process.env.CORS_ORIGIN }))
  app.use(express.json({ limit: '10mb' }))
  app.use(requestId())  // Attach X-Request-Id

  // Routes
  app.use('/api/v1/projects', projectRoutes)
  app.use('/api/v1/users', userRoutes)

  // Health check (no auth)
  app.get('/health', (req, res) => res.json({ status: 'healthy' }))

  // 404 handler
  app.use((req, res) => res.status(404).json({ error: 'NOT_FOUND' }))

  // Global error handler
  app.use(errorHandler)

  return app
}
```

### 3. Custom Error Class

```javascript
// utils/AppError.js
class AppError extends Error {
  constructor(code, message, status = 500, details = null) {
    super(message)
    this.code = code
    this.status = status
    this.details = details
  }

  static notFound(message = 'Resource not found') {
    return new AppError('NOT_FOUND', message, 404)
  }

  static badRequest(message, details = null) {
    return new AppError('BAD_REQUEST', message, 400, details)
  }

  static unauthorized(message = 'Unauthorized') {
    return new AppError('UNAUTHORIZED', message, 401)
  }

  static forbidden(message = 'Forbidden') {
    return new AppError('FORBIDDEN', message, 403)
  }

  static conflict(message = 'Resource already exists') {
    return new AppError('CONFLICT', message, 409)
  }
}
```

### 4. Error Handler Middleware

```javascript
// middleware/errorHandler.js
function errorHandler(err, req, res, next) {
  const status = err.status || 500
  const code = err.code || 'INTERNAL_ERROR'

  logger.error({
    requestId: req.id,
    method: req.method,
    path: req.path,
    code,
    message: err.message,
    stack: process.env.NODE_ENV === 'development' ? err.stack : undefined,
  })

  res.status(status).json({
    error: {
      code,
      message: status === 500 ? 'Internal server error' : err.message,
      details: err.details || undefined,
      requestId: req.id,
    },
  })
}
```

### 5. Controller Pattern

```javascript
// controllers/projects.controller.js
const projectService = require('../services/projects.service')

exports.list = async (req, res, next) => {
  try {
    const { page = 1, perPage = 20 } = req.query
    const result = await projectService.list(req.user, { page: +page, perPage: +perPage })
    res.json(result)
  } catch (err) {
    next(err)
  }
}

exports.create = async (req, res, next) => {
  try {
    const project = await projectService.create(req.user, req.body)
    res.status(201).json(project)
  } catch (err) {
    next(err)
  }
}
```

### 6. Service Layer

```javascript
// services/projects.service.js
const { prisma } = require('../config/database')

exports.list = async (user, { page, perPage }) => {
  const where = { ownerId: user.id }
  const [data, total] = await Promise.all([
    prisma.project.findMany({
      where,
      skip: (page - 1) * perPage,
      take: perPage,
      orderBy: { createdAt: 'desc' },
    }),
    prisma.project.count({ where }),
  ])
  return { data, total, page, perPage }
}

exports.create = async (user, body) => {
  const existing = await prisma.project.findUnique({ where: { name: body.name } })
  if (existing) throw AppError.conflict(`Project "${body.name}" already exists`)

  return prisma.project.create({
    data: { ...body, ownerId: user.id },
  })
}
```

### Checklist

- [ ] Express app factory pattern (testable without supertest hacks)
- [ ] Custom error class with typed static constructors
- [ ] Global error handler (no try/catch in every route)
- [ ] Request validation middleware (Joi/Zod)
- [ ] Helmet, CORS, rate limiting in production
- [ ] Structured logging (pino/winston, not console.log)
- [ ] Graceful shutdown (SIGTERM handler)
- [ ] Pagination on all list endpoints
- [ ] Prisma/SQL with parameterized queries (no injection)

## Related Skills

- **backend-senior-engineer** — for the higher-level service architecture and cross-cutting concerns (circuit breakers, service mesh, async messaging) that sit above Express
- **code-reviewer** — when the Express router layer exposes a public API and versioning strategy, error envelope design, and OpenAPI spec matter
- **postgres-pro** — for Prisma schema design, migration strategy, connection pooling with PgBouncer, and query optimization for the service's database layer
- **security-reviewer** — pair on every production-bound Express service to audit JWT validation, rate-limit bypass vectors, and injection surface in route handlers
- **test-engineer** — for Supertest integration test patterns, service-layer unit tests with mocked Prisma, and contract testing against downstream APIs
- **devops-release-engineer** — for Dockerizing the Express app, setting up health-check probes, and configuring graceful shutdown in Kubernetes or ECS
