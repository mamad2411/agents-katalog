---
name: follow-tool-aube
description: Guidelines for using the Aube package manager for Node.js projects
argument-hint: "[scope]"
related:
  - use-agent-browser
  - use-astgrep
  - follow-tool-auto-it
  - follow-tool-usage
  - follow-best-practice
  - setup-cicd
---

## Goal

Use Aube as the primary Node.js package manager for projects that need high speed, security, and maximum efficiency

## Scope

Use `follow-tool-aube` for the specified tasks and workflows

- Boundary: Aube is a Node.js package manager (install/run/update deps) — use it instead of `npm`/`pnpm`/`yarn`/`bun install` when the project chose Aube; for Bun runtime setup see `/use-bun-native-api`, for CI work see `/setup-cicd`
- Latest: `aube@2.4.0` (GitHub `aubepkg/aube`, crates.io `aube`) / npm `@endevco/aube@2.4.0` (npm dist-tag lags) (verified 2026-09-26)
- References:  | [apis](references/apis.md) | [cli](references/cli.md) 
## Execute

### 1. Installation

> Goal: install Aube and verify the version

1. Install Aube with `mise use -g aube` (recommended) or `brew install jdx/tap/aube`, `cargo install aube --locked`, `npm i -g @endevco/aube` — see other methods at https://aube.jdx.dev/installation
2. Verify the version with `aube --version`
3. Aube auto-installs dependencies when running scripts automatically

### 2. First Run

> Goal: first run using existing lockfiles

1. Aube reads and writes existing lockfiles (yarn.lock, pnpm-lock.yaml, package-lock.json)
2. No per-project lockfile migration needed — Aube supports all of them
3. Run scripts normally — Aube auto-installs when dependencies change

### 3. Daily Commands

> Goal: use `aubr` and `aubx` correctly per use case

Use `aubr` for running scripts that need dependencies:

```bash
aubr test      # run test script, auto-installs first
aubr build     # run build script, auto-installs first
aubr dev       # run dev script, auto-installs first
```

Use `aubx` for one-off tools that do not need dependencies:

```bash
aubx vitest    # run vitest without installing
aubx tsc       # run tsc without installing
```

Use `aube exec` for local binaries already installed in the project:

```bash
aube exec vitest
aube exec tsc -- --noEmit
```

### 4. Dependency Management

> Goal: manage dependencies with Aube

```bash
aube add react          # add dependency
aube add -D vitest      # add dev dependency
aube remove react       # remove dependency
aube update             # update dependencies within package.json ranges
```

### 5. Security Configuration

> Goal: add, remove, and update dependencies with Aube

Aube ships optimal security defaults:
- Trust downgrades fail at resolve
- New releases have a 24h cooling window
- Known-malicious packages are blocked
- Prompt on near-zero-download installs
- Lifecycle scripts wait for approval
- Exotic transitive deps blocked

Enable paranoid mode for maximum security in `aube-workspace.yaml`:

```yaml
# aube-workspace.yaml
paranoid: true
```

Approve lifecycle build scripts with `aube approve-builds` or set `allowBuilds` in `aube-workspace.yaml`

### 6. CI Integration

> Goal: use Aube in CI without a separate install step

```yaml
- uses: jdx/aube-action@v1
- run: aubr test
```

Aube auto-installs and caches dependencies automatically

### 7. Workspace Support

> Goal: Aube supports workspaces and monorepos
- Global content-addressable store for sharing package files
- Reduced disk usage without copying all dependencies into each project
- Efficient node_modules layout
- Run across all workspaces with `aube -r run build` or filter with `aube -F '@scope/*' run test`

### 8. Lockfile Compatibility

> Goal: Aube supports multiple lockfile types
- yarn.lock
- pnpm-lock.yaml
- package-lock.json

Reads and writes lockfiles in place without migration

## Rules

### 1. Command Selection

Pick the command by use case:
- aubr: for running scripts that need dependencies (test, build, dev)
- aubx: for one-off tools that need no dependencies (vitest, tsc)
- aube add: for adding dependencies
- aube remove: for removing dependencies
- aube update: for updating dependencies

### 2. Auto-Install Behavior

- Aube auto-installs when running scripts with `aubr`
- Install is skipped when dependencies are fresh on repeat runs
- Use `aubx` for tools that need no install

### 3. Security Best Practices

- Enable `paranoid: true` for production
- Review lifecycle scripts before approving
- Block exotic transitive dependencies
- Trust downgrades fail at resolve

### 4. Lockfile Strategy

- Use existing lockfiles (yarn.lock, pnpm-lock.yaml, package-lock.json)
- No per-project lockfile migration needed
- Aube reads/writes lockfiles in place

### 5. Disk Optimization

- Global content-addressable store reduces disk usage
- Package files shared across projects
- Efficient node_modules layout

- Use /use-agent-browser if needed
- Use /use-astgrep if needed
- Use /follow-tool-auto-it if needed
- Use /follow-tool-usage if needed
- Use /follow-best-practice if needed
- Use /setup-cicd if needed

- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- Aube installed and working
- Auto-install dependencies when running scripts
- Optimal security defaults
- Reduced disk usage via the global store
- Support for multiple lockfile types
