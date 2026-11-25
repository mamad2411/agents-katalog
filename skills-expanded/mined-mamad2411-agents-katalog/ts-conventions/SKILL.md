---
name: ts-conventions
description:
  This skill should be used when working on TypeScript projects, writing TypeScript code,
  configuring tsconfig, or reviewing TypeScript code.
version: 0.1.0
---

# TypeScript Conventions and Best Practices

This skill defines strict TypeScript conventions for maximum type safety, maintainability, and
developer experience. These practices ensure production-ready code that leverages TypeScript's full
type system capabilities.

## Type Safety Principles

### Strict Mode Required

**ALWAYS enable strict mode and all strict options in tsconfig.json.**

CORRECT:

```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true,
    "exactOptionalPropertyTypes": true,
    "noFallthroughCasesInSwitch": true,
    "noImplicitReturns": true,
    "noPropertyAccessFromIndexSignature": true,
    "noUncheckedSideEffectImports": true,
    "allowUnusedLabels": false,
    "allowUnreachableCode": false
  }
}
```

WRONG:

```json
{
  "compilerOptions": {
    "strict": false,
    "noImplicitAny": false
  }
}
```

### Never Use `any`

**ALWAYS use `unknown` instead of `any`, then narrow with type guards.**

WRONG:

```typescript
function processData(data: any) {
  return data.value; // No type safety
}

function fetchApi(): Promise<any> {
  return fetch('/api/data').then((r) => r.json());
}
```

CORRECT:

```typescript
function processData(data: unknown) {
  if (typeof data === 'object' && data !== null && 'value' in data) {
    return (data as { value: unknown }).value;
  }
  throw new Error('Invalid data shape');
}

// Better: Use type guard
type DataWithValue = { value: string };

function isDataWithValue(data: unknown): data is DataWithValue {
  return (
    typeof data === 'object' &&
    data !== null &&
    'value' in data &&
    typeof (data as DataWithValue).value === 'string'
  );
}

function processData(data: unknown) {
  if (isDataWithValue(data)) {
    return data.value; // Type-safe!
  }
  throw new Error('Invalid data shape');
}

// For API calls, define response types
type ApiResponse = {
  data: UserData;
  status: 'success' | 'error';
};

async function fetchApi(): Promise<ApiResponse> {
  const response = await fetch('/api/data');
  const data: unknown = await response.json();

  if (isApiResponse(data)) {
    return data;
  }
  throw new Error('Invalid API response');
}

function isApiResponse(data: unknown): data is ApiResponse {
  return typeof data === 'object' && data !== null && 'status' in data && 'data' in data;
}
```

### Never Use `@ts-ignore` or `@ts-expect-error`

**ALWAYS fix the underlying type issue instead of suppressing errors.**

WRONG:

```typescript
// @ts-ignore
const value = user.profile.settings.theme;

// @ts-expect-error - API types are wrong
const data = await fetchUser();
```

CORRECT:

```typescript
// Use optional chaining
const value = user?.profile?.settings?.theme;

// Fix the API types
type User = {
  id: string;
  profile: {
    settings: {
      theme: 'light' | 'dark';
    };
  };
};

const data = (await fetchUser()) as User; // Only if runtime shape is guaranteed
// Better: Validate at runtime with Zod
```

### Type Narrowing Over Assertions

**ALWAYS narrow types with type guards instead of using `as` assertions.**

WRONG:

```typescript
function processInput(input: string | number) {
  const str = input as string;
  return str.toUpperCase();
}

function handleEvent(event: Event) {
  const clickEvent = event as MouseEvent;
  console.log(clickEvent.clientX);
}
```

CORRECT:

```typescript
function processInput(input: string | number) {
  if (typeof input === 'string') {
    return input.toUpperCase();
  }
  return input.toString().toUpperCase();
}

function handleEvent(event: Event) {
  if (event instanceof MouseEvent) {
    console.log(event.clientX); // Type-safe
  }
}

// For custom type guards
function isMouseEvent(event: Event): event is MouseEvent {
  return event instanceof MouseEvent;
}

function handleEvent(event: Event) {
  if (isMouseEvent(event)) {
    console.log(event.clientX);
  }
}
```

### Discriminated Unions for State

**ALWAYS use discriminated unions for complex state and API responses.**

WRONG:

```typescript
type RequestState = {
  loading: boolean;
  error?: string;
  data?: User;
};

// Impossible states are possible:
const state: RequestState = {
  loading: true,
  error: 'Failed',
  data: user, // Can have error AND data!
};
```

CORRECT:

```typescript
type RequestState =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: User }
  | { status: 'error'; error: string };

// Only valid states are possible
function handleState(state: RequestState) {
  switch (state.status) {
    case 'idle':
      return 'Not started';
    case 'loading':
      return 'Loading...';
    case 'success':
      return state.data.name; // data is guaranteed
    case 'error':
      return state.error; // error is guaranteed
  }
}
```

### Use `satisfies` for Type Validation

**Use `satisfies` to validate types without widening.**

WRONG:

```typescript
const config = {
  endpoint: '/api/users',
  timeout: 5000,
  retries: 3,
}; // Type is inferred as { endpoint: string, timeout: number, retries: number }

// OR

const config: Config = {
  endpoint: '/api/users',
  timeout: 5000,
  retries: 3,
}; // Type is widened to Config, loses literal types
```

CORRECT:

```typescript
type Config = {
  endpoint: string;
  timeout: number;
  retries: number;
};

const config = {
  endpoint: '/api/users',
  timeout: 5000,
  retries: 3,
} satisfies Config;

// config.endpoint has type '/api/users' (literal), not string
// config.timeout has type 5000 (literal), not number
// But TypeScript validates the shape matches Config
```

### Const Assertions for Literals

**Use const assertions to preserve literal types.**

WRONG:

```typescript
const colors = ['red', 'green', 'blue']; // Type: string[]
const config = { apiUrl: 'https://api.example.com' }; // Type: { apiUrl: string }
```

CORRECT:

```typescript
const colors = ['red', 'green', 'blue'] as const; // Type: readonly ['red', 'green', 'blue']
type Color = (typeof colors)[number]; // Type: 'red' | 'green' | 'blue'

const config = {
  apiUrl: 'https://api.example.com',
} as const;
// Type: { readonly apiUrl: 'https://api.example.com' }
```

### Branded Types for Domain Modeling

**Use branded types to prevent mixing incompatible values.**

WRONG:

```typescript
type UserId = string;
type ProductId = string;

function getUser(id: UserId): User {
  /* ... */
}
function getProduct(id: ProductId): Product {
  /* ... */
}

const userId: UserId = '123';
const productId: ProductId = '456';

getUser(productId); // Oops! No error, both are just strings
```

CORRECT:

```typescript
// Branded types
type UserId = string & { readonly __brand: 'UserId' };
type ProductId = string & { readonly __brand: 'ProductId' };

// Constructors
function createUserId(id: string): UserId {
  return id as UserId;
}

function createProductId(id: string): ProductId {
  return id as ProductId;
}

function getUser(id: UserId): User {
  /* ... */
}
function getProduct(id: ProductId): Product {
  /* ... */
}

const userId = createUserId('123');
const productId = createProductId('456');

getUser(productId); // Error! Type 'ProductId' is not assignable to type 'UserId'
```

### Readonly by Default

**ALWAYS use `Readonly` for data that shouldn't be mutated.**

WRONG:

```typescript
type Config = {
  apiUrl: string;
  timeout: number;
};

function init(config: Config) {
  config.apiUrl = 'changed'; // Oops! Mutated
}
```

CORRECT:

```typescript
type Config = {
  readonly apiUrl: string;
  readonly timeout: number;
};

// Or use Readonly utility
type Config = Readonly<{
  apiUrl: string;
  timeout: number;
}>;

function init(config: Config) {
  config.apiUrl = 'changed'; // Error! Cannot assign to readonly property
}

// For arrays
function processItems(items: readonly string[]) {
  items.push('new'); // Error! push doesn't exist on readonly array
  return items.map((x) => x.toUpperCase()); // OK, map returns new array
}
```

## Code Style and Patterns

### Interface vs Type

**Use `interface` for object shapes, `type` for unions, intersections, and utilities.**

CORRECT:

```typescript
// Interface for object shapes (can be extended)
interface User {
  id: string;
  name: string;
  email: string;
}

interface Admin extends User {
  permissions: string[];
}

// Type for unions
type Status = 'idle' | 'loading' | 'success' | 'error';

// Type for intersections
type AdminUser = User & { permissions: string[] };

// Type for mapped types
type Nullable<T> = {
  [K in keyof T]: T[K] | null;
};

// Type for function signatures
type EventHandler = (event: Event) => void;
```

WRONG:

```typescript
// Don't use type for simple object shapes that might be extended
type User = {
  id: string;
  name: string;
};

// Don't use interface for unions (not possible)
interface Status {
  /* Can't do this */
}
```

### No Enums - Use Union Types

**NEVER use enums. Use const objects or union types instead.**

WRONG:

```typescript
enum Color {
  Red = 'RED',
  Green = 'GREEN',
  Blue = 'BLUE',
}

// Problems:
// - Runtime overhead
// - Can't use as const context
// - Awkward type inference
```

CORRECT:

```typescript
// Union type
type Color = 'red' | 'green' | 'blue';

// Or const object for values
const Color = {
  Red: 'red',
  Green: 'green',
  Blue: 'blue',
} as const;

type Color = (typeof Color)[keyof typeof Color];

// Usage
function setColor(color: Color) {
  console.log(color);
}

setColor(Color.Red); // OK
setColor('red'); // OK
setColor('yellow'); // Error
```

### Named Exports Over Default Exports

**ALWAYS use named exports for better refactoring and tree-shaking.**

WRONG:

```typescript
// Button.tsx
export default function Button() {
  /* ... */
}

// Usage
import Button from './Button'; // Name can be anything
import Btn from './Button'; // Easy to create inconsistency
```

CORRECT:

```typescript
// Button.tsx
export function Button() {
  /* ... */
}
export type ButtonProps = {
  /* ... */
};

// Usage
import { Button, type ButtonProps } from './Button';
// Name is fixed, refactoring is easier
```

### Barrel Exports Sparingly

**Use barrel exports only for public API, not for internal modules.**

WRONG:

```typescript
// src/components/index.ts - exports everything
export * from './Button';
export * from './Input';
export * from './Select';
export * from './internal/Helper';
export * from './internal/Utils';

// Creates circular dependencies and bundles everything
```

CORRECT:

```typescript
// src/components/index.ts - only public API
export { Button, type ButtonProps } from './Button';
export { Input, type InputProps } from './Input';
export { Select, type SelectProps } from './Select';

// internal/* modules are not exported
// Import directly when needed: import { Helper } from './components/internal/Helper';
```

### Use `import type` for Type-Only Imports

**ALWAYS use `import type` for types to enable better tree-shaking.**

WRONG:

```typescript
import { User, formatUser } from './user';

// If you only use User as a type, it still bundles the module
type Response = {
  user: User;
};
```

CORRECT:

```typescript
import { formatUser } from './user';
import type { User } from './user';

type Response = {
  user: User;
};

// Or inline
import { type User, formatUser } from './user';
```

Configure TypeScript to enforce this:

```json
{
  "compilerOptions": {
    "verbatimModuleSyntax": true
  }
}
```

### Async/Await Over Promises

**ALWAYS use async/await instead of promise chains.**

WRONG:

```typescript
function fetchUserData(id: string) {
  return fetch(`/api/users/${id}`)
    .then((response) => {
      if (!response.ok) {
        throw new Error('Failed to fetch');
      }
      return response.json();
    })
    .then((data) => {
      return processUser(data);
    })
    .catch((error) => {
      console.error(error);
      throw error;
    });
}
```

CORRECT:

```typescript
async function fetchUserData(id: string): Promise<User> {
  try {
    const response = await fetch(`/api/users/${id}`);

    if (!response.ok) {
      throw new Error('Failed to fetch');
    }

    const data: unknown = await response.json();

    if (!isUserData(data)) {
      throw new Error('Invalid user data');
    }

    return processUser(data);
  } catch (error) {
    console.error(error);
    throw error;
  }
}
```

### Runtime Validation with Zod

**For external data (API responses, user input, env vars), ALWAYS validate at runtime.**

WRONG:

```typescript
async function fetchUser(id: string): Promise<User> {
  const response = await fetch(`/api/users/${id}`);
  return response.json(); // Assumes correct shape
}
```

CORRECT:

```typescript
import { z } from 'zod';

const UserSchema = z.object({
  id: z.string(),
  name: z.string(),
  email: z.string().email(),
  age: z.number().int().positive(),
});

type User = z.infer<typeof UserSchema>;

async function fetchUser(id: string): Promise<User> {
  const response = await fetch(`/api/users/${id}`);
  const data: unknown = await response.json();

  // Runtime validation
  const user = UserSchema.parse(data); // Throws on invalid data

  return user;
}

// For environment variables
const EnvSchema = z.object({
  DATABASE_URL: z.string().url(),
  API_KEY: z.string().min(20),
  PORT: z.coerce.number().default(3000),
});

export const env = EnvSchema.parse(process.env);
```

## Tooling Configuration

### ESLint Flat Config

**ALWAYS use ESLint flat config (eslint.config.js) for ESLint 9+.**

CORRECT:

```javascript
// eslint.config.js
import js from '@eslint/js';
import tseslint from 'typescript-eslint';

export default tseslint.config(
  {
    ignores: ['dist', 'node_modules', 'coverage'],
  },
  js.configs.recommended,
  ...tseslint.configs.strictTypeChecked,
  ...tseslint.configs.stylisticTypeChecked,
  {
    languageOptions: {
      parserOptions: {
        project: true,
        tsconfigRootDir: import.meta.dirname,
      },
    },
    rules: {
      '@typescript-eslint/no-unused-vars': [
        'error',
        { argsIgnorePattern: '^_', varsIgnorePattern: '^_' },
      ],
      '@typescript-eslint/consistent-type-imports': [
        'error',
        { prefer: 'type-imports', fixStyle: 'inline-type-imports' },
      ],
      '@typescript-eslint/no-explicit-any': 'error',
      '@typescript-eslint/ban-ts-comment': 'error',
    },
  }
);
```

### Prettier Configuration

**Use Prettier for formatting, ESLint for code quality.**

CORRECT:

```json
{
  "semi": true,
  "singleQuote": true,
  "trailingComma": "es5",
  "printWidth": 100,
  "tabWidth": 2,
  "useTabs": false,
  "arrowParens": "always"
}
```

### Vitest Over Jest

**ALWAYS use Vitest for new projects.**

CORRECT:

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    globals: true,
    environment: 'node', // or 'jsdom' for React
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      exclude: ['node_modules/', 'dist/', '**/*.config.*'],
    },
  },
});
```

### Use `tsx` for Running TypeScript

**Use `tsx` for development, not `ts-node`.**

CORRECT:

```json
{
  "scripts": {
    "dev": "tsx watch src/server.ts",
    "start": "node dist/server.js"
  }
}
```

WRONG:

```json
{
  "scripts": {
    "dev": "ts-node src/server.ts"
  }
}
```

## Function and Variable Patterns

### Explicit Return Types for Exported Functions

**ALWAYS add explicit return types to exported functions.**

WRONG:

```typescript
export function calculateTotal(items: Item[]) {
  return items.reduce((sum, item) => sum + item.price, 0);
}
```

CORRECT:

```typescript
export function calculateTotal(items: Item[]): number {
  return items.reduce((sum, item) => sum + item.price, 0);
}

export async function fetchUser(id: string): Promise<User> {
  // ...
}
```

### Use Function Declarations Over Arrow Functions for Top-Level

**For top-level functions, prefer function declarations.**

CORRECT:

```typescript
export function formatUser(user: User): string {
  return `${user.name} <${user.email}>`;
}

// Arrow functions are good for callbacks and short inline functions
const names = users.map((user) => user.name);
```

WRONG:

```typescript
export const formatUser = (user: User): string => {
  return `${user.name} <${user.email}>`;
};
```

### Avoid Optional Parameters - Use Overloads or Separate Functions

**For complex functions, use overloads instead of optional parameters.**

WRONG:

```typescript
function fetchData(id: string, options?: FetchOptions, callback?: Callback) {
  // Complex logic handling all combinations
}
```

CORRECT:

```typescript
// Separate functions
function fetchData(id: string): Promise<Data> {
  /* ... */
}
function fetchDataWithOptions(id: string, options: FetchOptions): Promise<Data> {
  /* ... */
}

// Or overloads
function fetchData(id: string): Promise<Data>;
function fetchData(id: string, options: FetchOptions): Promise<Data>;
function fetchData(id: string, options?: FetchOptions): Promise<Data> {
  // Implementation
}
```

## Generic Type Patterns

### Constrain Generics Appropriately

**ALWAYS constrain generics to the minimum required type.**

WRONG:

```typescript
function getProperty<T>(obj: T, key: string) {
  return obj[key]; // Error: Type 'string' can't be used to index type 'T'
}
```

CORRECT:

```typescript
function getProperty<T extends Record<string, unknown>, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}

// Usage
const user = { name: 'Alice', age: 30 };
const name = getProperty(user, 'name'); // Type: string
const age = getProperty(user, 'age'); // Type: number
```

### Use Type Inference Where Possible

**Let TypeScript infer types when obvious, be explicit when needed for API surface.**

CORRECT:

```typescript
// Let inference work
const numbers = [1, 2, 3]; // Inferred as number[]
const doubled = numbers.map((n) => n * 2); // Inferred as number[]

// Be explicit for API surface
export function processItems(items: string[]): ProcessedItem[] {
  return items.map((item) => ({ value: item }));
}
```

### Utility Types for Transformations

**Use built-in utility types for common transformations.**

CORRECT:

```typescript
type User = {
  id: string;
  name: string;
  email: string;
  password: string;
};

// Make all properties optional
type PartialUser = Partial<User>;

// Pick specific properties
type UserCredentials = Pick<User, 'email' | 'password'>;

// Omit specific properties
type PublicUser = Omit<User, 'password'>;

// Make all properties readonly
type ImmutableUser = Readonly<User>;

// Make all properties required
type RequiredUser = Required<PartialUser>;

// Extract from union
type Status = 'idle' | 'loading' | 'success' | 'error';
type SuccessOrError = Extract<Status, 'success' | 'error'>; // 'success' | 'error'

// Exclude from union
type LoadingStates = Exclude<Status, 'success' | 'error'>; // 'idle' | 'loading'
```

## Error Handling Patterns

### Result Type for Expected Errors

**Use Result type instead of throwing for expected errors.**

WRONG:

```typescript
function parseJson(text: string): unknown {
  return JSON.parse(text); // Throws on invalid JSON
}

// Caller has to remember to try/catch
try {
  const data = parseJson(input);
} catch {
  // Handle error
}
```

CORRECT:

```typescript
type Result<T, E> = { success: true; value: T } | { success: false; error: E };

function parseJson(text: string): Result<unknown, string> {
  try {
    const value = JSON.parse(text);
    return { success: true, value };
  } catch (error) {
    return {
      success: false,
      error: error instanceof Error ? error.message : 'Unknown error',
    };
  }
}

// Caller is forced to handle both cases
const result = parseJson(input);
if (result.success) {
  console.log(result.value);
} else {
  console.error(result.error);
}
```

### Use `never` for Exhaustive Checking

**Use `never` type to ensure all cases are handled.**

CORRECT:

```typescript
type Shape =
  | { kind: 'circle'; radius: number }
  | { kind: 'square'; size: number }
  | { kind: 'rectangle'; width: number; height: number };

function area(shape: Shape): number {
  switch (shape.kind) {
    case 'circle':
      return Math.PI * shape.radius ** 2;
    case 'square':
      return shape.size ** 2;
    case 'rectangle':
      return shape.width * shape.height;
    default:
      // If we add a new shape and forget to handle it, this will error
      const exhaustive: never = shape;
      throw new Error(`Unhandled shape: ${exhaustive}`);
  }
}
```

## Module and Path Configuration

### Use Path Aliases

**Configure path aliases for cleaner imports.**

CORRECT tsconfig.json:

```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"],
      "@components/*": ["./src/components/*"],
      "@utils/*": ["./src/utils/*"]
    }
  }
}
```

Usage:

```typescript
// Instead of
import { Button } from '../../../components/Button';

// Use
import { Button } from '@components/Button';
```

### Module Type for ESM

**Set "type": "module" in package.json for ESM projects.**

CORRECT:

```json
{
  "type": "module",
  "compilerOptions": {
    "module": "ESNext",
    "moduleResolution": "Bundler"
  }
}
```

## Summary Checklist

When writing or reviewing TypeScript code, ensure:

1. Strict mode enabled with all strict flags
1. No `any` types - use `unknown` and narrow
1. No `@ts-ignore` or `@ts-expect-error` without fix
1. Discriminated unions for complex state
1. Type guards for runtime type checking
1. `satisfies` operator for type validation
1. Const assertions for literals
1. Branded types for domain modeling
1. `Readonly` for immutable data
1. Named exports over default exports
1. `import type` for type-only imports
1. Async/await over promise chains
1. Runtime validation with Zod for external data
1. ESLint flat config configured
1. Vitest for testing
1. Explicit return types on exported functions
1. Appropriate generic constraints
1. Result type for expected errors
1. `never` type for exhaustive checking
1. Path aliases configured

These conventions ensure type-safe, maintainable TypeScript code.
