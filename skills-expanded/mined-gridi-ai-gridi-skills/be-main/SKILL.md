---
name: be-main
description: >
  A skill for developing backend APIs based on test code and OpenAPI specs.
  Writes API implementations that pass tests using TDD methodology.
  Use this skill for backend development, API implementation, or server development requests.
---

## 🌐 Language

> All output documents and user-facing messages must be written in the language specified
> by `crew-config.json → preferences.language`. If not set, default to English.

## 🔧 Project Configuration Reference

> **You must read `crew-config.json` first and operate according to the project settings.**
> - `backend.framework`: Framework to use (NestJS, Express, FastAPI, etc.)
> - `backend.language`: Language (TypeScript, Python, Go, etc.)
> - `backend.orm`: ORM (Prisma, TypeORM, etc.)
> - `backend.testFramework`: Test framework
> - `conventions.idStrategy`: ID strategy (see below)
>
> If `crew-config.json` does not exist, guide the user to run the `/project-init` skill first.

## ⚠️ ID Strategy (crew-config.json → conventions.idStrategy)

> **Follow the `conventions.idStrategy` setting in `crew-config.json`.**
>
> | Setting | Behavior |
> |---------|----------|
> | `uuid` | Use UUID. Generated at the application level, DB column VARCHAR(120) |
> | `auto-increment` | Use DB auto-increment (SERIAL, AUTO_INCREMENT) |
> | `ulid` | Use ULID |
> | `nanoid` | Use nanoid |
>
> **If the setting is missing or `crew-config.json` does not exist, use UUID as the default.**

### UUID Generation Methods

```typescript
// Node.js (crypto module)
import { randomUUID } from 'crypto';
const id = randomUUID();

// Or uuid package
import { v4 as uuidv4 } from 'uuid';
const id = uuidv4();
```

```python
# Python
import uuid
id = str(uuid.uuid4())
```

```go
// Go
import "github.com/google/uuid"
id := uuid.New().String()
```

```java
// Java
import java.util.UUID;
String id = UUID.randomUUID().toString();
```

# Backend Main Developer

Develops API implementations based on test code and OpenAPI specs.

## Workflow

### 1. Verify Input Documents

Receive the following documents/files as input:
- Test code (tests/)
- OpenAPI spec (docs/openapi.yaml)
- Tech spec document

```
Example inputs:
- "Implement the code to pass tests/unit/services/auth.service.test.ts"
- "Implement the /auth/signup API according to the OpenAPI spec"
```

### 2. Project Analysis

1. Understand the existing project structure
2. Identify the framework in use
3. Analyze the architecture pattern
4. Check dependencies

#### Supported Frameworks

| Language | Framework | ORM |
|----------|-----------|-----|
| Node.js | Express, Fastify, NestJS | Prisma, TypeORM |
| Python | FastAPI, Django, Flask | SQLAlchemy, Django ORM |
| Go | Gin, Echo, Fiber | GORM, Ent |
| Java | Spring Boot | JPA, MyBatis |
| Kotlin | Ktor, Spring Boot | Exposed, JPA |

### 3. Code Structure

#### 3.1 Layered Architecture (Recommended)

> Adapt the directory structure to your project's framework and conventions.

```
src/
├── controllers/          # HTTP handlers
│   └── auth.controller.ts
├── services/             # Business logic
│   └── auth.service.ts
├── repositories/         # Data access
│   └── user.repository.ts
├── models/               # Domain models
│   └── user.model.ts
├── dtos/                 # Data transfer objects
│   ├── requests/
│   │   └── signup.request.ts
│   └── responses/
│       └── user.response.ts
├── middlewares/          # Middlewares
│   ├── auth.middleware.ts
│   └── validation.middleware.ts
├── utils/                # Utilities
│   └── crypto.ts
└── config/               # Configuration
    └── database.ts
```

#### 3.2 Controller Implementation

```typescript
// src/controllers/auth.controller.ts
import { Router, Request, Response, NextFunction } from 'express';
import { AuthService } from '@/services/auth.service';
import { SignupRequest } from '@/dtos/requests/signup.request';
import { validateBody } from '@/middlewares/validation.middleware';
import { signupSchema } from '@/schemas/auth.schema';

export class AuthController {
  public router: Router;
  private authService: AuthService;

  constructor(authService: AuthService) {
    this.authService = authService;
    this.router = Router();
    this.initializeRoutes();
  }

  private initializeRoutes() {
    this.router.post(
      '/signup',
      validateBody(signupSchema),
      this.signup.bind(this)
    );
    this.router.post(
      '/login',
      validateBody(loginSchema),
      this.login.bind(this)
    );
  }

  /**
   * POST /auth/signup
   * Sign up
   */
  private async signup(
    req: Request,
    res: Response,
    next: NextFunction
  ) {
    try {
      const dto: SignupRequest = req.body;
      const user = await this.authService.signup(dto);

      // Return DTO directly as per API spec
      res.status(201).json(user);
    } catch (error) {
      next(error);
    }
  }
}
```

#### 3.3 Service Implementation

```typescript
// src/services/auth.service.ts
import { UserRepository } from '@/repositories/user.repository';
import { SignupRequest } from '@/dtos/requests/signup.request';
import { UserResponse } from '@/dtos/responses/user.response';
import { hashPassword, verifyPassword } from '@/utils/crypto';
import { ConflictError } from '@/errors/conflict.error';
import { UnauthorizedError } from '@/errors/unauthorized.error';

export class AuthService {
  constructor(private userRepository: UserRepository) {}

  async signup(dto: SignupRequest): Promise<UserResponse> {
    // 1. Check for duplicate email
    const existingUser = await this.userRepository.findByEmail(dto.email);
    if (existingUser) {
      throw new ConflictError('Email is already registered.');
    }

    // 2. Hash password
    const hashedPassword = await hashPassword(dto.password);

    // 3. Create user
    const user = await this.userRepository.create({
      email: dto.email,
      password: hashedPassword,
    });

    // 4. Convert to response DTO
    return UserResponse.from(user);
  }

  async login(email: string, password: string): Promise<TokenResponse> {
    // 1. Look up user
    const user = await this.userRepository.findByEmail(email);
    if (!user) {
      throw new UnauthorizedError('Email or password is incorrect.');
    }

    // 2. Verify password
    const isValid = await verifyPassword(password, user.password);
    if (!isValid) {
      throw new UnauthorizedError('Email or password is incorrect.');
    }

    // 3. Generate tokens
    const accessToken = this.generateAccessToken(user);
    const refreshToken = this.generateRefreshToken(user);

    return { accessToken, refreshToken };
  }
}
```

#### 3.4 Repository Implementation

```typescript
// src/repositories/user.repository.ts
import { PrismaClient, User } from '@prisma/client';
import { randomUUID } from 'crypto';

export class UserRepository {
  constructor(private prisma: PrismaClient) {}

  async findById(id: string): Promise<User | null> {
    return this.prisma.user.findUnique({
      where: { id },
    });
  }

  async findByEmail(email: string): Promise<User | null> {
    return this.prisma.user.findUnique({
      where: { email },
    });
  }

  async create(data: { email: string; password: string }): Promise<User> {
    // Generate ID according to conventions.idStrategy in crew-config.json
    return this.prisma.user.create({
      data: {
        id: randomUUID(),  // Generate UUID
        ...data,
      },
    });
  }

  async update(id: string, data: Partial<User>): Promise<User> {
    return this.prisma.user.update({
      where: { id },
      data,
    });
  }

  async delete(id: string): Promise<void> {
    await this.prisma.user.delete({
      where: { id },
    });
  }
}
```

> **Prisma schema example**:
> ```prisma
> model User {
>   id        String   @id @db.VarChar(120)  // UUID, VARCHAR(120)
>   email     String   @unique
>   password  String
>   createdAt DateTime @default(now())
>   updatedAt DateTime @updatedAt
> }
> ```

### 4. TDD Development Process

1. **Run tests**: Run existing tests to confirm failures
2. **Implement**: Write the minimum code to pass the tests
3. **Refactor**: Improve the code
4. **Repeat**: Move to the next test

```bash
# Run tests (watch mode)
npm run test:watch

# Run a specific test file
npm run test -- auth.service.test.ts

# Check coverage
npm run test:coverage
```

### 5. Error Handling

#### Custom Error Classes

```typescript
// src/errors/base.error.ts
export abstract class BaseError extends Error {
  abstract statusCode: number;
  abstract code: string;

  constructor(message: string) {
    super(message);
    this.name = this.constructor.name;
  }

  toJSON() {
    return {
      error: {
        code: this.code,
        message: this.message,
      },
    };
  }
}

// src/errors/validation.error.ts
export class ValidationError extends BaseError {
  statusCode = 400;
  code = 'VALIDATION_ERROR';
  details: Array<{ field: string; message: string }>;

  constructor(details: Array<{ field: string; message: string }>) {
    super('The input values are invalid.');
    this.details = details;
  }

  toJSON() {
    return {
      error: {
        code: this.code,
        message: this.message,
        details: this.details,
      },
    };
  }
}
```

#### Error Handler Middleware

```typescript
// src/middlewares/error.middleware.ts
export function errorHandler(
  error: Error,
  req: Request,
  res: Response,
  next: NextFunction
) {
  if (error instanceof BaseError) {
    return res.status(error.statusCode).json(error.toJSON());
  }

  console.error(error);

  return res.status(500).json({
    error: {
      code: 'INTERNAL_ERROR',
      message: 'A server error occurred.',
    },
  });
}
```

### 6. Validation

```typescript
// src/schemas/auth.schema.ts
import { z } from 'zod';

export const signupSchema = z.object({
  email: z.string().email('Please enter a valid email address.'),
  password: z
    .string()
    .min(8, 'Password must be at least 8 characters.')
    .regex(
      /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])/,
      'Password must include uppercase letters, lowercase letters, numbers, and special characters.'
    ),
});

// src/middlewares/validation.middleware.ts
export function validateBody(schema: z.ZodSchema) {
  return (req: Request, res: Response, next: NextFunction) => {
    const result = schema.safeParse(req.body);

    if (!result.success) {
      const details = result.error.errors.map((err) => ({
        field: err.path.join('.'),
        message: err.message,
      }));
      throw new ValidationError(details);
    }

    req.body = result.data;
    next();
  };
}
```

### 7. File Output

```
src/
├── controllers/{domain}.controller.ts
├── services/{domain}.service.ts
├── repositories/{model}.repository.ts
├── dtos/
│   ├── requests/{action}.request.ts
│   └── responses/{model}.response.ts
└── schemas/{domain}.schema.ts
```

## ⛔ Lint Check Required Principle

> **Warning**: After writing/modifying code, you must run a lint check, fix all errors, and only then finish.

### Required Execution Order

```
1. Code writing/modification complete ──────────────── ✅
           │
           ▼
2. Run lint auto-fix (--fix) ───────────────────────── ✅ Required
           │
           ├── All errors fixed ──▶ Go to step 3
           │
           └── Unfixed errors remain ──▶ Fix manually, then re-run step 2
           │
           ▼
3. Lint check (confirm 0 errors) ───────────────────── ✅ Required
           │
           ▼
4. Run tests ───────────────────────────────────────── ✅ Required
           │
           ▼
5. Task complete
```

### Lint Commands

> **Check `crew-config.json` for project-specific lint commands.** If not configured, use the defaults below.

### Lint Commands by Framework

| Framework | Lint Auto-fix | Lint Check |
|-----------|--------------|------------|
| Node.js (ESLint) | `npm run lint -- --fix` | `npm run lint` |
| Python (Ruff) | `ruff check --fix .` | `ruff check .` |
| Python (Black) | `black .` | `black --check .` |
| Go (golangci-lint) | `golangci-lint run --fix` | `golangci-lint run` |
| Java (Checkstyle) | - | `./gradlew checkstyleMain` |
| Kotlin (ktlint) | `ktlint -F` | `ktlint` |

### Handling Errors Not Auto-fixable

Errors not resolved by `--fix` **must be fixed manually**:

```typescript
// ❌ Not auto-fixable: unused variable
const unusedVar = 'hello';  // ESLint: 'unusedVar' is defined but never used

// ✅ Fix manually: remove the variable or use it
// Option 1: Remove
// Option 2: Add usage
console.log(unusedVar);
```

### Completion Criteria

- ⛔ **Task cannot be completed if lint errors remain**
- ✅ Task is complete only when the project's lint command shows 0 errors

---

## Development Principles

> **Follow the conventions defined in `crew-config.json`.** The principles below are universal recommendations.
> For framework-specific patterns, see `crew-config.json → backend.framework` and the corresponding reference files.

### 1. ID Strategy
- Follow `conventions.idStrategy` in `crew-config.json`
- If not configured, use UUID as the default (see ID Strategy section above)

### 2. Lint Check Required
- Always run lint auto-fix after writing code (check `crew-config.json` for lint commands)
- Manually fix errors that are not auto-fixable
- Task can only be completed with 0 lint errors

### 3. Tests First
- Always check tests first
- Maintain test coverage

### 4. Single Responsibility
- Each class/module has only one responsibility
- Clear role separation between layers

### 5. Dependency Injection
- Use constructor injection (or framework-appropriate DI)
- Ensure testability

### 6. API Spec Compliance
- Follow the response format defined in the API spec
- Standardize error codes

## References

- Architecture guide: [references/architecture-guide.md](references/architecture-guide.md)
- Security guide: [references/security-guide.md](references/security-guide.md)

## Framework-Specific References

Consult the reference that matches your project's `crew-config.json → backend.framework`:

| Framework | Reference |
|-----------|-----------|
| NestJS | [references/nestjs-patterns.md](references/nestjs-patterns.md) |
| Express | [references/express-patterns.md](references/express-patterns.md) |
| FastAPI | [references/fastapi-patterns.md](references/fastapi-patterns.md) |
| Django | [references/django-patterns.md](references/django-patterns.md) |
| Spring Boot | [references/spring-boot-patterns.md](references/spring-boot-patterns.md) |
| Gin | [references/gin-patterns.md](references/gin-patterns.md) |
