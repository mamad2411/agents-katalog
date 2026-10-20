---
name: QPLAN
version: 1.0.0
description: Analyze codebase and create consistent, minimal implementation plan that reuses existing patterns. Extracts requirements, estimates story points, validates interfaces.
trigger: QPLAN
dependencies:
  agents:
    - planner
    - requirements-analyst
tools:
  - planning-poker-calc.py
  - interface-validator.py
claude_tools:
  - Read
  - Grep
  - Glob
  - Edit
  - Write
  - Bash
---

# QPLAN - Implementation Planning

## Purpose

Analyze codebase to create implementation plans that are consistent with existing patterns, minimal in scope, and reuse existing components.

## Workflow

### 1. Classify Task Type
**Agent: planner**
- New feature, enhancement, bug fix, refactoring?
- Complexity estimate (simple/moderate/hard)
- Required expertise areas

### 2. Extract Requirements
**Agent: requirements-analyst**
- Parse user request for explicit requirements
- Identify implicit requirements (error handling, validation, etc.)
- Document acceptance criteria
- Flag edge cases and assumptions

### 3. Analyze Codebase
**Agent: planner**
- Find similar implementations (Grep patterns)
- Identify reusable utilities, types, components
- Document file structure and naming conventions
- Check for existing tests to use as templates

### 4. Generate Implementation Plan
**Agent: planner**
- Break down into subtasks (0.05-5 SP each for coding)
- Use planning-poker-calc.py for estimates
- Define interface contracts
- Identify dependencies (libraries, services, other features)
- Document technical risks and mitigation strategies

### 5. Validate Interfaces
**Tool: interface-validator.py**
- Check proposed interfaces against existing patterns
- Validate type consistency
- Ensure backward compatibility if modifying existing code

## Tools

### planning-poker-calc.py
Calculates story point estimates based on:
- Code complexity (cyclomatic)
- Number of files to modify
- Test coverage requirements
- Integration points

**Usage:**
```bash
python planning-poker-calc.py \
  --files-count 3 \
  --test-files 2 \
  --complexity moderate \
  --integrations 1
```

### interface-validator.py
Validates interface contracts:
- Type consistency
- Naming conventions
- Breaking changes detection

**Usage:**
```bash
python interface-validator.py \
  --interface-file proposed-interface.ts \
  --codebase-path ./src
```

## Output Format

```markdown
# Implementation Plan: [Feature Name]

**Classification:** [New Feature/Enhancement/Bug Fix/Refactor]
**Complexity:** [Simple/Moderate/Hard]
**Total Estimate:** [X] SP

## Requirements Analysis

### REQ-101: [Requirement]
- **Acceptance Criteria:** [testable criteria]
- **Priority:** P0/P1/P2
- **Edge Cases:** [list]

### REQ-102: [Requirement]
...

## Codebase Analysis

**Similar Implementations:**
- `/path/to/similar-feature.ts` - [pattern to reuse]
- `/path/to/another-example.ts` - [utility functions]

**Reusable Components:**
- `utilityFunction()` - for [purpose]
- `SharedType` - interface for [data]

**Naming Conventions:**
- Files: `kebab-case.ts`
- Functions: `camelCase`
- Types: `PascalCase`

## Implementation Tasks

### Task 1: Setup Types & Interfaces (0.5 SP)
- Create `types/feature-name.ts`
- Define core interfaces
- Export from index
- **Dependencies:** None
- **Risk:** Low

### Task 2: Implement Core Logic (2 SP)
- Create `feature-name.service.ts`
- Implement main functions
- Add input validation
- **Dependencies:** Task 1
- **Risk:** Medium - requires [library] integration

### Task 3: Add Tests (1.5 SP)
- Create `feature-name.spec.ts`
- Test happy path (REQ-101)
- Test edge cases (REQ-102)
- Achieve 80%+ coverage
- **Dependencies:** Task 2
- **Risk:** Low

### Task 4: Integration (1 SP)
- Wire into existing system
- Update dependencies
- Add error handling
- **Dependencies:** Task 3
- **Risk:** Medium - breaking change risk

## Dependencies

**External Libraries:**
- [library-name] v[version] - for [purpose]
  - Risk: [description]
  - Mitigation: [strategy]

**Internal Services:**
- [service-name] - provides [functionality]
  - Risk: [description]
  - Mitigation: [strategy]

## Technical Risks

### Risk 1: [Description]
- **Impact:** High/Medium/Low
- **Probability:** High/Medium/Low
- **Mitigation:** [strategy]

## Interface Contracts

```typescript
// Proposed interfaces
export interface FeatureName {
  id: string;
  // ...
}
```

## Validation Results

**Interface Validator:**
- Consistency: PASS
- Breaking Changes: NONE
- Convention Alignment: PASS

## Story Point Summary

| Task | SP | Confidence |
|------|----|-----------|
| Task 1 | 0.5 | High |
| Task 2 | 2.0 | Medium |
| Task 3 | 1.5 | High |
| Task 4 | 1.0 | Medium |
| **Total** | **5.0** | **Medium** |

## Build vs Buy

[If applicable: analysis of whether to build custom or use existing solution]

## Next Steps

1. Run QCODET to generate test stubs
2. Implement tests until they fail (TDD red phase)
3. Run QCODE to implement functionality
4. Run QCHECK for code review
```

## Success Criteria

- Clear task breakdown with SP estimates
- All requirements have REQ-IDs
- Reusable components identified
- Dependencies documented with risks
- Interface contracts defined
- Validation checks pass

## Related Skills

- **QNEW**: Use first for initial feature scoping
- **QCODET**: Next step - write tests based on plan
- **QCODE**: Implement functionality per plan
- **QCHECK**: Final review of implementation
