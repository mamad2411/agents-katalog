---
name: vendor-subclassing-patterns
description: Subclass vendored TS classes missing from barrel exports.
license: MIT
metadata:
  hermes:
    tags:
    - typescript
    - vendor
    - monorepo
    - subclassing
    - barrel-export
    related_skills:
    - deepseek-harness
  source_frontmatter:
    author: minimx
    version: 1.0.0
    category: coding
  imported_from: hermes
---

# Vendor Subclassing Patterns

When a TypeScript monorepo vendors upstream packages and you need to subclass a class that the upstream barrel doesn't export.

## When to Use

- Extending a vendor class that isn't in the public barrel export
- `Cannot find module ... has no exported member named 'X'` when importing from a vendored package
- Need to override `resolveBase()`, `doFetch()`, or other protected methods on a vendor transport/client class

## Detection

```bash
# 1. Find the class source
rg "class WebApiClient" vendor/

# 2. Check if it's re-exported from the barrel
rg "WebApiClient" vendor/.../client/index.ts

# 3. Check tsconfig paths that resolve the module
rg "dsh-client-connection" apps/vscode/tsconfig.json
```

## The Pattern

1. **Locate the vendor barrel** — the `index.ts` (or `index.js`) that re-exports public API. In monorepos this is usually at `packages/<pkg>/src/<subpath>/index.ts`.

2. **Add the re-export** — append a value export (not `export type` — you need the class at runtime):
   ```ts
   export { WebApiClient } from './web-api-client.ts'
   ```
   This is additive and non-breaking. Existing consumers are unaffected.

3. **Verify tsconfig resolution** — the `paths` mapping in `tsconfig.json` must resolve to the barrel you edited. If it points elsewhere (e.g. a `lib/` build artifact), the re-export won't be visible at typecheck time.

4. **Subclass in the app** — import from the same barrel path, extend, override the needed method:
   ```ts
   import { WebApiClient } from '@deepseek-ai/dsh-client-connection/client'
   export class DshWebApiClient extends WebApiClient {
     constructor(private readonly baseUrl: string, timeoutMs?: number) {
       super(timeoutMs)
     }
     protected override resolveBase(): string { return this.baseUrl }
   }
   ```

5. **Typecheck** — run the project-level `tsc --noEmit` (not bare `tsc --noEmit file.ts`). Bare invocation doesn't pick up `tsconfig.json` paths.

## Pitfalls

- **`export type` vs `export`**: If the barrel uses `export type { Foo }`, you get the type but not the runtime class. For subclassing you need `export { Foo }` (value export).
- **`verbatimModuleSyntax`**: When enabled, `import type { Foo }` is enforced for type-only imports. Value imports of classes must use `import { Foo }`, not `import type`.
- **esbuild aliases**: The build system may alias `@scope/pkg/subpath` to the barrel source. If you edit the barrel but esbuild resolves a different path, the re-export won't be bundled. Check `scripts/build.mjs` alias entries.
- **Vendor rev bumps**: A re-export added to `vendor/` will be lost when the vendor submodule is updated. Track it in project docs (e.g. AGENTS.md or dedup-plan) so it can be re-applied.
- **Bare tsc vs project tsc**: `npx tsc --noEmit src/file.ts` ignores `tsconfig.json` paths. Always run `npx tsc --noEmit` from the project root.
