---
name: path-scoped
description: Context-aware TypeScript helper. Auto-activates when TypeScript files are in scope.
paths: [src/**/*.ts, lib/**/*.ts]
allowed-tools: [Read, Glob, Grep]
---

When TypeScript files are in context, apply these conventions:

1. Prefer `interface` over `type` for object shapes
2. Avoid `any` — use `unknown` or proper generics
3. Export types from a dedicated `types.ts` file, not inline
