# AI Chatbot Code Generation Instructions

## Core Requirements

**File Path Inclusion**: Always include the complete file path as a comment at the top of every generated file.

**Type Safety**: Never generate loosely-typed variables. Use strict TypeScript with proper interfaces, types, and generics. Ensure all code is fully compatible with the existing codebase.

**Logging**: Use the logger utility from `@/lib/logger.ts` for all logging operations. Import appropriate service loggers (e.g., `businessLogger`, `authLogger`, `apiLogger`).

## Architecture & Standards

**Follow Documentation**: Strictly adhere to patterns and guidelines in `CODING_STANDARD.md` and `README.md`.

**Feature-Based Organization**: Code must be self-sustaining within features. Avoid cross-feature dependencies. Use shared layer (`@/hooks`, `@/lib`) for common functionality.

**Component Priority**:

1. First check `components/animate-ui/` for animated components
2. Fall back to `components/ui/` only if animate-ui doesn't have the component
3. Example: Use `components/animate-ui/radix/dropdown-menu.tsx` instead of `components/ui/dropdown-menu.tsx`

**Naming Convention**: Use `kebab-case` for all files and directories.

## Code Generation Continuity

**Interruption Handling**: When code generation is disrupted or usage limits are exceeded:

1. Analyze where you left off carefully
2. Redo the current function/const/anonymous function completely
3. Continue from that point seamlessly
4. Maintain consistent code quality and patterns

**Specificity**: Be specific in naming and implementation. If you must be generic, ensure the component/file is highly extendable for future use cases.

## File Structure Pattern

```typescript
// features/[feature-name]/components/[component-name].tsx
'use client'; // Only when needed

import * as React from 'react';
import { logger } from '@/lib/logger';
// ... other imports

interface ComponentProps {
  // Properly typed props
}

export function ComponentName(props: ComponentProps) {
  // Implementation with logging
}
```

Keep implementations feature-complete, type-safe, and maintainable.
