---
tags: [frontend, folder, coloc, style, types]
name: folder-coloc-style-types
description: Keep component, style, and types files at the same depth; never split into styles/ or types/ subfolders
source_project: lucida-builder-r3
version: 1.0.0
category: frontend
---

# Folder co-location for components

## Trigger
- Creating a new React component folder.
- Reviewing a PR that adds `styles/` or `types/` subfolders.

## Steps
1. Put `.tsx`, `.style.ts`, and `types.ts` at the **same depth** inside the component folder.
2. Name shared styles `common.style.ts`; per-component styles `{ComponentName}.style.ts`.
3. Put all folder-shared types in a single `types.ts`.
4. Only `hooks/` and `utils/` subfolders are allowed. Never create `styles/` or `types/` subfolders.
5. Tests go next to their subject as `{file}.test.ts` in the same folder.

## Rejected shape
```
layer/
  styles/Grass.style.ts   # reject
  types/GrassTypes.ts     # reject
```

## Accepted shape
```
layer/grass/
  types.ts
  common.style.ts
  GrassChart.tsx
  GrassChart.style.ts
  utils/calcLayout.ts
```
