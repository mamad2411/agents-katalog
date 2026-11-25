---
name: npm-global-package-path-discovery
description: Industrial protocol for locating the exact filesystem path of globally installed npm packages and their executable shims, including mise-managed Node environments.
category: Environment-Management
---

# NPM Global Package Path Discovery Skill

This skill defines the canonical workflow for discovering where a globally installed npm package actually lives on disk,
and whether it provides an executable shim in the global bin directory.

Use this whenever the user asks where a package was installed after `npm install --global <pkg>`.

***

## 1. Environment And Dependency Verification

Before running discovery commands, verify that the required tooling exists.

### 1.1 Required tools

- `npm`
- `node`
- `which` or `command -v`

### 1.2 Verification sequence

Run the following checks in order.

```bash
which npm
npm --version
node --version
```

Command breakdown:

- `which npm`: prints the exact npm executable resolved from PATH.
- `npm --version`: confirms npm is callable and reports active version.
- `node --version`: confirms Node runtime for package metadata inspection.

If npm is missing or mismatched with expected environment management, refer to
[mise-tool-management](../mise-tool-management/SKILL.md) and
[system-wide-tool-management](../system-wide-tool-management/SKILL.md).

***

## 2. Core Discovery Workflow

### 2.1 Resolve global root and prefix

```bash
npm root -g
npm prefix -g
```

Command breakdown:

- `npm root -g`:
    - `root`: prints npm package root directory.
    - `-g`: targets the global scope, not local project dependencies.
- `npm prefix -g`:
    - `prefix`: prints global installation prefix.
    - `-g`: forces global mode.

Expected relationship:

- Package directory pattern: `<global-root>/<package-name>`
- Global bin directory pattern: `<global-prefix>/bin`

### 2.2 Resolve exact package installation path

```bash
npm list -g <package-name> --parseable
```

Command breakdown:

- `list`: prints installed dependency tree.
- `-g`: restricts query to globally installed packages.
- `<package-name>`: narrows result to the target package.
- `--parseable`: returns machine-friendly absolute paths instead of tree glyphs.

Primary result interpretation:

- If found, first path is the package directory.
- If not found, package is not installed in this npm global context.

### 2.3 Inspect package metadata for CLI shim availability

```bash
node -p "const p=require('$(npm root -g)/<package-name>/package.json'); ({name:p.name,version:p.version,main:p.main,bin:p.bin})"
```

Command breakdown:

- `node -p`: evaluates JavaScript expression and prints result.
- `require(...)`: loads target package.json.
- `p.bin`: reports declared executable map.

Interpretation:

- `bin` present: npm should create one or more shims in global bin.
- `bin` absent or `undefined`: no direct CLI command is generated.

### 2.4 Resolve executable shim path if present

```bash
command -v <package-command>
ls -la "$(npm prefix -g)/bin"
```

Command breakdown:

- `command -v <package-command>`: shell built-in lookup for runnable command path.
- `ls -la "$(npm prefix -g)/bin"`:
    - `-l`: long listing with symlink targets.
    - `-a`: includes hidden files where relevant.

If the command exists, capture both:

1. Resolved shim path.
2. Symlink target under global bin.

### 2.5 Optional direct package directory proof

```bash
npm explore -g <package-name> -- pwd
```

Command breakdown:

- `explore`: runs a command in package directory context.
- `-g`: targets global package context.
- `-- pwd`: executes `pwd` inside the package directory.

This gives a direct directory proof from npm itself.

***

## 3. Reporting Contract

When returning results, always provide:

1. npm executable path (`which npm`).
2. Global root (`npm root -g`).
3. Global prefix (`npm prefix -g`).
4. Exact package path.
5. Whether package exposes a CLI shim (`bin` field).
6. Shim path in global bin if available.
7. Direct runtime fallback command (`node <main-entry>`) when no shim exists.

Example fallback pattern when no CLI shim exists:

```bash
node "$(npm root -g)/<package-name>/<main-entry-file>"
```

***

## 4. Failure Modes And Recovery

### 4.1 Package absent in current global context

Symptoms:

- `npm list -g <package-name> --parseable` returns no package path.

Recovery:

- Re-check active npm executable with `which npm`.
- Confirm active Node context when using `mise` (multiple Node installs can coexist).

### 4.2 Command not found despite global install

Symptoms:

- Package exists at global root, but `command -v <package-command>` returns nothing.

Recovery:

- Inspect `bin` field in package.json.
- If `bin` is undefined, this is expected behavior; run package entry via node.
- If `bin` exists, verify `<prefix>/bin` is present on PATH.

### 4.3 Mismatched shell context

Symptoms:

- One terminal sees the package; another does not.

Recovery:

- Compare `which npm` and `npm prefix -g` across both shells.
- Align shell initialization for `mise` activation.

***

## 5. Related Skills

- [mise-tool-management](../mise-tool-management/SKILL.md): for resolving mismatched mise-managed Node/npm
  environments.
- [system-wide-tool-management](../system-wide-tool-management/SKILL.md): for verifying or installing missing
  system-level tools needed by this workflow.

## 6. Traceability

- Conversation context: user requested a reusable skill after diagnosing the global npm install location and
  executable behavior for `mcp-ssh`.
- This skill is intentionally scoped to npm global package path discovery and CLI-shim verification.
