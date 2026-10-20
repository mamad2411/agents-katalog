# Module Manager Module

This module contributes the `kota module` CLI surface: `list`, `inspect`, `new`, and `reload`.

- `kota module list` — show all loaded modules with contribution counts.
- `kota module inspect <name>` — show full detail for one module.
- `kota module new <name>` — scaffold a new TypeScript or Python module.
- `kota module reload <name>` — reload a module from disk via daemon config reload.

## Boundaries

- Uses `ctx.getModuleSummaries()` for live module data; no independent loader.
- Contributes an HTTP route for listing modules.
- Contributes the live modules/agents inspection surface through
  `KotaModule.uiSurfaces`; the projection reads the existing client namespaces.
- Avoid importing the repo module discovery entrypoint from here; this command should inspect loaded state, not rebuild it.
