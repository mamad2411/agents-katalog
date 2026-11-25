---
name: follow-create-vitest-plugin
description: Build and use Vitest plugins correctly per the Plugin API (Vitest 5)
argument-hint: "[scope]"
related:
  - follow-create-sdk
  - deep-review-codebase
  - follow-tool-vitest
  - follow-create-plugins
  - ship
  - run-test

---
## Goal

Set up and use Vitest plugins correctly per the Plugin API (Vitest 5, API since 3.1.0+)

## Scope

For projects that need to build and use Vitest plugins per the standard Plugin API

- Packages: `vitest` (5.x requires Vite >= 6.4.0, Node.js >= 22.12.0), `@vitest/coverage-v8` — always confirm the latest versions with `/deep-research` + `/follow-best-practice` (not pinned in this file — per `/update-devin-global-skills`)

## Execute

### 1. Review Tech Stack

> Goal: Review the tech stack before building

1. Run `/deep-research` + `/follow-best-practice` to confirm the latest versions and patterns, then run `/deep-review-codebase` to summarize the tech stack
3. Record the rationale for the chosen stack and libraries for future reference (create vitest plugins)

### 2. Understand Plugin API

> Goal: Study the Plugin API 3.1.0+ and the context it provides

1. Study the Vitest Plugin API (stable since 3.1.0) — works with the Vitest lifecycle at the config-resolution level
2. Understand the `configureVitest` hook — called early, before reporters are created (unlike `reporter.onInit`, which comes later), so `coverage`/`reporters` can still be modified
3. Know the context: `project`, `vitest`, `injectTestProjects`
4. Study `defineCacheKeyGenerator` (stable since 5.0.0, formerly `experimental_defineCacheKeyGenerator` in 4.x)

### 3. Create Plugin

> Goal: Create the plugin with the `configureVitest` method

1. Create the plugin with the `configureVitest` method — if the plugin is used with both Vite and Vitest, use the `Plugin` type from `vite` + `/// <reference types="vitest/config" />`
2. Accept the context parameter
3. Implement the desired plugin logic
4. Give it a unique `name`

```ts
export function myPlugin(options: PluginOptions) {
  return {
    name: 'my-vitest-plugin',
    transform(code) {
      // transform logic
    },
    configureVitest({ project, vitest, injectTestProjects, defineCacheKeyGenerator }) {
      // plugin configuration
      vitest.config.coverage.enabled = false
    }
  }
}
```

### 4. Use Context Properties

> Goal: Use the context properties as intended

1. Use `project` to access the current test project (TestProject — has `name`, `vitest`, `config`, `globalConfig`, `vite`, `browser`, `hash`, `provide()`, `globTestFiles()`, `matchesTestGlob()`, `import()`, `isBrowserEnabled()`); if you use the browser feature, `project.browser` isn't set yet — use `reporter.onBrowserInit` instead
2. Use `vitest` to access the global Vitest instance
3. Use `injectTestProjects` to inject additional projects — accepts a glob pattern, a filepath, or inline config (`extends: project.vite.config.configFile` + `test: {...}`), returns `TestProject[]`
4. Modify `vitest.config` directly when needed

### 5. Implement Cache Key Generator

> Goal: Use a cache key generator when needed (Vitest 5.0.0+)

1. Use `defineCacheKeyGenerator` (stable in 5.0, formerly `experimental_defineCacheKeyGenerator` in 4.0.11+) when the plugin registers with different options — returning `false` disables the module's fs cache; only works when the top-level `test.fsModuleCache` is enabled (formerly `experimental.fsModuleCache`); opt out with `api.vitest.ignoreFsModuleCache: true`
2. Return a unique string derived from the plugin options
3. Handle `false` to disable caching
4. Use when `test.fsModuleCache` is enabled (top-level config since 5.0, formerly `experimental.fsModuleCache`)
5. Set `api.vitest.ignoreFsModuleCache: true` on the plugin object if the plugin shouldn't affect the cache

```ts
configureVitest({ defineCacheKeyGenerator }) {
  defineCacheKeyGenerator(() => {
    // return unique string from options
    return options.replacePropertyKey + options.replacePropertyValue
  })
}
```

### 6. Test Plugin

> Goal: Create a test project to test the plugin

1. Create a test project to exercise the plugin
2. Verify the plugin works
3. Test config injection
4. Check cache behavior

### 7. Ship

> Goal: Deliver the work

1. Run `/ship`
2. If `ship` fails → report the status

## Rules

### 1. Plugin Structure

- Use `configureVitest` for plugin configuration — modify config only through `vitest.config` (mutating `vitest.reporters` directly has no effect because it gets overwritten; `setupFile` isn't re-resolved — resolve paths yourself before pushing)
- Give the plugin a unique `name`
- The plugin should have a clear interface

### 2. Context Usage

- `project`: the current test project the plugin lives in
- `vitest`: the global Vitest instance - `vitest.config` can be mutated
- `injectTestProjects`: function for injecting additional projects
- The config is already resolved - some properties may have different types than the user config

### 3. injectTestProjects

```ts
const newProjects = await injectTestProjects({
  extends: project.vite.config.configFile,
  test: {
    name: 'my-custom-project',
    alias: {
      customAlias: resolve('./custom-path.js'),
    },
  },
})
```

- Accepts a config glob, a filepath, or inline config
- Returns an array of resolved test projects
- Projects must have unique names (no clash with existing projects)
- Filters may apply - update `vitest.config.project` when needed

### 4. Cache Key Generator (5.0.0+)

- Return a string for cache key hashing
- Return `false` to disable file system caching
- Use when the plugin is registered with different options
- Works when `test.fsModuleCache` is enabled (moved out of `experimental` in Vitest 5)
- Set `api.vitest.ignoreFsModuleCache: true` to opt out (the generator can still be defined)

### 5. Config Mutations

- `vitest.config` can be modified directly
- Reporters aren't created yet - modify the config instead
- `setupFile` is not resolved again - resolve paths yourself when adding new files
- Some properties have types different from the user config (already resolved)

- Use /follow-create-sdk when needed
- Use /follow-tool-vitest when needed
- Use /follow-create-vite-plugin when needed (create vitest plugins)
- Use /run-test when needed
- Use /follow-create-plugins when needed


## Expected Outcome

- Vitest plugin using the Plugin API 3.1.0+ correctly
- Proper use of configureVitest context
- Correct project injection (when needed)
- Working cache key generator (when needed)
- Well-tested plugin functionality

## Guide

- [Plugin API | Vitest](https://vitest.dev/api/advanced/plugin)
- [Test Project | Vitest](https://vitest.dev/api/advanced/test-project)
- [Vitest Instance | Vitest](https://vitest.dev/api/advanced/vitest)
