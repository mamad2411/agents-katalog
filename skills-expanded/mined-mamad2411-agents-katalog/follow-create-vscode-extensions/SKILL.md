---
name: follow-create-vscode-extensions
description: Build VSCode extensions with TypeScript, official generator, or reactive-vscode
argument-hint: "[scope]"
related:
  - follow-create-bun-cli
  - follow-create-sdk
  - follow-lang-typescript
  - follow-release
  - follow-tool-vite
  - run-test
  - deep-review-codebase
  - report

---
## Goal

Create a VSCode extension project in TypeScript with a `package.json` manifest, commands, activation events, contribution points, build, package, and publish

## Scope

For building general VSCode extensions, supporting the official `yo generator-code`, `reactive-vscode`, and manual setup

- Packages: `generator-code`, `@vscode/vsce` (`vsce` is deprecated/renamed — requires Node 20+) — always confirm the VS Code/latest versions with `/deep-research` + `/follow-best-practice` (not pinned in this file — per `/update-devin-global-skills`)

## Execute

### 1. Review Tech Stack

> Goal: Review the tech stack before building

1. Run `/deep-research` + `/follow-best-practice` to confirm the latest versions and patterns, then run `/deep-review-codebase` to summarize the tech stack
2. Run `/deep-review-codebase` to review the tech stack, dependencies, and library design (create vscode extensions)
3. Record the rationale for the chosen stack and libraries for future reference (create vscode extensions)

### 2. Setup Project

> Goal: Create the extension structure

1. Option A (official): `bun add -g yo generator-code` then run `yo code`, or one-off `bunx -p yo -p generator-code yo code`
2. Option B: `bun create reactive-vscode` or `bun add -D reactive-vscode`
3. Option C: create `package.json`, `tsconfig.json`, `src/` yourself
4. Create `src/extension.ts`, `README.md`, `CHANGELOG.md`, `.vscodeignore`

### 3. Configure Package And Manifest

> Goal: Define `package.json` per the VSCode schema

1. Specify `name`, `displayName`, `description`, `version`, `publisher`
2. Specify `engines.vscode` such as `^<major>.0.0` based on the latest VS Code version from your research
3. Specify `categories`, `keywords`, `activationEvents`, `main`
4. Specify `contributes.commands`, `menus`, `keybindings`, `configuration`
5. Specify `scripts` for `compile`, `watch`, `package`, `publish`

### 4. Implement Extension

> Goal: Implement the extension logic

1. Create `src/extension.ts` with `activate(context: vscode.ExtensionContext)`
2. Register commands with `vscode.commands.registerCommand`
3. Push disposables into `context.subscriptions`
4. Use `reactive-vscode` if you chose option B

### 5. Build And Watch

> Goal: Compile TypeScript

1. Install `esbuild` or `tsc`
2. Configure `tsconfig.json` with `strict: true`
3. Run `bun run watch` for dev
4. Run `bun run compile` for build

### 6. Test In Extension Host

> Goal: Test in VSCode

1. Open the project in VSCode
2. Press `F5` to launch the Extension Development Host
3. Test the commands and features
4. Check the Debug Console
5. For automated tests use `@vscode/test-cli` + `@vscode/test-electron`, run via the `vscode-test` CLI

### 7. Package And Publish

> Goal: Create the `.vsix` and publish

1. Install `@vscode/vsce` (the `vsce` package was renamed/deprecated) or the `reactive-vscode` CLI
2. Run `bunx @vscode/vsce package` to create the `.vsix` (use `--allow-missing-repository` only when there is no git repo)
3. Create a publisher account in the Marketplace
4. Run `bunx @vscode/vsce publish` or use GitHub Actions
5. Run `/ship`

## Rules

- TypeScript first
- `engines.vscode` must match the API you use
- Use `context.subscriptions.push` for every disposable
- Never hardcode secrets or absolute paths
- `activationEvents` must match the actual command or event
- Use `@vscode/vsce` for packaging and publishing (the old `vsce` was renamed)

- Use /follow-create-bun-cli when needed
- Use /follow-create-sdk when needed
- Use /follow-lang-typescript when needed
- Use /follow-release when needed
- Use /follow-tool-vite when needed
- Use /run-test when needed
- Use /report when needed

## Expected Outcome

- VSCode extension builds successfully
- Extension works in the Extension Development Host
- `.vsix` can be created
- Ready to publish to the VSCode Marketplace

