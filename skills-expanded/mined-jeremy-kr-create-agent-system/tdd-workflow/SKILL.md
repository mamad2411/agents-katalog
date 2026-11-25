---
name: tdd-workflow
description: "TDD workflow guide. Test first → Sanity Check → Implement → QA pattern. Use for test writing or TDD-related work."
---

# TDD Workflow

## Principles
- Write tests first (Red)
- **PO/PM gates test quality via Sanity Check (Gate)**
- Implementation agent makes tests pass (Green)
- QA agent performs comprehensive verification (Verify)

## Phase Flow

### Red Phase (test-writer)
1. Convert ticket acceptance criteria into test cases
2. Cover happy path + error path + edge cases
3. Run `pnpm test` → Confirm all tests FAIL
4. Save files: `tests/{module}/{feature}.test.ts`
5. Write test names that clearly map to acceptance criteria

### Gate Phase (po-pm)
1. Verify 1:1 mapping between test cases and acceptance criteria
2. Check for any uncovered acceptance criteria
3. Ensure no tests for behavior outside the spec
4. PASS/FAIL verdict (one revision on FAIL, escalate to Human on second failure)

### Green Phase (backend-dev)
1. Review test files
2. Implement minimal code to pass tests
3. Run `pnpm test` → Confirm all tests PASS
4. Remove unnecessary code (YAGNI)

### Verify Phase (qa-reviewer)
- Standard QA: Code review + test pass verification + build verification + scoring
- Visual QA Level 0 (CLI project, no screenshots needed)
