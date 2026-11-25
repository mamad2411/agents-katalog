---
name: backend-typescript
description: "Use when building or modifying backend APIs with TypeScript and Express. Covers project structure, strict TypeScript config, Express routes and middleware, Zod validation, error handling patterns, testing with Vitest, and linting with Biome. Also use when working with files under src/routes/, src/middleware/, src/schemas/, src/config/, tsconfig.json, or biome.json."
---

# Backend com TypeScript + Express

## Estrutura de diretórios

```
src/
├── index.ts              # Entry point (app.listen)
├── config/
│   └── env.ts            # Variáveis de ambiente validadas com Zod
├── routes/
│   ├── webhook.routes.ts # Rotas agrupadas por domínio
│   └── job.routes.ts
├── schemas/
│   └── *.schema.ts       # Zod schemas + tipos inferidos
├── middleware/
│   ├── error-handler.ts  # Middleware global de erro (500)
│   └── not-found.ts      # Middleware 404
└── types/
    └── index.ts          # Tipos compartilhados (evitar quando possível)
```

**Separação de concerns:** cada arquivo tem exatamente uma responsabilidade. Routes só roteiam, schemas só validam, middleware só intercepta.

## TypeScript Strict

### tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "noFallthroughCasesInSwitch": true,
    "noImplicitOverride": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "isolatedModules": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "outDir": "dist",
    "rootDir": "src",
    "declaration": true,
    "sourceMap": true
  },
  "include": ["src"]
}
```

### Regras

- **Sem `any`** — usar `z.infer` para tipos de payload, `unknown` + type guard quando necessário
- **Sem `as` casts** — preferir type guards, `satisfies`, ou declarar tipo explícito
- **Sem `!` non-null assertions** — usar early return, optional chaining (`?.`), ou fallback com `??`
- **Prefira `interface` para objetos públicos**, `type` para uniões e utilitários

## Express Setup

```ts
import express from "express";
import type { ErrorRequestHandler, RequestHandler } from "express";

const app = express();

app.use(express.json());          // body parser
app.use("/api", apiRouter);       // rotas modulares
app.use(notFoundHandler);         // 404 (depois das rotas)
app.use(errorHandler);            // 500 (sempre por último)

app.listen(PORT, () => {
  console.log(`Server running on :${PORT}`);
});
```

### Tipagem de handlers

```ts
import type { RequestHandler, ErrorRequestHandler } from "express";

// Handler normal — sempre tipar req.params se usar
const getById: RequestHandler<{ id: string }> = async (req, res) => {
  // ...
};

// Error handler — 4 parâmetros obrigatórios (mesmo que _next não usado)
export const errorHandler: ErrorRequestHandler = (err, _req, res, _next) => {
  console.error(err);
  res.status(500).json({ error: "Internal server error" });
};
```

**Atenção:** em handlers assíncronos, erros não capturados precisam ser tratados. Use `try/catch` ou um wrapper como `express-async-errors`.

## Routes

### Padrão

```ts
import { Router } from "express";
import { mySchema } from "../schemas/my.schema.js";

const router = Router();

router.post("/resource", async (req, res) => {
  const parsed = mySchema.safeParse(req.body);

  if (!parsed.success) {
    res.status(400).json({
      error: "Invalid payload",
      details: parsed.error.flatten().fieldErrors,
    });
    return; // sempre return após res.json() para parar a execução
  }

  const result = await process(parsed.data);
  res.status(201).json(result);
});

export { router as myRouter };
```

**Sempre usar `return` explícito após `res.json()`/`res.status()`** para evitar chamar dois `res` no mesmo request.

### Registro no index.ts

```ts
import { myRouter } from "./routes/my.routes.js";
app.use("/api", myRouter);
```

## Zod Validation

### Schema como fonte única de verdade

```ts
import { z } from "zod";

export const mySchema = z.object({
  name: z.string().min(1, "name is required"),
  email: z.string().email(),
  role: z.enum(["ADMIN", "USER"]).default("USER"),
  age: z.number().int().positive().optional(),
});

// Tipo inferido — sem interface manual, sem any
export type MyPayload = z.infer<typeof mySchema>;
```

### Validação com safeParse

```ts
const parsed = mySchema.safeParse(req.body);

if (!parsed.success) {
  return res.status(400).json({
    error: "Invalid payload",
    details: parsed.error.flatten().fieldErrors,
    // { name: ["name is required"], email: ["Invalid email"] }
  });
}

// parsed.data já é MyPayload (tipado)
```

### Variáveis de ambiente

```ts
import { z } from "zod";

const envSchema = z.object({
  PORT: z.coerce.number().int().positive().default(3000),
  DATABASE_URL: z.string().url(),
  API_KEY: z.string().min(1),
});

type Env = z.infer<typeof envSchema>;

function loadEnv(): Env {
  const result = envSchema.safeParse(process.env);
  if (!result.success) {
    console.error("Invalid env:", result.error.flatten().fieldErrors);
    process.exit(1);
  }
  return result.data;
}

export const env = loadEnv();
```

Use `z.coerce` para valores que vêm como string mas deveriam ser número/boolean.

## Error Handling

### 404 — Rota não encontrada

```ts
import type { RequestHandler } from "express";

export const notFoundHandler: RequestHandler = (_req, res) => {
  res.status(404).json({ error: "Route not found" });
};
```

### 500 — Erro interno

```ts
import type { ErrorRequestHandler } from "express";

export const errorHandler: ErrorRequestHandler = (err, _req, res, _next) => {
  console.error("Unhandled error:", err);
  res.status(500).json({ error: "Internal server error" });
};
```

### Semântica HTTP

| Situação | Código | Body |
|---|---|---|
| Payload inválido | 400 | `{ error, details }` |
| Recurso criado/enfileirado | 201 / 202 | `{ id }` ou `{ jobId }` |
| Recurso encontrado | 200 | Dados do recurso |
| Recurso não encontrado | 404 | `{ error }` |
| Erro interno | 500 | `{ error }` |

## Testing com Vitest

### Configuração

```ts
// vitest.config.ts
import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    globals: true,
    environment: "node",
  },
});
```

### Testes de schema

```ts
import { describe, expect, it } from "vitest";
import { mySchema } from "./my.schema";

const valid = { name: "Foo", email: "foo@bar.com", role: "ADMIN" };

describe("mySchema", () => {
  it("accepts valid payload", () => {
    expect(mySchema.safeParse(valid).success).toBe(true);
  });

  it("rejects invalid email", () => {
    const result = mySchema.safeParse({ ...valid, email: "not-email" });
    expect(result.success).toBe(false);
  });

  it("rejects empty body", () => {
    expect(mySchema.safeParse({}).success).toBe(false);
  });
});
```

## Linting com Biome

```json
{
  "$schema": "https://biomejs.dev/schemas/1.9.4/schema.json",
  "organizeImports": { "enabled": true },
  "formatter": {
    "enabled": true,
    "indentStyle": "space",
    "indentWidth": 2,
    "lineWidth": 100
  },
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true,
      "complexity": { "noBannedTypes": "error" },
      "correctness": { "noUnusedVariables": "error" },
      "style": {
        "noNonNullAssertion": "error",
        "useConst": "error",
        "useTemplate": "error"
      },
      "suspicious": { "noExplicitAny": "error", "noConsoleLog": "off" }
    }
  },
  "javascript": {
    "formatter": { "quoteStyle": "double", "semicolons": "always" }
  }
}
```

Comandos:

```bash
npm run lint          # biome check src/
npm run lint:fix      # biome check --write src/
npm run format        # biome format --write src/
```

## Boas práticas

- **Imports ordenados** — Biome `organizeImports: true` ordena automaticamente
- **Módulos ESM** — `"type": "module"` no package.json, imports com `.js` extensão
- **Sem `console.log` em produção** — usar logs estruturados ou desligar regra `noConsoleLog` no Biome
- **Handler sempre retorna** — `return res.json(...)` para evitar `ERR_HTTP_HEADERS_SENT`
- **Rotas modulares** — um `Router` por domínio, registrado no `index.ts`
- **Sem types duplicados** — inferir de schemas Zod, não criar interfaces manuais
- **strict mode** — pega erros em tempo de compilação, não em runtime

## Referências no projeto

| Arquivo | Propósito |
|---|---|
| `tsconfig.json` | Configuração strict do TypeScript |
| `biome.json` | Linter e formatter |
| `src/config/env.ts` | Variáveis de ambiente validadas |
| `src/routes/webhook.routes.ts` | Rota POST com Zod |
| `src/routes/job.routes.ts` | Rota GET com parâmetro |
| `src/middleware/error-handler.ts` | Middleware 500 |
| `src/middleware/not-found.ts` | Middleware 404 |
| `src/schemas/violation.schema.ts` | Schema Zod + tipos inferidos |
| `src/schemas/violation.schema.test.ts` | Testes com Vitest |
| `src/index.ts` | Entry point Express |
