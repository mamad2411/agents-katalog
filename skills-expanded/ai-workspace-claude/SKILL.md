# AI Development Workspace

## Project Overview

This is a full-stack AI development workspace supporting TypeScript, React, and Python projects. The workspace is configured for AI-assisted development with Claude and Cursor.

## Tech Stack

- **Frontend**: React 18+ with TypeScript
- **Backend**: Node.js/Python
- **Testing**: Vitest (TS/React), pytest (Python)
- **Build Tools**: Vite, ESBuild
- **Package Manager**: pnpm preferred, npm/yarn supported

## Coding Standards

### TypeScript

- **No `any` type**: Use `unknown` for truly unknown types, then narrow with type guards
- **Explicit return types**: All functions must declare return types
- **Strict null checks**: Handle null/undefined explicitly
- **Interface over type**: Prefer `interface` for object shapes, `type` for unions/primitives

### Naming Conventions

- `PascalCase`: Components, Classes, Interfaces, Types
- `camelCase`: Variables, Functions, Methods
- `SCREAMING_SNAKE_CASE`: Constants, Environment Variables
- `kebab-case`: File names, CSS classes

### Code Quality

- Maximum function length: 50 lines
- Maximum file length: 300 lines
- Cyclomatic complexity limit: 10
- Always destructure props and imports

## Git Workflow

1. Create feature branch from `main`: `feature/description` or `fix/description`
2. Commit with conventional commits: `feat:`, `fix:`, `docs:`, `refactor:`, `test:`
3. Create PR with description and testing notes
4. Require review before merge
5. Squash merge to main

## Communication Guidelines

- **User Communication**: 日本語 (Japanese)
- **Code/Comments/Docs**: English
- **Commit Messages**: English
- **PR Descriptions**: English

## Directory Structure

```
ai-workspace/
├── src/           # Source code
├── tests/         # Test files
├── docs/          # Documentation
├── .claude/       # Claude AI configuration
└── .cursor/       # Cursor IDE configuration
```
