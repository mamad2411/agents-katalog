---
name: check-monorepo
description: Check whether a project is a monorepo
argument-hint: "[scope|boundaries|pipeline|config]"
related:
  - follow-monorepo
  - follow-tasks
  - follow-tool-moonrepo
  - report
  - run-build
  - run-test
---
## Goal

Determine whether the project is a monorepo so the appropriate structure can be chosen.

## Scope

Use to check the project type before starting work that requires knowing whether it is a monorepo.

## Execute

### Workflows

> Goal: dispatch to the domain workflow based on the argument — always run the detection flow (Steps 1-4) first

| Domain/Argument | Workflow |
|-----------------|----------|
| `boundaries` | `workflows/boundaries/SKILL.md` — cross-package imports, layer violations, cycles |
| `pipeline`, `tasks` | `workflows/pipeline/SKILL.md` — task coverage, orphan projects, cache config |
| `config` | `workflows/config/SKILL.md` — declared vs actual workspaces, manifest coherence, tool drift |

1. If the argument specifies a domain → run detection first (Steps 1-3) to confirm it is a monorepo, then read and execute `workflows/<domain>/SKILL.md`
2. If no domain is given → run only the detection flow (Steps 1-4), then suggest domains worth checking next

### 1. Check Package Manifests

> Goal: Check Package Manifests

Inspect the root `package.json` and the package manager workspace files for the workspaces configuration.

1. Read `package.json` at the project root
2. Check whether a `workspaces` field exists
3. Check `pnpm-workspace.yaml` or `bunfig.toml` for package manager workspaces
4. If a `workspaces` field or a package manager workspace file is present, continue to the next steps
5. If neither exists, go to Step 3 and check for other monorepo tools such as Moonrepo before reporting

### 2. Check Workspace Directories

> Goal: Check Workspace Directories

Verify that workspace directories actually exist, covering both package workspaces and Moonrepo projects.

1. If `package.json` or `pnpm-workspace.yaml` has a `workspaces` field, read the patterns (e.g. `apps/*`, `integrations/*`, `server/*`, `shared/*`)
2. Verify that the directories matching the glob patterns exist
3. For Moonrepo, read `.moon/workspace.yml` or `.moon/projects.yml` to see the `projects` mapping
4. List all workspaces found

### 3. Check Monorepo Tools

> Goal: Check Monorepo Tools

Check for monorepo management tools, both package-workspace based and tool-based.

1. Check whether `turbo.json` (Turborepo) exists
2. Check whether `pnpm-workspace.yaml` (pnpm workspaces) exists
3. Check whether `lerna.json` (Lerna) exists
4. Check whether `nx.json` (Nx) exists
5. Check whether a `.moon/` directory with `.moon/workspace.yml` or `.moon/projects.yml` exists (Moonrepo)
6. If there is no `workspaces` field in `package.json` but `.moon/` exists, treat the project as a monorepo

### 4. Report Result

> Goal: Report Result

Report the check result along with the appropriate run command.

1. Report whether the project is a monorepo
2. If it is a monorepo, list all workspaces
3. If it is a monorepo, name the monorepo tool in use
4. Give the common run command pattern, e.g. `moon run <project>:<task>` for Moonrepo or `<tool> run <task>` for Turborepo/pnpm
5. Use `/report` for the output

## Rules

### 1. Detection Criteria

- A `workspaces` field in `package.json` or a package manager workspace file = monorepo
- `turbo.json`, `pnpm-workspace.yaml`, `lerna.json`, `nx.json`, or a `.moon/` directory = monorepo
- If none of the above conditions match = single project

### 2. Output Format

- State the result as `monorepo` or `single-project`
- If it is a monorepo, list all workspaces and the monorepo tool

- Use /follow-monorepo if needed
- Use /follow-tasks if needed
- Use /follow-tool-moonrepo if needed
- Use /run-build if needed
- Use /run-test all if needed

## Expected Outcome

- Know whether the project is a monorepo, not limited to `package.json` workspaces alone
- If it is a monorepo, know all workspaces, the tool in use, and the run command pattern
