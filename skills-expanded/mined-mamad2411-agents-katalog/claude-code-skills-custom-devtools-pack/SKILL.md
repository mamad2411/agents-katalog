```markdown
# Claude-Code-Skills-Custom-DevTools-Pack Development Patterns

> Auto-generated skill from repository analysis

## Overview
This skill teaches you the development patterns and conventions used in the `Claude-Code-Skills-Custom-DevTools-Pack` repository. The codebase is written in JavaScript without a framework, focusing on custom developer tooling. You'll learn about file organization, code style, commit conventions, and testing patterns to maintain consistency and quality in your contributions.

## Coding Conventions

### File Naming
- Use **camelCase** for file names.
  - Example: `customDevTool.js`, `helperFunctions.js`

### Import Style
- Use **relative imports** for modules within the project.
  - Example:
    ```javascript
    import { helperFunction } from './helperFunctions.js';
    ```

### Export Style
- Use **named exports** for functions, constants, or objects.
  - Example:
    ```javascript
    // In helperFunctions.js
    export function helperFunction() {
      // ...
    }
    ```
    ```javascript
    // In another file
    import { helperFunction } from './helperFunctions.js';
    ```

### Commit Message Convention
- Use **conventional commits** with the prefix `feat`.
  - Example: `feat: add custom logger utility`
- Keep commit messages concise (average ~43 characters).

## Workflows

### Adding a New Dev Tool
**Trigger:** When you want to add a new developer utility or tool to the pack  
**Command:** `/add-dev-tool`

1. Create a new JavaScript file using camelCase (e.g., `myNewTool.js`).
2. Implement your tool using named exports.
3. Import your tool into the main entry point if needed.
4. Write a corresponding test file named `myNewTool.test.js`.
5. Commit your changes using the conventional commit format:
   ```
   feat: add myNewTool for X functionality
   ```
6. Push your branch and open a pull request.

### Refactoring Existing Code
**Trigger:** When improving or restructuring code without changing its external behavior  
**Command:** `/refactor-code`

1. Identify the code to refactor.
2. Update the code following the coding conventions (camelCase, named exports, etc.).
3. Ensure all related imports and exports are updated.
4. Run all relevant tests to confirm nothing breaks.
5. Commit with a message like:
   ```
   feat: refactor helperFunctions for clarity
   ```
6. Push and open a pull request.

### Writing and Running Tests
**Trigger:** When adding new features or fixing bugs  
**Command:** `/run-tests`

1. Create or update a test file matching the pattern `*.test.js`.
2. Write tests for your feature or fix.
3. Use the project's preferred test runner (framework not specified; check project docs or scripts).
4. Run tests locally to ensure they pass.
5. Commit with a message like:
   ```
   feat: add tests for customLogger
   ```

## Testing Patterns

- Test files are named using the pattern `*.test.js`.
- Place tests alongside the modules they test or in a dedicated `tests` directory.
- The testing framework is not specified; refer to project documentation or package scripts for details.
- Example test file:
  ```javascript
  // customLogger.test.js
  import { customLogger } from './customLogger.js';

  test('logs messages correctly', () => {
    // ...test implementation
  });
  ```

## Commands
| Command         | Purpose                                      |
|-----------------|----------------------------------------------|
| /add-dev-tool   | Add a new developer tool to the pack         |
| /refactor-code  | Refactor existing code following conventions |
| /run-tests      | Run all tests in the codebase                |
```
