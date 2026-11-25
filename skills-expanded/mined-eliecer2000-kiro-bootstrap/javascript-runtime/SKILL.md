---
name: javascript-runtime
description: JavaScript toolchain configuration and best practices. Use when setting up ESLint, Prettier, Vitest, npm scripts, Node.js conventions or JavaScript project standards.
---

# JavaScript Runtime

Skill para configurar y mantener toolchains JavaScript modernos: ESLint, Prettier, Vitest, scripts npm, convenciones Node.js, gestión de dependencias y estándares de proyecto.

## Principios fundamentales

- Node.js 20+ como runtime mínimo (LTS activo).
- ESM (`"type": "module"`) como formato de módulos por defecto en proyectos nuevos.
- ESLint + Prettier como estándar de linting y formato. Sin excepciones.
- Vitest como test runner (rápido, compatible con Jest API, ESM nativo).
- `package-lock.json` siempre commiteado. `npm ci` en CI, `npm install` en desarrollo.

## Estructura de proyecto recomendada

```
proyecto/
├── src/
│   ├── handlers/           # Entry points (Lambda handlers, API routes)
│   ├── services/           # Lógica de negocio
│   ├── repositories/       # Acceso a datos
│   ├── utils/              # Utilidades compartidas
│   └── index.js            # Export principal
├── tests/
│   ├── unit/
│   └── integration/
├── .eslintrc.cjs
├── .prettierrc
├── vitest.config.js
├── package.json
└── README.md
```

## package.json recomendado

```json
{
  "name": "mi-proyecto",
  "version": "1.0.0",
  "type": "module",
  "engines": { "node": ">=20.0.0" },
  "scripts": {
    "lint": "eslint src/ tests/",
    "lint:fix": "eslint src/ tests/ --fix",
    "format": "prettier --write .",
    "format:check": "prettier --check .",
    "test": "vitest run",
    "test:watch": "vitest",
    "test:coverage": "vitest run --coverage",
    "typecheck": "tsc --noEmit"
  },
  "devDependencies": {
    "eslint": "^9.0.0",
    "@eslint/js": "^9.0.0",
    "prettier": "^3.3.0",
    "vitest": "^2.0.0",
    "@vitest/coverage-v8": "^2.0.0"
  }
}
```

## ESLint (flat config, v9+)

```javascript
// eslint.config.js
import js from '@eslint/js';

export default [
  js.configs.recommended,
  {
    rules: {
      'no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
      'no-console': ['warn', { allow: ['warn', 'error'] }],
      'prefer-const': 'error',
      'no-var': 'error',
      'eqeqeq': ['error', 'always'],
      'curly': ['error', 'all'],
      'no-throw-literal': 'error',
    },
  },
  {
    ignores: ['dist/', 'node_modules/', 'coverage/'],
  },
];
```

## Prettier

```json
// .prettierrc
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

## Vitest

```javascript
// vitest.config.js
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    globals: true,
    environment: 'node',
    include: ['tests/**/*.test.js'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'lcov'],
      include: ['src/**/*.js'],
      exclude: ['src/**/index.js'],
      thresholds: {
        statements: 80,
        branches: 80,
        functions: 80,
        lines: 80,
      },
    },
  },
});
```

### Patrones de test
```javascript
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { OrderService } from '../src/services/order.js';

describe('OrderService', () => {
  const mockRepo = { save: vi.fn(), findById: vi.fn() };

  beforeEach(() => vi.clearAllMocks());

  it('should create order with valid data', async () => {
    mockRepo.save.mockResolvedValue(undefined);
    const service = new OrderService(mockRepo);
    const result = await service.create({ item: 'laptop', quantity: 1 });
    expect(result).toHaveProperty('id');
    expect(mockRepo.save).toHaveBeenCalledOnce();
  });

  it('should throw on invalid quantity', async () => {
    const service = new OrderService(mockRepo);
    await expect(service.create({ item: 'laptop', quantity: -1 }))
      .rejects.toThrow('quantity must be positive');
  });
});
```

## Convenciones Node.js

### Manejo de errores
```javascript
// Errores custom con código
class AppError extends Error {
  constructor(code, message, statusCode = 400) {
    super(message);
    this.name = 'AppError';
    this.code = code;
    this.statusCode = statusCode;
  }
}

// Nunca silenciar errores
try {
  await riskyOperation();
} catch (error) {
  logger.error('Operation failed', { error: error.message, stack: error.stack });
  throw new AppError('OPERATION_FAILED', 'Could not complete operation', 500);
}
```

### Async/await (nunca callbacks)
```javascript
// ✅ Correcto
const data = await fetchData();
const results = await Promise.all(items.map((item) => processItem(item)));

// ❌ Incorrecto
fetchData((err, data) => { /* callback hell */ });
```

### Variables de entorno
```javascript
// Validar al inicio, no en cada uso
const config = {
  tableName: requireEnv('TABLE_NAME'),
  stage: requireEnv('STAGE'),
  logLevel: process.env.LOG_LEVEL ?? 'INFO',
};

function requireEnv(name) {
  const value = process.env[name];
  if (!value) { throw new Error(`Missing required env var: ${name}`); }
  return value;
}
```

## Gestión de dependencias

```bash
# Instalar dependencias (desarrollo)
npm install

# Instalar dependencias (CI - reproducible)
npm ci

# Agregar dependencia de producción
npm install zod

# Agregar dependencia de desarrollo
npm install --save-dev vitest

# Auditar vulnerabilidades
npm audit

# Actualizar dependencias (minor/patch)
npm update
```

### Reglas de dependencias
- `package-lock.json` siempre commiteado.
- `npm ci` en CI/CD (instala exactamente lo del lockfile).
- `npm audit` en CI para detectar vulnerabilidades.
- Separar `dependencies` (producción) de `devDependencies` (desarrollo/test).
- Revisar dependencias nuevas antes de instalar (tamaño, mantenimiento, licencia).

## .gitignore

```
node_modules/
dist/
coverage/
.env
.env.local
*.log
```

## Anti-patrones a evitar

- ❌ `var` en lugar de `const`/`let`.
- ❌ Callbacks en lugar de async/await.
- ❌ `==` en lugar de `===`.
- ❌ `console.log` para logging en producción (usar logger estructurado).
- ❌ No validar variables de entorno al inicio.
- ❌ `require()` en proyectos ESM (usar `import`).
- ❌ Dependencias sin lockfile commiteado.
- ❌ `npm install` en CI (usar `npm ci`).
- ❌ No tener ESLint ni Prettier configurados.
- ❌ Tests sin assertions.
- ❌ Ignorar `npm audit` warnings.

## Checklist de proyecto JavaScript

- [ ] Node.js 20+ como runtime.
- [ ] `"type": "module"` en package.json.
- [ ] ESLint v9+ con flat config.
- [ ] Prettier configurado.
- [ ] Vitest con coverage mínimo 80%.
- [ ] `package-lock.json` commiteado.
- [ ] Scripts: lint, format, test, test:coverage.
- [ ] Variables de entorno validadas al inicio.
- [ ] Async/await en lugar de callbacks.
- [ ] `.gitignore` con node_modules, dist, coverage.
