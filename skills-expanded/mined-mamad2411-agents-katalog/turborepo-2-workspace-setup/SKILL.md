---
name: turborepo-2-workspace-setup
description: Sets up and validates Turborepo 2 workspaces. Use when adopting Turborepo 2, reviewing root package.json, workspace globs, lockfiles, turbo.json, package scripts, or monorepo layout.
license: MIT
compatibility: Requires a JavaScript or TypeScript repository with Node.js tooling. Optional validation script uses bash and node.
---

# Turborepo 2 Workspace Setup

Use this skill for initial Turborepo 2 setup, adoption into an existing repository, and workspace baseline validation.

## When to Use

Use this skill when the user asks to:

- Add Turborepo 2 to a repository.
- Check whether a repository is ready for Turborepo 2.
- Create or repair `turbo.json` or `turbo.jsonc`.
- Review root `package.json`, `packageManager`, lockfile, and workspaces.
- Add baseline build, lint, test, typecheck, or dev tasks.
- Validate workspace package layout.

## First Checks

Before editing files:

1. Identify the package manager from the lockfile:
   - `pnpm-lock.yaml`
   - `package-lock.json`
   - `yarn.lock`
   - `bun.lock` or `bun.lockb`
2. Inspect root `package.json`.
3. Confirm a root `packageManager` field exists or propose one matching the lockfile.
4. Inspect workspace declarations:
   - `pnpm-workspace.yaml` for pnpm.
   - `workspaces` in root `package.json` for npm, Yarn, or Bun.
5. Inspect root `turbo.json` or `turbo.jsonc`.
6. Inspect package `package.json` scripts before registering tasks.
7. Do not switch package managers unless the user explicitly asks.

## Workflow Reference

Use the workflow when adopting Turborepo 2 into an existing repository:

```text
workflows/turborepo-2-adopt-existing-repo-workflow.md
```

## Resources

Use this checklist during setup and review:

```text
resources/turborepo-2-workspace-checklist.md
```

## Examples

Use this baseline only as a starting point:

```text
examples/turborepo-2-turbo-json-baseline.md
```

Adjust task names, outputs, and environment variables to match the repository.

## Scripts

Before running the script, inspect its help:

```bash
.agents/plugins/turborepo-2/skills/turborepo-2-workspace-setup/scripts/turborepo-2-validate-workspace.sh --help
```

Run from the repository root:

```bash
.agents/plugins/turborepo-2/skills/turborepo-2-workspace-setup/scripts/turborepo-2-validate-workspace.sh .
```

The script is read-only. It reports missing baseline files and common Turborepo 2 readiness issues.

## Setup Strategy

### New Turborepo Workspace

For a new workspace, prefer official generators or the repository’s chosen package-manager workflow. After generation:

- Confirm `packageManager` is present.
- Confirm `turbo` is pinned in root dev dependencies.
- Confirm workspace globs are explicit and not nested ambiguous globs.
- Confirm root `turbo.json` uses `tasks`.
- Confirm package scripts match registered task names.

### Existing Repository Adoption

For an existing repository:

1. Preserve the current package manager.
2. Add or verify `packageManager`.
3. Add `turbo` as a root dev dependency using the current package manager.
4. Add root `turbo.json` with conservative tasks.
5. Register only scripts that already exist in packages, or add package scripts deliberately.
6. Run validation.
7. Run a small task such as lint or typecheck before broad build/test commands.
8. Keep migration commits small.

## Agent Safety

- Do not run codemods without approval.
- Do not rewrite all package scripts at once.
- Do not add framework-specific outputs unless the framework is already present.
- Do not use broad workspace globs like `apps/**` or `packages/**`.
- Do not delete lockfiles, `.turbo`, `node_modules`, or package folders without approval.
