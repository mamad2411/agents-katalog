---
name: refactoring
description: Safe, incremental code refactoring with behavior preservation
activation: manual
---

# Refactoring Skill

## Purpose
Improve code structure, readability, and maintainability WITHOUT changing behavior.

## Golden Rule
> After every refactoring step, ALL existing tests must still pass. If they don't, revert immediately.

## Protocol

### Phase 1: Identify Refactoring Targets
Scan for code smells:
- Duplicated code (DRY violations)
- Long functions (>30 lines = candidate)
- Deep nesting (>3 levels)
- Large files (>300 lines = candidate for splitting)
- God objects (one class/module doing everything)
- Magic numbers/strings
- Dead code (unused functions, unreachable branches)
- Inconsistent naming
- Tight coupling between modules

### Phase 2: Ensure Safety Net
1. Verify existing test coverage for the target code
2. If coverage is insufficient → write characterization tests FIRST
3. Characterization tests capture CURRENT behavior (even if buggy)
4. Run full test suite — establish green baseline

### Phase 3: Refactor Incrementally
1. Apply ONE refactoring at a time
2. After each change:
   - Save
   - Run tests
   - If green → commit with descriptive message
   - If red → revert immediately
3. Common refactoring moves:
   - Extract Function/Method
   - Rename for clarity
   - Inline unnecessary abstraction
   - Extract constant from magic value
   - Move function to appropriate module
   - Replace conditional with polymorphism
   - Simplify nested conditionals (guard clauses)

### Phase 4: Verify
1. Run full test suite — all green
2. Compare behavior: before vs after (same inputs → same outputs)
3. Review the diff — is it cleaner, more readable?
4. No functional changes should appear in the diff

## Rules
- NEVER refactor and add features simultaneously
- NEVER refactor without a passing test suite
- One refactoring move per commit
- If tests break → revert, don't fix forward
- Refactoring is about STRUCTURE, not behavior
