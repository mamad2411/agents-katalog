---
name: typescript-decorators
description: "When to activate: TypeScript decorators, class decorators, method decorators, reflect-metadata, NestJS decorators, experimental decorators"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: engineering
  language: typescript
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---

# TypeScript Decorators

## tsconfig Setup
```json
{
  "compilerOptions": {
    "experimentalDecorators": true,
    "emitDecoratorMetadata": true
  }
}
```

## Class Decorator
```ts
// Adds metadata to class
function Entity(tableName: string) {
  return function <T extends new (...args: any[]) => {}>(constructor: T) {
    Reflect.defineMetadata('tableName', tableName, constructor)
    return constructor
  }
}

@Entity('users')
class User {
  constructor(public id: string, public name: string) {}
}

const table = Reflect.getMetadata('tableName', User)  // 'users'
```

## Method Decorator
```ts
// Retry on failure
function Retry(retries = 3, delayMs = 200) {
  return function (
    _target: object,
    _key: string,
    descriptor: PropertyDescriptor
  ) {
    const original = descriptor.value as (...args: any[]) => Promise<any>
    descriptor.value = async function (...args: any[]) {
      for (let i = 0; i < retries; i++) {
        try { return await original.apply(this, args) }
        catch (e) {
          if (i === retries - 1) throw e
          await new Promise(r => setTimeout(r, delayMs * 2 ** i))
        }
      }
    }
    return descriptor
  }
}

class ApiClient {
  @Retry(3)
  async fetchUser(id: string) {
    return fetch(`/api/users/${id}`).then(r => r.json())
  }
}
```

## Property Decorator
```ts
// Validate on assignment
function Min(min: number) {
  return function (target: object, key: string) {
    let value: number
    Object.defineProperty(target, key, {
      get: () => value,
      set: (v: number) => {
        if (v < min) throw new RangeError(`${key} must be >= ${min}`)
        value = v
      },
    })
  }
}

class Price {
  @Min(0)
  amount: number = 0
}
```

## Parameter Decorator
```ts
// Mark required parameters for DI
function Inject(token: string) {
  return function (target: object, _key: string | undefined, paramIndex: number) {
    const existing: number[] = Reflect.getMetadata('inject:tokens', target) ?? []
    existing[paramIndex] = token as any
    Reflect.defineMetadata('inject:tokens', existing, target)
  }
}
```

## Logging Decorator (practical)
```ts
function Log(level: 'info' | 'warn' | 'error' = 'info') {
  return function (_target: object, key: string, descriptor: PropertyDescriptor) {
    const original = descriptor.value
    descriptor.value = async function (...args: any[]) {
      const start = Date.now()
      try {
        const result = await original.apply(this, args)
        console[level](`${key} completed in ${Date.now() - start}ms`)
        return result
      } catch (err) {
        console.error(`${key} failed after ${Date.now() - start}ms`, err)
        throw err
      }
    }
  }
}

class UserService {
  @Log('info')
  async createUser(data: CreateUserDto) { /* ... */ }

  @Log('warn')
  async deleteUser(id: string) { /* ... */ }
}
```

## Memoize Decorator
```ts
function Memoize() {
  return function (_target: object, key: string, descriptor: PropertyDescriptor) {
    const cache = new Map<string, any>()
    const original = descriptor.value
    descriptor.value = function (...args: any[]) {
      const cacheKey = JSON.stringify(args)
      if (cache.has(cacheKey)) return cache.get(cacheKey)
      const result = original.apply(this, args)
      cache.set(cacheKey, result)
      return result
    }
  }
}
```

## TC39 Stage 3 Decorators (new syntax)
```ts
// New decorator format — supported in TS 5.0+
function log(fn: Function, ctx: ClassMethodDecoratorContext) {
  return function (this: unknown, ...args: unknown[]) {
    console.log(`Calling ${String(ctx.name)}`)
    return fn.apply(this, args)
  }
}

class Service {
  @log
  async fetch(id: string) { /* ... */ }
}
```
