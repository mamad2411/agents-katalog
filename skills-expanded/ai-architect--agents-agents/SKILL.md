# Workspace Rules

### Real Developer Refactoring Standard
When resolving linter errors, type-check failures, or bugs, do not use superficial "band-aid" fixes (e.g., casting to `any`/`unknown`, using `ts-ignore`, or mildly altering mutable state). Instead, act as a senior software engineer:
1. **Strict Typing:** Always trace and import the exact domain models (interfaces/types) rather than using generic objects or `Record` types.
2. **Structural Integrity:** If a function relies on complex mutable state (`let` variables reassigned in massive `if/else` blocks), refactor the logic. Use helper functions, pure functions, or Immediately Invoked Function Expressions (IIFEs) to return `const` objects.
3. **Declarative over Imperative:** Prioritize declarative patterns. If you touch a piece of code to fix a bug, leave the surrounding function cleaner and more robust than you found it.
