---
name: aws-lambda-typescript
description: AWS Lambda development with TypeScript. Use when writing Lambda handlers, bundling with esbuild, using AWS SDK v3/Powertools, strict typing or optimizing Node.js Lambda performance.
---

# AWS Lambda TypeScript

Skill para desarrollo de funciones Lambda en TypeScript: handlers, bundling con esbuild, AWS SDK v3, Powertools, tipado estricto, manejo de errores, testing y mejores prácticas de rendimiento.

## Principios fundamentales

- Un handler, una responsabilidad. Evitar Lambdas monolíticos.
- Separar lógica de negocio del handler. El handler solo parsea el evento, invoca la lógica y formatea la respuesta.
- Usar AWS Lambda Powertools para TypeScript: Logger, Tracer, Metrics, Idempotency, Parameters.
- AWS SDK v3 obligatorio (modular, tree-shakeable). Nunca usar SDK v2.
- Tipado estricto: `strict: true` en tsconfig, no usar `any`.
- Inicializar clientes AWS fuera del handler (reutilización en warm starts).

## Estructura de proyecto recomendada

```
functions/
├── mi-funcion/
│   ├── handler.ts          # Entry point del Lambda
│   ├── service.ts          # Lógica de negocio
│   ├── repository.ts       # Acceso a datos
│   ├── types.ts            # Interfaces y tipos
│   └── errors.ts           # Errores custom
├── shared/
│   ├── middleware.ts
│   ├── constants.ts
│   └── types.ts
├── tests/
│   ├── unit/
│   │   ├── service.test.ts
│   │   └── handler.test.ts
│   └── integration/
│       └── api.test.ts
├── tsconfig.json
├── package.json
└── vitest.config.ts
```

## Handler con Powertools (patrón recomendado)

```typescript
import { Logger } from '@aws-lambda-powertools/logger';
import { Tracer } from '@aws-lambda-powertools/tracer';
import { Metrics, MetricUnit } from '@aws-lambda-powertools/metrics';
import { DynamoDBClient } from '@aws-sdk/client-dynamodb';
import { DynamoDBDocumentClient, QueryCommand, PutCommand } from '@aws-sdk/lib-dynamodb';
import type { APIGatewayProxyEventV2, APIGatewayProxyResultV2, Context } from 'aws-lambda';

const logger = new Logger({ serviceName: 'mi-servicio' });
const tracer = new Tracer({ serviceName: 'mi-servicio' });
const metrics = new Metrics({ namespace: 'MiApp', serviceName: 'mi-servicio' });

// Clientes AWS fuera del handler (warm start reuse)
const ddbClient = tracer.captureAWSv3Client(new DynamoDBClient({}));
const docClient = DynamoDBDocumentClient.from(ddbClient);
const TABLE_NAME = process.env.TABLE_NAME!;

export const handler = async (
  event: APIGatewayProxyEventV2,
  context: Context
): Promise<APIGatewayProxyResultV2> => {
  logger.addContext(context);

  try {
    const method = event.requestContext.http.method;
    const path = event.rawPath;

    if (method === 'GET' && path === '/items') {
      return await listItems();
    }
    if (method === 'POST' && path === '/items') {
      return await createItem(JSON.parse(event.body ?? '{}'));
    }

    return { statusCode: 404, body: JSON.stringify({ error: { code: 'NOT_FOUND', message: 'Route not found' } }) };
  } catch (error) {
    logger.error('Unexpected error', { error });
    return { statusCode: 500, body: JSON.stringify({ error: { code: 'INTERNAL_ERROR', message: 'Internal server error' } }) };
  }
};
```

## Validación con Zod

```typescript
import { z } from 'zod';

const ItemCreateSchema = z.object({
  name: z.string().min(1).max(255).trim(),
  description: z.string().max(1000).default(''),
  price: z.number().positive(),
  category: z.string().regex(/^[a-z-]+$/),
});

type ItemCreate = z.infer<typeof ItemCreateSchema>;

function validateInput<T>(schema: z.ZodSchema<T>, data: unknown): T {
  const result = schema.safeParse(data);
  if (!result.success) {
    throw new AppError('VALIDATION_ERROR', result.error.issues.map(i => i.message).join(', '), 400);
  }
  return result.data;
}
```

## Manejo de errores tipado

```typescript
class AppError extends Error {
  constructor(
    public readonly code: string,
    message: string,
    public readonly statusCode: number = 400
  ) {
    super(message);
    this.name = 'AppError';
  }
}

function errorResponse(error: unknown): APIGatewayProxyResultV2 {
  if (error instanceof AppError) {
    logger.warn('App error', { code: error.code, message: error.message });
    return {
      statusCode: error.statusCode,
      body: JSON.stringify({ error: { code: error.code, message: error.message } }),
    };
  }
  logger.error('Unexpected error', { error });
  return {
    statusCode: 500,
    body: JSON.stringify({ error: { code: 'INTERNAL_ERROR', message: 'Internal server error' } }),
  };
}
```

## Idempotencia con Powertools

```typescript
import { IdempotencyConfig, makeIdempotent } from '@aws-lambda-powertools/idempotency';
import { DynamoDBPersistenceLayer } from '@aws-lambda-powertools/idempotency/dynamodb';

const persistenceStore = new DynamoDBPersistenceLayer({ tableName: process.env.IDEMPOTENCY_TABLE! });
const idempotencyConfig = new IdempotencyConfig({ expiresAfterSeconds: 3600 });

const processOrder = makeIdempotent(
  async (order: Order): Promise<OrderResult> => {
    const result = await paymentService.charge(order);
    return { status: 'processed', transactionId: result.id };
  },
  { persistenceStore, config: idempotencyConfig }
);
```

## Bundling con esbuild

```json
// tsconfig.json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "esModuleInterop": true,
    "outDir": "dist",
    "sourceMap": true,
    "declaration": true
  },
  "include": ["functions/**/*.ts"],
  "exclude": ["node_modules", "dist", "**/*.test.ts"]
}
```

Con CDK `NodejsFunction` el bundling es automático:
```typescript
new NodejsFunction(this, 'Handler', {
  entry: 'functions/mi-funcion/handler.ts',
  handler: 'handler',
  runtime: Runtime.NODEJS_20_X,
  bundling: {
    minify: true,
    sourceMap: true,
    externalModules: ['@aws-sdk/*'], // Ya incluido en el runtime
  },
});
```

## Testing con Vitest

```typescript
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { handler } from './handler';

// Mock DynamoDB
vi.mock('@aws-sdk/lib-dynamodb', () => ({
  DynamoDBDocumentClient: { from: vi.fn(() => mockDocClient) },
  QueryCommand: vi.fn(),
  PutCommand: vi.fn(),
}));

const mockDocClient = { send: vi.fn() };

describe('handler', () => {
  beforeEach(() => { vi.clearAllMocks(); });

  it('should list items', async () => {
    mockDocClient.send.mockResolvedValue({ Items: [{ name: 'Test' }] });
    const event = makeApiEvent('GET', '/items');
    const result = await handler(event, mockContext);
    expect(result.statusCode).toBe(200);
    expect(JSON.parse(result.body as string).items).toHaveLength(1);
  });

  it('should return 400 for invalid input', async () => {
    const event = makeApiEvent('POST', '/items', { name: '', price: -1 });
    const result = await handler(event, mockContext);
    expect(result.statusCode).toBe(400);
  });
});
```

## NestJS en Lambda

Para APIs complejas con dependency injection, modular architecture y ecosistema rico, NestJS es una opción viable en Lambda.

### Estructura NestJS Lambda

```
my-nestjs-lambda/
├── src/
│   ├── app.module.ts
│   ├── main.ts              # Entry point local
│   ├── lambda.ts            # Entry point Lambda
│   └── modules/
│       └── api/
├── package.json
├── tsconfig.json
└── serverless.yml
```

### Entry point Lambda con NestJS

```typescript
// lambda.ts
import { NestFactory } from '@nestjs/core';
import { ExpressAdapter } from '@nestjs/platform-express';
import serverlessExpress from '@codegenie/serverless-express';
import { Context, Handler } from 'aws-lambda';
import express from 'express';
import { AppModule } from './src/app.module';

let cachedServer: Handler;

async function bootstrap(): Promise<Handler> {
  const expressApp = express();
  const adapter = new ExpressAdapter(expressApp);
  const nestApp = await NestFactory.create(AppModule, adapter);
  await nestApp.init();
  return serverlessExpress({ app: expressApp });
}

export const handler: Handler = async (event: any, context: Context) => {
  if (!cachedServer) {
    cachedServer = await bootstrap();
  }
  return cachedServer(event, context);
};
```

### Comparativa de enfoques

| Aspecto | Raw TypeScript | NestJS |
|---|---|---|
| Cold start | < 100ms | < 500ms |
| Bundle size | < 50KB | 100KB+ |
| Caso de uso | Microservicios, handlers simples | APIs complejas, enterprise, DI |
| Complejidad | Baja | Media |
| Memoria recomendada | 256MB | 512MB |
| Timeout recomendado | 3-10s | 10-30s |

### Cuándo usar NestJS vs Raw TypeScript

- **NestJS**: APIs con múltiples módulos, dependency injection, middleware complejo, validación con class-validator, guards, interceptors.
- **Raw TypeScript**: Handlers de eventos, microservicios simples, procesadores SQS/SNS, funciones con requisitos estrictos de cold start.

## Rendimiento y Cold Start

### Estrategias de optimización

| Estrategia | Impacto | Complejidad |
|---|---|---|
| Clientes SDK fuera del handler | Alto | Bajo |
| Tree shaking con esbuild | Alto | Bajo |
| Lazy loading de dependencias pesadas | Medio | Bajo |
| Minificación del bundle | Medio | Bajo |
| Aumentar memoria (más CPU) | Medio | Bajo |
| Excluir `@aws-sdk/*` del bundle | Medio | Bajo |
| Provisioned Concurrency | Alto | Medio |

### Lazy loading

```typescript
// ✅ Lazy loading para dependencias pesadas que no siempre se usan
let heavyLib: typeof import('heavy-lib') | undefined;

const getHeavyLib = async () => {
  if (!heavyLib) {
    heavyLib = await import('heavy-lib');
  }
  return heavyLib;
};
```

### Reglas de rendimiento

- Inicializar clientes SDK v3 fuera del handler (global scope) para reutilización en warm starts.
- Usar `@aws-sdk/client-xxx` individual, nunca el paquete completo `aws-sdk`.
- Memory: empezar con 256MB (raw) o 512MB (NestJS), medir con Powertools Tracer y ajustar.
- Timeout: 2x el p99 observado, mínimo 10s para APIs.
- `minify: true` y `sourceMap: true` en bundling para reducir tamaño y mantener debugging.
- Excluir `@aws-sdk/*` del bundle (ya está en el runtime de Lambda).
- Usar Provisioned Concurrency solo si p99 cold start es inaceptable.
- Node.js 20.x ofrece el mejor rendimiento actual.

### Límites de Lambda a tener en cuenta

- Deployment package: 250MB descomprimido (50MB comprimido)
- Memoria: 128MB a 10GB
- Timeout: 15 minutos máximo
- Ejecuciones concurrentes: 1000 por defecto (ajustable)
- Variables de entorno: 4KB total

## Variables de entorno recomendadas

```
POWERTOOLS_SERVICE_NAME=mi-servicio
POWERTOOLS_LOG_LEVEL=INFO
POWERTOOLS_METRICS_NAMESPACE=MiApp
TABLE_NAME=mi-tabla
STAGE=dev
NODE_OPTIONS=--enable-source-maps
```

## Anti-patrones a evitar

- ❌ Usar `any` en lugar de tipos concretos.
- ❌ AWS SDK v2 (`aws-sdk`) en lugar de SDK v3 modular.
- ❌ `console.log` en lugar de Powertools Logger.
- ❌ Lógica de negocio directamente en el handler.
- ❌ Crear clientes DynamoDB/S3/SQS dentro del handler.
- ❌ No validar input del evento (confiar en el cliente).
- ❌ Capturar errores sin logging ni re-throw.
- ❌ Hardcodear nombres de recursos o ARNs.
- ❌ `strict: false` en tsconfig.
- ❌ No tener tests unitarios.

## Despliegue

### Con Serverless Framework

```yaml
service: my-typescript-api
provider:
  name: aws
  runtime: nodejs20.x
functions:
  api:
    handler: dist/handler.handler
    events:
      - http:
          path: /{proxy+}
          method: ANY
```

### Con SAM

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31
Resources:
  ApiFunction:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: dist/
      Handler: handler.handler
      Runtime: nodejs20.x
      Events:
        ApiEvent:
          Type: Api
          Properties:
            Path: /{proxy+}
            Method: ANY
```

## Checklist de revisión Lambda TypeScript

- [ ] Handler delgado, lógica en service/repository.
- [ ] Powertools configurado (Logger, Tracer, Metrics).
- [ ] Validación de input con Zod o similar.
- [ ] Manejo de errores tipado con respuestas consistentes.
- [ ] SDK v3 con clientes inicializados fuera del handler.
- [ ] `strict: true` en tsconfig.json.
- [ ] Bundling con esbuild (minify + sourceMap).
- [ ] Tests unitarios con Vitest y mocks.
- [ ] Variables de entorno para configuración.
- [ ] Idempotencia implementada donde aplica.
- [ ] Cold start medido y optimizado según enfoque (raw vs NestJS).
- [ ] Bundle size verificado (< 50KB raw, < 150KB NestJS).
- [ ] Lazy loading para dependencias pesadas opcionales.
