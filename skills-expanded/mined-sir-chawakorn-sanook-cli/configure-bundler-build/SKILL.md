---
name: configure-bundler-build
description: Configures and optimizes the JS/TS build toolchain — tsconfig plus a bundler (Vite/esbuild/Rollup/tsup/webpack) — for correct module output (ESM/CJS/dual + types), code splitting, tree-shaking, sourcemaps, env injection, and fast incremental builds.
when_to_use: Setting up or fixing how an app or library compiles and bundles — wrong module format, broken tree-shaking, missing/incorrect types, slow builds, tsconfig errors. Distinct from dockerfile-optimize (container images) and optimize-core-web-vitals (browser runtime metrics).
---

## When to Use

Reach for this skill when the problem is **how source compiles and emits**, not how it runs in a browser or container:

- "Set up the build for this app/library" (pick bundler, tsconfig, output format)
- "My library ships ESM but breaks in a CJS `require()`" (or vice versa) — dual-package output
- "Consumers get `Could not find a declaration file`" — missing/mislocated `.d.ts`
- "Tree-shaking isn't dropping unused exports" — dead code in the bundle
- "`tsc`/`vite build` is slow" — switch transform to esbuild/swc, add a persistent cache
- "`define`/`import.meta.env` isn't replacing my env var" or a secret leaked into the client bundle
- tsconfig errors: `module`/`moduleResolution` mismatch, `"x.js" has no exported member`, paths not resolving

NOT this skill:
- Shrinking the runtime container image, multi-stage Docker layers → dockerfile-optimize
- LCP/INP/CLS, lazy-loading images, render-blocking JS in the browser → optimize-core-web-vitals
- Cross-package build orchestration, workspace topo build order, Turbo/Nx pipelines → setup-monorepo-tooling
- `npm publish`, `files`/`publishConfig`, provenance, version bump → publish-package-registry
- ESLint/Prettier/pre-commit wiring → setup-lint-format-precommit
- Pinning the Node/pnpm/tsc *versions* themselves (engines, `.nvmrc`, Volta) → pin-toolchain-versions

## Steps

1. **Pick the bundler by build target — do not default to webpack.**

   | Target | Use | Why |
   |---|---|---|
   | **App** (SPA/SSR, has an entry HTML or framework) | **Vite** | Rollup-based prod build, esbuild dev, HMR, code-splitting out of the box |
   | **Library** (published to npm, consumers bundle it) | **tsup** (esbuild) or **Rollup** | dual ESM+CJS + `.d.ts` in one config; Rollup when you need fine-grained chunking |
   | **Node tool / CLI / serverless fn** (single self-run entry) | **esbuild** | fastest, bundle deps in, `--platform=node`, no chunk graph needed |
   | Legacy app needing module federation / exotic loaders | webpack | only when a Vite/Rollup plugin doesn't exist |

   Default: **app → Vite, library → tsup, node-tool → esbuild.** One tool emits JS; **`tsc` emits types** (or `tsup --dts` / `vite-plugin-dts` wraps it). Never run `tsc` as the bundler for shipping code — it doesn't bundle, tree-shake, or split.

2. **Set the tsconfig essentials — `moduleResolution` is the #1 footgun.** Pick the resolution mode by who resolves modules:

   | Scenario | `module` | `moduleResolution` |
   |---|---|---|
   | Bundler handles resolution (Vite/tsup/esbuild) | `ESNext` (or `Preserve`) | `bundler` |
   | Node runs the output directly (Node ESM/CJS) | `NodeNext` | `nodenext` |

   ```jsonc
   // tsconfig.json — app/library baseline
   {
     "compilerOptions": {
       "target": "ES2022",          // match your lowest runtime; don't ship ES5 needlessly
       "lib": ["ES2022", "DOM"],    // drop "DOM" for node-only code
       "module": "ESNext",
       "moduleResolution": "bundler",
       "strict": true,
       "skipLibCheck": true,
       "esModuleInterop": true,
       "isolatedModules": true,     // required: esbuild/swc compile file-by-file
       "verbatimModuleSyntax": true,// makes `import type` explicit — kills accidental value imports
       "declaration": true,         // emit .d.ts (libraries)
       "declarationMap": true,      // go-to-definition into your source
       "sourceMap": true,
       "outDir": "dist",
       "paths": { "@/*": ["./src/*"] }
     }
   }
   ```
   `paths` are a **type-level alias only** — the bundler must be told too (Vite `resolve.alias`, tsup/esbuild via `vite-tsconfig-paths`/`esbuild` alias, or `tsconfig-paths`). tsc does not rewrite them in emitted JS.

3. **For a library, emit dual ESM+CJS with a correct `exports` map — the `exports` map is the contract, file extensions are the proof.** tsup config:
   ```ts
   // tsup.config.ts
   import { defineConfig } from "tsup";
   export default defineConfig({
     entry: ["src/index.ts"],
     format: ["esm", "cjs"],   // → index.js (esm) + index.cjs
     dts: true,                // → index.d.ts (+ .d.cts for cjs types)
     sourcemap: true,
     treeshake: true,
     clean: true,
     target: "node18",
     external: [/^node:/],     // never bundle node builtins
   });
   ```
   ```jsonc
   // package.json — types condition MUST come first in each block
   {
     "type": "module",
     "exports": {
       ".": {
         "import": { "types": "./dist/index.d.ts",  "default": "./dist/index.js"  },
         "require": { "types": "./dist/index.d.cts", "default": "./dist/index.cjs" }
       },
       "./package.json": "./package.json"
     },
     "main": "./dist/index.cjs",      // legacy fallback for old resolvers
     "module": "./dist/index.js",
     "types": "./dist/index.d.ts",
     "sideEffects": false,
     "files": ["dist"]
   }
   ```
   Keep `peerDependencies` (react, etc.) in `external` so you don't bundle two copies into the consumer.

4. **App: split code with dynamic `import()`, then control chunks deliberately.** Route-level `const Page = lazy(() => import('./Page'))` and `import('heavy-lib')` create async chunks automatically. Pull stable vendor deps into their own long-cached chunk:
   ```ts
   // vite.config.ts
   build: {
     sourcemap: true,
     rollupOptions: {
       output: {
         manualChunks: { vendor: ["react", "react-dom"] }, // or a function for finer control
       },
     },
     chunkSizeWarningLimit: 500,
   }
   ```
   Don't over-split (HTTP/2 helps, but hundreds of tiny chunks add request + parse overhead). Split on real route/feature boundaries, not per-file.

5. **Enable tree-shaking — it only works on static ESM.** Author with `import`/`export` (no `require`, no `module.exports`); CJS interop defeats it. Mark the package `"sideEffects": false` (or list the few files with real side effects, e.g. `["**/*.css", "./src/polyfill.ts"]`) so the bundler may drop unused modules. Annotate top-level calls that look impure but aren't with `/*#__PURE__*/`:
   ```ts
   export const icon = /*#__PURE__*/ createIcon(path); // droppable if `icon` is unused
   ```
   A `"sideEffects": false` lie (a module that *does* mutate global state on import) causes silently-missing behavior — list those files.

6. **Inject env at build time via `define`/`import.meta.env` — never bake a secret.** Static replacement only:
   ```ts
   // vite: only VITE_* are exposed to client; access via import.meta.env.VITE_API_URL
   // esbuild/tsup: define: { "process.env.NODE_ENV": JSON.stringify("production") }
   ```
   **Anything bundled for the browser is public.** Put API keys/DB URLs behind a server route or read them at runtime on the server (`process.env`) — a `define`'d secret is grep-able in `dist/`. Gate dev-only code behind `if (import.meta.env.DEV)` / `process.env.NODE_ENV !== "production"` so it tree-shakes out of prod.

7. **Always emit sourcemaps; choose by environment.** `sourcemap: true` (full, external `.map`) for libraries and CI artifacts. For a public web app, ship `hidden` sourcemaps (uploaded to your error tracker, not referenced in the bundle) so stack traces de-minify without exposing source to every visitor. Never `eval`/inline sourcemaps in production.

8. **Make builds fast and incremental.** Use an esbuild/swc transform (Vite and tsup already do) instead of `ts-loader`/`babel` for the JS transform — 10–100× faster. Keep type-checking **out of the bundle path**: run `tsc --noEmit` (or `vite build` + a parallel `tsc -b --watch`) so a type error doesn't block fast iteration but still gates CI. Turn on the persistent cache (Vite caches in `node_modules/.vite`; for `tsc -b` use `incremental: true` + `tsBuildInfoFile`). Add `--metafile` (esbuild) / `rollup-plugin-visualizer` to find what's bloating the bundle.

9. **Verify the output shape before declaring done** (see Verify) — `publint` + `@arethetypeswrong/cli` catch the dual-package and types-resolution bugs that don't surface until a consumer installs you.

## Common Errors

- **`moduleResolution: node` (classic) with modern packages.** Fails to resolve `exports`-map-only packages. Use `bundler` (bundler resolves) or `nodenext` (Node resolves) — never the legacy `node`/`node10`.
- **`types` condition placed last in the `exports` map.** TS reads conditions top-down and takes the first match; if `import`/`require` come before `types`, the consumer gets "no declaration file." `types` must be the **first** key in each condition block.
- **`.cjs` file emitting `export {}` (or `.mjs` with `require`).** The `exports` map points at the wrong file per condition, or `"type": "module"` mismatches the extension. ESM → `.js`/`.mjs`, CJS → `.cjs`. Verify with `node -e "require('your-pkg')"` and a separate `import`.
- **`"sideEffects": false` on a package that has side effects.** Tree-shaking drops a polyfill/CSS/registration import → feature silently missing in prod only. List the real side-effect files instead of a blanket `false`.
- **Secret in a `VITE_`/`define`d var.** It's inlined into client JS and shipped to every browser. Only public values get `VITE_`/`NEXT_PUBLIC_`; secrets stay server-side at runtime.
- **`paths` alias resolves in the editor but `Cannot find module '@/x'` at build.** tsc/`paths` is type-only; the bundler needs its own alias (`vite-tsconfig-paths`, `resolve.alias`, or `tsconfig-paths`). Configure both.
- **`isolatedModules` errors on `export { Foo }` where `Foo` is a type.** esbuild/swc compile each file alone and can't tell types from values. Use `export type { Foo }` / `import type` (enforced by `verbatimModuleSyntax`).
- **Bundling `peerDependencies` (react, etc.) into a library.** Consumer gets two React copies → "invalid hook call." Mark peers `external`.
- **Running `tsc` as the production bundler.** It transpiles per-file but doesn't bundle, tree-shake, split, or rewrite `paths` — output has unresolved aliases and no chunking. Use a real bundler for JS; `tsc` only for `.d.ts`.
- **No sourcemaps in prod (or inline/eval maps).** Minified stack traces are useless; inline maps bloat the bundle and leak source. Emit external (`hidden` for public web), upload to the error tracker.
- **Targeting `ES5`/old `lib` by reflex.** Forces heavy down-leveling and polyfills for runtimes that support modern JS. Set `target`/`lib` to your *actual* lowest runtime.

## Verify

1. **Clean build succeeds:** `rm -rf dist && <build>` exits 0 and `dist/` contains the expected entry files (`.js`, `.cjs`, `.d.ts`, `.map`).
2. **Types resolve both ways (library):** `npx @arethetypeswrong/cli --pack` reports no ❌ — no "masquerading as CJS/ESM", no missing types per condition.
3. **Package shape is publishable:** `npx publint` is clean — `exports`, `main`/`module`/`types`, and file extensions all consistent.
4. **Dual import actually loads:** in a scratch dir, `node -e "import('your-pkg').then(m=>console.log(Object.keys(m)))"` **and** `node -e "console.log(Object.keys(require('your-pkg')))"` both print the API — no `ERR_REQUIRE_ESM` / `ERR_PACKAGE_PATH_NOT_EXPORTED`.
5. **Type-check passes independently:** `tsc --noEmit` exits 0 (proves the build path didn't skip a type error).
6. **Tree-shaking works:** bundle a fixture importing one named export; the visualizer/`--metafile` shows unused siblings absent from output. Bundle size drops when an unused heavy import is removed.
7. **Code-splitting present (app):** prod build emits ≥1 async chunk per lazy route, and the vendor chunk is separate from app code (check `dist/assets/`).
8. **No secret in the bundle:** `grep -r "<a known secret substring>" dist/` returns nothing; only intended public `VITE_*`/`NEXT_PUBLIC_*` values appear.
9. **Sourcemaps map back:** open a built file's `.map` or trigger an error — stack trace points to original `src/` lines, not minified columns.
10. **Incremental rebuild is fast:** a one-line edit triggers a sub-second rebuild (warm cache), not a full cold compile.

Done = clean build emits the correct module formats + types, `attw` and `publint` are clean, both `import()` and `require()` load the API, `tsc --noEmit` passes, tree-shaking and code-splitting are confirmed in the output, no secret leaked into `dist/`, and warm rebuilds are fast.
