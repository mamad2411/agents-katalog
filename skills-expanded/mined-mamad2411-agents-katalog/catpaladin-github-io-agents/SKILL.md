# Agent Coding Guidelines

This repository is a Hugo static site with Svelte 5 components. Follow these guidelines when working
with this codebase.

See [docs/commands.md](docs/commands.md) for essential development, testing, and build commands.

## Code Style Guidelines

See [docs/code-style.md](docs/code-style.md) for code style guidelines including TypeScript config,
imports, formatting, naming, error handling, and accessibility.

## Svelte 5 Patterns

See [docs/svelte-patterns.md](docs/svelte-patterns.md) for Svelte 5 patterns and component patterns.

## Linting

See [docs/linting.md](docs/linting.md) for ESLint configuration and linting rules.

## Testing Guidelines

See [docs/testing.md](docs/testing.md) for testing guidelines using Vitest and
@testing-library/svelte.

## Styling (Tailwind)

See [docs/tailwind.md](docs/tailwind.md) for Tailwind CSS styling guidelines and dark mode patterns.

## File Locations

See [docs/project-structure.md](docs/project-structure.md) for project structure, file locations,
and build output details.

## Workflow

See [docs/workflow.md](docs/workflow.md) for workflow checklist and session completion procedures.

## Browser Automation

Use `agent-browser` for web automation. Run `agent-browser --help` for all commands.

Core workflow:

1. `agent-browser open <url>` - Navigate to page
2. `agent-browser snapshot -i` - Get interactive elements with refs (@e1, @e2)
3. `agent-browser click @e1` / `fill @e2 "text"` - Interact using refs
4. Re-snapshot after page changes
