---
description: "Fix code style issues according to project conventions"
allowed-tools: ["Edit", "MultiEdit", "Read", "Bash", "Grep", "Glob"]
---

Automatically fix code style issues throughout the project:

1. **Detect Project Style Conventions**:
   - Look for configuration files (.eslintrc, .prettierrc, pyproject.toml, etc.)
   - Identify the primary programming languages in the project
   - Check for existing formatter/linter setup

2. **Language-Specific Style Fixes**:

   **JavaScript/TypeScript**:
   - Run Prettier for formatting if configured
   - Fix ESLint issues that can be auto-corrected
   - Standardize import statements and ordering

   **Python**:
   - Apply Black formatting if available
   - Run isort for import organization
   - Fix basic PEP 8 violations

   **Go**:
   - Run `gofmt` or `goimports`
   - Apply standard Go formatting

   **Rust**:
   - Run `rustfmt` for code formatting
   - Apply standard Rust conventions

3. **Universal Style Fixes**:
   - Remove trailing whitespace
   - Ensure consistent line endings
   - Fix indentation issues (tabs vs spaces)
   - Remove unnecessary empty lines
   - Ensure files end with newline

4. **Code Organization**:
   - Sort imports alphabetically where appropriate
   - Group related imports together
   - Remove unused imports and variables

5. **Execution**:
   - Show what changes will be made
   - Apply fixes file by file
   - Run project linters/formatters if available
   - Provide summary of changes made

Ask for confirmation before making changes to multiple files.