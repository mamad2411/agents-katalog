---
description: TypeScript standards for shared types, errors, and package boundaries
globs: "**/*.{ts,tsx}"
alwaysApply: false
---

# TypeScript

- Strict mode. No `any`. No `@ts-ignore` without a one-line why.
- Shared DTOs and Zod schemas live in `packages/shared`. Do not fork types between main and renderer.
- Export explicit return types from package public APIs.
- Discriminated unions for message status, provider errors, privacy mode. Switches must be exhaustive.

```ts
// ❌
catch (e) {}
function compile(x: any) { return x }

// ✅
catch (e) {
  throw mapProviderError(e); // → { code: "rate_limit" | "auth" | ... }
}
export function compile(input: CompileInput): ProviderAgnosticPacket {}
```

User-facing error strings go through i18n (`pt-BR` + `en`), never raw SDK messages.
