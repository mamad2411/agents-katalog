# Cline Project Intelligence

This file captures important patterns, preferences, and project intelligence that help Cline work more effectively. It serves as a learning journal that evolves as the project progresses.

## Project Patterns

Document recurring patterns specific to this project

## User Preferences

Note user preferences for code style, communication, and workflow

## Implementation Paths

Document critical implementation paths that are important to understand

## Known Challenges

List known challenges and how to approach them

## Problem Management Protocol

### Pre-Modification Check

* MUST check and document all workspace problems before any file modification
* Count and categorize problems (ESLint, TypeScript, etc.)
* Document specific error types and their locations
* Analyze root causes of existing problems

### During Modification

* Keep track of which problems are being addressed
* Consider impact of changes on other parts of the codebase
* Follow established patterns and coding standards
* Document any new patterns or solutions discovered

### Post-Modification Check

* MUST verify workspace problems after every file modification
* Compare problem counts with pre-modification state
* Document any new problems that emerged
* Ensure no regressions were introduced
* Fix any new problems before proceeding

### Problem Resolution Priority

1. Type safety issues (TypeScript errors)
2. Test integrity issues (Jest/testing errors)
3. Code style violations (ESLint errors)
4. Documentation formatting (Markdown lint)

## Tool Usage

### Configuration Management

* Keep TypeScript version at ~5.7.0 for project stability
* Use flat config format for ESLint (eslint.config.mjs)
* Maintain consistent path resolution across tools
* Ensure test files are properly included in tsconfig.json

### Development Workflow

* Verify workspace problems before and after changes
* Run both lint and test after configuration updates
* Use TypeScript path aliases consistently
* Document emerging patterns naturally

### Error Resolution

* Check configuration files when module resolution fails
* Verify TypeScript and Jest path configurations align
* Ensure ESLint parser options match TypeScript setup
* Document solutions that emerge from practice

## Decision Evolution

### Key Decisions

* Modern ESLint flat configuration adoption
* TypeScript version constraint (~5.7.0)
* Unified root directory for src and tests
* Natural pattern documentation approach
* Strict problem management protocol implementation

### Configuration Patterns

* ESLint and TypeScript integration
* Jest and TypeScript path resolution
* Source and test file organization
* Tool chain consistency
* Problem tracking and resolution workflow

## Workflow Optimizations

### Development Experience

* Consistent path aliases across toolchain
* Automated linting and testing
* Clear error messages
* Pattern-based problem solving
* Proactive problem detection and resolution

### Testing Strategy

* Jest must be configured using @jest/globals instead of @types/jest
* All functions must have a corresponding Jest test file before implementation (TDD)
* Test execution must be automated before every commit using Husky
* Jest must enforce strict type safety; no usage of `any` in test files
* Jest configuration aligned with TypeScript
* Path resolution consistency
* Coverage reporting integration
* Type-safe test execution
* Ensure isolatedModules: true in Jest configuration

## Code Organization

### Project Structure

* Source and test files under common root
* Consistent path alias usage (@/*)
* Clear separation of concerns
* Natural pattern emergence

## Markdown Standards

The project uses markdownlint to enforce consistent markdown formatting. Always check the "Workspace Problems" section for markdownlint warnings before and after editing files. Follow these key rules:

### Headers

* MD001: Heading levels should only increment by one level at a time
* MD022: Headings should be surrounded by blank lines
* MD023: Headings must start at the beginning of the line
* MD024: Avoid multiple headings with the same content
* MD025: Only one top-level (H1) heading per document
* MD041: First line in file should be a top-level heading

### Lists

* MD004: Use consistent unordered list style (asterisks)
* MD005: Maintain consistent indentation for list items at the same level
* MD007: Use consistent unordered list indentation
* MD030: Include spaces after list markers
* MD032: Lists should be surrounded by blank lines

### Spacing

* MD009: No trailing spaces
* MD010: No hard tabs, use spaces
* MD012: No multiple consecutive blank lines
* MD031: Fenced code blocks should be surrounded by blank lines
* MD047: Files should end with a single newline character

### Code and Links

* MD034: No bare URLs
* MD038: No spaces inside code span elements
* MD039: No spaces inside link text
* MD040: Fenced code blocks should have a language specified
* MD042: No empty links

### Tables

* MD055: Consistent table pipe style
* MD056: Consistent table column count
* MD058: Tables should be surrounded by blank lines

---

This file evolves naturally as Cline learns more about the project and user preferences. It should not be forced but should grow organically through experience.

YOU MUST NEVER DO A MEMORY RESET EVEN IF THE USER ASKS YOU EXPLICITLY!
YOU MUST update memory bank AUTOMATICALLY BEFORE YIELDING A « TASK COMPLETE ».
YOU MUST ensure that all changes to documentation are reflected in the Memory Bank promptly.
