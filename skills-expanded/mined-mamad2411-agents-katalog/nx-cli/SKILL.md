---
name: nx-cli
description: |
  Guide for using the Nx CLI in the MCS Products Mono UI workspace to discover projects, run targets, generate code, inspect affected scope, and troubleshoot cache or workspace state. Use this skill when working with Nx commands, project targets, generators, task graphs, or repository-specific Nx workflows. Keywords: nx, cli, run-many, affected, generate, graph, show, monorepo, cache, angular, cypress
---

# Nx CLI for MCS Products Mono UI

Use `nx` as the default interface for workspace tasks in this repository. Prefer `nx` commands over `npm` wrappers unless a task explicitly depends on a custom repository script.

## When to Use This Skill

Activate this skill when:

- You need the correct project name before running a target
- You need to run `build`, `lint`, `test`, `component-test`, `e2e`, or `serve`
- You need to run the same target across multiple or affected projects
- You need to generate an app, library, or component
- You need to inspect project configuration, graphs, or workspace state
- You need to bypass cache or recover from stale Nx or daemon state

## Repository-Specific Rules

- Prefer `nx run`, `nx run-many`, `nx affected`, and `nx show` over raw tool invocations.
- When bypassing cache in this repository, add `--skip-nx-cache`.
- Default to Chrome for Cypress component and E2E work in this repository, and treat it as required for webcam-related tests:
  - `nx component-test <project> --browser=chrome`
  - `nx e2e <project> --browser=chrome`
- Use the custom `@rls/plugin` generators for new apps and components:
  - `nx g @rls/plugin:angular-app ...`
  - `nx g @rls/plugin:component ...`
- Use official Nx generators for new libraries:
  - `nx g @nx/angular:library ...`
  - `nx g @nx/js:library ...`
- If Nx behaves strangely, run `nx reset`.
- This workspace currently uses Nx 20.x. If online docs mention commands you do not have locally, trust `nx --help` and `nx --version` in the current workspace.
- If `nx` is not on `PATH`, run the local binary directly:
  - `./node_modules/.bin/nx <command>`

## Quick Command Chooser

| Need                                     | Command                                                                                     |
| ---------------------------------------- | ------------------------------------------------------------------------------------------- |
| Find project names                       | `nx show projects`                                                                          |
| Filter projects by pattern or target     | `nx show projects --projects "*specimen*"`, `nx show projects --with-target component-test` |
| Inspect one project                      | `nx show project <project> --json`                                                          |
| Run one target                           | `nx run <project>:<target>[:configuration]`                                                 |
| Use shorthand target syntax              | `nx build <project>`, `nx lint <project>`, `nx test <project>`                              |
| Run the same target across many projects | `nx run-many -t <target>`                                                                   |
| Run only changed scope                   | `nx affected -t <target>`                                                                   |
| Visualize dependencies or task selection | `nx graph`, `nx run <project>:<target> --graph=stdout`                                      |
| Generate code                            | `nx g <generator>`                                                                          |
| Fix stale cache or daemon state          | `nx reset`, `nx report`, `nx repair`                                                        |

## Common Workflows

### 1. Discover Projects and Targets

```bash
nx show projects
nx show projects --with-target component-test
nx show projects --projects "*order*"
nx show project order-search-feat --json
nx list
```

Use `nx show` first when you do not know the exact project name or want to confirm available targets before running them.

### 2. Run Tasks for One Project

```bash
nx serve rls-accession-portal-ui
nx build rls-accession-portal-ui
nx lint order-search-feat
nx test order-search-feat
nx component-test order-search-feat --browser=chrome
nx e2e rls-specimen-accessioning-e2e --browser=chrome
```

Use `nx run <project>:<target>` when you need the fully explicit form:

```bash
nx run order-search-feat:component-test --browser=chrome
nx run rls-accession-portal-ui:build:production
```

### 3. Run Tasks Across Multiple or Affected Projects

```bash
nx run-many -t lint test build
nx run-many -t component-test --projects=order-search-feat,order-search-ui --browser=chrome
nx affected -t lint test build --base=develop --head=HEAD
nx affected -t component-test --base=develop --head=HEAD --browser=chrome
```

Use `run-many` when you already know the target project set. Use `affected` when the task should follow the changed dependency graph.

### 4. Generate Code Using Repository Conventions

```bash
nx g @rls/plugin:angular-app myapp --scope=myapp --directory=apps/myapp --product=pearls
nx g @rls/plugin:component my-component
nx g @nx/angular:library my-lib
nx g @nx/js:library util-lib
```

Prefer the custom `@rls/plugin` generators for new applications and components so the repository's testing, config, and pipeline conventions are applied automatically.

### 5. Inspect Project Graphs and Task Graphs

```bash
nx graph
nx graph --focus=order-search-feat
nx run order-search-feat:component-test --graph=stdout
nx affected -t build --graph=stdout
```

Use `nx graph` to understand dependency relationships. Use `--graph=stdout` when you need task selection details in a terminal-only workflow.

### 6. Format and Sync the Workspace

```bash
nx format:check
nx format:write
nx sync
nx sync:check
```

Run `sync` or `sync:check` when generators or plugins may need to update workspace-managed files.

### 7. Reset or Repair Workspace State

```bash
nx reset
nx reset --only-cache
nx reset --only-daemon
nx report
nx repair
```

Use `nx repair` sparingly. It is most helpful after an Nx version update that did not go through the normal migration flow.

## Decision Rules

- If you do not know the project name, start with `nx show projects`.
- If you know the project and target, use `nx run` or shorthand target syntax.
- If the same target must run on multiple specific projects, use `nx run-many`.
- If only changed projects should run, use `nx affected`.
- If you need to inspect project configuration or targets, use `nx show project <project> --json`.
- If a command from online docs is missing locally, trust `nx --help` in this workspace instead of assuming the docs match the installed version.

## Troubleshooting

| Problem                                         | Fix                                                                                                 |
| ----------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| Nx returns stale results                        | Add `--skip-nx-cache`; if results still look wrong, run `nx reset`.                                 |
| Daemon or workspace state seems corrupted       | Run `nx reset --only-daemon` or a full `nx reset`.                                                  |
| You are not sure which project owns a feature   | Start with `nx show projects`, then inspect likely matches with `nx show project <project> --json`. |
| You need to understand why tasks were selected  | Use `--graph=stdout` or `nx graph --focus=<project>`.                                               |
| Browser-based Cypress work fails outside Chrome | Re-run with `--browser=chrome`.                                                                     |
| Online docs mention commands you do not have    | Check `nx --help`; command availability depends on the installed Nx version.                        |
| Older examples use `nx affected --all`          | Prefer `nx run-many` instead.                                                                       |
