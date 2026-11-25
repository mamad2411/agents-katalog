```markdown
# dokion Development Patterns

> Auto-generated skill from repository analysis

## Overview
This skill teaches the core development patterns and conventions used in the `dokion` Python repository. You'll learn how to structure files, write imports and exports, and follow commit and testing practices specific to this codebase. This guide is essential for contributing code that aligns with the established style and workflow of the project.

## Coding Conventions

### File Naming
- Use **kebab-case** for all file names.
  - **Example:**  
    ```
    my-module.py
    data-processor.py
    ```

### Import Style
- Use **relative imports** within the package.
  - **Example:**  
    ```python
    from .utils import parse_data
    from .models import Document
    ```

### Export Style
- Use **named exports** to explicitly define what is available from a module.
  - **Example:**  
    ```python
    def process_document(doc):
        # processing logic
        return ...

    __all__ = ["process_document"]
    ```

### Commit Patterns
- Commit messages are freeform, with no strict prefixes.
- Average commit message length is about 58 characters.
  - **Example:**  
    ```
    Add initial document parsing logic and tests
    ```

## Workflows

### Adding a New Module
**Trigger:** When you need to introduce new functionality.
**Command:** `/add-module`

1. Create a new Python file using kebab-case (e.g., `new-feature.py`).
2. Implement your logic, using relative imports for dependencies.
3. Define named exports via `__all__`.
4. Write corresponding test files (see Testing Patterns).
5. Commit your changes with a clear, descriptive message.

### Updating an Existing Module
**Trigger:** When modifying or extending current functionality.
**Command:** `/update-module`

1. Locate the relevant module file.
2. Make changes, ensuring you maintain relative import style.
3. Update `__all__` if new exports are added.
4. Update or add tests as needed.
5. Commit with a descriptive message.

### Running Tests
**Trigger:** To verify code correctness after changes.
**Command:** `/run-tests`

1. Identify test files matching the `*.test.*` pattern.
2. Run tests using your preferred Python test runner (framework is unspecified).
   - **Example:**  
     ```
     python my-module.test.py
     ```
3. Review output and fix any failing tests.

## Testing Patterns

- Test files use the `*.test.*` naming convention.
  - **Example:**  
    ```
    parser.test.py
    utils.test.py
    ```
- The testing framework is not specified; use standard Python testing approaches.
- Place tests alongside or near the modules they cover.

## Commands
| Command         | Purpose                                      |
|-----------------|----------------------------------------------|
| /add-module     | Scaffold and implement a new module          |
| /update-module  | Update existing module and maintain exports  |
| /run-tests      | Run all test files matching `*.test.*`       |
```