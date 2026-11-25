---
name: typescript
description: "Apply for any TypeScript project. Covers: strict config, type patterns, generics, discriminated unions, type guards, utility types, and common anti-patterns. Trigger for: TypeScript, TS, types, interfaces, generics."
---

# TYPESCRIPT — Strict Mode Production Patterns

## tsconfig — Strict baseline (non-negotiable)
```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "target": "ES2022",
    "moduleResolution": "bundler"
  }
}
```

## Type vs Interface
```ts
// Interface → objects, classes, extendable contracts
interface User { id: string; email: string }
interface AdminUser extends User { role: 'admin' }

// Type → unions, intersections, computed, primitives
type Status = 'pending' | 'running' | 'done' | 'failed'
type ApiResponse<T> = { data: T; timestamp: number } | { error: string }
```

## Discriminated Unions — Replace enums
```ts
type JobResult =
  | { status: 'success'; output: string; duration: number }
  | { status: 'failed'; error: string; attempt: number }
  | { status: 'pending' }

function handleResult(result: JobResult) {
  switch (result.status) {
    case 'success': return process(result.output)  // TypeScript knows output exists
    case 'failed':  return retry(result.attempt)   // TypeScript knows attempt exists
    case 'pending': return wait()
  }
}
```

## Generics — When and how
```ts
// Repository pattern with generics
interface Repository<T extends { id: string }> {
  findById(id: string): Promise<T | null>
  save(entity: T): Promise<T>
  delete(id: string): Promise<void>
}

// Constrained generics
function first<T extends readonly unknown[]>(arr: T): T[0] | undefined {
  return arr[0]
}
```

## Type Guards
```ts
function isUser(value: unknown): value is User {
  return typeof value === 'object' && value !== null &&
    'id' in value && typeof (value as User).id === 'string'
}

// Use for: API responses, localStorage, external data
const raw = JSON.parse(data)
if (isUser(raw)) { /* TypeScript knows it's User */ }
```

## Utility Types — Know these
```ts
Partial<User>           // all optional
Required<User>          // all required
Pick<User, 'id'|'email'>
Omit<User, 'password'>
Record<string, number>
Readonly<User>
ReturnType<typeof fetchUser>  // infer return type
Parameters<typeof submitJob>  // infer params
```

## Forbidden
❌ `any` — use `unknown` + type guard instead
❌ `as` casting without guard — use `satisfies` or guard
❌ `!` non-null assertion without certainty
❌ Enums (runtime overhead) — use `const` objects or discriminated unions
❌ `// @ts-ignore` — fix the type instead
❌ `Function` type — always specify signature
