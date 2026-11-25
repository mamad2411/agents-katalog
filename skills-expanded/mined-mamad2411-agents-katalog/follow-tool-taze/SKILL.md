---
name: follow-tool-taze
description: Use Taze for automated dependency management in projects and monorepos
argument-hint: "[scope]"
related:
  - follow-tool-turborepo
  - follow-monorepo
  - follow-tasks
  - follow-tool-semantic-release
  - follow-tool-renovate
  - run-install
---

## Goal

Use Taze to check and update dependencies automatically, in both single projects and monorepos

## Scope

Use for projects or workspaces that need to keep dependencies up-to-date via the Taze CLI

- Boundary: Taze is for interactive/manual dependency bumps in a repo; for automated PR-based updates use `/follow-tool-renovate` instead
- Latest: `taze@21.1.0` (verified 2026-09-13)

## Execute

### Workflows

| Topic | Workflow |-------|----------| Install, `major`/`minor`/`latest` checks, monorepo `-r` usage | `workflows/setup-taze/SKILL.md` 
### 1. Run Taze

> Goal: Start checking for updates

1. Run `bunx taze` to scan dependencies
2. Use `bunx taze major|minor|patch|latest` per the desired mode
3. Use `bunx taze --json` for machine-readable output
4. See options details in 

### 2. Configure Update Behavior

> Goal: Set the mode and scope of the update

1. Use `-r` for a recursive scan in a monorepo
2. Use `-w` to write into `package.json`
3. Use `-i` to install dependencies after the bump
4. Use `-I` for interactive mode
5. Run `bunx taze latest -r -w -i` when a full update is wanted

### 3. Add to Package Scripts

> Goal: Make Taze run automatically

1. Add a `prepare` script in `package.json`: `"prepare": "bunx taze latest -w -r -i"`
2. Check that `prepare` doesn't break CI
3. Use a `pre-commit` hook if preferred over `prepare`
4. See package scripts example in 

### 4. Advanced Configuration

> Goal: Tune the Taze config for the project

1. Create `taze.config.ts` when a complex config is needed
2. Set `exclude`, `include`, `packageMode`, `depFields`
3. Configure `ignorePaths` for `package.json` lookup
4. Use `maturityPeriodExclude` to exclude specific packages

### 5. Validate Updates

> Goal: Verify the updates don't break the project

1. Run `bun install` after writing
2. Run `bun run test` to verify
3. Run `bun run lint` and `bun run typecheck`
4. Review the `package.json` diff before committing

## Rules

### 1. Usage

- Use `bunx taze` for one-off runs
- Use `-r -w -i` for monorepo updates
- Use `--json` for agents and CI

### 2. Configuration

- Create `taze.config.ts` when there are package-specific rules
- Use `exclude` for packages that shouldn't be updated
- Set `packageMode` for packages needing a special mode

### 3. Safety

- Review the diff before committing
- Run tests after updating
- Never update dependencies in a production branch without review

### 4. Monorepo

- Use `-r` to scan every workspace
- Use `ignoreOtherWorkspaces` when needed
- Check compatibility across workspaces

- Use /follow-tool-turborepo if needed
- Use /follow-monorepo if needed
- Use /follow-tasks if needed
- Use /follow-tool-semantic-release if needed (tool taze)
- Use /follow-tool-renovate if needed
- Use /run-install if needed

## References

- [CLI reference](references/cli.md)

- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- Dependencies update automatically
- `package.json` scripts ready to use
- Updates pass tests and lint
- The monorepo manages dependencies coherently

