---
name: writing-react-ts-code
description: "Core React/TypeScript standards: strict typing, Result-based error handling, component patterns, code style. Use when writing or editing any React/TypeScript code. ALWAYS load this skill before working with any react code."
---

# Writing React/TypeScript Code

This is the authoritative standard for all React/TypeScript code. Every file you write or modify must conform to these rules. They are not suggestions.

---

## 1. TypeScript Strict Configuration

### ESLint Flat Config

Use `typescript-eslint` with **strict + type-checked** presets, plus additional rules. Some rules use `warnInDevModeErrorInProd()` — warn during development, error in CI/production.

**Key enforced rules** (beyond the strict preset):

```typescript
// Zero tolerance for type escape hatches
'@typescript-eslint/no-explicit-any': 'error',
'@typescript-eslint/no-unsafe-assignment': 'error',
'@typescript-eslint/no-unsafe-call': 'error',
'@typescript-eslint/no-unsafe-member-access': 'error',
'@typescript-eslint/no-unsafe-return': 'error',
'@typescript-eslint/no-unsafe-argument': 'error',
'@typescript-eslint/no-non-null-assertion': 'error',
'@typescript-eslint/ban-ts-comment': 'error',

// Forbid vague types
'@typescript-eslint/no-empty-object-type': 'error',    // {} banned
'@typescript-eslint/no-unsafe-function-type': 'error',  // Function banned
'@typescript-eslint/no-wrapper-object-types': 'error',  // Object/String/Number banned
'@typescript-eslint/no-restricted-types': ['error', {   // object banned
  types: { object: { message: 'Use Record<string, unknown> or a specific interface' } }
}],

// Enforce explicit, predictable code
'@typescript-eslint/strict-boolean-expressions': ['error', {
  allowString: false,
  allowNumber: false,
  allowNullableObject: true,
  allowNullableBoolean: true,
  allowNullableString: false,
  allowNullableNumber: false,
  allowAny: false,
}],
'@typescript-eslint/prefer-nullish-coalescing': 'error',
'@typescript-eslint/prefer-optional-chain': 'error',
'@typescript-eslint/switch-exhaustiveness-check': 'error',
'@typescript-eslint/no-unnecessary-condition': 'error',
'@typescript-eslint/no-unnecessary-type-assertion': 'error',
'@typescript-eslint/consistent-type-assertions': ['error', {
  assertionStyle: 'as',
  objectLiteralTypeAssertions: 'never',
}],
'@typescript-eslint/explicit-function-return-type': ['error', {
  allowExpressions: true,
  allowTypedFunctionExpressions: true,
  allowHigherOrderFunctions: true,
  allowDirectConstAssertionInArrowFunctions: true,
  allowConciseArrowFunctionExpressionsStartingWithVoid: true,
  allowFunctionsWithoutTypeParameters: true,
  allowIIFEs: true,
}],

// Code quality
eqeqeq: 'error',
'prefer-const': 'error',
'no-console': warnInDevModeErrorInProd(),

// React hooks (from next/core-web-vitals + explicit)
'react-hooks/exhaustive-deps': 'error',
'react-hooks/rules-of-hooks': 'error',

// Import organization
'import/order': [warnInDevModeErrorInProd(), {
  'newlines-between': 'always',
  alphabetize: { order: 'asc', caseInsensitive: true },
  groups: ['builtin', 'external', 'internal', ['parent', 'sibling', 'index'], 'type'],
  pathGroups: [{ pattern: '@/**', group: 'internal', position: 'before' }],
}],
'unused-imports/no-unused-imports': warnInDevModeErrorInProd(),

// Custom: process.env banned in src/ (except NODE_ENV) — use env.ts
'local-rules/no-process-env-in-src': ['error', { allow: ['NODE_ENV'] }],
```

**Relaxed rules for vendored components** (`src/components/ui/**`, `src/components/kbar/**`): all strict type rules, boolean safety, and vague type rules are turned off. These are generated/vendored code — do not manually enforce rules on them.

### tsconfig.json

```jsonc
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "forceConsistentCasingInFileNames": true,
    "paths": { "@/*": ["./src/*"] }
  }
}
```

---

## 2. Type Safety Rules

### Forbidden Types

These types destroy type safety. Never use them.

| Forbidden | Use Instead | Why |
|---|---|---|
| `any` | `unknown`, explicit union, constrained generic | `any` disables the type checker entirely |
| `{}` | `Record<string, unknown>` | `{}` matches anything except `null`/`undefined` |
| `object` | specific interface or `Record<string, unknown>` | `object` says nothing about shape |
| `Function` | `(args: X) => Y` explicit signature | `Function` accepts any callable with no checking |
| `!` (non-null assertion) | proper null check, optional chaining, or narrowing | `!` lies to the compiler — the value might be null |
| `as` on object literals | assign to a typed variable or use `satisfies` | `objectLiteralTypeAssertions: 'never'` — object literals must be type-checked structurally |
| `@ts-ignore` / `@ts-expect-error` | fix the type error or use targeted ESLint disable | `ban-ts-comment` is error — don't bypass the compiler |

### Type Safety Hierarchy

Each level requires justification to reach the next.

| Level | Approach | When |
|---|---|---|
| **Preferred** | Full typing: interfaces, generics, Zod schemas | All new code |
| **Migration only** | `as` cast with comment explaining why | Migrating untyped code, temporary |
| **Suppression only** | `// eslint-disable-next-line @typescript-eslint/no-unsafe-*` with comment | Third-party lib with broken types, after all alternatives exhausted |
| **Forbidden** | `any`, blanket `@ts-ignore`, empty `catch {}` | Never |

### React Component Generics

Use constrained generics, not `any`. The type system only works if you give it information.

```typescript
// WRONG — kills type checking for the entire array
const items: ReactElement<any>[] = [];

// RIGHT — preserves type checking
const items: ReactElement<Record<string, unknown>>[] = [];

// WRONG — any props accepted
type Props = ComponentProps<any>;

// RIGHT — constrained to a specific element
type Props = ComponentProps<'button'>;
```

### Third-Party Library Type Strategy

When a library has weak or missing types, try these in order. Stop at the first one that works.

1. **Official `@types` packages** — `pnpm add -D @types/library-name`
2. **Community typing packages** — search npm for types
3. **Write own type definitions** — `declare module 'library-name' { ... }` in a `.d.ts` file
4. **Module augmentation** for incomplete types:
   ```typescript
   // types/library-name.d.ts
   declare module 'library-name' {
     interface ExistingInterface {
       missingProperty: string;
     }
   }
   ```
5. **Runtime assertion pattern** with Result:
   ```typescript
   function parseLibraryResponse(raw: unknown): Result<LibraryData, ValidationError> {
     const parsed = libraryDataSchema.safeParse(raw);
     if (!parsed.success) {
       return { success: false, error: { message: parsed.error.message } };
     }
     return { success: true, data: parsed.data };
   }
   ```
6. **Last resort** — targeted ESLint disable with explanation:
   ```typescript
   // eslint-disable-next-line @typescript-eslint/no-unsafe-assignment -- library X exports untyped config, tracked in PROJ-1234
   const config = libraryFunction();
   ```

---

## 3. Result Pattern

Every operation that can fail returns a `Result`. No exceptions for expected failures.

### Core Types

```typescript
// src/lib/result.ts
export type Result<T, E> =
  | { readonly success: true; readonly data: T }
  | { readonly success: false; readonly error: E };
```

### Layer-Specific Types

```typescript
// API layer — src/lib/api/api.types.ts
type ApiError = {
  code: ErrorCode;          // 'VALIDATION_ERROR', 'UNAUTHORIZED', etc.
  message: string;
  fields?: FieldErrors;     // Field-specific validation errors
  status?: number;
  details?: unknown;
};
type ApiResult<T> = Result<T, ApiError>;

// Store layer — defined per store
type StoreError = Readonly<{
  message: string;
  details?: unknown;
}>;
type StoreResult<T> = Result<T, StoreError>;

// Store error state for UI display
type StoreErrorState = Readonly<{
  error: StoreError;
  errorMessageForUser: string;
}>;
```

### Mapping Between Layers

Never leak API errors into the UI. Map explicitly at the store boundary.

```typescript
function mapApiResultToStoreResult<T>(apiResult: ApiResult<T>): StoreResult<T> {
  if (apiResult.success) {
    return { success: true, data: apiResult.data };
  }
  return {
    success: false,
    error: {
      message: apiResult.error.message,
      details: apiResult.error,
    },
  };
}
```

### Always Check Before Access

```typescript
// WRONG — TypeScript will stop you, but don't even try
const data = result.data;

// RIGHT — narrow first
if (result.success) {
  const data = result.data; // TypeScript knows this is T
} else {
  const error = result.error; // TypeScript knows this is E
}
```

### Decision Table: Result vs Throw

| Situation | Mechanism | Rationale |
|---|---|---|
| Network request fails | `Result<T, ApiError>` | Expected — the caller must handle it |
| Validation fails | `Result<T, ValidationError>` | Expected — show feedback to user |
| JSON parsing fails | `Result<T, ParseError>` | Expected — external data can be malformed |
| Array index out of bounds in logic | `throw Error` | Programming error — this is a bug |
| Switch hits impossible case | `throw Error` | Invariant violation — this is a bug |
| Required config missing at startup | `throw Error` | Fail fast — app cannot run |
| Third-party lib that throws | Catch and wrap in `Result` | Normalize to our error-handling model |

---

## 4. Error Handling Strategy

Errors flow through layers. Each layer has a single responsibility.

### Layer Architecture

```
API layer        → catches exceptions   → returns ApiResult<T>
Store layer      → maps ApiResult       → sets StoreError state
Component layer  → reads store state    → renders error UI or data
Form layer       → reads error.fields   → maps to field-level errors
Rendering crash  → React ErrorBoundary  → catches and displays fallback
```

### API Boundary

Catch everything. Return `ApiResult<T>`. No raw exceptions escape. The template provides `apiRequestWrapper` in `src/lib/api/` which handles fetch, Zod validation, auth token injection, and 401 auto-refresh.

```typescript
// Simplified pattern — the real apiRequestWrapper handles more (auth, refresh, etc.)
async function apiRequestWrapper<T>(
  request: () => Promise<Response>,
  schema: ZodSchema<T>
): Promise<ApiResult<T>> {
  try {
    const response = await request();

    if (!response.ok) {
      return {
        success: false,
        error: {
          code: 'NETWORK_ERROR',
          message: await response.text(),
          status: response.status,
        },
      };
    }

    const json: unknown = await response.json();
    const parsed = schema.safeParse(json);

    if (!parsed.success) {
      return {
        success: false,
        error: {
          code: 'VALIDATION_ERROR',
          message: `Response validation failed: ${parsed.error.message}`,
          status: response.status,
        },
      };
    }

    return { success: true, data: parsed.data };
  } catch (error: unknown) {
    return {
      success: false,
      error: {
        code: 'NETWORK_ERROR',
        message: error instanceof Error ? error.message : 'Unknown network error',
      },
    };
  }
}
```

### Store Boundary

Map `ApiResult` to `StoreResult`. Set `StoreErrorState` with a user-friendly message. Store actions return `StoreResult<T>` so callers can react.

```typescript
// Inside a Zustand store action
fetchProducts: async (): Promise<StoreResult<readonly Product[]>> => {
  set({ loading: true, error: null });
  const apiResult = await productsApi.getAll();
  const result = mapApiResultToStoreResult(apiResult);

  if (!result.success) {
    set({
      loading: false,
      error: {
        error: result.error,
        errorMessageForUser: 'Failed to load products',
      },
    });
    return result;
  }

  set({ products: result.data, loading: false });
  return result;
},
```

### Component Boundary

Components render based on store state. Error boundaries catch rendering crashes. Conditional rendering handles store errors via `StoreErrorState`.

```typescript
export function ProductList(): JSX.Element {
  const { products, error, loading } = useProductStore();

  if (loading) {
    return <ProductListSkeleton />;
  }

  if (error !== null) {
    return <ErrorMessage message={error.errorMessageForUser} />;
  }

  return (
    <ul>
      {products.map((product) => (
        <ProductCard key={product.id} product={product} />
      ))}
    </ul>
  );
}
```

### Form Errors

Zod schemas validate. React Hook Form manages state. Server errors map to fields.

```typescript
const formSchema = z.object({
  email: z.string().email('Invalid email address'),
  name: z.string().min(1, 'Name is required'),
});

type FormData = z.infer<typeof formSchema>;

export function UserForm(): JSX.Element {
  const form = useForm<FormData>({
    resolver: zodResolver(formSchema),
  });

  async function onSubmit(data: FormData): Promise<void> {
    const result = await userApi.create(data);

    if (!result.success) {
      // Map server field errors back to form fields
      if (result.error.fields != null) {
        for (const [field, messages] of Object.entries(result.error.fields)) {
          form.setError(field as keyof FormData, { message: messages.join(', ') });
        }
        return;
      }
      toast.error(result.error.message);
      return;
    }

    toast.success('User created');
  }

  return <form onSubmit={form.handleSubmit(onSubmit)}>{/* fields */}</form>;
}
```

---

## 5. Dynamic Data Handling

All data from outside the application boundary is untrusted. Validate immediately.

### Zod for Everything External

```typescript
// API responses — define schema, validate on receipt
const productSchema = z.object({
  id: z.string().uuid(),
  name: z.string(),
  price: z.number().positive(),
});

// JSON.parse always returns unknown — validate immediately
function parseJsonConfig(raw: string): Result<Config, ValidationError> {
  let parsed: unknown;
  try {
    parsed = JSON.parse(raw) as unknown;
  } catch {
    return { success: false, error: { message: 'Invalid JSON' } };
  }

  const result = configSchema.safeParse(parsed);
  if (!result.success) {
    return { success: false, error: { message: result.error.message } };
  }
  return { success: true, data: result.data };
}
```

### The safeParse + handleZodValidationOrThrow Pattern

```typescript
function handleZodValidationOrThrow<T>(
  result: z.SafeParseReturnType<unknown, T>,
  context: string
): T {
  if (result.success) {
    return result.data;
  }
  // This is a programming error — the data should have been valid
  throw new Error(
    `Zod validation failed in ${context}: ${result.error.message}`
  );
}

// Use when invalid data is a bug (internal config, known-good sources)
const config = handleZodValidationOrThrow(
  configSchema.safeParse(rawConfig),
  'app configuration'
);
```

### What Gets Validated

| Source | Method | On Failure |
|---|---|---|
| API responses | `schema.safeParse()` wrapped in `Result` | Return error to caller |
| `JSON.parse` output | `schema.safeParse()` wrapped in `Result` | Return error to caller |
| Environment variables | t3-env with Zod schemas | Build fails immediately |
| Form inputs | Zod + React Hook Form | Show validation errors |
| Route params | Zod schema in loader/page | Redirect to 404 |

---

## 6. Component Patterns

### Standard Component Structure

```typescript
interface ProductCardProps {
  readonly product: Product;
  readonly onAddToCart: (productId: string) => Promise<void>;
}

export function ProductCard({
  product,
  onAddToCart,
}: ProductCardProps): JSX.Element {
  const [isAdding, setIsAdding] = useState<boolean>(false);

  async function handleAddToCart(): Promise<void> {
    setIsAdding(true);
    try {
      await onAddToCart(product.id);
      toast.success('Added to cart');
    } catch (error: unknown) {
      toast.error('Failed to add to cart');
    } finally {
      setIsAdding(false);
    }
  }

  return (
    <div>
      <h3>{product.name}</h3>
      <p>{formatPrice(product.price)}</p>
      <Button onClick={handleAddToCart} disabled={isAdding}>
        {isAdding ? 'Adding...' : 'Add to Cart'}
      </Button>
    </div>
  );
}
```

### Rules

- **Named exports only.** No `export default`. Exception: Next.js `page.tsx` and `layout.tsx` files require default exports.
- **Explicit return types** on all exported functions: `JSX.Element`, `Promise<void>`, etc.
- **`readonly` on all props interface properties.** Props are immutable input.
- **Explicit types for state.** `useState<boolean>(false)`, not `useState(false)`.
- **Async event handlers** return `Promise<void>` and handle their own errors inside. Never let a rejected promise go unhandled.
- **No inline object/array creation in JSX props** when it causes unnecessary re-renders. Extract to `useMemo` or a constant outside the render.

### App Router Pattern

Route files are thin wrappers. Logic lives in components and stores.

```typescript
// src/app/users/page.tsx — thin route file (default export required by Next.js)
export default function UsersPage(): JSX.Element {
  return <UserList />;
}

// src/components/UserList.tsx — all logic here (named export)
export function UserList(): JSX.Element {
  const { users, loading, error, fetchUsers } = useUserStore();
  // loading states, error handling, data rendering
}
```

---

## 7. Naming Conventions

Naming is a navigation system, not a style preference.

| Kind | Convention | Example |
|---|---|---|
| Component | `PascalCase.tsx` | `ProductCard.tsx` |
| Store | `kebab-case-store.ts` | `product-store.ts` |
| API client | `kebab-case-api.ts` | `product-api.ts` |
| Types | `kebab-case.ts` | `product-types.ts` |
| Schemas | `kebab-case-schema.ts` | `product-schema.ts` |
| Hooks | `useKebabCase.ts` | `useProductSearch.ts` |
| Utils | `kebab-case.ts` | `format-price.ts` |
| Constants | `SCREAMING_SNAKE_CASE` inside files | `MAX_RETRY_COUNT` |

---

## 8. Import Organization

Imports are grouped and alphabetized. Enforced by ESLint, not by discipline.

```typescript
// 1. Builtin (node:)
import { readFile } from 'node:fs/promises';

// 2. External packages
import { z } from 'zod';
import { create } from 'zustand';

// 3. Internal (@/ alias)
import { apiRequestWrapper } from '@/lib/api/api-client';
import { productSchema } from '@/schemas/product-schema';

// 4. Parent/sibling/index (grouped together)
import { formatPrice } from '../utils/format-price';
import { ProductImage } from './ProductImage';

// 5. Type imports (always last)
import type { Product } from '@/types/product-types';
```

Path alias: `@/*` maps to `./src/*`. Never use deep relative paths like `../../../lib/utils`. Use the alias.

---

## 9. Environment Variables

### All Access Through t3-env

```typescript
// src/env.ts
import { createEnv } from '@t3-oss/env-nextjs';
import { z } from 'zod';

export const env = createEnv({
  server: {
    DATABASE_URL: z.string().url(),
    API_SECRET: z.string().min(1),
  },
  client: {
    NEXT_PUBLIC_API_URL: z.string().url(),
  },
  runtimeEnv: {
    DATABASE_URL: process.env.DATABASE_URL,
    API_SECRET: process.env.API_SECRET,
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL,
  },
});
```

### Rules

- **`process.env` is banned in `src/`** by a custom ESLint rule (`scripts/eslint/rules/no-process-env-in-src`). The only exception is `NODE_ENV`. All other access goes through `env.ts`.
- **Build fails** if any required variable is missing or fails Zod validation. No silent fallback to `undefined`.
- **Server vs client**: Only `NEXT_PUBLIC_` prefixed variables are available in browser code. Server variables stay on the server.
- **Always import from `@/env`**:
  ```typescript
  // WRONG — ESLint error
  const url = process.env.NEXT_PUBLIC_API_URL;

  // RIGHT — typed, validated, guaranteed to exist
  import { env } from '@/env';
  const url = env.NEXT_PUBLIC_API_URL;
  ```

---

## 10. Code Style

### Prettier Configuration

```json
{
  "tabWidth": 2,
  "singleQuote": true,
  "trailingComma": "none",
  "plugins": ["prettier-plugin-tailwindcss"]
}
```

### Rules

- **`prefer-const`** everywhere. Use `let` only when reassignment is necessary.
- **`===` enforced** via `eqeqeq` ESLint rule. `==` is banned.
- **`??` over `||`** for nullish defaults. `||` coerces empty strings and `0` to falsy.
- **`?.` over `&&` chains** for optional property access.
- **Explicit return types** on all exported functions and any function longer than a few lines. TypeScript may infer for simple local one-liners.
- **Early returns** for error/edge cases. Keep the happy path unindented and linear.

```typescript
// WRONG — deeply nested
function process(input: string | null): Result<Data, ProcessError> {
  if (input !== null) {
    if (input.length > 0) {
      // actual logic buried in nesting
    }
  }
}

// RIGHT — early returns, flat structure
function process(input: string | null): Result<Data, ProcessError> {
  if (input === null) {
    return { success: false, error: { message: 'Input is null' } };
  }
  if (input.length === 0) {
    return { success: false, error: { message: 'Input is empty' } };
  }

  // actual logic at top-level indentation
  return { success: true, data: transform(input) };
}
```

### Boolean Expressions

`strict-boolean-expressions` is enabled. No truthy checks on strings or numbers. Nullable booleans are allowed.

```typescript
// WRONG — fails strict-boolean-expressions
if (name) { ... }
if (count) { ... }
if (items.length) { ... }

// RIGHT — explicit comparisons
if (name !== '') { ... }
if (count > 0) { ... }
if (items.length > 0) { ... }
if (value !== null && value !== undefined) { ... }

// OK — nullable booleans are allowed (allowNullableBoolean: true)
if (isEnabled) { ... }  // where isEnabled: boolean | null
```

### Console Usage

- **`no-console`** uses `warnInDevModeErrorInProd()` — warns in development, errors in CI/production builds.
- **Never commit `console.log` calls** except for startup/shutdown messages in server code.

---

## 11. Security

These are non-negotiable. Violations are bugs, not style issues.

| Rule | Rationale |
|---|---|
| No raw `process.env` access | All env vars go through t3-env with Zod validation |
| No `dangerouslySetInnerHTML` | XSS vector. If truly unavoidable, sanitize with DOMPurify first |
| HttpOnly cookies for auth tokens | Prevents JavaScript access to sensitive tokens |
| `credentials: 'include'` on authenticated requests | Required for cookie-based auth; configure CORS on backend to match |
| Input validation via Zod before processing | All user input, route params, query strings — validate first, use after |
| No string concatenation for SQL/HTML | Use parameterized queries and template components |
| No secrets in client code | `NEXT_PUBLIC_` prefix exposes to browser bundle |
| Server components for sensitive logic | Keep API keys and DB queries out of client bundles |

---

## 12. API Code Generation

Zod schemas for API responses are auto-generated from OpenAPI/Swagger specs. Do not write them by hand.

- **Generate**: `pnpm api:gen <feature>` reads the Swagger spec and outputs Zod schemas into `api/generated/` directories
- **Use in API clients**: Import generated schemas and pass to `apiRequestWrapper` for runtime validation
- **Single source of truth**: Backend OpenAPI spec defines the contract; generated Zod schemas enforce it at runtime

### Feature Directory Structure

```
src/mfes/{domain}/
  app.tsx                  # Main React component
  index.ts                 # single-spa lifecycles export
  stores/
    {domain}-store.ts      # Zustand store with Result pattern
  api/
    {domain}-api.ts        # API client using apiRequestWrapper
    generated/             # Auto-generated Zod schemas (pnpm api:gen)
  components/              # Domain-specific components (optional)
```
