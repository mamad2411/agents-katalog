---
name: typescript-best-practices
description: Write TypeScript code following best practices, type safety patterns, and modern TypeScript features. Use when writing TypeScript code, defining types, or when the user asks about TypeScript, types, type safety, or TypeScript patterns.
---

# TypeScript Best Practices

Write type-safe, maintainable TypeScript code following best practices and modern patterns.

## Type Safety

### Use Strict Mode

```json
// tsconfig.json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "strictBindCallApply": true,
    "strictPropertyInitialization": true,
    "noImplicitThis": true,
    "alwaysStrict": true
  }
}
```

### Avoid `any`

```typescript
// ❌ Bad - Loses type safety
function processData(data: any) {
  return data.value;
}

// ✅ Good - Use specific types
function processData(data: { value: string }) {
  return data.value;
}

// ✅ Better - Use generics
function processData<T extends { value: string }>(data: T): string {
  return data.value;
}
```

### Use `unknown` Instead of `any`

```typescript
// ❌ Bad
function parseJSON(json: string): any {
  return JSON.parse(json);
}

// ✅ Good
function parseJSON<T>(json: string): T {
  return JSON.parse(json) as T;
}

// ✅ Better - Type guard
function parseJSON<T>(json: string): T | null {
  try {
    return JSON.parse(json) as T;
  } catch {
    return null;
  }
}
```

## Type Definitions

### Use Interfaces for Objects

```typescript
// ✅ Good - Use interfaces for object shapes
interface User {
  id: number;
  email: string;
  name: string;
  createdAt: Date;
}

// ✅ Good - Extend interfaces
interface AdminUser extends User {
  role: "admin";
  permissions: string[];
}
```

### Use Types for Unions and Intersections

```typescript
// ✅ Good - Use types for unions
type Status = "pending" | "approved" | "rejected";

// ✅ Good - Use types for intersections
type UserWithRole = User & { role: string };

// ✅ Good - Use types for complex types
type EventHandler = (event: Event) => void;
```

### Discriminated Unions

```typescript
// ✅ Good - Discriminated unions for type safety
type Result<T> = { success: true; data: T } | { success: false; error: string };

function handleResult<T>(result: Result<T>) {
  if (result.success) {
    // TypeScript knows result.data exists
    console.log(result.data);
  } else {
    // TypeScript knows result.error exists
    console.error(result.error);
  }
}
```

## `satisfies` and literal inference

Use **`satisfies`** to check an object or array against a type while keeping inferred literal types where TypeScript allows:

```typescript
type HttpMethod = "GET" | "POST";
interface Endpoint {
  path: string;
  method: HttpMethod;
}

// ✅ Good — keys and shapes checked; excess or wrong `method` is an error
const api = {
  listUsers: { path: "/users", method: "GET" },
  createUser: { path: "/users", method: "POST" },
} satisfies Record<string, Endpoint>;
```

Use **`as const`** on objects and arrays when you need readonly deeply-narrowed literals (often paired with `satisfies` on the outer value).

**`const` type parameters** (TypeScript 5.0+): infer literals from arguments without forcing call-site `as const`:

```typescript
declare function ensureTuple<const T extends readonly unknown[]>(items: T): T;

const t = ensureTuple(["a", "b"]); // readonly ["a", "b"], not string[]
```

Prefer these over `as any` or loose assertions when shaping config maps, route tables, and discriminated-union payloads.

## Utility Types

### Common Utility Types

```typescript
// Partial - Make all properties optional
type PartialUser = Partial<User>;

// Required - Make all properties required
type RequiredUser = Required<PartialUser>;

// Pick - Select specific properties
type UserPreview = Pick<User, "id" | "name" | "email">;

// Omit - Exclude specific properties
type CreateUserData = Omit<User, "id" | "createdAt">;

// Record - Create object type
type UserRoles = Record<string, string[]>;

// Readonly - Make properties readonly
type ImmutableUser = Readonly<User>;
```

### Custom Utility Types

```typescript
// Make specific properties optional
type Optional<T, K extends keyof T> = Omit<T, K> & Partial<Pick<T, K>>;

type UpdateUserData = Optional<User, "id" | "createdAt">;

// Make specific properties required
type RequiredFields<T, K extends keyof T> = T & Required<Pick<T, K>>;

type UserWithEmail = RequiredFields<User, "email">;
```

## Generics

### Generic Functions

```typescript
// ✅ Good - Generic function
function identity<T>(value: T): T {
  return value;
}

// ✅ Good - Generic with constraints
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}

// ✅ Good - Generic classes
class Repository<T> {
  async findById(id: number): Promise<T | null> {
    // ...
  }

  async create(data: Omit<T, "id">): Promise<T> {
    // ...
  }
}
```

### Generic Constraints

```typescript
// ✅ Good - Constrain generic types
interface HasId {
  id: number;
}

function updateEntity<T extends HasId>(entity: T, updates: Partial<T>): T {
  return { ...entity, ...updates };
}
```

## Type Guards

### Type Predicates

```typescript
// ✅ Good - Type guard function
function isUser(obj: any): obj is User {
  return (
    typeof obj === "object" &&
    typeof obj.id === "number" &&
    typeof obj.email === "string"
  );
}

// Usage
function processData(data: unknown) {
  if (isUser(data)) {
    // TypeScript knows data is User
    console.log(data.email);
  }
}
```

### `in` Operator

```typescript
// ✅ Good - Use 'in' operator for type narrowing
function processEvent(event: UserCreatedEvent | OrderCreatedEvent) {
  if ("userId" in event) {
    // TypeScript knows this is UserCreatedEvent
    console.log(event.userId);
  } else {
    // TypeScript knows this is OrderCreatedEvent
    console.log(event.orderId);
  }
}
```

### `typeof` and `instanceof`

```typescript
// ✅ Good - Use typeof for primitives
function processValue(value: string | number) {
  if (typeof value === "string") {
    return value.toUpperCase();
  }
  return value.toFixed(2);
}

// ✅ Good - Use instanceof for classes
function processError(error: Error | ValidationError) {
  if (error instanceof ValidationError) {
    return error.errors;
  }
  return { message: error.message };
}
```

## Async Patterns

### Promise Types

```typescript
// ✅ Good - Explicit return types
async function fetchUser(id: number): Promise<User> {
  const response = await fetch(`/users/${id}`);
  return response.json();
}

// ✅ Good - Handle errors
async function fetchUserSafe(id: number): Promise<User | null> {
  try {
    return await fetchUser(id);
  } catch {
    return null;
  }
}
```

### Async/Await Best Practices

```typescript
// ✅ Good - Parallel execution
async function fetchUserData(userId: number) {
  const [user, orders, notifications] = await Promise.all([
    fetchUser(userId),
    fetchOrders(userId),
    fetchNotifications(userId),
  ]);
  return { user, orders, notifications };
}

// ✅ Good - Error handling
async function processOrder(orderId: number) {
  try {
    const order = await getOrder(orderId);
    await validateOrder(order);
    await processPayment(order);
    return { success: true, order };
  } catch (error) {
    logger.error("Order processing failed", { orderId, error });
    throw error;
  }
}
```

## Module Organization

### Export Patterns

```typescript
// ✅ Good - Named exports
export function createUser(data: CreateUserData): Promise<User> {
  // ...
}

export class UserService {
  // ...
}

// ✅ Good - Default export for main class
export default class UserController {
  // ...
}

// ✅ Good - Re-export from index
// services/index.ts
export { UserService } from "./UserService";
export { OrderService } from "./OrderService";
```

### Type Exports

```typescript
// ✅ Good - Export types
export type { User, CreateUserData, UpdateUserData };

// ✅ Good - Export interfaces
export interface UserRepository {
  findById(id: number): Promise<User | null>;
}
```

## Best Practices

### 1. Use Explicit Return Types

```typescript
// ✅ Good
function calculateTotal(items: Item[]): number {
  return items.reduce((sum, item) => sum + item.price, 0);
}

// ❌ Bad - Infer return type
function calculateTotal(items: Item[]) {
  return items.reduce((sum, item) => sum + item.price, 0);
}
```

### 2. Use `const` Assertions

```typescript
// ✅ Good - Const assertion for literal types
const statuses = ["pending", "approved", "rejected"] as const;
type Status = (typeof statuses)[number]; // 'pending' | 'approved' | 'rejected'

// ✅ Good - Const assertion for objects
const config = {
  apiUrl: "https://api.example.com",
  timeout: 5000,
} as const;
```

### 3. Avoid Type Assertions

```typescript
// ❌ Bad - Unsafe type assertion
const user = data as User;

// ✅ Good - Use type guard
if (isUser(data)) {
  const user = data; // TypeScript knows it's User
}

// ✅ Good - Validate and assert
function parseUser(data: unknown): User {
  if (!isUser(data)) {
    throw new Error("Invalid user data");
  }
  return data;
}
```

### 4. Use Enums Carefully

```typescript
// ✅ Good - String enums
enum UserRole {
  Admin = "admin",
  User = "user",
  Guest = "guest",
}

// ✅ Better - Union types (preferred)
type UserRole = "admin" | "user" | "guest";
```

### 5. Prefer Composition Over Inheritance

```typescript
// ✅ Good - Composition
interface Timestamped {
  createdAt: Date;
  updatedAt: Date;
}

interface User extends Timestamped {
  id: number;
  email: string;
}
```

## When Writing TypeScript

1. **Enable strict mode** - Catch errors at compile time
2. **Avoid `any`** - Use `unknown` or specific types
3. **Use type guards** - Narrow types safely
4. **Define explicit types** - Don't rely on inference for public APIs
5. **Use utility types** - Reduce boilerplate
6. **Leverage generics** - Write reusable code
7. **Export types** - Make types available to consumers
8. **Use discriminated unions** - For type-safe state management
9. **Handle null/undefined** - Use strict null checks
10. **Document complex types** - Add JSDoc comments
