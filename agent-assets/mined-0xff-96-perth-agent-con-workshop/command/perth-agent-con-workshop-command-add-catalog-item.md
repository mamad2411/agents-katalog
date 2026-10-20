---
description: Add an A2UI catalog primitive (L4) — a definition plus a renderer
argument-hint: <PrimitiveName> <what it renders>
allowed-tools: Read, Edit, Bash
---
Arguments: `$ARGUMENTS`
Treat the **first token** as the primitive name (PascalCase) and **the rest** as
what it renders. If no arguments were given, ask me for them.

Add a new primitive to the A2UI catalog, following the existing pattern exactly.

Steps:
1. Read `src/catalog/definitions.ts` (the shape of each primitive definition) and
   `src/catalog/renderers.tsx` (how each definition maps to a React renderer via
   `createCatalog`).
2. Add the primitive's definition to `demonstrationCatalogDefinitions` in
   `definitions.ts`, mirroring an existing entry (e.g. `Card` or `Text`).
3. Add the matching renderer in `renderers.tsx` so the primitive paints real UI.
   Default every array/object field.
4. Run `npm run typecheck` and `npx vitest run`; fix anything red.
5. Summarize what you added and an L4 prompt that would make the agent compose with it.

Do not add new dependencies. Do not commit unless I ask.
