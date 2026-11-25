---
description: Instructions for Cursor AI on how to use project rules effectively
globs: **/*
alwaysApply: true
---

# Cursor AI Instructions

## Rule Priority

When working with this codebase, prioritize rules in this order:

1. First consult the project-specific rules to understand the system architecture
2. Then apply the specific component rules relevant to the current task
3. Always adhere to the TypeScript best practices and accessibility requirements

## Project Overview Mode

When starting work on a new task:

1. Begin by reviewing [Project Overview](mdc:.cursor/rules/project-overview.mdc) to understand the system architecture
2. Identify which component(s) the task involves (CLI, Plugin, Core Engine, VS Code Extension)
3. Review the relevant component documentation before starting development
4. Understand the Nx-based build system described in [Build System](mdc:.cursor/rules/build-system.mdc)

## Code Generation Guidelines

When generating or modifying code:

1. Maintain strict TypeScript typing - do NOT use `any`. Avoid `unknown` except when necessary for type narrowing
2. Follow the established patterns and conventions in the existing codebase
3. Write code that is self-documenting with meaningful variable/function names
4. Include JSDoc comments for public APIs and complex functions
5. Implement proper error handling with the Result pattern
6. Ensure all user-facing components follow accessibility guidelines
7. Use the Nx build commands when instructing on building or testing

## Documentation Format

When generating documentation:

1. Use Markdown format with proper heading hierarchy
2. Follow the established documentation structure
3. Include code examples where appropriate
4. Link to related documentation files when referencing other components

## OpenAI Integration Guidelines

When working with OpenAI API code:

1. Maximize token efficiency while maintaining quality
2. Implement proper error handling and retries
3. Follow established prompt engineering patterns
4. Always respect cost management and budget constraints

## MCP Server Guidelines

When working with Model Context Protocol servers:

1. Follow type-safe function calling patterns
2. Optimize context window usage for token efficiency
3. Implement proper tool registration and documentation
4. Handle errors gracefully with appropriate recovery mechanisms
5. Consider security implications for all operations
6. Maintain consistent server state management
7. Follow registration patterns for tools in the VS Code extension
