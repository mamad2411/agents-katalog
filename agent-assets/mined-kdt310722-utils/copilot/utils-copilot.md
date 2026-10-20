---
applyTo: '**'
---

# Project Coding Guidelines

This document provides comprehensive coding standards for AI assistants working on this project.

## Project Overview

This project (`@kdt310722/utils`) is a TypeScript utility library that provides a collection of utility functions for JavaScript/TypeScript applications. The library is designed to be modular, type-safe, and easy to use, with utilities organized into logical modules like array, promise, string, object, and more.

## Tech Stack

- **Node.js LTS** - Runtime environment (>=22.15.0)
- **TypeScript** - Programming language with static typing
- **PNPM** - Package manager
- **@kdt310722/tsconfig** - TypeScript configuration
- **@kdt310722/eslint-config** - ESLint configuration and style enforcement
- **Vitest** - Testing framework
- **tsup** - TypeScript bundler for building ESM/CJS outputs
- **changelogen** - Changelog generation
- **simple-git-hooks** - Git hooks management

## Project Structure

The project follows a modular structure where each utility category has its own directory:

- `src/array/` - Array manipulation utilities
- `src/promise/` - Promise and async utilities
- `src/string/` - String manipulation utilities
- `src/object/` - Object manipulation utilities
- `src/function/` - Function utilities
- `src/common/` - Common types and utilities
- `src/node/` - Node.js specific utilities
- `src/json/` - JSON parsing and serialization
- `src/buffer/` - Buffer manipulation
- `src/number/` - Number formatting and utilities
- `src/time/` - Time and date utilities
- `src/event/` - Event emitter utilities

## TypeScript Configuration

### Project-Specific Settings

- Target ES modules (`"type": "module"` in package.json)
- Use strict TypeScript configuration from `@kdt310722/tsconfig`
- Dual package exports (ESM/CJS) via tsup

### Type Safety Rules

- Use TypeScript's strict type checking
- Prefer `unknown` over `any` type
- Use type-only imports: `import type { Type }` for types only
- Prefer inline type imports: `import { type Type, value }` when mixing
- Define clear types for functions and variables
- Only specify return types for complex types or when not obvious from code
- Use utility types (`Pick`, `Omit`, `Partial`) for type manipulation
- Extract nested interfaces into separate interfaces for reusability

## Code Formatting

### Indentation & Spacing

- Use 4 spaces for indentation, never tabs
- No enforced maximum line length
- Remove trailing whitespace
- Add blank line at end of files
- Use LF (`\n`) line endings
- Place spaces inside object braces: `{ like: this }`
- Add space before opening braces: `function name() {`

### Punctuation & Symbols

- No semicolons at end of statements
- Use single quotes (`'`) for strings in JS/TS
- Use double quotes (`"`) for JSX attributes
- Use trailing commas in ES5 style:
    - Always for multiline arrays and objects
    - Never for imports/exports
    - Never for function parameters
- Always use parentheses with arrow functions: `(param) => {}`
- Use "one true brace style": opening brace on same line
- Closing bracket on new line
- Empty arrow function bodies on single line: `() => {}`

### Line Breaking & Padding

- Add blank lines before and after major code blocks
- Add blank line before `return` statements
- Always blank line before and after: `class`, `interface`, `function`, `if`, `for`, `while`, `switch`, `try`
- No blank lines between `case` statements in `switch`
- Add blank line between variable assignment and subsequent method calls

## Import Organization

### Import Order (Strict)

1. Node.js built-in modules (with `node:` prefix)
2. External libraries (alphabetical)
3. Side-effect imports (`import 'module'`)
4. Internal modules (by proximity: `../`, `./`)

### Import Rules

- Remove unused imports automatically
- Keep import statements at top of file
- Keep each import on one line (no line breaks in import statements)
- Keep export statements on one line without line breaks
- No import type side effects

## Function & Variable Rules

### Function Guidelines

- Keep return statements clear and explicit
- Maximum 30 lines per function (recommended)
- Maximum 3 levels of nesting depth
- Prefix unused parameters with underscore: `_error`, `_unused`
- Use descriptive names indicating purpose
- Prefer arrow functions with direct return for simple transformations
- Keep entire return expressions on one line when possible
- Extract complex inline objects to variables for readability
- For async functions returning single awaited expression, return directly
- Omit `await` in direct returns if not needed for error handling
- **Function signatures should be on single lines when possible** for better readability
- Use concise forms for simple conditional logic (e.g., logical OR operator for simple conditions)
- Prefer single-line implementations for simple timeout/conditional logic
- **Prefer single-line returns for simple method implementations** - When a method simply calls another function or returns a direct expression, use single-line returns without intermediate variables
- **Use consistent parameter destructuring patterns** - When functions accept options objects, use destructuring with default values in the parameter signature (e.g., `{ option1 = default1, option2 = default2 } = {}`) for consistency across the codebase

### Variable Rules

- Use camelCase for variables and functions
- Use PascalCase for classes and components
- Use UPPERCASE_SNAKE_CASE for global constants
- Keep function parameters on same line when reasonable
- Group variable declarations by type (`let` vs `const`) with blank lines between groups
- Apply grouping only to single-line declarations (multi-line declarations remain separate)

## Naming Conventions

### File & Directory Naming

- Files: kebab-case for regular files, PascalCase for component files
- Directories: kebab-case grouped by functionality
- TypeScript files: `.ts` extension
- Test files: `.test.ts` suffix

### Code Naming

- Variables and functions: camelCase
- Classes and interfaces: PascalCase
- Constants: UPPERCASE_SNAKE_CASE
- Private class fields: prefer `#privateField` syntax

## Code Organization

### File Structure

1. Imports (following grouping rules)
2. Type definitions and interfaces
3. Constants and configuration
4. Implementation (functions, classes)
5. Exports (prefer named exports, alphabetically organized)

### Module Organization

- Each module has its own directory under `src/`
- Each module exports through `index.ts` file
- Use `export * from './file'` pattern for re-exports
- Use `export type * from './types'` for type-only exports
- Group related functionality in the same module

### Export Patterns

- Use named exports over default exports
- Export types separately: `export type * from './types'`
- Main index exports modules as namespaces: `export * as arr from './array'`
- Each module index re-exports all functionality from its files

## Testing Guidelines

### Testing Framework

- Use Vitest for testing
- Test files should be in `test/` directory with `.test.ts` extension
- Use `expect` and `test` from vitest
- Run tests with `pnpm test` or `pnpm dev` for watch mode

### Test Directory Structure

- **Mirror source structure**: Test directory structure should mirror the `src` directory structure
- **Function-based naming**: Test file names should use the actual function name in kebab-case + `.test.ts`
- **Examples**:
    - `src/promise/deferred.ts` → `test/promise/create-deferred.test.ts`
    - `src/array/chunk.ts` → `test/array/chunk.test.ts`
    - `src/string/trim.ts` → `test/string/trim-string.test.ts`

### Testing Patterns

- Write comprehensive unit tests for all utility functions
- Test edge cases and error conditions
- Use descriptive test names that explain the behavior being tested
- Group related tests using `describe` blocks for better organization
- Aim for 100% test coverage (statements, branches, functions, lines)
- **Do not create test files for index.ts files that only re-export from other modules** - focus testing on actual implementation files

## Build and Development

### Build Process

- Use `tsup` for building both ESM and CJS outputs
- Generate TypeScript declarations with separate `tsc` command
- Copy source files to dist for development reference
- Clean dist directory before each build

### Development Scripts

- `pnpm dev` - Run tests in watch mode
- `pnpm build` - Build the library
- `pnpm test` - Run tests once
- `pnpm lint` - Lint code
- `pnpm lint:fix` - Fix linting issues
- `pnpm typecheck` - Type checking

## Code Quality Guidelines

### Performance Considerations

- Use appropriate data structures for the use case
- Avoid unnecessary async/await in direct returns
- Prefer native array methods over manual loops when appropriate

### Error Handling

- Use proper error types and messages
- Handle edge cases gracefully
- Validate input parameters when necessary

## Implementation Guidelines

### Scope Limitation Rule

- **Only implement exactly what is requested in the task**
- Do not create additional code, features, or functionality beyond the explicit requirements
- If you think there might be related improvements or additions, ask the user first before implementing
- Focus on the specific requirements and avoid scope creep
- Stick to the minimal viable implementation that satisfies the request

### Default Exclusions Rule

By default, **skip the following unless explicitly requested**:

- **Input validation and parameter checking** - Only add when specifically asked
- **Documentation** - Comments, JSDoc, README updates, or inline documentation
- **Unit tests and test files** - Only create when testing is specifically requested
- **Demo files and usage examples** - Only provide when examples are explicitly needed
- **Example implementations** - Only create when the user asks for examples

**Important**: Only create these items when the user specifically asks for them in their request. This keeps implementations focused and prevents unnecessary work.

### Code Documentation Rule

- **Never generate comments in source code by default** - Code should be self-documenting through clear naming and structure
- Only add comments when explicitly requested or when code behavior is genuinely non-obvious
- Prefer refactoring unclear code over adding explanatory comments
- Use meaningful variable and function names that eliminate the need for comments

### Code Quality Checks Rule

- **Never run automated checks unless explicitly requested** - Do not automatically run ESLint, TypeScript checks, tests, or other validation tools
- Only execute `pnpm lint`, `pnpm typecheck`, `pnpm test`, or similar commands when the user specifically asks for them
- Focus on implementing the requested changes without automatic validation unless verification is requested
- Let the user decide when to run quality checks and validation

## Code Reuse Guidelines

### Reuse Principles

- Follow Open/Closed principle: extend without modifying existing code
- Prefer composition over inheritance
- Extract reusable logic into utility functions
- Maintain backward compatibility when extending functionality

### Avoiding Duplication

- Follow DRY (Don't Repeat Yourself) principle
- Apply Rule of Three: if code is copy-pasted 3 times, extract it into reusable function
- Search existing utilities before implementing new functionality

### Maintainability

- Keep functions focused on single responsibility
- Use meaningful variable and function names
- Maintain consistent code organization across modules
- Use TypeScript's type system to prevent runtime errors
