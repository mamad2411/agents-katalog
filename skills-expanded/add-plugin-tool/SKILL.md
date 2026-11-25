---
name: add-plugin-tool
description: Add or change an agent-callable tool contributed by a Studio plugin (manifest declaration, backend handler, consent, docs and tests). Use for bundled plugins in src/plugins/* or when changing how plugin tools are validated or dispatched.
---

# Add a plugin tool

A plugin tool is declared in the plugin's `plugin.json`, handled by its isolated backend
process and exposed to every engine as `<plugin-id>__<tool-name>`. Contract reference:
`docs/plugins.md` (manifest table, API versions, consent model) and `src/plugin-sdk/index.d.ts`.

## Files

1. **Manifest** - `src/plugins/<id>/plugin.json`, `tools[]`:
   `{name, description, parameters:{type:"object", properties, required}}`.
   - `name`: lowercase id, unique within the plugin.
   - Parameters are scalar (`string|number|boolean`) under API 1 and 2; `object` only
     with `apiVersion: 3`. Anything else is rejected by `validateManifest`
     (`src/substrate/plugins/manifest.ts`).
   - Add `confirmation` (1-300 chars, API 2+) when the tool spends money, publishes or
     otherwise needs the user's consent before each run.
   - The description is model-facing: say when to use it, what it costs and what not to do.
2. **Backend** - the `tool(name, args, ctx)` handler returned by `activate()` in the
   plugin's backend (`src/plugins/example/backend.mjs` is the minimal pattern;
   `src/plugins/genex/backend.ts`, `src/plugins/blender/backend.ts` are real ones).
   - Treat `args` as untrusted: check types and ranges again, reject unknown operations.
   - Reach host services only through `ctx.host(...)`; a backend cannot read credentials,
     open URLs or touch files outside the bound project and its own storage.
   - Return plain JSON. Throw an `Error` with an actionable message on refusal.
3. **Skill text** - if the agent needs guidance, update the plugin's `skills[]` entry so it
   names the tool by its full `<id>__<tool>` name.
4. **Host changes** (only when changing the tool system itself): validation in
   `src/substrate/plugins/manifest.ts`, dispatch/consent in `src/substrate/plugins/registry.ts`,
   the call, its consent wait and its durable record in `src/main/core/plugin-tools.ts`
   (`PluginToolService`), and engine exposure in `src/main/core/delegation.ts` (search
   `pluginTools`: the tool list handed to a session and the dispatch of its calls).
5. **Docs** - `docs/plugins.md` for contract changes; `docs/product/assets-plugins.md` for
   anything a user sees.

## Tests (red first)

- Registry behaviour against a copied package: `tests/conformance/plugins.test.ts`
  (`fixture()` copies `src/plugins/example` into a temp root) - declared vs undeclared
  fields, wrong types, disabled plugin fails closed, cancelled call not retried.
- Manifest rules: `validateManifest` cases in the same file.
- Consent: `tests/conformance/plugin-consent.test.ts` when `confirmation` is involved.
- Genex/Blender tools: `tests/conformance/genex-plugin-cli.test.ts`,
  `tests/conformance/blender.test.ts`.
- Package as a user would see it: `npm run plugin:doctor -- src/plugins/<id>`.

```sh
npm test -- tests/conformance/plugins.test.ts tests/conformance/plugin-devkit.test.ts
npm run plugin:doctor -- src/plugins/example
```

Never let a tool argument choose a program, URL or path outside the project; those come
from reviewed plugin code.
