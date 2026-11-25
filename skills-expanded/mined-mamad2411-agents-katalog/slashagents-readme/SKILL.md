# SlashAgents

**Version:** 1.4.0 | **Updated:** 2025-01-11 | **Author:** Ricardo Carvalho

A curated collection of 53 battle-tested Claude Code extensions designed to help developers **stay in flow**. This toolkit includes 16 slash commands (workflow automation like `/pr` and `/ci-orchestrate`), 35 agents (specialized agents for testing, code quality, BMAD workflows, and automation), and 2 skills (reusable PR and refactoring operations).

Whether you're managing pull requests, orchestrating CI pipelines, or following structured BMAD development cycles, these tools preserve your creative momentum by automating repetitive tasks and providing intelligent assistance exactly when you need it.

## Contents

| Type | Count | Description |
| ------ | ------- | ------------- |
| **Commands** | 16 | Slash commands for workflows (`/pr`, `/ci-orchestrate`, etc.) |
| **Agents** | 35 | Specialized agents for testing, quality, BMAD, and automation |
| **Skills** | 2 | Reusable skill definitions (PR workflows, safe refactoring) |

> **Note:** Plugin installation includes 16 command aliases for convenience (e.g., `/pr` instead of `/cc-agents-commands:pr`).

## Prerequisites

Before installing CC_Agents_Commands, ensure you have:

- **Required:**
  - [Claude Code CLI](https://claude.ai/code) installed and working

- **Optional (enhances specific tools):**
  - **MCP servers** - Some commands require MCP servers (e.g., `github` MCP for `/pr` and `/ci-orchestrate`). See [plugin/MCP_SETUP.md](plugin/MCP_SETUP.md) for detailed MCP server configuration.
  - **BMAD framework** - Required for epic development workflows (`/epic-dev`, `/epic-dev-full`, `/epic-dev-init`). Install from [BMAD repository](https://github.com/codevalley/BMAD).

## Installation

Choose your installation method based on your needs:

| Method | Command | Scope | Pros | Cons | Best For |
| ------ | ------- | ----- | ---- | ---- | -------- |
| **Plugin Install** (Recommended) | `claude --plugin-dir ./plugin` | Project-local | Single command, includes MCP configs, auto-loads aliases, includes utility scripts | Requires staying in project directory | Most users, quick setup, full feature access |
| **File Install** (Alternative) | `cp -r commands/ ~/.claude/commands/` etc. | Global or project | Full control, works anywhere, no plugin dependencies | Manual copy steps, no MCP auto-config, no aliases | Power users, custom setups, selective tool installation |

> **Note:** Plugin Install automatically configures MCP servers and command aliases. File Install requires manual MCP setup.

### Recommended: Plugin Install

The easiest way to get started with all features enabled:

1. **Clone the repository**

   ```bash
   git clone https://github.com/Autopsias/slashagents.git
   cd slashagents
   ```

2. **Install as plugin**

   ```bash
   claude --plugin-dir ./plugin
   ```

   This single command loads all 53 extensions (16 commands, 35 agents, 2 skills) plus:
   - 16 command aliases for convenience (e.g., `/pr` instead of `/cc-agents-commands:pr`)
   - MCP server configurations (.mcp.json)
   - Event hooks (hooks.json)
   - Utility scripts

3. **Verify installation**

   In your Claude Code session, type `/help` and you should see the installed commands.

> **Tip:** For MCP server configuration and advanced features, see [plugin/MCP_SETUP.md](plugin/MCP_SETUP.md).

### Alternative: File Install (Power Users)

For users who prefer manual installation with full control:

> ⚠️ **Warning:** If you have existing commands in `~/.claude/`, back them up first. New files with the same name will overwrite existing ones.

1. **Clone the repository**

   ```bash
   git clone https://github.com/Autopsias/slashagents.git
   cd slashagents
   ```

2. **Backup existing commands** (if any exist)

   ```bash
   cp -r ~/.claude ~/.claude.backup
   ```

3. **Copy tools to your target location**

   Choose between **global** installation (tools available in all projects) or **project** installation (project-specific, version-controlled).

   **Global installation** (`~/.claude/`) - recommended for personal productivity tools:

   ```bash
   cp -r commands/ ~/.claude/commands/
   cp -r agents/ ~/.claude/agents/
   cp -r skills/ ~/.claude/skills/
   ```

   **Project installation** (`.claude/`) - recommended for team projects:

   ```bash
   cp -r commands/ .claude/commands/
   cp -r agents/ .claude/agents/
   cp -r skills/ .claude/skills/
   ```

4. **Start a new Claude Code session**

   Commands load automatically when you start a new session (no restart required).

5. **Verify installation**

   In your Claude Code session, type `/help` and you should see your installed commands listed.

> **Note:** File Install does not include MCP configurations or command aliases. You'll need to configure MCP servers manually and use full command names (e.g., `/commit-orchestrate` instead of `/commit`).

## Quick Start

Try these commands to experience immediate value:

### Resume Your Workflow

Generates a continuation prompt to pick up where you left off in a new session.

```bash
/nextsession
```

### Check PR Status

Shows your open pull requests and their current state. _Note: Enhanced with `github` MCP server for full functionality._

```bash
/pr status
```

### Orchestrate Quality Checks

Runs quality checks, stages changes, and creates a well-formatted commit.

```bash
/commit-orchestrate
```

### The 'Aha' Moment: Auto-Fix CI Failures

Analyzes CI failures, spawns parallel agents, and fixes issues automatically. _Note: Enhanced with `github` MCP server for full functionality._

```bash
/ci-orchestrate
```

## Ralph Loop (Unattended Execution)

Several commands support **Ralph Loop mode** for unattended/overnight execution. This pattern spawns fresh Claude instances per iteration, preventing context exhaustion on long-running tasks.

### Usage

Add `--loop N` to any supported command:

```bash
# Run epic development overnight (max 10 iterations)
/epic-dev 2 --loop 10

# Run code quality fixes with 30s delay between iterations
/code-quality --fix --loop 5 --loop-delay 30

# CI fixes in loop mode
/ci-orchestrate --loop 10
```

### Supported Commands

| Command | Completion Signal | Granularity |
|---------|-------------------|-------------|
| `/epic-dev` | Epic complete | **Phase-level** (CREATE → DEVELOP → REVIEW) |
| `/epic-dev-full` | Epic complete | **Phase-level** (8 phases: CREATE → VALIDATION → ATDD → DEV → REVIEW → AUTOMATE → TEST_REVIEW → TRACE) |
| `/code-quality` | All violations fixed | **Rule-level** (complexity → file-length → duplication) |
| `/test-orchestrate` | All tests passing | **Type-level** (unit → integration → e2e) |
| `/ci-orchestrate` | All CI checks passing | **Category-level** (linting → types → tests) |

### The `--loop N` Parameter

`N` is the **maximum iterations**, not the exact count:
- Loop exits **early** on completion signals (e.g., "All tests passing", "Epic complete")
- Loop exits on **blocking signals** requiring human intervention (e.g., "HALT", "Manual intervention required")
- If neither signal detected after N iterations, loop ends with partial completion

Think of N as a **safety limit** for unattended/overnight runs.

| Signal Type | Example | Behavior |
|-------------|---------|----------|
| **Completion** | `All tests passing`, `Epic complete` | ✅ Exit with success |
| **Blocking** | `HALT`, `Manual intervention required` | ⚠️ Exit, needs human |
| **Max reached** | Iteration N completes | ⚠️ Exit, may have remaining work |

### How It Works

1. Spawns a **fresh Claude instance** per iteration (full 200K context)
2. Executes **one phase/category** per iteration (not entire workflow)
3. Detects **completion signals** to exit early on success
4. Detects **blocking signals** to halt for human intervention
5. Configurable max iterations (`--loop N`) and delay (`--loop-delay S`)

### Phase-Level Granularity (v1.5.0+)

Ralph loops now operate at **phase level** instead of story/task level for improved token efficiency and fresh perspective per phase:

| Aspect | Before (Story-Level) | After (Phase-Level) |
|--------|---------------------|---------------------|
| **Token Cost** | 150-200K per iteration | 20-50K per iteration |
| **Context** | Accumulated (tunnel vision) | Fresh per phase |
| **Checkpoints** | 1 per story | 1 per phase |
| **User Intervention** | Between stories only | Between phases |

**Example flow with `/epic-dev 2 --loop 10`:**

```
Iteration 1: [PHASE: CREATE] Creating story 2-1-auth
Iteration 2: [PHASE: DEVELOP] Implementing story 2-1-auth (with Gate 2.5 verification)
Iteration 3: [PHASE: REVIEW] Reviewing story 2-1-auth (with Gate 3.5 verification)
Iteration 4: [PHASE: CREATE] Creating story 2-2-profile
...
```

Each iteration gets fresh context, preventing accumulated confusion and enabling better recovery from failures.

> **Attribution:** Pattern inspired by [snarktank/ralph](https://github.com/snarktank/ralph)

## CI/CD

This project uses self-hosted macOS runners for continuous integration. See [docs/SELF_HOSTED_RUNNERS.md](docs/SELF_HOSTED_RUNNERS.md) for runner setup and maintenance instructions.

**Pipeline:** `.github/workflows/docs-ci.yml`

- Markdown linting (markdownlint-cli2)
- Link validation (markdown-link-check)
- Shell script linting (ShellCheck)
- File structure validation
- Content validation (frontmatter, hardcoded paths)

**Maintenance:** Weekly automated cleanup via `runner-maintenance.yml`

## Commands Reference

Commands are organized by workflow moment to help you quickly find the right tool for your task.

### Shared Libraries

Commands in `commands/lib/` provide reusable patterns used internally by orchestrators:

| Library | Purpose |
|---------|---------|
| `ralph-loop.md` | Fresh-context loop pattern for unattended execution |
| `status-updater.md` | Reliable status file update patterns for orchestrators |

### Starting Work

| Command | What it does | Prerequisites |
| --------- | -------------- | --------------- |
| `/nextsession` | Generates continuation prompt for next session | — |
| `/epic-dev-init` | Verifies BMAD project setup for epic development | BMAD framework |

### Building

| Command | What it does | Prerequisites |
| --------- | -------------- | --------------- |
| `/epic-dev` | Automates BMAD development cycle for epic stories (supports `--loop`) | BMAD framework |
| `/epic-dev-full` | Executes full TDD/ATDD-driven BMAD development (supports `--loop`) | BMAD framework |
| `/epic-dev-epic-end-tests` | Validates epic completion with NFR assessment | BMAD framework |
| `/parallel` | Smart parallelization with file conflict detection and specialist routing | — |

### Quality Gates

| Command | What it does | Prerequisites |
| --------- | -------------- | --------------- |
| `/ci-orchestrate` | Orchestrates CI failure analysis and fixes (supports `--loop`) | `github` MCP |
| `/test-orchestrate` | Orchestrates test failure analysis and fixes (supports `--loop`) | test files and results |
| `/code-quality` | Analyzes and fixes code quality issues (supports `--loop`) | code files in project |
| `/coverage` | Orchestrates test coverage improvement | test coverage tools |
| `/create-test-plan` | Creates comprehensive test plans | project documentation |
| `/test-epic-full` | Tests epic-dev-full command workflow | BMAD framework |
| `/user-testing` | Facilitates user testing sessions (uses `interactive-guide` agent) | user testing setup |
| `/usertestgates` | Finds and runs next test gate (uses `evidence-collector` agent) | test gates in project |

### Shipping

| Command | What it does | Prerequisites |
| --------- | -------------- | --------------- |
| `/pr` | Manages pull request workflows | `github` MCP |
| `/commit-orchestrate` | Orchestrates git commit with quality checks | — |

## Agents Reference

Agents are organized by domain to help you quickly find the right specialist for your task.

### Test Fixers

| Agent | What it does | Prerequisites |
| ------- | -------------- | --------------- |
| `unit-test-fixer` | Fixes Python test failures for pytest and unittest | test files in project |
| `api-test-fixer` | Fixes API endpoint test failures | API test files in project |
| `database-test-fixer` | Fixes database mock and integration test failures | database test files in project |
| `e2e-test-fixer` | Fixes Playwright E2E test failures | E2E test files in project |

### Code Quality

| Agent | What it does | Prerequisites |
| ------- | -------------- | --------------- |
| `linting-fixer` | Fixes Python linting and formatting issues | linting config in project |
| `type-error-fixer` | Fixes Python type errors and annotations | Python/TypeScript project |
| `import-error-fixer` | Fixes Python import and dependency errors | code files in project |
| `security-scanner` | Scans code for security vulnerabilities | code files in project |
| `code-quality-analyzer` | Analyzes code quality metrics and patterns | code files in project |
| `requirements-analyzer` | Analyzes and validates project requirements | project documentation |

### Workflow Support

| Agent | What it does | Prerequisites |
| ------- | -------------- | --------------- |
| `pr-workflow-manager` | Manages pull request workflows via GitHub | `github` MCP |
| `parallel-orchestrator` | Spawns parallel agents with conflict detection | — |
| `digdeep` | Performs Five Whys root cause analysis | `perplexity-ask` MCP |

### Testing & Strategy

> **Tip:** Use `/user-testing` and `/usertestgates` commands to orchestrate these agents for user acceptance testing.

| Agent | What it does | Prerequisites |
| ------- | -------------- | --------------- |
| `test-strategy-analyst` | Analyzes test failures with Five Whys methodology | `perplexity-ask` MCP, `exa` MCP |
| `test-documentation-generator` | Generates test failure runbooks and documentation | test files in project |
| `ui-test-discovery` | Discovers UI components for test generation | UI code in project |
| `validation-planner` | Plans validation strategies for features | project files |
| `scenario-designer` | Transforms requirements into test scenarios | project files |
| `evidence-collector` | Validates and collects test evidence (used by `/usertestgates`) | project files |
| `interactive-guide` | Guides human testers through validation (used by `/user-testing`) | project files |

### BMAD Workflow

| Agent | What it does | Prerequisites |
| ------- | -------------- | --------------- |
| `epic-story-creator` | Creates user stories from epics | BMAD framework |
| `epic-story-validator` | Validates stories and quality gates | BMAD framework |
| `epic-test-generator` | Generates ATDD tests for stories | BMAD framework |
| `epic-atdd-writer` | Generates failing acceptance tests (TDD RED phase) | BMAD framework |
| `epic-implementer` | Implements stories (TDD GREEN phase) | BMAD framework |
| `epic-test-expander` | Expands test coverage after implementation | BMAD framework |
| `epic-test-reviewer` | Reviews test quality against best practices | BMAD framework |
| `epic-code-reviewer` | Adversarial code review (finds 3-10 issues) | BMAD framework |

### CI/DevOps

| Agent | What it does | Prerequisites |
| ------- | -------------- | --------------- |
| `ci-strategy-analyst` | Analyzes CI/CD pipeline issues strategically | `perplexity-ask` MCP, `exa` MCP |
| `ci-infrastructure-builder` | Builds CI/CD infrastructure and workflows | `github` MCP |
| `ci-documentation-generator` | Generates CI/CD documentation | CI infrastructure |

### Browser Automation

| Agent | What it does | Prerequisites |

| ------- | -------------- | --------------- |

| `browser-executor` | Executes browser automation with Chrome DevTools | `chrome-devtools` MCP or `playwright` MCP |

| `chrome-browser-executor` | Chrome-specific browser automation executor | `chrome-devtools` MCP |

| `playwright-browser-executor` | Playwright-specific browser automation executor | `playwright` MCP |

## Skills Reference

Skills leverage agents to provide natural language interfaces for complex multi-step workflows.

| Skill | What it does | Prerequisites |
| ------- | -------------- | --------------- |
| `pr-workflow` | Manages PR workflows - create, status, merge, sync | `github` MCP (via pr-workflow-manager) |
| `safe-refactor` | Test-safe file refactoring with facade pattern | code files in project |

## Troubleshooting

**Prerequisites notation:**
The Prerequisites column uses `—` for standalone tools, `server-name` MCP for tools requiring MCP servers, and "BMAD framework" or descriptive text for specialized requirements.

**MCP server not working?**
Configure the required MCP server in your Claude settings (e.g., `github` or `perplexity-ask`). Check the Prerequisites column in reference tables above to see which tools require MCP servers. Then restart Claude Code to apply the changes.

**BMAD commands not found?**
Install the BMAD framework from [BMAD repository](https://github.com/codevalley/BMAD) before using `/epic-dev`, `/epic-dev-full`, or `/epic-dev-init` commands. See BMAD documentation for installation instructions.

**Command or agent not recognized?**
Verify files are in the correct location (`~/.claude/` for global or `.claude/` for project). Then start a new Claude Code session (commands load automatically). Ensure you are in an active Claude Code session, not a regular terminal.

## Requirements

- [Claude Code](https://claude.ai/code) CLI installed
- Some extensions require specific MCP servers (noted in individual files)
- BMAD extensions require BMAD framework installed

## License

MIT
