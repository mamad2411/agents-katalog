# Agents Template - Agent Package Manager (APM) Project

## Project Overview

This project is a comprehensive **Agent Package Manager (APM)** workspace designed to manage, extend, and orchestrate AI agents, commands, and skills for Claude Code. It serves as a golden template repository for quickly starting with AI agents in a new project.

### Key Technologies
- **APM (Agent Package Manager):** Used for managing dependencies and workspace configuration.
- **Claude Code:** The primary platform for the agents and commands defined here.
- **Everything Claude Code (ECC):** A major dependency and framework for the project's capabilities.
- **Node.js:** Powers the various hooks and scripts integrated into the workspace.

## Project Structure

- `.claude/`: Contains Claude-specific configuration, including:
    - `agents/`: Definitions for specialized AI agents (e.g., `architect.md`, `code-reviewer.md`, `security-reviewer.md`).
    - `commands/`: Custom commands available in the Claude CLI.
    - `settings.json`: Configures project hooks (PreToolUse, PostToolUse, Stop, etc.) and global settings.
- `.gemini/`: Contains Gemini-specific resources, mirroring the Claude structure with:
    - `skills/`: A vast library of specialized skills (e.g., `tdd-workflow`, `security-scan`, `api-design`).
    - `commands/`: TOML-based command definitions.
- `.github/`: Houses shared agents, hooks, and prompts intended for GitHub integration.
- `apm_modules/`: Stores installed dependencies from the APM registry.
- `apm.yml`: The main project configuration file defining dependencies and metadata.

## Development Conventions

### Hook System
The project employs a robust hook system managed through `.claude/settings.json`. These hooks automate tasks such as:
- **Quality Gates:** Running checks after file edits.
- **Context Management:** Suggesting compaction and saving state.
- **Continuous Learning:** Observing tool usage to extract patterns.
- **Batch Processing:** Formatting and type-checking files at the end of a response.

### Adding Capabilities
- **Agents:** Add new `.md` files to `.claude/agents/` to define specialized personas.
- **Commands:** Define new commands in `.claude/commands/` (for Claude) or `.gemini/commands/` (for Gemini).
- **Skills:** Extend functionality by adding new skill directories to `.gemini/skills/`.

## Usage and Scripts

As an APM-managed workspace, key operations are typically handled via `apm` commands or custom Claude/Gemini commands.

- **Sync Dependencies:** `apm install` (inferred)
- **Run Custom Commands:** Use `/command_name` within the respective AI interface.
- **TODO:** Identify specific build or test scripts if they are added to the `scripts` section of `apm.yml`.

## Important Files
- `apm.yml`: Primary manifest for project dependencies.
- `.claude/settings.json`: Critical configuration for CLI behavior and automation.
- `GEMINI.md`: (This file) Provides instructional context for Gemini CLI interactions.
