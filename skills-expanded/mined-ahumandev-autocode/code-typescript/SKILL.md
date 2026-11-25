---
name: code-typescript
description: Typescript/Javascript Standards - Use this skill to learn how to update Typescript or Javascript code. This is the Java coding standard that you MUST apply to all your Typescript code or when you update `.ts` or `.js` files.
---

# TypeScript Coding Standard - Quick Reference

## Type Inference vs Explicit Types

**Always explicit for function signatures and returns:**

```typescript
// ❌ AVOID: Missing return types
function getUserName(userId: number) {
  return 'John';
}

// ✅ CORRECT: Explicit return types
function getUserName(userId: number): string {
  return 'John';
}

async function fetchData(url: string): Promise<Data> {
  const response = await fetch(url);
  return response.json();
}
```

---

## Null/Undefined Handling Pitfalls

**Confusion between optional (`?`) and union with undefined**

```typescript
// ❌ AVOID: Using null in optional properties
interface User {
  middleName: string | null; // Use undefined instead
}

// ✅ CORRECT: Use undefined for optional
interface User {
  middleName?: string; // Optional property
  email: string;
}

// ❌ AVOID: Unsafe access
function getUserEmail(user: User | null): string {
  return user.email; // Crashes if user is null
}

// ✅ CORRECT: Null-safe access
function getUserEmail(user: User | undefined): string {
  return user?.email ?? 'unknown@example.com';
}

// ✅ CORRECT: Explicit null checks
function process(value: string | undefined): void {
  if (value !== undefined) {
    console.log(value.toUpperCase());
  }
}
```

---

## Structural Typing Pitfalls

**TypeScript uses structural typing (duck typing), not nominal typing**

```typescript
// ❌ PITFALL: Structural typing can cause unexpected matches
interface Animal {
  name: string;
  makeSound(): void;
}

interface Vehicle {
  name: string;
  makeSound(): void;
}

const dog = {
  name: 'Buddy',
  makeSound() { console.log('Woof!'); }
};

const animal: Animal = dog; // OK: matches structure
const vehicle: Vehicle = dog; // Also OK: matches structure!

// ✅ CORRECT: Use branded types when strict matching needed
interface Named {
  readonly __brand: 'Named';
  name: string;
}

const namedUser: Named = {
  __brand: 'Named',
  name: 'John',
};
```

---

## This Context Binding Issues

**Arrow functions in classes cause performance issues**

```typescript
// ❌ AVOID: Arrow function properties (creates new function per instance)
class DataProcessor {
  data: number[] = [];

  process = (): void => {
    this.data = [];
  }; // Performance issue: function created for each instance

  asyncProcess(): void {
    Promise.resolve().then(function () {
      this.process(); // 'this' is undefined here
    });
  }
}

// ✅ CORRECT: Regular methods with arrow in callbacks
class DataProcessor {
  private data: number[] = [];

  process(newData: number[]): void {
    this.data = newData;
    this.validate();
  }

  private validate(): void {
    console.log('Data validated:', this.data);
  }

  asyncProcess(): Promise<void> {
    return Promise.resolve().then(() => {
      this.process([1, 2, 3]); // Arrow function preserves 'this'
    });
  }
}

// ✅ CORRECT: Use bind() if needed
class DataProcessor {
  getCallback(): () => void {
    return this.processCallback.bind(this);
  }

  private processCallback(): void {
    // implementation
  }
}
```

---

## Named Exports Requirement

**Default exports are STRICTLY PROHIBITED - use named exports only**

```typescript
// ❌ WRONG: Default export
export default class UserService { }

// ✅ CORRECT: Named exports
export class UserService { }
export interface User { id: number; }
export const DEFAULT_TIMEOUT = 5000;
```

---

## Disallowed Features

**Never use:** eval(), debugger, const enum, with keyword, wrapper classes (new Number/String/Boolean), modifying built-in prototypes.

---

## Cognitive Complexity Anti-Pattern

**Functions with too many nested conditions (SonarQube catches this)**

```typescript
// ❌ SMELL: Overly complex function
function processOrder(order: any): void {
  if (order.type === 'A') {
    if (order.quantity > 10) {
      if (order.priority === 'high') {
        // Many more nested conditions...
      }
    }
  }
}

// ✅ CORRECT: Extract logic into helper functions
function processOrder(order: Order): void {
  if (isHighPriorityBulkOrder(order)) {
    applyExpressShipping(order);
  }
}

function isHighPriorityBulkOrder(order: Order): boolean {
  return order.type === 'A' && order.quantity > 10 && order.priority === 'high';
}
```

---

## Variable Declaration Rules

**Default to `const`, use `let` only for reassignment, never use `var`**

---

## Async/Await Common Mistakes

```typescript
// ❌ CRITICAL BUG: Missing await
async function fetchData(): Promise<void> {
  const data = fetch('/api/data'); // Missing await!
  console.log(data); // Logs Promise, not the actual data
}

// ✅ CORRECT: Use await
async function fetchData(): Promise<Data> {
  const response = await fetch('/api/data');
  if (!response.ok) {
    throw new Error('Failed to fetch');
  }
  return response.json();
}

// ❌ AVOID: Unhandled promise rejection
async function processUser(userId: number): Promise<void> {
  const user = await getUser(userId); // No error handling
  console.log(user);
}

// ✅ CORRECT: Proper error handling
async function processUser(userId: number): Promise<void> {
  try {
    const user = await getUser(userId);
    console.log(user);
  } catch (error) {
    console.error('Failed to process user:', error);
    throw error;
  }
}
```

---

## Type Safety Violations

**Using `any` type defeats TypeScript's purpose**

```typescript
// ❌ AVOID: Using any
function process(data: any): any {
  return data.value; // No type checking
}

// ✅ CORRECT: Use specific types
interface DataInput {
  value: number;
}

function process(data: DataInput): number {
  return data.value;
}

// ✅ CORRECT: Use unknown for truly unknown types
function handleUnknown(data: unknown): void {
  if (typeof data === 'object' && data !== null && 'value' in data) {
    console.log((data as { value: any }).value);
  }
}
```

---

## Complex Type Simplification

**Deeply nested types are hard to maintain**

```typescript
// ❌ AVOID: Overly complex nested types
type ComplexResponse = {
  status: number;
  data: {
    user: {
      id: number;
      profile: {
        name: string;
        email: string;
        settings: {
          notifications: boolean;
        };
      };
    }[];
  };
};

// ✅ CORRECT: Break into smaller types
type UserSettings = {
  notifications: boolean;
};

type UserProfile = {
  name: string;
  email: string;
  settings: UserSettings;
};

type User = {
  id: number;
  profile: UserProfile;
};

type ApiResponse<T> = {
  status: number;
  data: T;
};

type UserApiResponse = ApiResponse<User[]>;
```

---

## React-Specific Pitfalls

**Keys in lists - array indices are anti-pattern**

```typescript
// ❌ CRITICAL: Using array index as key
function UserList({ users }): JSX.Element {
  return (
    <ul>
      {users.map((user, index) => (
        <li key={index}>{user.name}</li> // Key changes when list reorders!
      ))}
    </ul>
  );
}

// ✅ CORRECT: Use stable identifiers
function UserList({ users }): JSX.Element {
  return (
    <ul>
      {users.map((user) => (
        <li key={user.id}>{user.name}</li> // Stable identifier
      ))}
    </ul>
  );
}
```

**Use hooks, not class lifecycle methods**

```typescript
// ✅ CORRECT: Use hooks
function UserProfile(): JSX.Element {
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    // Fetch data
    return () => { /* Cleanup */ };
  }, []);

  return <div>{user?.name}</div>;
}
```

---

## Loop Variable Capture

**`var` in loops with callbacks creates closure bugs**

```typescript
// ❌ BUG: var captured by closure
for (var i = 0; i < 3; i++) {
  setTimeout(() => {
    console.log(i); // Always logs 3 (var is function-scoped)
  }, 100);
}

// ✅ CORRECT: Use const with for...of
for (const i of [0, 1, 2]) {
  setTimeout(() => {
    console.log(i); // Logs 0, 1, 2 correctly
  }, 100);
}
```

---

## Security Pitfalls

**These will fail SonarQube and code reviews**

```typescript
// ❌ CRITICAL: XSS vulnerability
document.getElementById('content').innerHTML = userInput; // Raw HTML injection!

// ✅ CORRECT: Use textContent
document.getElementById('content').textContent = userInput;

// ❌ CRITICAL: Hard-coded credentials
const DB_PASSWORD = 'admin123';
const API_KEY = 'sk_live_abc123';

// ✅ CORRECT: Environment variables
const DB_PASSWORD = process.env.DB_PASSWORD;
const API_KEY = process.env.API_KEY;

// ❌ HOTSPOT: Logging sensitive data
function login(username: string, password: string): void {
  console.log(`User ${username} logged in with ${password}`); // Logs password!
}

// ✅ CORRECT: Log only non-sensitive info
function login(username: string, password: string): void {
  console.log(`User ${username} logged in successfully`);
}
```

---

## Strict Equality

**Always use `===` and `!==`, never `==` or `!=`**

---

## SonarQube Quality Gate Violations

**Common catches:** Unused variables, unreachable code, missing default cases, code duplication, overly complex functions.

Extract common logic to avoid duplication. Remove unused variables. Keep functions focused.

---


**Document Status:** Non-obvious mistakes and SonarQube pitfalls reference  
**Languages:** TypeScript, JavaScript  
**Focus:** Quick-reference for code reviewers and developers
