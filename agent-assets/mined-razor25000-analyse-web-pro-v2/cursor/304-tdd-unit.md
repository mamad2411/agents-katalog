---
description: 
globs: 
alwaysApply: false
---
## Context:

-  Create a component following TDD principles
-  Only apply to components that don't include integration tests (such as databases)
- You need to FIRST create the TEST file and then the component

## Workflow

0. Plan what you will do like where the components will be created, the name of the component etc...
1. Create a test file in the `__tests__` folder
2. Create the component in the correct folder (like `src/features`)
3. Run the tests with `pnpm test:ci`
4. Correct the component until the tests pass