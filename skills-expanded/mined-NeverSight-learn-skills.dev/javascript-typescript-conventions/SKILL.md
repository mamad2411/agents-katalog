---
name: javascript-typescript-conventions
description: Provides JavaScript and TypeScript coding conventions including casing rules, naming patterns, and best practices for variables, constants, components, and types. Use when writing or editing .ts, .tsx, .js, .jsx files, creating React components, or working with TypeScript types.
author: Mike Scott
version: '1.0.0'
updated: '2026-07-11'
---

# JavaScript/TypeScript Conventions

## Quick Start

```typescript
// Variables and constants - camelCase
const maxRetries = 3;
const defaultTimeout = 30;
const campaignsPerPage = 10;

// Function parameters and return types - camelCase
function processUserData(userName: string, userId: number): void {
    const isActive = true;
    const totalAmount = 100;
}

// Component names - PascalCase
function ActiveBadge({ count }: Props) { ... }
export function CampaignCard({ campaign }: CampaignCardProps) { ... }

// Type names - PascalCase
type CampaignData = {
    name: string;
    location: string;
};

interface Props {
    count: number;
}

// Environment variables - SCREAMING_SNAKE_CASE
const appName = import.meta.env.VITE_APP_NAME;
```

## Casing Rules

### Variables, Parameters, and Constants

Use **camelCase** for:
- Variable declarations
- Function parameters
- Constant values (even though they're declared with `const`)

```typescript
// Good
const maxRetries = 3;
const defaultTimeout = 30;
const campaignsPerPage = 10;

function processUserData(userName: string, userId: number): void {
    const isActive = true;
}

// Bad
const MAX_RETRIES = 3;  // Only use for environment variables
const default_timeout = 30;  // Don't use snake_case
```

### Component Names

Use **PascalCase** for:
- React components (both functions and classes)
- Component file names (e.g., `LoginCard.tsx`)

```typescript
// Good
function ActiveBadge({ count }: Props) { ... }
export function CampaignCard({ campaign }: CampaignCardProps) { ... }

// Bad
function activeBadge({ count }: Props) { ... }
function loginCard() { ... }
```

### Type Names

Use **PascalCase** for:
- TypeScript types (`type`)
- Interfaces
- Enum values

```typescript
// Good
type CampaignData = {
    name: string;
    location: string;
};

interface Props {
    count: number;
}

// Bad
type campaignData = { ... };
type user_props = { ... };
```

### Environment Variables

Use **SCREAMING_SNAKE_CASE** only for environment variables, particularly those accessed via `import.meta.env`:

```typescript
// Good
const appName = import.meta.env.VITE_APP_NAME;
const apiKey = import.meta.env.VITE_API_KEY;

// Bad (regular constants should be camelCase)
const APP_NAME = import.meta.env.VITE_APP_NAME;
```

## Naming Best Practices

### Variables and Functions

- Use descriptive, semantic names
- Prefer nouns for variables, verbs for functions
- Avoid single letters except in loops

```typescript
// Good
const userCount = 10;
const isActive = true;
function getUserById(id: number) { ... }
function calculateTotal(items: Item[]) { ... }

// Bad
const n = 10;
const x = true;
function get(id: number) { ... }
function calc(items: Item[]) { ... }
```

### Boolean Variables

Use prefixes like `is`, `has`, `can`, `should` for boolean values:

```typescript
// Good
const isActive = true;
const hasPermission = false;
const canEdit = true;
const shouldRedirect = false;

// Bad
const active = true;
const permission = false;
```

### Component Props

- Use PascalCase for prop types
- Append `Props` to the component name for the type

```typescript
// Good
interface ButtonProps {
    onClick: () => void;
    variant?: 'primary' | 'secondary';
}

function Button({ onClick, variant = 'primary' }: ButtonProps) { ... }

// Bad
interface buttonProps {
    onclick: () => void;
}
```

## File Naming

- Use PascalCase for component files: `LoginCard.tsx`, `UserProfile.tsx`
- Use camelCase for utility files: `formatDate.ts`, `apiClient.ts`
- Use lowercase with dashes for config files: `eslint.config.js`, `vite.config.ts`