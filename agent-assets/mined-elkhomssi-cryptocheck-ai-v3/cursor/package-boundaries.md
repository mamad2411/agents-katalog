---
description: Enforce package boundary — no @/ imports in packages/
globs: ["packages/**/*.ts", "packages/**/*.tsx"]
alwaysApply: true
---

# Package boundary rule

Files inside packages/ must be publishable to npm without modification.
This means zero @/ path alias imports and zero Next.js-specific imports.

If you need shared logic:
- Types → packages/ccai-connect/src/types.ts
- Signing/HMAC → @cryptocheck/signing
- Pure utilities → copy to packages/<pkg>/src/lib/ with a "keep in sync" comment

Do NOT add @/ imports to fix a TypeScript error — fix the type properly instead.
