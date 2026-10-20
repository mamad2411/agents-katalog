# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ReactHookDebugger is a TypeScript development tool for troubleshooting React hooks (useEffect, useMemo, useCallback). It provides debugging utilities that log dependency changes, render counts, and timing information to help developers understand why hooks are re-executing.

## Development Commands

### Linting

```bash
# Run ESLint
npx eslint src/

# Run ESLint with auto-fix
npx eslint src/ --fix
```

### Package Management

```bash
# Install dependencies (use legacy peer deps for compatibility)
npm install --legacy-peer-deps

# Check for outdated packages
npm outdated
```

Note: The project uses ESLint 9 with flat config format (eslint.config.js). Package installation requires `--legacy-peer-deps` flag due to peer dependency conflicts between packages. The project currently has no build scripts or test commands defined in package.json.

## Code Architecture

### Core Structure

The codebase consists of a single main module that exports a debugging wrapper:

- **src/reactHookDebugger.ts**: Main implementation containing the `reactHookDebugger` function
- **src/index.ts**: Public export entry point
- **src/cleanSlate.ts**: Empty file (placeholder or deprecated)

### Key Design Pattern

The `reactHookDebugger` function uses a **wrapper pattern** that returns an object with three methods (useEffect, useMemo, useCallback). Each wrapper:

1. Calls the internal `useDebugHook` function to track and log dependency changes
2. Delegates to the actual React hook with the same arguments

The debugging logic uses React hooks internally:

- `usePrevious` (custom hook): Stores previous dependency values via useRef
- `useState`: Tracks render count
- `useEffect`: Logs changes when dependencies differ from previous render

### Usage Pattern

```typescript
const { useEffect } = reactHookDebugger("MyComponent", ["prop1", "prop2"]);
useEffect(() => {
  /* ... */
}, [prop1, prop2]);
```

The tool logs:

- Initial dependency values on mount
- Changed dependencies on re-renders with before/after values
- Call count and timestamp for each trigger

## ESLint Configuration

The project uses **ESLint 9** with the new **flat config format** (eslint.config.js instead of .eslintrc.js).

Key linting rules:

- `react-hooks/exhaustive-deps`: "error" - Enforces complete dependency arrays
- `react-hooks/rules-of-hooks`: "error" - Enforces hooks usage rules
- TypeScript ESLint v8 recommended rules
- Prettier integration
- Console statements generate warnings

Note: The reactHookDebugger.ts file intentionally disables:

- `react-hooks/exhaustive-deps` (the debug logic intentionally omits deps)
- `no-console` (debugging tool needs console access)
- `@typescript-eslint/no-explicit-any` (uses any for generic hook functions)

## Current Versions

- React: 19.2.0
- TypeScript: 5.7.3
- ESLint: 9.37.0
- TypeScript ESLint: 8.46.1
- React Hooks ESLint Plugin: 7.0.0
