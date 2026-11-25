---
name: 2026-migration-patterns
description: Use when upgrading Zod 3→4, Vitest 2→4, Tailwind CSS 3→4. Covers non-obvious gotchas that cause runtime failures - things NOT prominently documented.
---

# 2026 Migration Gotchas

Edge cases and runtime errors discovered during major version upgrades. **For documented changes, use Context7 to fetch official migration guides.**

---

## Zod 4: Enum Keys Require ALL Values

**Not obvious from docs.** If you use `z.enum()` as record keys, Zod 4 requires ALL enum values to be present. Partial records silently worked in Zod 3.

```typescript
// Zod 3: This worked
const schema = z.record(z.enum(['a', 'b', 'c']), z.string())
schema.parse({ a: 'foo' }) // OK

// Zod 4: FAILS - missing 'b' and 'c'
// Error: "Invalid enum value"

// Fix: Use z.string() if partial records needed
const schema = z.record(z.string(), z.string())
```

**Find affected code:**
```bash
rg "z\.record\(z\.enum" --type ts
```

---

## Vitest 4: Arrow Functions Can't Be Constructors

**Runtime error, not compile-time.** Mocks using arrow functions fail when called with `new`:

```
TypeError: () => ({...}) is not a constructor
```

```typescript
// BROKEN - arrow function
vi.mock("ai", () => ({
  DefaultChatTransport: vi.fn().mockImplementation(() => ({
    api: "test"
  }))
}))

// FIXED - regular function
vi.mock("ai", () => ({
  DefaultChatTransport: vi.fn().mockImplementation(function(this: any, config: any) {
    this.api = config.api
  })
}))
```

---

## Vitest 4: Observer Mocks for Test Setup

Copy-paste ready. These break silently in Vitest 4 if using arrow functions:

```typescript
// test/setup.ts

global.ResizeObserver = vi.fn().mockImplementation(function(
  this: { observe: () => void; unobserve: () => void; disconnect: () => void }
) {
  this.observe = vi.fn();
  this.unobserve = vi.fn();
  this.disconnect = vi.fn();
});

global.IntersectionObserver = vi.fn().mockImplementation(function(
  this: { observe: () => void; unobserve: () => void; disconnect: () => void }
) {
  this.observe = vi.fn();
  this.unobserve = vi.fn();
  this.disconnect = vi.fn();
});
```

---

## Vitest 4: Mock Type Casting

TypeScript errors when assigning mocks to native APIs:

```typescript
// Error: Type 'Mock<...>' is not assignable to type '(...data: any[]) => void'
console.log = mockConsole.log

// Fix: explicit cast
console.log = mockConsole.log as typeof console.log
```

---

## Tailwind 4: Migration Tool Requires Clean Git

**The `@tailwindcss/upgrade` tool fails silently or refuses to run with uncommitted changes.**

```bash
# This will fail if you have uncommitted changes
npx @tailwindcss/upgrade

# Do this first
git add -A && git commit -m "pre-tailwind-upgrade"
npx @tailwindcss/upgrade
```

---

## Quick Find Commands

```bash
# Zod: enum record keys (may need redesign)
rg "z\.record\(z\.enum" --type ts

# Vitest: arrow function mocks (need regular function)
rg "mockImplementation\(\(\)" --type ts

# Zod: old error property
rg "\.error\.errors" --type ts

# Pinecone: old upsert API
rg "\.upsert\(\[" --type ts
```
