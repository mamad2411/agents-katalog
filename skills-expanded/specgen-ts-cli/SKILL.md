---
name: specgen-ts-cli
model: claude-opus-4-8
effort: high
description: >
  Generate a detailed specification document for building a distributable Node.js CLI
  application written in TypeScript. Uses Commander.js for command parsing, tsup for
  bundling, and @yao-pkg/pkg for cross-platform binary packaging (Windows, macOS, Linux).
  Interactive prompts (Inquirer.js), persistent user config (conf), project-level config
  (cosmiconfig), shell execution (execa), HTTP client (got), plugin system, and
  auto-update checking are configurable based on application needs.
  Standardized input: application name (mandatory), version (mandatory), command (optional).
  Use this skill whenever the user asks to create a spec, specification, blueprint, or
  technical design document for a new CLI tool, command-line application, terminal tool,
  or developer tool. Also trigger when the user says things like "spec out a new CLI",
  "design a TypeScript CLI", "write a technical spec for my CLI tool",
  "scaffold spec for a Node CLI", or any request describing a command-line application.
  Even if the user only mentions a subset (e.g., "CLI with config file support" or
  "distributable Node tool"), this skill likely applies â€” ask and confirm.
---

# TypeScript CLI Application Specification Generator

This skill generates a comprehensive specification document (Markdown) that serves as a
blueprint for building a distributable Node.js CLI application in TypeScript. The spec is
intended to be followed by a developer or coding agent to produce a fully functional,
packageable CLI tool.

The specification does NOT generate code. It produces a detailed, opinionated technical
document describing every layer of the application â€” from `package.json` configuration to
command action handlers to binary packaging â€” so that implementation becomes a mechanical
exercise.

## Technology Stack

### Core Stack (Always Included)

These are the fixed versions the spec targets. Do not deviate unless the user explicitly
requests different versions.

| Component       | Version  |
|-----------------|----------|
| Node.js         | 22.x LTS |
| TypeScript      | 5.x      |
| Commander.js    | 12.x     |
| tsup            | 8.x      |
| Zod             | 3.x      |
| Chalk           | 5.x      |
| Ora             | 8.x      |

> **Note:** Chalk 5.x and Ora 8.x are ESM-only packages. The project uses
> `"type": "module"` in `package.json` and targets ESM output from tsup.
> All imports use the `.js` extension suffix even for TypeScript source files.

### Optional Integration Versions

Include in the version table only when the corresponding integration is selected.

| Component              | Version | When Selected           |
|------------------------|---------|-------------------------|
| @inquirer/prompts      | 7.x     | Prompts = yes           |
| conf                   | 13.x    | User Config = yes       |
| cosmiconfig            | 9.x     | Project Config = yes    |
| better-sqlite3         | 11.x    | Local Database = yes    |
| drizzle-orm            | 0.36.x  | Local Database = yes    |
| env-paths              | 3.x     | Local Database = yes    |
| drizzle-kit            | 0.28.x  | Local Database = yes (dev) |
| execa                  | 9.x     | Shell Execution = yes   |
| got                    | 14.x    | HTTP Client = yes       |
| update-notifier        | 7.x     | Auto-update = yes       |
| @yao-pkg/pkg           | 5.x     | Binary Packaging = yes  |
| cli-table3             | 0.6.x   | Table Output = yes      |
| boxen                  | 8.x     | Banner/Box UI = yes     |
| glob                   | 11.x    | File Operations = yes   |

> **Async patterns (Polling, Inline Batch, Background Daemon) use no additional
> npm packages** â€” they are implemented entirely with Node.js built-ins
> (`setTimeout`, `process.kill`, `child_process.spawn`) and the packages already
> in the core stack (ora for progress, chalk for output). The async pattern type
> is detected from PRD.md NFRs and user stories; no new dependency version rows
> are needed.

## Core Dependencies (package.json)

The spec must include these in the `dependencies` configuration section (always):

- `commander` â€” CLI argument parsing and command routing
- `chalk` â€” Terminal colour output (ESM-only, v5+)
- `ora` â€” Spinner / progress indicators
- `zod` â€” Schema validation for config, arguments, and API payloads

Always in `devDependencies`:
- `typescript` â€” TypeScript compiler
- `tsup` â€” TypeScript bundler (esbuild-based, handles ESM, shebang injection)
- `vitest` â€” Unit and integration testing
- `@types/node` â€” Node.js type declarations
- `tsx` â€” TypeScript execution for scripts and development
- `eslint` + `@typescript-eslint/eslint-plugin` â€” Linting

### Conditional Dependencies

**If Prompts = yes:**
- `@inquirer/prompts` â€” Modern interactive prompts (officially maintained Inquirer v9+)

**If User Config = yes:**
- `conf` â€” Persistent user-level configuration stored in OS config directory

**If Project Config = yes:**
- `cosmiconfig` â€” Project-level config file loading (supports `.json`, `.yaml`, `.js`, `package.json`)

**If Local Database = yes:**
- `better-sqlite3` â€” Synchronous SQLite driver (no async complexity in CLI context)
- `drizzle-orm` â€” TypeScript-first ORM with schema-as-code and type-safe query builder
- `env-paths` â€” OS-correct data directory resolution (macOS / Linux / Windows)
- `@types/better-sqlite3` â€” TypeScript type declarations (devDependency)
- `drizzle-kit` â€” Migration generator and Drizzle Studio (devDependency)

**If Shell Execution = yes:**
- `execa` â€” Child process execution with better ergonomics and ESM support

**If HTTP Client = yes:**
- `got` â€” HTTP client with TypeScript-first design (ESM-only, v14+)

**If Auto-update = yes:**
- `update-notifier` â€” Non-blocking update checks against npm registry

**If Binary Packaging = yes (devDependency):**
- `@yao-pkg/pkg` â€” Compiles Node.js application into standalone executables

**If Table Output = yes:**
- `cli-table3` â€” Tabular terminal output with borders and alignment

**If Banner/Box UI = yes:**
- `boxen` â€” Bordered terminal box output (ESM-only)

**If File Operations = yes:**
- `glob` â€” File system globbing with ESM support

## When the Skill Triggers

Generate the spec when the user provides an **application name** and **version** that
corresponds to one of the custom applications defined in `CLAUDE.md`. The skill
reads all required inputs from the project's context files â€” no interactive Q&A is needed
for the core inputs.

The user invokes this skill by specifying the target application and version, for example:
- `/specgen-ts-cli my_tool v0.1.0`
- `/specgen-ts-cli my_tool v0.1.0 command:deploy`
- `/specgen-ts-cli "My Tool" v0.1.0`

The skill then locates the matching context folder and reads all input files automatically.

## Version Gate

Before starting any work, resolve the application folder first (see Input Resolution below), then check `CHANGELOG.md` in the application folder (`<app_folder>/CHANGELOG.md`):

1. If `<app_folder>/CHANGELOG.md` does not exist, skip this check (first-ever execution for this application).
2. If `<app_folder>/CHANGELOG.md` exists, scan all `## vX.Y.Z` headings and determine the **highest version** using semantic versioning comparison.
3. Compare the requested version against the highest version:
   - If requested version **>=** highest version: proceed normally.
   - If requested version **<** highest version: **STOP immediately**. Print: `"Version {requested} is lower than the current application version {highest} recorded in <app_folder>/CHANGELOG.md. Execution rejected."` Do NOT proceed with any work.

## Input Resolution

This skill uses standardized input resolution. Provide:

| Argument          | Required | Example           | Description                                 |
|-------------------|----------|-------------------|---------------------------------------------|
| `<application>`   | Yes      | `my_tool`         | Application name to locate the context folder |
| `<version>`       | Yes      | `v0.1.0`          | Version to scope processing                 |
| `command:<name>`  | No       | `command:deploy`  | Limit generation to a single command spec   |

### Application Folder Resolution

The application name is matched against root-level application folders:
1. Strip any leading `<number>_` prefix from folder names (e.g., `1_my_tool` â†’ `my_tool`)
2. Match case-insensitively against the provided application name
3. Accept snake_case, kebab-case, or title-case input (all match the same folder)
4. If no match found, list available applications and stop

### Auto-Resolved Paths

| File           | Resolved Path                          |
|----------------|----------------------------------------|
| PRD.md         | `<app_folder>/context/PRD.md`          |
| Command Models | `<app_folder>/context/model/`          |
| Output         | `<app_folder>/context/specification/`  |

### Version Filtering

When a version is provided, only include user stories, NFRs, and constraints from versions
<= the provided version. For example, if `v0.3.0` is specified:
- Include items tagged `[v0.1.0]`, `[v0.2.0]`, `[v0.3.0]`
- Exclude items tagged `[v0.4.0]` or later
- Version comparison uses semantic versioning order

### Command Filtering

When `command:<name>` is provided:
- Only generate the `SPEC.md` for that specific command
- Other existing command spec files remain untouched
- `SPECIFICATION.md` (root) gets a partial update â€” only that command's TOC entry is
  added or updated; all other entries are preserved as-is

## Gathering Input

The specification is driven by **four input sources** read from the project's context files.
The skill does NOT ask the user for prompts, config, packaging, or other choices â€” it
**determines** these automatically from the context.

### Input 1: Application Name (from CLAUDE.md)

From CLAUDE.md (already loaded in context), locate the target application under the
**Custom Applications** section. Extract:

- **Application name**: The section heading (e.g., "My Tool", "Deploy CLI")
- **Binary name**: The kebab-case executable name (e.g., `my-tool`, `deploy`)
- **Application description**: The description paragraph below the heading
- **Target audiences**: The "Used by" or "Consumers" list
- **Dependencies**: The "Depends on" list â€” primary source for determining optional components

The application name is used to derive:
- **Package name**: kebab-case of the application name with `@scope/` prefix if scoped
- **Binary name**: The `bin` entry in `package.json`
- **Main TypeScript namespace**: PascalCase (e.g., `MyTool`)

### Input 2: User Stories (from PRD.md)

Read `<app_folder>/context/PRD.md`. This file contains all user stories organized by
command. Extract:

- **Commands**: Each `## Command: <name>` or `### <CommandName>` section
- **User stories per command**: Tagged items like `[USCLI00101] As a user, I want to...`
  These define the functional requirements for each command's action handler and prompts

The user stories directly inform:
- Which arguments and options each command exposes
- What interactive prompts are shown (if any)
- What output the command produces (table, JSON, plain text)
- Which service methods are called

**Important:** Items with strikethrough (`~~text~~`) are deprecated. List them in the
"Removed / Replaced" subsection of the traceability table. Carry version tags through
to the generated specification's traceability section.

### Input 3: Non-Functional Requirements (from PRD.md)

Within the same `PRD.md`, each command has a `### Non Functional Requirement` section
with tagged items like `[NFRCLI0120]`. These inform:

- Output format requirements (JSON, table, plain text, `--output` flag)
- Performance constraints (timeout, caching)
- Security requirements (credential storage, token handling)
- Platform constraints (Windows compatibility, PATH requirements)

### Input 4: Command Model (from model/ folder)

Read `<app_folder>/context/model/MODEL.md` first as the index, then read the individual
command model files in each command subfolder.

**MODEL.md** provides:
- Summary table of all commands with argument/option counts
- Links to each command's detailed model files

**Per-command files** (e.g., `model/deploy/model.md`):
- Complete argument definitions with types and descriptions
- Option definitions with flags, types, defaults
- Config keys read or written by this command
- External services or APIs called

The command model directly maps to:
- `Command` argument and option declarations in Commander.js
- Zod schemas for config validation
- Service interface method signatures
- `--help` text content

## PRD.md Extended Sections

Before determining optional components, check PRD.md for the following extended sections:

### Architecture Principle Extraction

If PRD.md contains an `# Architecture Principle` section, extract patterns that affect CLI decisions:

| Pattern to Extract | How It Influences the Specification |
|---|---|
| "Container based deployment" | Include Dockerfile section; favor environment variables over config files |
| "Event-driven" | CLI may need webhook listeners or polling patterns |
| Async patterns (polling, batch, daemon) | Inform command handler async strategies |

If the section is absent, proceed with existing detection.

### High Level Process Flow Extraction

If PRD.md contains a `# High Level Process Flow` section:
1. Process flows describing CLI-initiated operations inform command action handler sequences
2. Each flow step can emit a spinner/progress update
3. Error handling chains follow the flow's error paths

If the section is absent, derive command flow from user stories only (existing behavior).

---

## Determining Optional Components

Instead of asking the user, the skill determines optional components by analyzing the
dependencies and requirements in `CLAUDE.md` and cross-referencing with `PRD.md` NFRs.

### Prompts Detection

| Content Pattern | Prompts Selection |
|---|---|
| NFRs mention "interactive", "ask user", "prompt for", "wizard" | Prompts = yes |
| User stories describe `--interactive` mode or guided setup | Prompts = yes |
| User stories describe `init`, `setup`, `configure` commands | Prompts = yes |
| All inputs are non-interactive flags | Prompts = no |

### User Config Detection

| Content Pattern | User Config Selection |
|---|---|
| NFRs mention "remember", "save preference", "user setting", "persist" | User Config = yes |
| Commands like `config set`, `config get`, `login`, `logout` exist | User Config = yes |
| NFRs mention "API key", "token storage", "credential" | User Config = yes |
| No persistent state needed | User Config = no |

### Project Config Detection

| Content Pattern | Project Config Selection |
|---|---|
| NFRs mention "project configuration", "workspace config", "per-project" | Project Config = yes |
| A config file like `.mytoolrc`, `mytool.config.js`, or `package.json#mytool` is referenced | Project Config = yes |
| Tool operates at project/workspace level | Project Config = yes |
| Tool is purely global/user-scoped | Project Config = no |

### Local Database Detection

| Content Pattern | Local Database Selection |
|---|---|
| NFRs mention "run history", "execution log", "audit trail", "activity log" | Local Database = yes |
| NFRs mention "cache", "local cache", "offline", "sync state", "last sync" | Local Database = yes |
| User stories describe `history`, `log`, `list runs`, `show recent` commands | Local Database = yes |
| User stories describe tracking multiple entities of the same type locally | Local Database = yes |
| NFRs mention "retain for X days", "auto-prune", "retention policy" | Local Database = yes |
| Data needs filtering, sorting, or aggregation beyond a simple list | Local Database = yes |
| All persistent data fits in simple key-value pairs (use `conf` instead) | Local Database = no |

> **Local Database vs `conf`:** If the data has multiple rows, grows over time, needs
> querying, or involves relationships â€” use SQLite. If it is a handful of user
> preferences or a single token â€” use `conf`.

### Shell Execution Detection

| Content Pattern | Shell Execution Selection |
|---|---|
| NFRs mention "run command", "execute", "spawn", "shell", "subprocess" | Shell Execution = yes |
| Commands orchestrate other CLI tools (git, docker, npm, etc.) | Shell Execution = yes |
| Build/deploy commands that invoke external binaries | Shell Execution = yes |

### HTTP Client Detection

| Content Pattern | HTTP Client Selection |
|---|---|
| CLAUDE.md "Depends on" references any REST API or web service | HTTP Client = yes |
| NFRs mention "API call", "webhook", "REST", "HTTP", "fetch" | HTTP Client = yes |
| Commands interact with cloud providers, registries, or dashboards | HTTP Client = yes |

### Auto-Update Detection

| Content Pattern | Auto-Update Selection |
|---|---|
| NFRs mention "notify of updates", "check for new version", "self-update" | Auto-update = yes |
| Application is distributed via npm or GitHub releases | Auto-update = yes (default) |
| Internal tool used only within a controlled environment | Auto-update = no |

### Binary Packaging Detection

| Content Pattern | Binary Packaging Selection |
|---|---|
| CLAUDE.md mentions "standalone binary", "no Node.js required", "self-contained" | Binary Packaging = yes |
| Target users are unlikely to have Node.js installed | Binary Packaging = yes |
| Distribution via GitHub releases, Homebrew, or Chocolatey is mentioned | Binary Packaging = yes |
| Published to npm for developer toolchain use | Binary Packaging = no (npm distribution only) |

### Async Pattern Detection

Three sub-types are detected independently. A single application may use more than one.

#### Polling Detection

| Content Pattern | Polling Selection |
|---|---|
| User stories describe `--watch`, `--follow`, `--wait`, `--poll` flags | Polling = yes |
| NFRs say "wait until complete", "follow progress", "tail status" | Polling = yes |
| Commands trigger async operations that have a terminal state (success/failed) | Polling = yes |
| All operations complete synchronously within the API call | Polling = no |

#### Inline Batch Detection

| Content Pattern | Inline Batch Selection |
|---|---|
| User stories describe processing "all records", "all items", "bulk import/export" | Inline Batch = yes |
| NFRs mention `--concurrency`, parallel processing, rate limiting | Inline Batch = yes |
| Commands iterate over a potentially large collection (files, API resources, DB rows) | Inline Batch = yes |
| NFRs mention "skip errors", "continue on failure", "bail on first error" | Inline Batch = yes |
| NFRs mention "resume", "checkpoint", "skip already processed" | Inline Batch = yes (+ Local Database) |
| Processing is always a single item | Inline Batch = no |

#### Background Daemon Detection

| Content Pattern | Background Daemon Selection |
|---|---|
| User stories describe `daemon start`, `daemon stop`, `daemon status` commands | Background Daemon = yes |
| NFRs mention "background process", "persistent watcher", "always-on agent" | Background Daemon = yes |
| User stories describe a `worker` or `watcher` sub-command group | Background Daemon = yes |
| NFRs mention "detach", "run in background", "PID file" | Background Daemon = yes |
| All operations complete within a single command invocation | Background Daemon = no |

> **Async pattern vs User Config:** Any application with a Background Daemon also
> requires User Config = yes (to store the PID). The skill must force this
> dependency automatically when Background Daemon is detected.

### Table Output Detection

| Content Pattern | Table Output Selection |
|---|---|
| Commands produce list output (resources, records, results) | Table Output = yes |
| NFRs mention "tabular", "list view", "columns" | Table Output = yes |

### Summary of Determination

After analyzing all inputs, produce a determination summary before generating the spec:

```
Optional Component Determination:
- Prompts:              yes (from PRD.md â†’ init command has interactive wizard)
- User Config:          yes (from PRD.md â†’ login command stores API token)
- Project Config:       yes (from PRD.md â†’ per-project .mytoolrc support)
- Local Database:       yes (from PRD.md â†’ history command lists past runs)
- Async - Polling:      yes (from PRD.md â†’ deploy --watch flag)
- Async - Inline Batch: yes (from PRD.md â†’ sync --all processes 1000s of items)
- Async - Daemon:       no
- Shell Execution:      no
- HTTP Client:          yes (from CLAUDE.md â†’ depends on My API)
- Auto-update:          yes (default for npm-distributed tool)
- Binary Packaging:     no (npm distribution only)
- Table Output:         yes (from PRD.md â†’ list commands produce tabular output)
- Banner/Box UI:        no
- File Operations:      no
```

If the user disagrees with any determination, allow them to override before proceeding.

## Generating the Specification

Once inputs are gathered and optional components are determined, generate the specification
as a **multi-file output split by command**. Read the spec template at
`references/spec-template.md` for the exact structure and content of each section.
The template is the authoritative guide â€” follow it closely.

The specification is split into two categories:

1. **Root `SPECIFICATION.md`** â€” Shared infrastructure: `package.json`, TypeScript config,
   build tooling, CLI entry point, shared services, UI utilities, config management,
   error handling, testing strategy, and packaging.
2. **Per-command `<command-name>/SPEC.md`** â€” Each command gets its own folder with a
   self-contained specification covering argument/option definitions, service methods,
   prompt flows, and output formatting.

**Important:** The generated spec must use **real application data** from the context files:

- **Commands** must use the actual command names from PRD.md (e.g., `init`, `deploy`, `status`)
- **Arguments and options** must match the actual definitions in `model/<command>/model.md`
- **Service methods** must map to the actual user stories
- **Config keys** must match what the model defines
- **Version tags** on every user story ID, NFR ID, constraint ID
- **Removed / Replaced items** listed for deprecated items

### Output Structure

```
<app_folder>/context/specification/
â”œâ”€â”€ SPECIFICATION.md              â† Shared infrastructure + TOC
â”œâ”€â”€ init/
â”‚   â””â”€â”€ SPEC.md                   â† Command blueprint for 'init'
â”œâ”€â”€ deploy/
â”‚   â””â”€â”€ SPEC.md                   â† Command blueprint for 'deploy'
â”œâ”€â”€ config/
â”‚   â””â”€â”€ SPEC.md                   â† Command blueprint for 'config'
â””â”€â”€ ...                           â† One folder per command from PRD.md
```

### What Goes in `SPECIFICATION.md` (Root)

#### 1. Project Overview
Application metadata, description, tech stack summary, binary name, target platforms,
the complete command list, and distribution strategy.

#### 2. package.json Configuration
Complete `package.json` with `"type": "module"`, `bin` entry, `files`, `engines`,
all runtime dependencies (core + selected conditional), all `devDependencies`, and `scripts`
(dev, build, typecheck, test, lint, plus platform-specific pkg scripts if Binary Packaging = yes).

#### 3. TypeScript & Build Configuration
Complete `tsconfig.json` targeting ESM. Complete `tsup.config.ts` with shebang injection,
ESM format, and conditional sourcemap/minify for production. ESLint configuration.

#### 3a. Application Version Configuration
The `package.json` `version` field MUST be set to the version value derived from the
version argument provided during skill invocation (e.g., `1.0.3`). If multiple versions
were provided, use the highest one.

Commander.js uses `package.json` version automatically for `--version` output. The CLI
entry point (`src/cli.ts`) must call `.version(packageJson.version)` on the Commander
program instance so that `<tool> --version` prints the correct version.

The version MUST also be included in JSON output when `--json` flag is used (e.g.,
`{"version": "1.0.3", "data": {...}}`).

#### 3b. `.env` File Generation from ENVIRONMENT.md
Generate a `.env` file at the project root by reading `ENVIRONMENT.md` from the project root.
The `.env` file maps ENVIRONMENT.md credential and platform values to the environment variable
names used by the CLI application. The spec must define the complete `.env` content with
actual values from ENVIRONMENT.md.

**Process:**
1. Read `ENVIRONMENT.md` from the project root
2. Extract credential values from `ENVIRONMENT.md` (`# Supporting 3rd Party Applications`
   and `# External Services` for API hosts, ports, tokens); read any toolchain paths
   (e.g., Node.js) from `DEVTOOL.md`
3. Map each value to the corresponding environment variable name used by the CLI
4. Generate the `.env` file with `KEY=value` pairs

**Example `.env` output (derived from ENVIRONMENT.md):**
```properties
# API
API_BASE_URL=http://localhost:8080/api/v1
API_KEY=

# Platform
NODE_HOME=C:\nvm4w\nodejs
```

**Rules:**
- Only include variables that are actually used by the application (via `process.env`)
- Use actual values from ENVIRONMENT.md â€” never use placeholders or `TODO`
- If ENVIRONMENT.md does not exist or a value is not found, use sensible defaults for local
  development (e.g., `localhost`, default ports)
- The `.env` file must be loaded using `dotenv` (add as a dependency if not already present)
- The `.env` file is gitignored

#### 4. Application Entry Point
`src/cli.ts` â€” the Commander.js `Program` setup: name, description, version, global options
(`--verbose`, `--json`, `--no-color`), command registration imports, and `program.parse()`.
See `references/command-patterns.md` for the root program setup, global option propagation
pattern, and async error handling with `parseAsync`.

#### 5. Project Directory Structure
Full `src/` directory tree with all files, named after actual commands and services
from the context.

#### 6. Shared Types
`src/types/index.ts` â€” all shared TypeScript interfaces and type aliases used across
commands and services.

#### 7. Terminal UI Utilities
- `src/ui/logger.ts` â€” chalk-based logger with `info`, `success`, `warn`, `error`,
  `debug` (gated on `--verbose`) methods
- `src/ui/spinner.ts` â€” ora wrapper with typed start/succeed/fail/stop helpers
- `src/ui/table.ts` â€” cli-table3 wrapper *(conditional on Table Output = yes)*
- `src/ui/output.ts` â€” Unified output handler respecting `--json` flag

#### 8. Error Handling
`src/errors.ts` â€” Base `CliError` class with exit code mapping. `handleError()` function
used in every command `action` handler to catch, format, and exit cleanly.

#### 9. User Configuration Management *(conditional â€” include only if User Config = yes)*
`src/config/user.config.ts` â€” `conf` setup with schema (Zod), typed accessors, and
migration strategy. Key names, default values, and OS storage paths.
See `references/config-patterns.md`.

#### 10. Project Configuration Management *(conditional â€” include only if Project Config = yes)*
`src/config/project.config.ts` â€” `cosmiconfig` loader with Zod validation. Config file
search path, supported formats, and merge strategy with defaults.
See `references/config-patterns.md`.

#### 11. HTTP Client Setup *(conditional â€” include only if HTTP Client = yes)*
`src/services/http.client.ts` â€” `got` instance with base URL, auth header injection,
retry configuration, and typed error handling.

#### 12. Shell Execution Utilities *(conditional â€” include only if Shell Execution = yes)*
`src/utils/shell.ts` â€” `execa` wrapper with logging, timeout, and error handling.

#### 13. Auto-Update Notifier *(conditional â€” include only if Auto-update = yes)*
`src/utils/updater.ts` â€” `update-notifier` integration called once at CLI startup with
non-blocking async check.

#### 14. Testing Strategy
Vitest configuration, command testing patterns with `process.argv` mocking, service unit
testing, config testing with temp directories.
See `references/testing-patterns.md`.

#### 15. Packaging & Distribution *(conditional â€” include only if Binary Packaging = yes)*
`tsup` build pipeline, `@yao-pkg/pkg` configuration, platform targets, npm scripts for
each platform binary, GitHub Actions release workflow stub.
See `references/packaging-patterns.md`.

**For npm-only distribution:** `package.json` `files`, `bin`, `engines`, `prepublishOnly`
script, `.npmignore`, semantic versioning guidance.

#### 16. Local Database *(conditional â€” include only if Local Database = yes)*
`src/db/schema.ts` â€” Drizzle table definitions (all entity tables derived from model files).
`src/db/client.ts` â€” `better-sqlite3` singleton with WAL mode, foreign keys, and
automatic migration runner on first open.
`src/db/path.ts` â€” `env-paths` based OS data directory resolution.
`src/db/repositories/` â€” One repository class per entity exposing typed CRUD and query
methods. `drizzle.config.ts`, `drizzle/` migration folder, and `db:generate` / `db:migrate`
/ `db:studio` npm scripts.
See `references/database-patterns.md`.

#### 17. Async Patterns *(conditional â€” include only if any async pattern is detected)*

Include only the sub-sections that apply. Multiple sub-sections may be included together.

**17a. Shared Signal Handling** *(include whenever any async pattern is yes)*
`src/utils/signal.ts` â€” `onSignal(cleanupFn)` utility that registers SIGINT and SIGTERM
handlers, runs the cleanup function, then exits with code 130 (Ctrl+C) or 0 (SIGTERM).
Used by polling loops, batch processors, and the daemon runner to ensure Ctrl+C always
produces a clean exit rather than a Node.js stack trace.

**17b. Polling** *(conditional â€” include only if Polling = yes)*
`src/utils/poll.ts` â€” `poll<T>(options)` function with configurable interval, timeout,
spinner integration, and `onTick` callback for dynamic status text. Command handlers
pass `--watch` / `--follow` / `--wait` flags down to the poll utility. Non-watch invocation
(fire-and-forget) must remain supported when the flag is absent.
See `references/async-patterns.md`.

**17c. Inline Batch Processing** *(conditional â€” include only if Inline Batch = yes)*
`src/utils/batch.ts` â€” `runBatch<TInput, TOutput>(options)` function with configurable
concurrency, bail-on-error mode, per-item error collection, and `onProgress` callback.
`src/ui/progress.ts` â€” `ProgressBar` wrapper over ora showing `[percent%] n/total â€” ETA Xs`.
When `Local Database = yes`, include the resume pattern: services filter out already-processed
IDs from the item list by querying the repository before the batch starts.
See `references/async-patterns.md`.

**17d. Background Daemon** *(conditional â€” include only if Background Daemon = yes)*
`src/daemon/runner.ts` â€” `runDaemon()` function implementing the daemon's event loop;
called when the process detects `MY_TOOL_DAEMON_MODE=1` in the environment before
Commander parses arguments.
`src/services/daemon.service.ts` â€” `DaemonManager` class with `start()` (spawn detached),
`stop()` (SIGTERM + timeout + SIGKILL), `isRunning()` (signal-0 check), `getStatus()`,
and `getRecentLogs()`. PID stored in `conf` (requires User Config = yes).
`src/commands/daemon/index.ts` â€” `start`, `stop`, `status`, `logs` sub-commands.
See `references/async-patterns.md`.

### What Goes in Each `<command-name>/SPEC.md` (Per-Command)

For EACH command from PRD.md, create a folder named after the command (kebab-case) and
generate a `SPEC.md` inside it. Each file is **self-contained** â€” a coding agent can
implement the command after the shared infrastructure is in place.

Each command SPEC.md must include:

- **Header** with command name and back-reference to root `SPECIFICATION.md`
- **Traceability**: user story IDs, NFR IDs, constraint IDs
- **Command definition**: full Commander.js `.command()` chain with all arguments,
  options, and description strings
- **Argument & Option contracts**: Zod schema for validation, complete option flag table
- **Prompt flow** *(conditional)*: `@inquirer/prompts` sequence for interactive mode
- **Service interface**: methods this command calls with TypeScript signatures
- **Service implementation**: full business logic, no terminal I/O
- **Output contract**: exact structure for `--json` output and human-readable output,
  including async output contracts if Polling or Inline Batch apply to this command
- **Error cases**: every error type, exit code, and user-facing message
- **Complete code samples** for every component

See `references/command-patterns.md` for the canonical command registration patterns
covering simple commands, sub-command groups, confirmation prompts, `--dry-run`,
tabular output, global option propagation, help text conventions, and exit code table.

## Changelog Append

After all specification files are successfully generated, append an entry to `CHANGELOG.md` in the application folder (`<app_folder>/CHANGELOG.md`):

1. Read `<app_folder>/CHANGELOG.md`. If it does not exist, create it with:
   ```markdown
   # Changelog

   - This file tracks all skill executions by version for this application.
   - The highest version recorded here is the current application version.
   - Skills MUST NOT execute for a version lower than the highest version in this file.

   ---
   ```
2. Search for a `## {version}` heading matching the current version.
3. If the section **exists**: append a new row to its table.
4. If the section **does not exist**: insert a new section after the `---` below the context header and before any existing `## vX.Y.Z` section (newest-first ordering), with a new table header and the first row.
5. Row format: `| {YYYY-MM-DD} | {application_name} | specgen-ts-cli | {module or "All"} | Generated TypeScript CLI technical specification |`
6. **Never modify or delete existing rows.**

## Output Format

```
<app_folder>/context/specification/
â”œâ”€â”€ SPECIFICATION.md              â† Root: TOC + shared infrastructure
â”œâ”€â”€ <command-1>/
â”‚   â””â”€â”€ SPEC.md                   â† Self-contained command blueprint
â”œâ”€â”€ <command-2>/
â”‚   â””â”€â”€ SPEC.md
â””â”€â”€ <command-N>/
    â””â”€â”€ SPEC.md
```

**Sample code is mandatory.** Every component described in any spec file must include a
complete, self-explanatory code sample. The code must be continuous (no `// ...` gaps)
and usable as a direct reference by a coding agent.

## Constraints

These constraints are non-negotiable. Every code sample in the generated spec must follow
them.

### Universal Constraints

**Use ESM throughout.** The project sets `"type": "module"` in `package.json`. All
imports in TypeScript source use the `.js` extension (TypeScript resolves to `.ts`).
Never use `require()` or CommonJS `module.exports`.

**No `any` types.** Every function signature, variable, and generic must be explicitly
typed. Use `unknown` with runtime narrowing (Zod) instead of `any`.

**Constructor injection for services.** Services accept their dependencies (config, HTTP
client, logger) through the constructor. No global singletons imported directly in service
files. This enables clean unit testing with mocks.

**Commands must not contain business logic.** The command `action` handler is a thin
orchestrator: parse options â†’ call service â†’ format output â†’ handle errors. All domain
logic lives in `src/services/`.

**Separate output from logic.** Service methods return typed data structures. The command
handler is responsible for formatting and printing. Services never call `console.log`
or manipulate terminal state.

**Always handle exit codes.** Every command `action` handler wraps its body in
`try/catch`. On error: print formatted message, call `process.exit(1)` (or the
appropriate code). On success: `process.exit(0)` is implicit.

**ESM import paths use `.js` extension.** In TypeScript source files:
```ts
import { UserConfig } from '../config/user.config.js'  // âœ“ correct
import { UserConfig } from '../config/user.config'      // âœ— wrong
```

**All user-facing strings go through the logger or output module.** Never call
`console.log` directly in commands or services. Use `logger.info()`, `logger.error()`,
`output.print()`, etc.

**Zod for all external data.** Any data from config files, API responses, or CLI
arguments that crosses a system boundary must be parsed with a Zod schema before use.

**Use `@inquirer/prompts` not `inquirer`.** The modern scoped package is the officially
maintained version. Import individual prompt functions, not the legacy `inquirer` default.

### Conditional Constraints

**If Binary Packaging = yes:**
- Use dynamic `import()` for any modules not compatible with pkg's static analysis
- Avoid `__filename` / `__dirname` â€” use `import.meta.url` with `fileURLToPath`
- All asset files (templates, default configs) must be embedded via `pkg`'s `assets` config

**If User Config = yes:**
- Credentials and tokens must be stored using `conf` (uses OS keychain on macOS)
- Never write secrets to plain text files manually
- The `conf` schema must be defined with Zod and validated on read

**If Project Config = yes:**
- Config loading must be non-fatal if no config file is found (use defaults)
- Loaded config must be merged with defaults using a predictable precedence order:
  CLI flags > environment variables > project config file > user config > hardcoded defaults

**If HTTP Client = yes:**
- All API calls must use the shared `got` instance (never raw `fetch` or `axios`)
- HTTP errors must be caught, parsed for `statusCode`, and rethrown as `CliError`
- Authentication tokens must come from the config system, never hardcoded

**If Local Database = yes:**
- All database access must go through repository classes â€” services never use `db` directly
- Repositories receive `DbClient` via constructor injection â€” no global `getDb()` calls
  inside service files (only in the composition root `cli.ts` or service constructors)
- Every write statement (`insert`, `update`, `delete`) must call `.run()` to execute â€”
  Drizzle returns a prepared statement object that is not automatically executed
- All multi-step writes that must succeed or fail together must use `db.transaction()`
- JSON columns must be serialised with `JSON.stringify` on insert and `JSON.parse` on
  read â€” never store raw objects in `text` columns
- Migration files in `drizzle/` are committed to source control; never edit generated
  SQL files after commit â€” always generate new ones via `drizzle-kit generate`
- The database file path must come from `getDatabasePath()` â€” never hardcode a path

**If any Async Pattern is yes (Polling, Inline Batch, or Background Daemon):**
- Every long-running loop MUST register an `onSignal` handler before entering the loop
  and dispose it via the returned function when the loop exits normally
- Ctrl+C must NEVER produce a Node.js stack trace â€” the signal handler catches it,
  runs cleanup, and calls `process.exit(130)`
- SIGTERM must exit cleanly with code `0` â€” it signals intentional shutdown
  (e.g. `daemon stop`), not an error

**If Polling = yes:**
- Every command with a watch flag must also work without it (fire-and-forget behaviour
  is always supported; `--watch` / `--follow` is additive)
- The polling timeout must be configurable via a `--timeout <seconds>` option; the
  default (300s) is a maximum, not a guarantee

**If Inline Batch = yes:**
- Concurrency must be configurable via `--concurrency <n>` â€” never hardcode parallelism
- Both `--bail` (stop on first error) and the default (collect all errors, continue) must
  be supported
- Exit code must be `1` when any items fail, even if the majority succeeded
- The `onProgress` callback updates the spinner â€” service code never touches ora directly

**If Background Daemon = yes:**
- The daemon process is the SAME binary launched with `MY_TOOL_DAEMON_MODE=1` in the
  environment â€” never ship a separate daemon binary
- The daemon entry point check in `cli.ts` must appear BEFORE Commander parses `argv`,
  so the daemon mode is invisible to all user-facing `--help` output
- PID storage requires User Config (`conf`) â€” Background Daemon detection automatically
  forces User Config = yes in the determination summary
- `DaemonManager.isRunning()` must use signal-0 (`process.kill(pid, 0)`) to test
  process liveness â€” never rely on PID alone (PIDs are reused by the OS)

## Principles Embedded in the Spec

### Always-Applicable Principles
- ESM-first TypeScript with strict mode (`"strict": true`)
- Thin command action handlers â€” orchestrate, don't implement
- Services are pure TypeScript â€” no CLI concerns, fully testable
- Single output module respects `--json` flag for machine-readable output
- Every command has `--help` text that matches the user stories
- Errors produce clean, human-friendly messages with non-zero exit codes
- Verbose mode (`--verbose`, `-v`) reveals internal steps via `logger.debug()`
- All file paths use `node:path` and `node:url` â€” no raw string concatenation

### Conditional Principles
- **If Prompts = yes:** Interactive and non-interactive modes are both supported. Every
  prompt has a corresponding flag so the command can run non-interactively in CI.
- **If User Config = yes:** The `config` command exposes `get`, `set`, `list`, and
  `reset` sub-commands for user-visible settings.
- **If Local Database = yes:** SQLite is the single source of truth for all structured
  local data. `conf` remains for user preferences and tokens; SQLite is for anything
  with multiple rows, history, or relational structure. The database opens and migrates
  automatically on first command run â€” no manual `init-db` step required.
- **If Polling = yes:** Every watched command has a non-watch path that exits immediately.
  The `poll()` utility owns all timing and spinner state; the command handler only
  provides the `check` function and interprets the final result.
- **If Inline Batch = yes:** The `runBatch()` utility owns concurrency and error
  collection; the service owns per-item logic; the command handler owns progress display
  and final output. These three responsibilities must never be mixed.
- **If Background Daemon = yes:** The daemon runner (`runDaemon`) is a plain async
  function â€” it has no Commander, no prompts, and no user interaction. Its only
  interface is `MY_TOOL_DAEMON_MODE=1` (start) and SIGTERM (stop).
- **If Binary Packaging = yes:** The binary must work with zero Node.js dependency on the
  target machine. Asset embedding and path resolution must be validated for each platform.
