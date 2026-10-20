---
name: follow-tool-dprint
description: Set up and use dprint for multi-language code formatting with a pluggable architecture
argument-hint: "[scope]"
related:
  - use-agent-browser
  - use-astgrep
  - follow-tool-aube
  - follow-tool-usage
  - follow-best-practice
  - setup-cicd
  - follow-tool-biome
  - run-lint
  - run-format
---

## Goal

Set up and use dprint for formatting code in many languages with its pluggable architecture

## Scope

Use for projects that need multi-language code formatting

- Boundary: dprint is a formatter-only, pluggable tool (TS/JS, JSON, markdown, toml, yaml, CSS, HTML, Python, Go, PHP) — no linting; when one tool should lint+format JS/TS, use `/follow-tool-biome` instead (or use dprint only for languages Biome does not cover)
- Latest: `dprint@0.57.4` (verified 2026-09-24) — since 0.56.0, plugins from the npm registry (`npm:@dprint/...`) are recommended
- References: [apis](references/apis.md) | [cli](references/cli.md) 
## Execute

### 1. Precondition Check

> Goal: check the environment before installing

- Check that Bun is installed
- Check that package.json already exists
- Check that the project has a correct structure

### 2. Install Dprint

> Goal: install dprint with Bun

- Run `bun add -D dprint` to install dprint as a dev dependency
- Verify the installation succeeded by checking bun.lock and package.json
- Verify that `dprint --version` runs

### 3. Create Configuration File

> Goal: create the dprint.json config file

- Download the config from the reference repository with `gh download https://github.com/newkub/my-config/blob/main/dprint.json`
- Or create a new dprint.json with the basic configuration:

```json [dprint.json]
{
  "includes": [
    "/*.{ts,tsx,js,jsx,json,md,toml,yaml,yml,css,scss,sass,less,html,vue,svelte,astro,py,go}"
  ],
  "excludes": [
    "/node_modules",
    "/dist",
    "/.git"
  ],
  "plugins": [
    "npm:@dprint/typescript@0.96.1",
    "npm:@dprint/json@0.24.0",
    "npm:@dprint/markdown@0.24.0",
    "npm:@dprint/toml@0.8.0",
    "npm:dprint-plugin-yaml@0.6.0",
    "npm:@dprint/dockerfile@0.6.0",
    "npm:dprint-plugin-malva@0.16.0",
    "npm:dprint-plugin-markup@0.27.3",
    "npm:@dprint/ruff@0.8.8",
    "npm:@jakebailey/dprint-plugin-gofumpt@0.0.18",
    "npm:@dprint/mago@0.28.0"
  ]
}
```

- Verify that dprint.json was created correctly
- Adjust the configuration to the project's needs (if necessary)

### 4. Add Format Scripts

> Goal: add scripts to package.json

- Add a `format` script to format files automatically

```json [package.json]
{
  "scripts": {
    "format": "dprint fmt"
  }
}
```

- Verify the scripts were added to package.json correctly
- Verify there is no conflict with existing scripts

### 5. Verify Installation

> Goal: test that dprint works

- Run `bun run format` to format all files
- Verify dprint works correctly with every stated file type
- Verify the plugins are downloaded and functional

## Rules

Always follow these rules and requirements

- Always use Bun as the package manager for installing dprint
- Always install dprint as a dev dependency with the -D flag
- Download the config from the reference repository first, when it exists
- Specify plugins for every language you want to support
- Always define excludes patterns for node_modules, dist, and .git
- Add a format script in package.json
- Use `dprint add <plugin>` to add a plugin and `dprint config update` to update plugin versions in the config
- Always use indentWidth: 2 for TypeScript and JSON
- Always use lineWidth: 100 for TypeScript
- Always use quoteStyle: alwaysSingle for TypeScript
- Always use semiColons: asi for TypeScript

- Use /use-agent-browser if needed
- Use /use-astgrep if needed
- Use /follow-tool-aube if needed
- Use /follow-tool-usage if needed
- Use /follow-best-practice if needed
- Use /setup-cicd if needed
- Use /follow-tool-biome if needed
- Use /run-lint if needed
- Use /run-format if needed

- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- dprint installed and configured in the project
- Multiple languages supported via the pluggable architecture
- A `dprint.json` ready with plugins and config
- A format script present in package.json
