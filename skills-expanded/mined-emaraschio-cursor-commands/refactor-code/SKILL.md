---
name: refactor-code
description: Refactor for clarity without behavior change
user-invocable: false
---
## Overview

Refactor the selected code to improve its quality while maintaining the same functionality, providing the refactored code with explanations of the improvements made.

## Steps

1. **Code Quality Improvements**
    - Extract reusable functions or components
    - Eliminate code duplication
    - Improve variable and function naming
    - Simplify complex logic and reduce nesting
2. **Performance Optimizations**
    - Identify and fix performance bottlenecks
    - Optimize algorithms and data structures
    - Reduce unnecessary computations
    - Improve memory usage
3. **Maintainability**
    - Make the code more readable and self-documenting
    - Add appropriate comments where needed
    - Follow SOLID principles and design patterns
    - Improve error handling and edge case coverage

## Refactor Code Checklist

- [ ] Extracted reusable functions or components
- [ ] Eliminated code duplication
- [ ] Improved variable and function naming
- [ ] Simplified complex logic and reduced nesting
- [ ] Identified and fixed performance bottlenecks
- [ ] Optimized algorithms and data structures
- [ ] Made code more readable and self-documenting
- [ ] Followed SOLID principles and design patterns
- [ ] Improved error handling and edge case coverage

## Guardrails

- Preserve existing behavior; a refactor must not change observable output.
- Keep changes within the refactor target; do not touch unrelated code.
- Do not commit, push, merge, or run production scripts without consent; wait for an explicit request before any destructive git action.
- Do not print, log, or commit secrets or credentials encountered while refactoring; flag any exposed secret instead.