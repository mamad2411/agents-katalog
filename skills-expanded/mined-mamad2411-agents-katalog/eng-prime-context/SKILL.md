---
name: eng-prime-context
description: Prime and build a comprehensive understanding of a codebase by analyzing directory structure, tech stack, conventions, and key entry points. Use when onboarding to a project or preparing context before starting development workflows.
---

# Prime Context

Build high-fidelity understanding of a project's codebase, architecture, dependencies, and development conventions.

## Process

### 1. Project Structure & Entry Points
1. Enumerate project root files and high-level directory tree.
2. Identify package/project configuration files (`package.json`, `Cargo.toml`, `pyproject.toml`, `go.mod`, `pom.xml`, etc.).
3. Identify main application entry points and architectural layers (e.g. controllers, services, repositories, components).

### 2. Tech Stack & Tooling Discovery
1. Determine runtime language(s) and framework versions.
2. Identify build tools, bundlers, and package managers.
3. Discover test runners, linter configurations, and formatters (`eslint`, `prettier`, `pytest`, `cargo test`, etc.).

### 3. Guidelines & Conventions
1. Check for `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, or architecture docs.
2. Note established naming conventions, module structures, and error handling practices.

### 4. Git & Workspace State
1. Check active branch and working tree status (`git status`).
2. Review recent commit logs (`git log -n 5 --oneline`) to understand active changes.

---

## Output Report Structure

Provide a structured, easy-to-scan summary:

```markdown
# Project Intelligence Summary

## Overview
- **Project Name / Type**: <Application Type & Domain>
- **Core Stack**: <Languages, Frameworks, Libraries>
- **Build / Package Manager**: <pnpm / npm / cargo / poetry / etc.>

## Architecture & Layout
- **Key Modules / Directories**:
  - `src/...`: <Purpose>
  - `tests/...`: <Testing structure>

## Testing & Tooling Commands
- **Lint / Format**: `<command>`
- **Run Tests**: `<command>`
- **Build / Dev**: `<command>`

## Conventions & Rules
- Key project rules discovered in docs or observed in codebase.
```

---

## Checkable Completion Criteria

- [ ] Entry points, architectural layers, and key modules identified from real project files.
- [ ] Tech stack versions, build tools, and package manager discovered from manifests.
- [ ] Test, lint, and build commands extracted from actual project configuration.
- [ ] Conventions and rules sourced from docs (AGENTS.md/CLAUDE.md/CONTRIBUTING.md) or verified codebase observation.
- [ ] Project Intelligence Summary delivered in the structured report format.
