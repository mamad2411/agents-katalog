---
name: follow-create-bun-cli
description: Build CLI applications with the Bun runtime per context and best practices
argument-hint: "[scope]"
related:
  - follow-create-cli
  - follow-create-web
  - use-bun-native-api
  - follow-tool-bunup
  - deep-review-codebase
  - flatten-directory
  - rethink
  - run-test

---
## Goal

Build high-performance CLI applications with the Bun runtime, structured per context.

## Scope

For building CLI applications with the Bun runtime — does not cover library bundling (see `/follow-tool-bunup`) — if Bun vs Rust is not yet decided, use `/follow-create-cli` to pick the stack first

- Packages: `bun`, `cac` (ESM-only — `cli.on` → `cli.addEventListener`), `picocolors`, `bunup` — always confirm the latest versions with `/deep-research` + `/follow-best-practice` (never pinned in this file — per `/update-devin-global-skills`); check the latest Bun native APIs via `/learn-from-cli` (`bun --help`)

## Execute

### 1. Review Tech Stack

> Goal: Verify the tech stack before building

1. Run `/deep-review-codebase` to summarize the tech stack in use
2. Run `/deep-review-codebase` to review the tech stack, dependencies, and library design (create bun cli)
3. Record the reasons for choosing the stack and libraries as a reference for the next step (create bun cli)

### 2. Setup Project Structure

> Goal: Create the project structure per a suitable architecture

1. Run `/deep-review-codebase` or `/deep-review-codebase` to choose the architecture per context — scaffold with `bun init` or `bunx @bunup/cli@latest create` if you want a template
2. Pick the structure by workload:
   - Simple CLI → `src/cli/`, `src/commands/`, `src/index.ts`, `src/utils/`
   - Needs to support multiple outputs/consumers → `src/core/`, `src/shell/`, `src/cli/`, `src/index.ts`
   - Multiple complex adapters → `src/core/`, `src/ports/`, `src/app/`, `src/adapters/`, `src/presentation/cli.ts`
3. Create entry points per the chosen architecture, e.g. `src/cli.ts`, `src/index.ts`, or `src/presentation/cli.ts`
4. If a directory nests deeper than 3 levels without need → run `/flatten-directory --mode code`

### 3. Configure Build Tools

> Goal: Configure build tools for production

1. Install `bunup` with `bun add -d bunup`
2. Create `bunup.config.ts` with `dts.splitting: true`
3. Install `picocolors` instead of `chalk` for terminal colors
4. Install `cac` instead of `commander` for argument parsing
5. Set in `tsconfig.json`: `declaration: true`, `isolatedDeclarations: true`

### 4. Setup Scripts

> Goal: Configure `package.json` scripts per `/follow-tasks`

1. Add `dev`: `bun run <cli-entry>` where `<cli-entry>` may be `src/cli.ts` or `src/presentation/cli.ts` per the chosen architecture
2. Add `build`: `bunx bunup`
3. Add `build:watch`: `bunx bunup --watch`
4. Add `lint`: `bunx tsc --noEmit && bunx biome lint --write`
5. Add `test`: `bun test`

### 5. Choose CLI Libraries and APIs

> Goal: Use lightweight libraries and Bun native APIs

1. Follow `/use-bun-native-api`, using `Bun.file`, `Bun.write`, `Bun.spawn`, `Bun.Glob` instead of `node:*`
2. Use `picocolors` for terminal colors
3. Use `cac` for argument parsing and command structure
4. Avoid `chalk`, `commander`, and `node:fs`/`node:child_process` when a Bun native equivalent exists

### 6. Development Workflow

> Goal: Use an efficient development workflow

1. Use `bun run dev` to run the CLI directly
2. Use `bun run build:watch` for watch build mode
3. Use `bun run build` for a production build
4. Run lint and typecheck before commit

### 7. Ship

> Goal: Deliver the work

1. Run `/ship`
2. If `ship` fails → report the status

## Rules

### 1. Project Structure

- Choose the architecture per context without forcing Clean or Layered
- Simple CLI → split `src/cli/`, `src/commands/`, `src/index.ts`, `src/utils/`
- Multiple outputs/consumers → split `src/core/`, `src/shell/`, `src/cli/`, `src/index.ts`
- Multiple complex adapters → use `src/core/`, `src/ports/`, `src/app/`, `src/adapters/`
- `presentation/cli.ts` or `src/cli.ts` is the CLI entry point per the chosen architecture
- `src/index.ts` = library entry point

### 2. Build Configuration

- Use `bunup` for building — see `/follow-tool-bunup` for config options
- Set `dts.splitting: true` for type declarations
- TypeScript: `declaration: true`, `isolatedDeclarations: true`
- Set `packages: "bundle"` in `bunup.config.ts` if you want zero runtime dependencies
- For single-file executable distribution, use `bun build --compile src/cli.ts --outfile mycli` or the bunup `compile` option

### 3. Scripts

- `dev` = run the CLI directly (`bun run src/presentation/cli.ts`)
- `build:watch` = `bunx bunup --watch`
- Use `bunx` instead of `npx`
- Run lint and typecheck before commit

### 4. Dependencies

- Use `picocolors` instead of `chalk`
- Use `cac` instead of `commander`
- Use Bun native APIs (`Bun.file`, `Bun.write`, `Bun.spawn`, `Bun.Glob`) instead of `node:*` modules
- Bundle dependencies with `bunup` to reduce runtime dependencies when appropriate

- Use /follow-create-web if needed
- Use /rethink if needed
- Use /deep-test cli if needed
- Use /run-test if needed


## Expected Outcome

- A CLI project structured per the chosen architecture and maintainable
- Directories not nested too deeply (use `/flatten-directory` if needed)
- `bun run dev` runs the CLI directly
- `bun run build` produces dist/ with type declarations
- Scripts consistent with `/follow-tasks`

## Examples

```text
project/
├── src/
│   ├── cli/              # CLI parsing
│   ├── commands/         # Command handlers
│   ├── services/         # Business logic
│   ├── types/            # Shared types
│   ├── utils/            # Utilities
│   └── index.ts          # Library entry
├── test/
├── package.json
├── bunup.config.ts
└── tsconfig.json
```

### `package.json` Scripts

```json
"scripts": {
  "dev": "bun run src/presentation/cli.ts",
  "build": "bunx bunup",
  "build:watch": "bunx bunup --watch",
  "lint": "bunx tsc --noEmit && bunx biome lint --write",
  "test": "bun test"
}
```

### `bunup.config.ts`

```ts
import { defineConfig } from "bunup";

export default defineConfig({
  dts: { splitting: true },
});
```

## Guide

- `/deep-review-codebase` — architecture selection
- `/use-bun-native-api` — Bun runtime setup, install, test, build
- `/follow-tool-bunup` — Bunup bundler configuration
- `/follow-tasks` — Scripts standards
- `/use-bun-native-api` — Bun native APIs instead of Node.js
- [Bun Documentation](https://bun.sh/docs)

