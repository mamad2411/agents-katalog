---
name: follow-release-deploy-vscode-marketplace
description: Publish a VS Code extension to the Marketplace with vsce — package, publish, verify
argument-hint: "[version-bump]"
related:
  - run-release
  - run-check
  - follow-secret-manager
  - open-web-for-config-secret
  - resolve-errors
  - learn
---

## Goal

Publish a VS Code extension to the Marketplace with `vsce` — complete metadata, auth ready, publish then verify on the Marketplace

## Scope

- covers: manual publish with `@vscode/vsce` — metadata, PAT auth, package, publish, verify
- CI automation → follow the parent `/follow-release` Step 5
- note: the original `vsce` package was renamed to `@vscode/vsce`

## Execute

### 1. Verify Extension Metadata

> Goal: `package.json` is ready to publish

1. check required fields: `publisher`, `name`, `version`, `displayName`, `description`, `engines.vscode`
2. check recommended fields: `repository`, `icon`, `categories`, `keywords`, `license`
3. check `.vscodeignore` excludes dev files from the package

### 2. Setup vsce And Auth

> Goal: `vsce` works and is authenticated

1. install `bun add -D @vscode/vsce`, then use `bunx vsce`
2. create a publisher on the Marketplace (if none yet) — use `/open-web-for-config-secret` to open the manage page
3. create a PAT from Azure DevOps (scope Marketplace → Manage), store it as `VSCE_PAT` via `/follow-secret-manager`
4. `vsce login <publisher>` or use `vsce publish -p <PAT>` for non-interactive/CI

### 3. Package And Check

> Goal: the `.vsix` is correct before publishing

1. run `/run-check` — tests/typecheck pass
2. run `vsce package` to create the `.vsix`, then check contents/warnings
3. check the version bump is correct per semver — `vsce publish` can bump for you (e.g. `vsce publish minor`); if unsure, check the official docs

### 4. Publish

> Goal: the extension reaches the Marketplace

1. run `vsce publish` (the bump can be given in the command)
2. or `vsce publish -p <PAT>` for non-interactive
3. record the published version

### 5. Post-Publish Verify

> Goal: the extension installs from the Marketplace

1. check the extension page on the Marketplace (propagation may take a short while)
2. verify the install: search in the VS Code Extensions view or `code --install-extension <publisher>.<name>`
3. if the publish went wrong → `vsce unpublish <publisher>.<name>` (destructive — emergencies only, requires user confirmation), then `/resolve-errors`
4. success → report the version, then run `/run-release` if the parent needs a multi-platform release

## Rules

### 1. Unpublish Is Destructive

- `vsce unpublish` removes the extension from the Marketplace — emergencies only, requires user confirmation
- for a published version, prefer a new bump over unpublishing whenever a fix is possible

### 2. Token Safety

- `VSCE_PAT` only through `/follow-secret-manager` — never commit it or put it in scripts

### 3. Docs First

- new `@vscode/vsce` flags/features → check official docs via `/learn-from-web` instead of guessing

## Expected Outcome

- the extension published on the Marketplace with the new version
- it installs for real from the Marketplace
