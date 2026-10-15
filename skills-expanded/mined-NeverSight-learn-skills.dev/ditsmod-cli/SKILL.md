---
name: ditsmod-cli
description: Guidance on using Ditsmod CLI (@ditsmod/cli, binaries "ditsmod", "dm") for project bootstrapping (new) and development watch-run (start). Primarily a human developer tool; AI agents must avoid running long-running watch/start tasks in the background to prevent resource leaks.
---

# Ditsmod CLI (`@ditsmod/cli`)

The `@ditsmod/cli` package provides command-line interface tools and development helpers for Ditsmod applications.

Binary aliases `ditsmod` and `dm` are available when the package is installed.

## Installation

You can install `@ditsmod/cli` locally:

```bash
npm i -D @ditsmod/cli
```

Or run it directly without installation using `npx`:

```bash
npx @ditsmod/cli <command>
```

---

## Commands

### 1. `ditsmod new <directory>` (or `dm new`)

Creates a new Ditsmod application in the target directory using official starter templates. This replaces the manual step of cloning a starter template git repository and re-initializing git.

```bash
npx @ditsmod/cli new my-app [options]
```

#### Options
* `-t, --template <name>`: Starter template to use:
  * `rest` (default)
  * `rest-monorepo`
  * `trpc-monorepo`
* `-m, --package-manager <name>`: Package manager to use (`npm`, `yarn`, `pnpm`). Default: `npm`.
* `--skip-install`: Do not automatically run package installation after bootstrapping.
* `--skip-git`: Do not initialize a new clean Git repository with an initial commit.

#### Examples
```bash
# Create a REST application using Yarn
npx @ditsmod/cli new my-rest-api -m yarn

# Create a tRPC monorepo without installing packages
npx @ditsmod/cli new my-trpc-app -t trpc-monorepo --skip-install
```

---

### 2. `ditsmod start [entryFile]` (or `dm start`)

Runs the Ditsmod application in development mode with incremental TypeScript watch compilation (using Project References for monorepos), automatic asset copying, and graceful process restarts.

```bash
npx @ditsmod/cli start [entryFile] [options]
```

#### Options
* `-p, --project <path>`: Path to TypeScript config file or project directory (supporting TS Project References). Default: `tsconfig.build.json`.
* `-e, --exec <binary>`: Binary to execute the entry file (e.g., `node`). Default: `node`.
* `-d, --debug [hostport]`: Run Node.js in debug mode with the `--inspect` flag.
* `--env-file <paths...>`: Environment file(s) to load into `process.env` (Node.js >= v20).
* `--entry-file <file>`: Relative path to the compiled JavaScript entry file. Default: `dist/main.js`.
* `--watch-assets <globs...>`: Non-TypeScript asset globs to watch and copy to `dist/` (e.g. `"src/**/*.json"`).
* `--preserve-watch-output`: Do not clear the terminal screen between compilation cycles.

#### Examples
```bash
# Start application with custom entry file and inspect debugger enabled on port 9229
npx @ditsmod/cli start tmp.ts -d 9229

# Start with environment file and watch json assets
npx @ditsmod/cli start --env-file .env.local --watch-assets "src/**/*.json"
```

---

## AI Agent Usage Rules

> [!WARNING]
> `@ditsmod/cli start` is designed for **human developers** to run interactively in their terminal.
> **AI agents must NOT start long-running background compilation/watch processes (`ditsmod start`)** during normal coding or editing cycles unless explicitly requested by the user, as this can lead to memory leaks, orphaned background processes, and blocked ports.
>
> If an agent needs to verify compilation or run tests, it should use standard one-off build/test scripts (like `npm run build` or `npm run test`) instead of interactive watch mode.

---

## Programmatic API

`@ditsmod/cli` exports classes and command helper functions:

```ts
import { WatchCompiler, ProcessManager, AssetWatcher, startCommand, newCommand } from '@ditsmod/cli';
```
