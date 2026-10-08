---
description: General Instructions - Consider for any file code related
globs: src/**/*.ts
alwaysApply: false
---
# General Guidelines

- Adhere to existing naming conventions and folder structures.
- Explore the codebase if unsure.
- public methods should always come on the top of the file.
- No need for comments on top of the function signature, except if its too complicated to understand.
- Prefix interface names with "I" (e.g., ICharacter).
- Specify function return types.
- When necessary, use `any` or `@ts-ignore` for complex typing. 
- KISS and DRY
- Do not remove working code, and avoid refactoring things unless specified.
- Use ts alias paths instead of relative paths
- Prefer named exports, avoid index.ts for re exporting components