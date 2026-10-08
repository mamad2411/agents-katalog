---
description: 
globs: 
alwaysApply: true
---
# General Instructions for AI Assistant

- Address me as "Captain" when responding to me
- Follow all instructions CAREFULLY to make sure we succeed with our tasks

## About the Project

We are building a Redis server clone. We are writing the software in Go.

## Core Philosophy

1. **Simplicity:** Prioritize simple, clear, and maintainable solutions. Avoid unnecessary complexity or over-engineering.
2. **Iterate:** Prefer iterating on existing, working code rather than building entirely new solutions from scratch, unless fundamentally necessary or explicitly requested.
3. **Focus:** Concentrate efforts on the specific task assigned. Avoid unrelated changes or scope creep.
4. **Quality:** Strive for a clean, organized, well-tested, and secure codebase.

## Identifying and Fixing Problems
- Work hard to understand the root cause of a problem
- Don't fix symptoms. Fix the root cause instead

## Code Quality Rules
- Always prefer simple and elegant code
- Avoid complex abstractions when simpler solutions are available
- Prefer using constants over "magic" numbers
- Prefer early returns from functions over nested code
- Prefer short functions over long functions
- Avoid mixing side-effects and logic in the same function when possible, to make it easier to unit test the logic in isolation
- Keep the boundaries between third-party libraries and our code clear
- Keep the boundaries between IO and business logic clear

## Performance Rules
- Avoid unnecessary memory allocations in hot code paths (for example in loops, or other frequently executed code paths)

## Code Commenting Rules
- Comments should answer the question "why?" instead of "what?"
- Add comments to give the reader the necessary context for understanding the code
- Avoid commenting obvious and self-documenting code. Strive to make the code self-documenting instead by using clear naming conventions

## Unit Testing Rules
- Write unit tests for implementations
- After making a change, always run the tests to verify that the change works as expected and doesn't break existing functionality
- Prefer simple unit tests. If a feature requires a complex unit test, consider refactoring the code to make it simpler to write tests for
- Only unit test public functions and methods
- Remember to test edge cases and unexpected input in unit tests
- The unit tests MUST NOT require starting the software itself (if applicable, eg. a server application)
- Removing a failing test IS NOT the correct solution for fixing the failing test. A failing test means that either the test or the implementation is wrong, and one of them (or both) need to be fixed

# Documenting learnings (important!)

When you're working on a task and learn something new (maybe through mistakes, or otherwise) that can
help you work better in the future, document it in `docs/ai-learnings.md`. 

Be sure to read `docs/ai-learnings.md` when starting work on new tasks as well.
