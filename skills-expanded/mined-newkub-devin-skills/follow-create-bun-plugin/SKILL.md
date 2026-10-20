---
name: follow-create-bun-plugin
description: Build Bun plugins with the Bun.plugin API for runtime and bundler
argument-hint: "[scope]"
related:
  - use-bun-native-api
  - follow-create-bun-cli
  - follow-tool-bunup
  - deep-review-codebase
  - follow-create-plugins

---
## Goal

Build Bun plugins with the `Bun.plugin` API, supporting both runtime and bundler via `onResolve`, `onLoad`, `onStart`, `onEnd`, `onBeforeParse` (native)

## Scope

For building plugins for the Bun runtime and the `bun build` bundler in TypeScript, covering `Bun.plugin`, namespaces, filters, loaders, build, and tests

- Packages: `bun`, `bun-types` — always confirm the latest versions with `/deep-research` + `/follow-best-practice` (never pinned in this file — per `/update-devin-global-skills`)

## Execute

### 1. Review Tech Stack

> Goal: Verify the tech stack before building

1. Run `/deep-research` + `/follow-best-practice` to confirm the latest versions and `Bun.plugin` API, then run `/deep-review-codebase` to summarize the tech stack
2. Record the reasons for choosing the stack and libraries as a reference for the next step (create bun plugins)
3. Record the reasons for choosing the stack and libraries as a reference for the next step (create bun plugins)

### 2. Setup Project

> Goal: Create the plugin package

1. Create the directory `packages/{plugin-name}/`
2. Create `package.json` with name `bun-plugin-{name}` or `{name}-bun-plugin`
3. Install `typescript`, `@types/bun`
4. Install a build tool: `bunup` or `tsdown`
5. Create `tsconfig.json` with `strict: true`, `declaration: true`

### 3. Create Plugin With Bun.plugin

> Goal: Implement the Bun plugin factory

1. Create `src/index.ts` with a factory function
2. Use `Bun.plugin` or return an object for setup:
   ```ts
   import type { BunPlugin } from "bun";
   export function myBunPlugin(options?: MyOptions): BunPlugin {
     return {
       name: "bun-plugin-my",
       setup(build) {
         // hooks
       }
     };
   }
   ```
3. Register a runtime plugin via a preload file that calls `plugin(myPlugin())`, then use `bun --preload ./preload.ts` or `preload = ["./preload.ts"]` in `bunfig.toml` if needed

### 4. Add onResolve

> Goal: Intercept and change module resolution

1. Use `build.onResolve({ filter: /\.ext$/ }, (args) => { ... })`
2. Specify a `namespace` if you want a custom module namespace
3. Return `path` and an optional `namespace`
4. Return `undefined` or `null` when there is no match

### 5. Add onLoad

> Goal: Load and transform module contents

1. Use `build.onLoad({ filter: /\.ext$/ }, async (args) => { ... })`
2. Return `contents`, `loader`, or `exports` (with `loader: "object"`)
3. Supported loaders: `js`, `jsx`, `ts`, `tsx`, `json`, `jsonc`, `toml`, `yaml`, `text`, `file`, `napi`, `wasm`, `css`, `html`, `object`
4. Use `Bun.file(args.path).text()` to read a file
5. Use a `namespace` when creating virtual modules
6. Use `await args.defer()` if the module's contents must wait for other modules to load first
7. Use `build.module(specifier, callback)` as shorthand for a single virtual module

### 6. Add Lifecycle Hooks

> Goal: Manage the build lifecycle

1. `build.onStart(() => { ... })` — bundle begins (async supported; the bundler waits for all to finish)
2. `build.onEnd((result) => { ... })` — build ends with a `BuildOutput`
3. `build.onBeforeParse(constraints, { napiModule, symbol })` — for native (NAPI/Rust) plugins only; runs in the parser thread
4. Use `build.config` to read/modify `BuildConfig` inside `setup()` (lifecycle callbacks cannot modify the config)

### 7. Build Package

> Goal: Build the plugin for npm

1. Create `bunup.config.ts` or `tsdown.config.ts`
2. External `bun` types but bundle runtime code
3. Output `esm` and `cjs` with `.d.ts`
4. Specify `exports`, `types`, `main` in `package.json`
5. Run `bun run build`

### 8. Add Tests

> Goal: Test the plugin

1. Create `test/plugin.test.ts`
2. Use `Bun.build({ ... plugins: [myPlugin()] })` for bundler tests
3. Use runtime tests with `Bun.plugin` + `import` statements
4. Verify the output contents
5. Run `bun test`

### 9. Add Examples

> Goal: Create usage examples

1. Create `examples/basic/` with a basic plugin
2. Create `examples/virtual-module/` with `onResolve` + `onLoad`
3. Run the examples until they pass

### 10. Ship

> Goal: Deliver the work

1. Run `/ship`
2. If `ship` fails → report the status

## Rules

### 1. Naming

- Use `bun-plugin-{name}` for Bun-specific plugins
- The plugin name in the `name` field must be unique
- Give namespaces clear names, e.g. `yaml:`, `svg:`

### 2. Plugin Registration

- Runtime: call `plugin(myPlugin())` (named import from `bun`) or `Bun.plugin(myPlugin())` in a preload file — not in the main entry file, because plugins may register after modules are resolved
- Bundler: pass via the `plugins` option of `Bun.build`
- `bunfig.toml`: use top-level `preload = ["./register-plugins.ts"]` — there is no `plugins` field in bunfig; or run `bun --preload ./file.ts`

### 3. Filters And Namespaces

- Use clear `filter` regexes — hooks match only specifiers containing `.` or `:`
- Use `namespace` to separate custom modules
- Return `undefined` quickly when there is no match
- Watch out for regex performance

### 4. Loaders

- Choose the loader based on the desired output
- `object` for virtual module exports
- `text` for raw contents
- `json` for parsed JSON

### 5. Native APIs

- Use `Bun.file` and `Bun.write` instead of `node:fs`
- Use `Bun.spawn` for child processes if needed
- Use `Bun.Glob` for file patterns

### 6. Build And External

- External `bun` types but bundle runtime code
- Generate `.d.ts` with `bunup` or `tsdown`
- Use the `exports` field in `package.json`

- Use /follow-create-elysia-plugin if needed
- Use /follow-create-plugins if needed


## Expected Outcome

- The Bun plugin builds successfully
- The plugin works with both `Bun.build` and the Bun runtime
- Tests cover bundler and runtime paths
- `.d.ts` files are fully generated
- Examples run

## Examples

```text
packages/bun-plugin-example/
├── src/
│   └── index.ts
├── test/
│   └── plugin.test.ts
├── examples/
│   ├── basic/
│   └── virtual-module/
├── package.json
├── tsconfig.json
├── bunup.config.ts
└── README.md
```

### `package.json` Scripts

```json
{
  "scripts": {
    "dev": "bun run src/index.ts",
    "build": "bunx bunup",
    "test": "bun test"
  }
}
```

### `src/index.ts`

```ts
import type { BunPlugin } from "bun";

export function yamlPlugin(): BunPlugin {
  return {
    name: "bun-plugin-yaml",
    setup(build) {
      build.onResolve({ filter: /\.yaml$/ }, (args) => ({
        path: args.path,
        namespace: "yaml"
      }));
      build.onLoad({ filter: /\.yaml$/, namespace: "yaml" }, async (args) => {
        const text = await Bun.file(args.path).text();
        const data = parseYaml(text); // implement parseYaml per context
        return { exports: { default: data }, loader: "object" };
      });
    }
  };
}
```

## Guide

- `use-bun-native-api` — Bun native APIs
- `use-bun-native-api` — Bun runtime setup
- `follow-create-bun-cli` — Bun CLI setup
- `follow-tool-bunup` — Bunup bundler
- [Bun Plugin Docs](https://bun.com/docs/runtime/plugins)
- [Bun Bundler Plugins](https://bun.com/docs/bundler/plugins)

