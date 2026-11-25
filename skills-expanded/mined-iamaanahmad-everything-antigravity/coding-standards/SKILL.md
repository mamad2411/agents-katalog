# Antigravity Coding Standards

**Use these standards to maintain high-quality code in the Antigravity ecosystem.**

## 1. General Principles
- **Readability**: Code should be self-documenting. Prioritize clarity over cleverness.
- **Maintainability**: Write code that is easy to extend and modify.
- **Consistency**: Follow the project's established style guide (e.g., specific linters, formatting rules).
- **Testability**: Design code components to be easily testable.

## 2. Naming Conventions
- **Variables**: Use `camelCase`, except for constants which use `UPPER_SNAKE_CASE`.
- **Functions**: Use `camelCase` with verb prefixes (e.g., `calculateTotal`, `fetchUserData`).
- **Files**: Use `kebab-case` for file names (e.g., `user-profile.ts`).
- **Classes**: Use `PascalCase` for class names (e.g., `UserProfile`).

## 3. Code Structure
- **Modularity**: Break down complex logic into small, reusable functions.
- **File Organization**: Group related files logically (e.g., by feature or domain).
- **Imports**: Group imports by source (standard library, third-party, internal).
- **Avoid Global State**: Minimize the use of global variables.

## 4. Documentation
- **Comments**: Only comment complexity or non-obvious logic. Avoid redundant comments.
- **Docstrings**: Document public APIs, interfaces using JSDoc (or equivalent for the language).
- **README**: Maintain a clear README for significant modules.

## 5. Performance
- **Optimize judiciously**: Don't optimize prematurely; benchmark first.
- **Complexity**: Be mindful of Big O complexity for critical paths.
- **Resource Management**: Properly close resources (files, connections, etc.).

## 6. Error Handling
- **Specific Errors**: Throw specific error types where possible.
- **Catch Errors**: Handle errors gracefully at appropriate boundaries.
- **Logging**: Log errors with sufficient context for debugging.
