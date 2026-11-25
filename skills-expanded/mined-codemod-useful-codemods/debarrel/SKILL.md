---
name: "debarrel"
description: "Prevent creation of barrel files in JS/TS codebases. Provides mass migration via npx codemod debarrel."
allowed-tools:
  - Bash(codemod debarrel)
  - Bash(npx codemod debarrel)
codemod-compatibility: skill-package-v1
codemod-skill-version: 1.0.0
---

# No Barrel Files Policy

## Mass Migration

To remove all existing barrel files and rewrite imports across the codebase, run:

```sh
npx codemod debarrel
```

This will:

- Identify all barrel `index.ts`/`index.js` files (files that only re-export from sibling modules).
- Rewrite every consumer import to point at the actual source module.
- Rename the old barrel file to `index.barrel.bak.ts` so it can be reviewed and deleted.

After running the debarrel codemod, barrel files have been removed from this codebase. Do NOT reintroduce them.

## What is a barrel file?

A barrel file is an `index.ts` (or `index.js`) file whose sole purpose is to re-export symbols from sibling modules. Examples of barrel file patterns to avoid:

```ts
// BAD — this is a barrel file
export { Button } from "./Button";
export { Modal } from "./Modal";
```

```ts
// BAD — re-exporting with aliases
export { internalFn as publicFn } from "./internal";
```

```ts
// BAD — namespace re-exports
export * from "./operations";
```

```ts
// BAD — import-then-reexport
import { calc } from "./calc";
export { calc };
```

## Rules

1. **Never create `index.ts`/`index.js` files that only re-export from other modules.** Each module should be imported directly by its path.
2. **Import from the actual source module**, not from a directory index. Use `import { Button } from "./components/Button"` instead of `import { Button } from "./components"`.
3. **An `index.ts` file that contains its own logic or declarations is fine.** The prohibition is specifically on files whose only purpose is aggregating and re-exporting other modules' symbols.
4. **When adding new modules**, export from the module file itself and update consumers to import from that file directly. Do not add the new export to a barrel/index file.
