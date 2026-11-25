---
name: tpl-backend-serverless-lambda
description: Template do pack (backend/06-serverless-lambda.md). Orienta o agente em APIs, servicos e arquitetura backend alinhado a esse contexto.
metadata:
  version: 1.0.0
  source_template: backend/06-serverless-lambda.md
  generated_by: install_pack_templates_as_claude_skills
---

# PROJECT: Serverless API (AWS Lambda + TypeScript)

Skill gerado a partir do pack `templates-claude-code`. Arquivo de origem: `backend/06-serverless-lambda.md`. Use como baseline e adapte ao projeto antes de mudancas grandes.

## Conteudo do template

## STACK

| Technology | Version | Purpose |
|------------|---------|---------|
| Node.js | 22.x (Lambda) | Runtime |
| TypeScript | 5.4+ | Language |
| SST | v3 | Infrastructure as code + local dev |
| AWS Lambda | — | Compute |
| API Gateway v2 (HTTP) | — | HTTP trigger |
| DynamoDB | — | Primary database |
| AWS SDK v3 | 3.x | DynamoDB DocumentClient |
| Zod | 3.x | Input validation |
| AWS Lambda Powertools | 2.x | Logger, Tracer, Metrics middleware |
| Jest | 29.x | Unit tests |
| esbuild | — | Bundler (via SST) |

---

## PROJECT STRUCTURE

```
sst.config.ts                # SST stack definitions (infra as code)
packages/
└── functions/
    ├── package.json
    ├── tsconfig.json
    ├── src/
    │   ├── handlers/
    │   │   ├── users/
    │   │   │   ├── create.ts    # POST /users
    │   │   │   ├── get.ts       # GET /users/{id}
    │   │   │   ├── list.ts      # GET /users
    │   │   │   └── delete.ts    # DELETE /users/{id}
    │   │   └── auth/
    │   │       ├── login.ts
    │   │       └── refresh.ts
    │   ├── services/
    │   │   └── users.service.ts # Business logic
    │   ├── repositories/
    │   │   └── users.repository.ts  # DynamoDB queries
    │   ├── middleware/
    │   │   ├── auth.ts          # JWT verification (Powertools middleware)
    │   │   └── validate.ts      # Zod validation middleware
    │   ├── lib/
    │   │   ├── dynamo.ts        # DocumentClient singleton
    │   │   ├── jwt.ts           # Sign/verify tokens
    │   │   └── response.ts      # Standard API Gateway response helpers
    │   └── types/
    │       └── index.ts
    └── tests/
        ├── unit/
        │   └── users.service.test.ts
        └── integration/
            └── users.handler.test.ts
```

---

## ARCHITECTURE RULES

- **Handler → Service → Repository** — strictly enforced even in Lambda
- Each Lambda handler is ONE file with ONE exported `handler` function
- Handler files: import middleware, validate input, call service, return response helper
- Services contain business logic — no AWS SDK imports
- Repositories contain ALL DynamoDB access — no business logic
- Use **Powertools middleware** for every handler (structured logging, tracing, error handling)
- Never import the entire AWS SDK — always use specific clients: `@aws-sdk/client-dynamodb`
- Shared code lives in `packages/core/` (separate SST package) to avoid duplicating across lambdas

---

## LAMBDA RULES

### Cold Start Optimization

```typescript
// ✅ Do: initialize clients OUTSIDE the handler (module scope)
// Runs once per container, not per invocation
const docClient = new DynamoDBDocumentClient(new DynamoDBClient({}))
const userRepo = new UserRepository(docClient)

export const handler = async (event: APIGatewayProxyEventV2) => {
  // handler code here — docClient already initialized
}

// ❌ Don't: initialize inside handler (cold start on every call)
export const handler = async (event: APIGatewayProxyEventV2) => {
  const docClient = new DynamoDBDocumentClient(new DynamoDBClient({})) // wrong
}
```

### Bundle Size Rules

- Target < 1MB per function (unzipped)
- Use `esbuild` tree-shaking — import only what you need from AWS SDK v3
- Mark `aws-sdk` as external in bundler (provided by Lambda runtime)
- Do NOT bundle fonts, images, or data files — use S3 or DynamoDB
- Run `sst analyze` to check bundle sizes before deploy

### Powertools Middleware Pattern

```typescript
// src/handlers/users/get.ts
import { APIGatewayProxyEventV2, APIGatewayProxyResultV2 } from 'aws-lambda'
import { Logger } from '@aws-lambda-powertools/logger'
import { Tracer } from '@aws-lambda-powertools/tracer'
import { Metrics, MetricUnits } from '@aws-lambda-powertools/metrics'
import { injectLambdaContext } from '@aws-lambda-powertools/logger/middleware'
import { captureLambdaHandler } from '@aws-lambda-powertools/tracer/middleware'
import middy from '@middy/core'
import { z } from 'zod'
import { UserService } from '../../services/users.service'
import { ok, notFound, badRequest } from '../../lib/response'

const logger = new Logger({ serviceName: 'users-api', logLevel: 'INFO' })
const tracer = new Tracer({ serviceName: 'users-api' })
const metrics = new Metrics({ namespace: 'UsersAPI', serviceName: 'users-api' })

const paramsSchema = z.object({
  id: z.string().uuid('Invalid user ID format'),
})

const lambdaHandler = async (event: APIGatewayProxyEventV2): Promise<APIGatewayProxyResultV2> => {
  const parsed = paramsSchema.safeParse(event.pathParameters)
  if (!parsed.success) {
    return badRequest(parsed.error.flatten())
  }

  const user = await UserService.getById(parsed.data.id)
  if (!user) {
    logger.warn('User not found', { userId: parsed.data.id })
    return notFound('User not found')
  }

  metrics.addMetric('UserFetched', MetricUnits.Count, 1)
  logger.info('User fetched', { userId: user.id })
  return ok(user)
}

export const handler = middy(lambdaHandler)
  .use(injectLambdaContext(logger, { clearState: true }))
  .use(captureLambdaHandler(tracer))
```

### Standard Response Helpers

```typescript
// src/lib/response.ts
import type { APIGatewayProxyResultV2 } from 'aws-lambda'

function json(statusCode: number, body: unknown): APIGatewayProxyResultV2 {
  return {
    statusCode,
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  }
}

export const ok = (data: unknown) => json(200, { data })
export const created = (data: unknown) => json(201, { data })
export const badRequest = (details: unknown) => json(400, { error: 'Bad Request', details })
export const unauthorized = () => json(401, { error: 'Unauthorized' })
export const forbidden = () => json(403, { error: 'Forbidden' })
export const notFound = (msg: string) => json(404, { error: msg })
export const internalError = () => json(500, { error: 'Internal Server Error' })
```

### IAM Least Privilege — SST Stack

```typescript
// sst.config.ts — define explicit permissions, never use AdministratorAccess
const usersTable = new sst.aws.Dynamo('UsersTable', {
  fields: { pk: 'string', sk: 'string' },
  primaryIndex: { hashKey: 'pk', rangeKey: 'sk' },
})

const getUserFn = new sst.aws.Function('GetUser', {
  handler: 'packages/functions/src/handlers/users/get.handler',
  environment: {
    USERS_TABLE_NAME: usersTable.name,
    JWT_SECRET: new sst.Secret('JwtSecret').value,
  },
  permissions: [
    // Only the actions this function needs
    { actions: ['dynamodb:GetItem'], resources: [usersTable.arn] },
  ],
})
```

### Environment Variables

- All secrets via SST Secrets (backed by SSM Parameter Store) — **never** in env vars directly
- Access: `Resource.JwtSecret.value` in SST v3 (type-safe binding)
- Non-secret config: SST `environment` object (becomes Lambda env var)

---

## ROUTING TABLE

| Trigger | Method | Route | Auth | Handler |
|---------|--------|-------|------|---------|
| Register | POST | `/users/register` | Public | handlers/auth/register.handler |
| Login | POST | `/auth/login` | Public | handlers/auth/login.handler |
| Refresh token | POST | `/auth/refresh` | Refresh token | handlers/auth/refresh.handler |
| Get user | GET | `/users/{id}` | Bearer JWT | handlers/users/get.handler |
| List users | GET | `/users` | Bearer + Admin | handlers/users/list.handler |
| Create user | POST | `/users` | Bearer + Admin | handlers/users/create.handler |
| Update user | PATCH | `/users/{id}` | Bearer + Admin | handlers/users/update.handler |
| Delete user | DELETE | `/users/{id}` | Bearer + Admin | handlers/users/delete.handler |
| Health | GET | `/health` | Public | handlers/health.handler |

---

## QUALITY GATES

Before deploying, verify ALL of the following:

- [ ] `npx tsc --noEmit` passes across all packages
- [ ] `jest --runInBand` passes (Lambda tests often can't run in parallel)
- [ ] Bundle size < 1MB per function: `sst analyze`
- [ ] No hardcoded secrets — all via `sst.Secret` or environment vars
- [ ] Each function's IAM permissions are minimal (least privilege)
- [ ] `logger.info/warn/error` used (not `console.log`) for structured logs
- [ ] X-Ray tracing enabled via Powertools tracer
- [ ] Environment variable access validated at startup (Zod parse of `process.env`)
- [ ] DynamoDB client initialized outside handler (module scope)
- [ ] Error responses use helper functions (`badRequest`, `internalError`) — no manual `statusCode`

---

## FORBIDDEN

- **NEVER** use `AdministratorAccess` IAM policy — define specific actions + resources
- **NEVER** store secrets as plaintext Lambda environment variables — use SST Secrets → SSM
- **NEVER** initialize AWS clients inside the handler function — only at module scope
- **NEVER** `console.log` in handlers — use Powertools `Logger`
- **NEVER** bundle test files into the Lambda package
- **NEVER** use `@aws-sdk/client-dynamodb` directly in handlers — go through repository layer
- **NEVER** return raw AWS SDK error messages to clients — map to user-friendly messages
- **NEVER** use memory > 1792MB without benchmarking (cost increases, not always faster)
- **NEVER** set Lambda timeout > 30s for API endpoints (API Gateway max is 29s)
- **NEVER** mix SST v2 and v3 APIs — they are incompatible
