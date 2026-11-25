# AGENTS.md for BlackRoad-OS/blackroad-hardware

# Repository Guidelines

## Session Start
- Review the root `README.md` first for product context and local run instructions.
- Check for existing automation, deployment, and workflow files before adding new ones.

## Project Structure
- Keep source changes inside the repo's existing app, package, or service structure.
- Prefer root-level documentation updates only when clarifying setup, architecture, or contributor workflow.

## Development Workflow
- Use the repo's existing package manager and task runner.
- Prefer small, reviewable changes over broad refactors.
- Preserve current file naming, formatting, and framework conventions.

## Validation
- Run the lightest relevant verification step available for the repo.
- If the repo exposes lint, type-check, or test commands, prefer those before broader builds.

## Changes
- Update documentation when behavior, setup, or commands change.
- Avoid destructive rewrites of unrelated files.
- Keep automation and local model tooling additive unless the repo already has a stronger pattern.

## Pull Requests
- Summarize user-visible changes, validation performed, and any required config changes.
