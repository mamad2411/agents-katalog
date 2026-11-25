# Backend Development Skill

Guidelines for building clean, secure, and scalable backend code in Rent4U.

## Stack

- **Runtime:** Node.js (Bun compatible)
- **Framework:** Express 5
- **ORM:** Prisma 7
- **Database:** SQLite (local dev) → PostgreSQL/MySQL (production)
- **Auth:** JWT (access + refresh tokens)
- **Encryption:** AES-256-GCM for sensitive data
- **Validation:** Zod
- **Language:** JavaScript (CommonJS) with JSDoc type hints

## Architecture

Module-based architecture. Each domain is a self-contained module.

```
backend/src/
├── app.js                      # Express app setup + server start
├── config/
│   └── index.js                # Validated env vars + constants
├── modules/
│   ├── auth/
│   │   ├── auth.controller.js  # Request/response handling
│   │   ├── auth.service.js     # Business logic
│   │   ├── auth.routes.js      # Route definitions
│   │   └── auth.validator.js   # Zod schemas
│   ├── user/
│   ├── house/
│   ├── role/
│   └── payment/
│       └── gateways/
│           ├── base.gateway.js     # Abstract gateway interface
│           └── sample.gateway.js   # Sample implementation
├── middlewares/
│   ├── authenticate.js         # JWT verification
│   ├── authorize.js            # Role-based access
│   ├── encryptResponse.js      # Field-level encryption
│   ├── errorHandler.js         # Global error handler
│   ├── rateLimiter.js          # Request throttling
│   └── requestLogger.js        # Structured request logging
└── utils/
    ├── prisma.js               # Prisma client singleton
    ├── crypto.js               # AES-256-GCM encrypt/decrypt
    ├── logger.js               # Winston logger
    ├── errors.js               # Custom error classes
    └── response.js             # Standardized response format
```

## Principles

### Separation of Concerns
- **Controller:** Parses request, calls service, sends response. No business logic.
- **Service:** Business logic, database calls, orchestration. No HTTP concerns.
- **Validator:** Zod schemas for request validation. Fail fast.
- **Routes:** Maps HTTP verbs + paths to controllers + middleware.

### Single Responsibility
Each function does ONE thing. If a function needs a comment explaining what it does, split it.

### Dependency Direction
Routes → Controllers → Services → Prisma. Never skip a layer.

## Security Rules

### Authentication
- Access token: short-lived (15min), sent in `Authorization: Bearer` header
- Refresh token: long-lived (7d), stored in HTTP-only secure cookie
- Refresh tokens stored in database for revocation
- On logout: revoke refresh token in DB + clear cookie
- Passwords: bcrypt with cost factor 12+

### Encryption (AES-256-GCM)
- Encrypt PII fields before sending in responses (email, phone, address)
- Never encrypt passwords (bcrypt hashes are already one-way)
- IV generated per encryption, prepended to ciphertext
- Auth tag appended to ciphertext for integrity verification

### Input Validation
- Validate ALL input at the boundary (controller level) using Zod schemas
- Strip unknown fields (`z.strict()`)
- Sanitize string inputs (trim, normalize email)
- Return 400 with field-level errors on validation failure

### Rate Limiting
- Global: 100 requests/15min per IP
- Auth endpoints: 5 requests/15min per IP
- Use `express-rate-limit`

### HTTP Security
- Helmet for security headers
- CORS with explicit origin whitelist
- Content-Security-Policy headers
- No `X-Powered-By` header

### Database
- Parameterized queries only (Prisma handles this)
- No raw SQL with user input
- Soft deletes for user-facing data
- Never expose internal IDs or DB structure in responses

## Code Style

### Naming
- Files: `kebab-case.js` or `camelCase.js` (match existing convention)
- Variables/functions: `camelCase`
- Constants: `UPPER_SNAKE_CASE`
- Classes/Constructors: `PascalCase`
- Database models: `PascalCase` (Prisma convention)

### Functions
```js
// Good: clear name, single responsibility, early returns
async function findUserByEmail(email) {
  const user = await prisma.user.findUnique({ where: { email } });
  if (!user) throw new NotFoundError('User not found');
  return user;
}

// Bad: vague name, multiple responsibilities
async function doStuff(id, data) {
  // ... 50 lines doing multiple things
}
```

### Error Handling
```js
// Use custom error classes, not generic throws
throw new ValidationError('Email already registered');
throw new NotFoundError('House not found');
throw new UnauthorizedError('Invalid credentials');
throw new ForbiddenError('Insufficient permissions');
```

### Response Format
```js
// Success
res.status(200).json(successResponse(data, 'User fetched'));
res.status(201).json(successResponse(data, 'User created'));

// Error (handled by global error handler)
res.status(400).json(errorResponse('Validation failed', errors));
```

### Environment Variables
- All env vars validated on startup via config module
- Never access `process.env` outside `config/index.js`
- Required vars crash the app with a clear error message

### Database Provider Abstraction
- SQLite for local development (provider = "sqlite")
- PostgreSQL for staging/production (provider = "postgresql")
- Switch via `DATABASE_PROVIDER` env var + Prisma schema
- Never use provider-specific raw SQL
- Test migrations against both providers before deploying

## Conventions

### Route Registration
```js
// In app.js
app.use('/api/v1/auth', authRoutes);
app.use('/api/v1/users', userRoutes);
app.use('/api/v1/houses', houseRoutes);
app.use('/api/v1/payments', paymentRoutes);
```

### Middleware Chain
```
request → rateLimiter → requestLogger → helmet → cors → authenticate → authorize → validator → controller → encryptResponse → response
```

### Controller Pattern
```js
async function createUser(req, res, next) {
  try {
    const validated = userCreateSchema.parse(req.body);
    const user = await userService.create(validated);
    res.status(201).json(successResponse(user, 'User created'));
  } catch (err) {
    next(err);
  }
}
```

### Service Pattern
```js
async function create(data) {
  const existing = await prisma.user.findUnique({ where: { email: data.email } });
  if (existing) throw new ValidationError('Email already registered');

  const hashedPassword = await bcrypt.hash(data.password, 12);
  return prisma.user.create({
    data: { ...data, password: hashedPassword },
    select: { id: true, name: true, email: true, createdAt: true },
  });
}
```

### Payment Gateway Pattern
```js
// base.gateway.js — interface contract
class BaseGateway {
  async createPayment(amount, currency, metadata) { throw new Error('Not implemented'); }
  async verifyPayment(paymentId) { throw new Error('Not implemented'); }
  async refundPayment(paymentId, amount) { throw new Error('Not implemented'); }
  async getPaymentStatus(paymentId) { throw new Error('Not implemented'); }
}

// sample.gateway.js — stub for local dev
class SampleGateway extends BaseGateway { /* ... */ }

// Factory: pick gateway based on env
function createGateway(provider) { /* ... */ }
```

## Testing Conventions

- One test file per module: `<module>.test.js`
- Use AAA pattern (Arrange, Act, Assert)
- Factory helpers for test data
- Clean database between tests
- Mock external services (payment gateways, email)
- See `backend-testing.md` skill for full testing guidelines

## Migration Guidelines

- Prisma migrations must work with both SQLite and PostgreSQL
- Test: `npx prisma migrate dev --name <name>`
- Never modify existing migration files — create new ones
- Always include rollback plan in migration PRs

## Logging

- Use Winston with structured JSON output
- Levels: error, warn, info, http, debug
- Log: requests, auth events, errors, business events
- Never log: passwords, tokens, encryption keys, PII
- Request logging via Morgan → Winston stream
