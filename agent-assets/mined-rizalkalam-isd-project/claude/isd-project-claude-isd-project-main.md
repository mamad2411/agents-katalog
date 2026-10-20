<!-- GSD:project-start source:PROJECT.md -->

## Project

**Library Management System (LMS)**

A web-based Library Management System for Universitas XYZ. It allows students to search the catalog and request borrows, while librarians manage the collection, approve requests, and monitor overdue items via a dashboard.

**Core Value:** Centralizing library operations to replace paper-based logs with an efficient, transparent, and mobile-responsive digital system.

### Constraints

- **Tech Stack**: FastAPI (Python) backend, React frontend, PostgreSQL database. — Team preference and university infrastructure.
- **Infra**: Must be deployable via Docker to university servers. — Existing deployment standard.
- **Performance**: Page and search responses must be under 2 seconds. — User experience requirement.
- **Security**: Authentication and authorization enforced via JWT. — Data protection requirement.

<!-- GSD:project-end -->

<!-- GSD:stack-start source:codebase/STACK.md -->

## Technology Stack

## Languages

- JavaScript (Node.js) >= 20.0.0 - Core logic of `gsd-core` and lifecycle hooks in `.claude/hooks/` and `.gemini/hooks/`.
- Python 3.x - Automation scripts located in `scripts/` (e.g., `scripts/verify_doc_links.py`).
- Markdown - Agent definitions (`.claude/agents/*.md`), documentation, and planning artifacts.
- Shell (Bash/PowerShell) - Integration hooks and orchestration scripts.

## Runtime

- Node.js >= 20.0.0
- Python 3.x
- npm
- Lockfile: Not present in root, but required for tool installation (e.g., `npx @opengsd/gsd-core@latest`).

## Frameworks

- GSD Core v1.4.3 - The primary framework for agentic workflow orchestration.
- Claude Code (Anthropic) - AI agent framework for the Claude path.
- Codex (OpenAI) - AI agent framework for the Codex path.
- Internal GSD Verification - Leverages `verify` and `uat` (User Acceptance Testing) workflows.
- Python scripts - `scripts/verify_doc_links.py` for documentation integrity.
- `gsd-tools.cjs` - Internal CLI tools for GSD management.

## Key Dependencies

- `git` >= 2.40 - Core version control system for tracking all changes and state.
- `gh` (GitHub CLI) >= 2.40 - Used for repository management, pull requests, and issues.
- Brave Search API - Integrated for web search capabilities during research phases.

## Configuration

- Configured via environment variables and project-specific JSON/TOML files.
- Key configs required: `BRAVE_API_KEY` (optional, for web search), LLM API keys (handled by respective agent CLIs).
- `.claude/gsd-file-manifest.json` - Tracks framework file integrity and versions.
- `settings.local.json` - Configures agent lifecycle hooks.

## Platform Requirements

- Cross-platform support: Windows (via WSL/PowerShell), macOS, and Linux.
- GitHub account and authenticated `gh` CLI required.
- Not applicable (This is a developer toolkit/framework).

<!-- GSD:stack-end -->

<!-- GSD:conventions-start source:CONVENTIONS.md -->

## Conventions

## Naming Patterns

- Kebab-case: `gsd-check-update.js`, `verify-doc-links.py`, `07-tech-stack.md`
- Markdown Docs: UPPERCASE for codebase docs (`STACK.md`, `ARCHITECTURE.md`), kebab-case for guides.
- JavaScript: camelCase (e.g., `parseCodeReviewFlags`, `gsd_run`, `toPosixPath`)
- Python: snake_case (e.g., `verify_links`)
- JavaScript: camelCase (e.g., `stdinTimeout`, `filePath`, `isFound`)
- Python: snake_case (e.g., `errors`, `target`, `md_file`)
- JavaScript (CommonJS): No explicit types, but PascalCase inferred for potential classes or constructors if used (rare in this codebase).

## Code Style

- Indentation: 2 spaces for JavaScript/JSON/Markdown, 4 spaces for Python.
- Semicolons: Required and used in JavaScript files.
- String Literals: Both single (`'`) and double (`"`) quotes observed in JS; double quotes common for JSON keys and strings. Single quotes preferred in some shell context.
- Not explicitly configured in root (no `.eslintrc` or `biome.json` found).
- Standard language-specific checks recommended: `node -c {file}` for JS syntax check.

## Import Organization

- Not detected; relative paths are used (e.g., `require('./lib/core.cjs')`).

## Error Handling

- `try-catch` blocks in JavaScript for parsing, file operations, and CLI command execution.
- Silent fails (`process.exit(0)`) for non-critical hooks to avoid blocking the user session.
- Exit codes (`sys.exit(1)` in Python, `exit 1` in Shell, `process.exit(1)` in Node) to signal failures in scripts and workflows.
- Informative error messages with specific prefixes (e.g., `ERROR:`, `⚠️`, `🛑`).

## Logging

- Use `process.stdout.write` for fine-grained control or banners.
- Use `console.log` for standard informational output.
- Diagnostic logs often include a banner or specific separator (e.g., `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`).
- Prefix symbols used for status: `◆` for progress, `✓` for success, `⚠️` for warning.

## Comments

- Top of file: Purpose, usage instructions, and dependencies.
- Logic-level: Explaining complex conditionals, guard clauses, and non-obvious implementation details.
- Workflow files (`.md`): `<purpose>` and `<step>` tags used for organization.
- Minimal usage in existing hook files, but present in some `gsd-core` files for function descriptions.

## Function Design

## Module Design

<!-- GSD:conventions-end -->

<!-- GSD:architecture-start source:ARCHITECTURE.md -->

## Architecture

## System Overview

```text

```

## Component Responsibilities

| Component | Responsibility | File |
|-----------|----------------|------|
| Agents | Orchestrate the GSD process, interface with the user, and execute workflows. | `.claude/agents/*.md` |
| Workflows | Define the step-by-step procedures for each phase (discuss, plan, execute, verify). | `.claude/gsd-core/workflows/*.md` |
| gsd-tools | Centralized CLI utility for all GSD workflow operations (state, roadmap, phase management). | `.claude/gsd-core/bin/gsd-tools.cjs` |
| Core Library | Specialized logic for state management, git operations, and project artifacts. | `.claude/gsd-core/bin/lib/*.cjs` |
| State | Tracks the current progress, active phase, and project metadata. | `.planning/STATE.md` |
| Roadmap | Defines the project milestones and phases. | `ROADMAP.md` |

## Pattern Overview

- **Workflow-Driven**: Agent behavior is governed by markdown-based workflows that describe steps and decision points.
- **CLI-Augmented**: Agents rely on a specialized CLI (`gsd-tools.cjs`) to perform complex filesystem and git operations safely and consistently.
- **File-Based State**: The system's source of truth is stored in markdown and JSON files within the `.planning/` directory, allowing for transparency and git-tracking.

## Layers

- Purpose: Provides specialized personas for different parts of the SDLC.
- Location: `.claude/agents/`
- Contains: System instructions and role-specific constraints.
- Depends on: Workflow Layer.
- Used by: User / LLM.
- Purpose: Defines the business logic of the GSD process.
- Location: `.claude/gsd-core/workflows/`
- Contains: Procedural markdown files with embedded shell commands.
- Depends on: Tooling Layer.
- Used by: Agent Layer.
- Purpose: Automates repetitive and complex tasks.
- Location: `.claude/gsd-core/bin/`
- Contains: Node.js scripts and libraries.
- Depends on: Filesystem/OS.
- Used by: Workflow Layer.

## Data Flow

### Primary Request Path (Phase Operation)

### State Management:

- Handled primarily by `bin/lib/state.cjs` and `bin/lib/planning-workspace.cjs`.
- Uses a file-locking mechanism (`_heldStateLocks` in `state.cjs`) to prevent concurrent modifications during the same process.
- Frontmatter in `.planning/STATE.md` serves as the primary data store for active project parameters.

## Key Abstractions

- Purpose: Validation checkpoints that control workflow progression.
- Examples: `.claude/gsd-core/references/gates.md`
- Pattern: Pre-flight, Revision, Escalation, and Abort.
- Purpose: Incremental units of work defined in the roadmap.
- Examples: `.planning/phases/NN-{name}/`
- Pattern: Decimal numbering (e.g., 01.10) for insertion and sequencing.
- Purpose: Isolated environments for executing plans without polluting the main branch.
- Examples: `bin/lib/worktree-safety.cjs`
- Pattern: Automated creation and cleanup of git worktrees.

## Entry Points

- Location: `.claude/gsd-core/bin/gsd-tools.cjs`
- Triggers: Shell commands from Agents or Workflows.
- Responsibilities: Dispatches commands to specialized libraries.
- Location: `CLAUDE.md`
- Triggers: Initial project load by the agent.
- Responsibilities: Provides high-level commands and environment context.

## Architectural Constraints

- **Threading:** Single-threaded Node.js execution for the CLI.
- **Global state:** No in-memory global state across agent turns; all persistence is in `.planning/`.
- **File System Dependency:** Heavily reliant on POSIX-style paths (handled by `toPosixPath` in `core.cjs`).
- **Git Integration:** Requires an initialized git repository for most operations (tracked via `.git`).

## Anti-Patterns

### Checkpoint Human-Automation

### Vague Task Definitions

### Reflexive SUMMARY Chaining

## Error Handling

- **Pre-flight Gates**: Check preconditions (e.g., file existence) before starting.
- **Revision Gates**: Evaluate output quality and loop back to the agent if needed (max 3 iterations).
- **Escalation Gates**: Pause for human input when automated resolution fails.

## Cross-Cutting Concerns

<!-- GSD:architecture-end -->

<!-- GSD:skills-start source:skills/ -->

## Project Skills

No project skills found. Add skills to any of: `.claude/skills/`, `.agents/skills/`, `.cursor/skills/`, `.github/skills/`, or `.codex/skills/` with a `SKILL.md` index file.
<!-- GSD:skills-end -->

<!-- GSD:workflow-start source:GSD defaults -->

## GSD Workflow Enforcement

Before using Edit, Write, or other file-changing tools, start work through a GSD command so planning artifacts and execution context stay in sync.

Use these entry points:

- `/gsd-quick` for small fixes, doc updates, and ad-hoc tasks
- `/gsd-debug` for investigation and bug fixing
- `/gsd-execute-phase` for planned phase work

Do not make direct repo edits outside a GSD workflow unless the user explicitly asks to bypass it.
<!-- GSD:workflow-end -->

<!-- GSD:profile-start -->

## Developer Profile

> Profile not yet configured. Run `/gsd-profile-user` to generate your developer profile.
> This section is managed by `generate-claude-profile` -- do not edit manually.
<!-- GSD:profile-end -->
