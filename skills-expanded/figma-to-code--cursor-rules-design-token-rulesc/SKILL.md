---
description: Design token rules — single source of truth and naming conventions
globs: src/design-system/**/*.ts
alwaysApply: false
---

# Design Token Rules

## Single source of truth

All CSS variables live in `src/design-system/tokens.ts` as the `TOKENS: DesignToken[]` array.
`TOKEN_NAMES` (a `Set<string>`) is derived from that array and used by the validator.

**Never** define a token value anywhere else.

## Adding a token

```typescript
// ✅ — add to TOKENS array in tokens.ts
{ name: '--color-risk-high', value: '#DC2626', category: 'fintech', description: 'High risk indicator' },

// ❌ — do not add to only the token array without the DesignToken shape
'--color-risk-high'
```

## Naming convention

```
--color-{semantic}-{scale}      --color-primary-500, --color-neutral-200
--color-status-{status}         --color-status-pending, --color-status-failed
--color-{domain}-{key}          --color-card-visa, --color-kyc-approved
--spacing-{step}                --spacing-4   (4px grid: 1=4px, 2=8px …)
--font-size-{t-shirt}           --font-size-sm, --font-size-2xl
--font-weight-{name}            --font-weight-semibold
--radius-{size}                 --radius-md, --radius-full
--shadow-{size}                 --shadow-sm, --shadow-lg
```

## Category values

Use one of: `'color' | 'spacing' | 'typography' | 'border' | 'shadow' | 'fintech'`

`'fintech'` is for domain-specific tokens (transaction status, card brands, KYC states).

## After adding tokens

Run `npm run build` to verify no TypeScript errors, then confirm the new token name
appears in `TOKEN_NAMES` by importing and checking:

```typescript
import { TOKEN_NAMES } from './tokens';
console.log(TOKEN_NAMES.has('--color-risk-high')); // true
```
