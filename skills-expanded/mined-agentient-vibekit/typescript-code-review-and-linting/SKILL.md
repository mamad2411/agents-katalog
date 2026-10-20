---
name: typescript-code-review-and-linting
version: "1.0"
description: >
  ESLint configuration, TypeScript type safety rules, and React-specific linting patterns.
  PROACTIVELY activate for: (1) Setting up ESLint for TypeScript, (2) Fixing type safety issues,
  (3) React-specific linting rules, (4) Resolving TypeScript compiler errors, (5) Code review for anti-patterns.
  Triggers: "eslint", "typescript", "type checking", "refactor", "ts review", "no-explicit-any", "ts-ignore"
core-integration:
  techniques:
    primary: ["systematic_analysis"]
    secondary: ["structured_evaluation"]
  contracts:
    input: "none"
    output: "none"
  patterns: "none"
  rubrics: "none"
---

# TypeScript Code Review and Linting Skill

## Metadata (Tier 1)

**Keywords**: eslint, typescript, type checking, refactor, ts review

**File Patterns**: *.ts, *.tsx, *.js, *.jsx

**Modes**: code_review

---

## Instructions (Tier 2)

### ESLint Configuration

```javascript
// eslint.config.js
import tseslint from '@typescript-eslint/eslint-plugin';

export default [
  {
    plugins: { '@typescript-eslint': tseslint },
    rules: {
      '@typescript-eslint/no-explicit-any': 'error',
      '@typescript-eslint/no-unused-vars': 'error',
      'no-console': 'warn',
    }
  }
];
```

### Critical Type Safety Rules

**@typescript-eslint/no-explicit-any**
```typescript
// Defeats TypeScript
function process(data: any): any {
    return data.value;
}

// Use proper types
interface Data {
    value: string;
}
function process(data: Data): string {
    return data.value;
}
```

**@typescript-eslint/no-unsafe-assignment**
```typescript
// Unsafe
const value: string = getData();  // getData returns 'any'

// Type assertion or guard
const value = getData() as string;
// Or
if (typeof getData() === 'string') {
    const value: string = getData();
}
```

### React-Specific Rules

**react/no-array-index-key**
```tsx
// Causes rendering bugs
{items.map((item, index) => (
    <div key={index}>{item.name}</div>
))}

// Use unique ID
{items.map(item => (
    <div key={item.id}>{item.name}</div>
))}
```

**react/no-danger**
```tsx
// XSS risk
<div dangerouslySetInnerHTML={{__html: userInput}} />

// Sanitize or use markdown
import DOMPurify from 'dompurify';
<div dangerouslySetInnerHTML={{__html: DOMPurify.sanitize(userInput)}} />
```

### TypeScript Compiler Errors

```typescript
// TS2339: Property 'name' does not exist on type '{}'
const user = {};
console.log(user.name);  // Error

// Fix: Define interface
interface User {
    name: string;
}
const user: User = { name: "Alice" };
```

### Anti-Patterns

- Overuse of `any` type
- Type assertions without validation
- Ignoring compiler errors with @ts-ignore
- Not enabling strict mode
