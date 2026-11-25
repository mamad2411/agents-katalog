---
name: library-variables-figma
description: "Discover and import design tokens from SUBSCRIBED Figma team libraries into the current file. Use when the user wants to reuse tokens that live in a shared library: triggers 'list library variables', 'what tokens are in our shared library', 'import a variable from our design system library', 'pull in the brand color token from the library'. Works on ANY plan via the Plugin API teamLibrary methods. For LOCAL variables use export-tokens-figma / manage-variables-figma."
disable-model-invocation: false
---

# library-variables-figma — discover & import team-library variables

Browse the variables published by libraries the current file subscribes to, then import the ones you
need. Imported variables get a local id that behaves like any local variable (bind it, read it,
reference it).

## Skill boundaries
- **`use_figma` rules** — load the official **`figma-use`** skill first; it is the full Figma Plugin API reference. Essentials these scripts rely on: plain JS with top-level `await` + `return` (no IIFE, no `figma.closePlugin()`; `console.log` is not returned), inputs inlined as `const` at the top of each script, colors in 0–1 range, load fonts before any text op, `await figma.getNodeByIdAsync(...)`, and **atomic errors** (a failed script applies nothing — read the error, fix, retry).
- Local (non-library) variables → `export-tokens-figma`, `manage-variables-figma`.

## Workflow

1. **Discover.** Run [`scripts/list-library-variables.js`](scripts/list-library-variables.js) via
   `use_figma` (`skillNames: "library-variables-figma"`). Optionally set the `LIBRARY_NAME` /
   `COLLECTION_NAME` / `TYPE` filters. It returns each subscribed collection and the `key` of every
   variable in it.
2. **Import.** Put the variable `key`(s) into
   [`scripts/import-library-variable.js`](scripts/import-library-variable.js) and run it. It returns
   the new `localId` for each. Re-importing is idempotent (same local id).
3. **Use.** Bind the imported variable to node properties or reference it from local semantic tokens
   (see `figma-use` / `manage-variables-figma` for binding).

## Notes
- Only **subscribed** libraries appear. If a collection is missing, enable the library in the file's
  library settings first (a manual Figma step).
- `getVariablesInLibraryCollectionAsync` takes the **collection key**, not its id.
- Library variables are read-only references to the source — edit values in the library file, not
  here.
