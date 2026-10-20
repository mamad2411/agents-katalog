## You should prioritize factual accuracy over agreeing with the user. 
### When a user makes a statement that is factually incorrect: 
1. Politely acknowledge receipt of the question. 
2. Clearly point out the factual error. 
3. Provide the correct information. 
4. Offer assistance with the corrected information.

## This document contains critical information about working with this codebase. Follow these guidelines precisely.

### Code Quality

1. Type hints required for all code
2. Public APIs must have docstrings
3. Functions must be focused and small
4. Follow existing patterns exactly
5. Line length: 88 chars maximum

### Code Style

1. PEP 8 naming (snake_case for functions/variables)
2. Class names in PascalCase
3. Constants in UPPER_SNAKE_CASE
4. Document with docstrings
5. Use f-strings for formatting

### Development Philosophy

1. Simplicity: Write simple, straightforward code
2. Readability: Make code easy to understand
3. Performance: Consider performance without sacrificing readability
4. Maintainability: Write code that's easy to update
5. Testability: Ensure code is testable
6. Reusability: Create reusable components and functions
Less Code = Less Debt: Minimize code footprint

### Coding Best Practices

1. Early Returns: Use to avoid nested conditions
2. Descriptive Names: Use clear variable/function names (prefix handlers with "handle")
3. Constants Over Functions: Use constants where possible
4. DRY Code: Don't repeat yourself
5. Functional Style: Prefer functional, immutable approaches when not verbose
6. Minimal Changes: Only modify code related to the task at hand
7. Function Ordering: Define composing functions before their components
8. TODO Comments: Mark issues in existing code with "TODO:" prefix
9. Simplicity: Prioritize simplicity and readability over clever solutions
10. Build Iteratively Start with minimal functionality and verify it works before adding complexity
11. Run Tests: Test your code frequently with realistic inputs and validate outputs
12. Build Test Environments: Create testing environments for components that are difficult to validate directly
13. Functional Code: Use functional and stateless approaches where they improve clarity
14. Clean logic: Keep core logic clean and push implementation details to the edges
15. File Organsiation: Balance file organization with simplicity - use an appropriate number of files for the project scale


