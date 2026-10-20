# backend/src/latticeApiDocs

Agent-facing API reference assets; rendering lives in `../latticeApiDocs.ts`.

## Editable source and size

- `LATTICE_API.template.md` and `LATTICE_API_RECIPES.template.md` are the
  editable source of truth. Project `.lattice/LATTICE_API*.md` files are
  generated; change the templates rather than those outputs.
- Agents read the index whole when following the system-prompt preamble.
  `../__tests__/latticeApiDocs.test.ts` enforces a 5 KB budget (under 5120 UTF-8
  bytes) with a long project path; repeated path substitutions consume space.
  Put detailed recipes in `LATTICE_API_RECIPES.template.md` and keep the index
  small, with its absolute `{{RECIPES_PATH}}` pointer to the sibling output.

## Renderer and regeneration

`../latticeApiDocs.ts` owns loading, literal substitution and versioned writes:

- Templates load lazily, trying the dist-adjacent asset before the source-tree
  fallback. Each candidate must contain the `{{API_URL}}` sanity token.
  Per-template process caching includes absence (`null`): loaded content and
  failed lookup results persist for that process; asset edits do not invalidate
  either. Missing assets disable only that file's generation.
- `{{API_PORT}}`, `{{API_URL}}`, `{{PROJECT}}`, `{{PROJECT_FWD}}`,
  `{{PROJECT_HASH}}` and `{{RECIPES_PATH}}` become literal project/port values,
  using the canonical project path and shared project hash. Recipes must not
  depend on shell expansion. Keep function replacers: string replacements
  interpret dollar sequences such as `$$` and `$&` in project paths.
- Only existing project `.lattice/` directories are seeded; generation never
  creates that directory. `refreshLatticeApiDocs` is best-effort so a doc
  failure cannot block a spawn; recipes failure does not prevent index output.
- Each output has its own first-line `lattice-docs-version` stamp, derived
  from its rendered content hash. Matching stamps skip writes; missing or
  different stamps trigger regeneration. The stamp, rather than a full body
  comparison, decides freshness; avoid manually editing generated files.

## Spawn and executor boundary

- `docPath.ts` only locates an existing index, returning its path or `null`.
  It is read-only. The detached executor's fingerprinted import graph must use
  this module, never the generator or templates, so API doc edits do not make
  it stale or require replacing live terminal sessions.
- The main backend refreshes references before spawn in
  `../terminalServerClient/spawnBody.ts` (`resolveHarnessSpawnBody`) and in
  `../terminalWsRelay.ts` for connections creating a pty without a session id.
- `../harnessSystemPrompts/latticePreamble.ts` supplies the system-prompt
  pointer that reaches the agent. `../terminalBanner.ts` supplies the user's
  scrollback banner; those bytes never reach the pty child or agent context.

## Assets and drift

- TypeScript does not emit these Markdown assets. `../../scripts/copy-assets.mjs`
  copies both templates into dist during build and dev startup; keep new
  runtime assets in its explicit copy list.
- `../__tests__/latticeApiDocsDrift.test.ts` checks both templates against live
  routes and checks the exhaustive route map `../routes/ROUTES.md`. New routes
  need agent documentation or an intentional `UNDOCUMENTED_ROUTES` exclusion
  with a reason, plus a ROUTES.md row; remove stale entries.

Reference commands from `backend/`: `npm run build`, `npm test`,
`npx tsc --noEmit`.
Existing coverage in `../__tests__/`: `latticeApiDocs.test.ts` (rendering,
budget, stamps), `latticeApiDocsDrift.test.ts` (route drift), and
`latticeApiDocsSpawnRefresh.test.ts` (pre-spawn refresh and fingerprint boundary).
