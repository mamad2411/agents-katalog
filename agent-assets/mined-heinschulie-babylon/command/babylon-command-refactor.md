# Refactor

Refactor implementation code while keeping all tests passing. Read the code cold, apply structural improvements, and verify after each change.

## Variables

adw_id: $1

## Instructions

### 1. Discover Changed Files

- Run `git diff --stat origin/main` to identify files changed on this branch
- Separate implementation files from test files
- Read all changed implementation and test files to understand the current state

### 2. Load Reference Context

Read these TDD reference docs for refactoring guidance:

- `.claude/skills/tdd/deep-modules.md` — deep module design (small interface, deep implementation)
- `.claude/skills/tdd/interface-design.md` — interface design for testability
- `.claude/skills/tdd/refactoring.md` — refactoring patterns and candidates

### 3. Run Tests (Baseline)

- Run the test suite to confirm all tests pass before any changes
- If tests fail before refactoring, STOP and report the failure — do not refactor broken code

### 4. Refactor

Apply structural improvements one at a time. After EACH change, run tests.

Candidates (from refactoring.md):
- Extract duplication
- Deepen modules (move complexity behind simple interfaces)
- Apply SOLID principles where natural
- Simplify complex conditionals
- Improve naming

**Constraints — no new behavior:**
- Do NOT add new features or functionality
- Do NOT write new tests
- Do NOT change observable behavior
- All existing tests must continue to pass after each refactor step
- If a refactor breaks a test, revert that change

### 5. Report

Output summary of changes made:
- What was refactored and why
- Run `git diff --stat` to show files changed
