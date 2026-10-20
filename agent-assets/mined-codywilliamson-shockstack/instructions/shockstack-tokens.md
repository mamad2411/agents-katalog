---
applyTo: "packages/tokens/**"
description: "Design token system guidelines"
---

## Design Tokens

- Style Dictionary 4 processes JSON token source files
- Outputs: CSS custom properties, Tailwind theme config, TypeScript constants, JSON
- Edit source tokens in `packages/tokens/tokens/*.json`
- Rebuild with `pnpm tokens:build`
- Themes use `[data-theme]` attribute switching on `<html>`
