---
name: typescript-runtime
description: TypeScript toolchain configuration and best practices. Use when setting up tsconfig, ESLint, Prettier, Vitest, bundling, type patterns or TypeScript project standards.
---

# TypeScript Runtime

Skill para configurar y mantener toolchains TypeScript modernos: tsconfig estricto, ESLint con typescript-eslint, Prettier, Vitest, bundling, gestión de tipos y estándares de proyecto.

## Principios fundamentales

- `strict: true` obligatorio en tsconfig. Sin excepciones.
- Nunca usar `any`. Usar `unknown` + type guards cuando el tipo es desconocido.
- ESLint con `@typescript-eslint/parser` + Prettier como estándar.
- Vitest como test runner (soporte nativo de TypeScript, rápido, ESM).
- Tipos explícitos en interfaces públicas (funciones exportadas, props de componentes). Inferencia para variables locales.

## tsconfig.json recomendado

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true,
    "noPropertyAccessFromIndexSignature": true,
    "exactOptionalPropertyTypes": false,
    "esModuleInterop": true,
    "forceConsistentCasingInFileNames": true,
    "skipLibCheck": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "outDir": "dist",
    "rootDir": "src"
  },
  "include": ["src/**/*.ts"],
  "exclude": ["node_modules", "dist", "**/*.test.ts"]
}
```

## Estructura de proyecto recomendada

```
proyecto/
├── src/
│   ├── handlers/
│   ├── services/
│   ├── repositories/
│   ├── types/              # Tipos e interfaces compartidos
│   │   └── index.ts
│   ├── utils/
│   └── index.ts
├── tests/
│   ├── unit/
│   ├── integration/
│   └── helpers/
│       └── fixtures.ts
├── tsconfig.json
├── eslint.config.mjs
├── .prettierrc
├── vitest.config.ts
├── package.json
└── README.md
```

## ESLint con typescript-eslint (flat config, v9+)

```javascript
// eslint.config.mjs
import eslint from '@eslint/js';
import tseslint from 'typescript-eslint';

export default tseslint.config(
  eslint.configs.recommended,
  ...tseslint.configs.strictTypeChecked,
  {
    languageOptions: {
      parserOptions: {
        projectService: true,
        tsconfigRootDir: import.meta.dirname,
      },
    },
    rules: {
      '@typescript-eslint/no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
      '@typescript-eslint/no-explicit-any': 'error',
      '@typescript-eslint/explicit-function-return-type': ['warn', {
        allowExpressions: true,
        allowTypedFunctionExpressions: true,
      }],
      '@typescript-eslint/strict-boolean-expressions': 'error',
      '@typescript-eslint/no-floating-promises': 'error',
      'no-console': ['warn', { allow: ['warn', 'error'] }],
    },
  },
  { ignores: ['dist/', 'node_modules/', 'coverage/'] },
);
```

## Prettier

```json
{
  "semi": true,
  "singleQuote": true,
  "trailingComma": "all",
  "printWidth": 100,
  "tabWidth": 2,
  "arrowParens": "always",
  "endOfLine": "lf"
}
```

## Vitest con TypeScript

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    globals: true,
    environment: 'node',
    include: ['tests/**/*.test.ts'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'lcov'],
      include: ['src/**/*.ts'],
      exclude: ['src/**/index.ts', 'src/types/**'],
      thresholds: { statements: 80, branches: 80, functions: 80, lines: 80 },
    },
  },
});
```

## package.json recomendado

```json
{
  "name": "mi-proyecto",
  "version": "1.0.0",
  "type": "module",
  "engines": { "node": ">=20.0.0" },
  "scripts": {
    "build": "tsc",
    "lint": "eslint src/ tests/",
    "lint:fix": "eslint src/ tests/ --fix",
    "format": "prettier --write .",
    "format:check": "prettier --check .",
    "typecheck": "tsc --noEmit",
    "test": "vitest run",
    "test:watch": "vitest",
    "test:coverage": "vitest run --coverage",
    "check": "npm run lint && npm run typecheck && npm run test"
  },
  "devDependencies": {
    "typescript": "^5.5.0",
    "eslint": "^9.0.0",
    "typescript-eslint": "^8.0.0",
    "@eslint/js": "^9.0.0",
    "prettier": "^3.3.0",
    "vitest": "^2.0.0",
    "@vitest/coverage-v8": "^2.0.0"
  }
}
```

## Patrones de tipado

### Interfaces para contratos públicos
```typescript
// Interfaces para objetos con forma conocida
interface Order {
  readonly id: string;
  readonly items: readonly OrderItem[];
  readonly total: number;
  readonly status: OrderStatus;
  readonly createdAt: Date;
}

interface OrderItem {
  readonly name: string;
  readonly price: number;
  readonly quantity: number;
}

type OrderStatus = 'pending' | 'confirmed' | 'shipped' | 'delivered' | 'cancelled';
```

### Branded types para IDs
```typescript
type OrderId = string & { readonly __brand: 'OrderId' };
type UserId = string & { readonly __brand: 'UserId' };

function createOrderId(id: string): OrderId {
  if (!id.startsWith('ORD-')) throw new Error('Invalid order ID format');
  return id as OrderId;
}
```

### Discriminated unions para estados
```typescript
type Result<T, E = Error> =
  | { readonly success: true; readonly data: T }
  | { readonly success: false; readonly error: E };

function processOrder(order: Order): Result<Order> {
  if (order.total <= 0) {
    return { success: false, error: new Error('Invalid total') };
  }
  return { success: true, data: { ...order, status: 'confirmed' } };
}
```

### Type guards
```typescript
function isOrder(value: unknown): value is Order {
  return (
    typeof value === 'object' &&
    value !== null &&
    'id' in value &&
    'items' in value &&
    'total' in value
  );
}
```

## Manejo de errores tipado

```typescript
class AppError extends Error {
  constructor(
    public readonly code: string,
    message: string,
    public readonly statusCode: number = 400,
    public readonly cause?: unknown,
  ) {
    super(message);
    this.name = 'AppError';
  }
}

// Nunca throw de valores que no sean Error
// ✅ throw new AppError('NOT_FOUND', 'Order not found', 404);
// ❌ throw 'something went wrong';
// ❌ throw { message: 'error' };
```

## Anti-patrones a evitar

- ❌ `any` en lugar de tipos concretos o `unknown`.
- ❌ `strict: false` en tsconfig.
- ❌ Type assertions (`as`) sin type guard previo.
- ❌ `!` (non-null assertion) sin verificación.
- ❌ `@ts-ignore` o `@ts-expect-error` sin justificación.
- ❌ Interfaces vacías o con `[key: string]: any`.
- ❌ No usar `readonly` en propiedades que no deben mutar.
- ❌ `console.log` para logging en producción.
- ❌ Dependencias sin tipos (`@types/xxx` faltante).
- ❌ Tests sin tipado (usar `vi.fn<>()` con generics).

## Checklist de proyecto TypeScript

- [ ] `strict: true` + `noUncheckedIndexedAccess` en tsconfig.
- [ ] ESLint con `typescript-eslint` strict type-checked.
- [ ] Prettier configurado.
- [ ] Vitest con coverage mínimo 80%.
- [ ] Tipos explícitos en interfaces públicas.
- [ ] `readonly` en propiedades inmutables.
- [ ] Discriminated unions para estados.
- [ ] Type guards para validación de tipos en runtime.
- [ ] Errores tipados (AppError class, nunca throw strings).
- [ ] Scripts: build, lint, typecheck, test, check (all-in-one).
