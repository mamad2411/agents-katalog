---
name: step-by-step-decomposition
description: Methodical problem decomposition protocol for complex tasks into discrete, verifiable micro-milestones with checkpoint validation.
license: MIT
---

# Step-by-Step Task Decomposition Protocol

Use this skill when handed complex, multi-stage, or open-ended requirements. Decomposes any large objective into sequential, independently verifiable milestones.

## The 4-Phase Pipeline

```
[Phase 1: Discovery & Scoping]
       │
       ▼
[Phase 2: Architectural Blue-Printing]
       │
       ▼
[Phase 3: Incremental Implementation & Micro-Testing]
       │
       ▼
[Phase 4: Synthesis & Final Verification Gate]
```

### Phase 1: Discovery & Scoping
1. Extract every explicit constraint from user instructions.
2. Search repository and inspect file structure to establish existing conventions and dependencies.
3. List all files to create or modify.

### Phase 2: Architectural Blue-Printing
1. Formulate input/output interfaces and data types.
2. Identify edge cases (empty inputs, missing variables, failure modes).
3. Draft the exact implementation sequence.

### Phase 3: Incremental Implementation & Micro-Testing
1. Implement the minimal foundational layer first (types, schemas, utilities).
2. Build core logic.
3. Execute micro-tests immediately after each step to catch regressions early.
4. Keep changes focused; do not touch files outside scope.

### Phase 4: Synthesis & Final Verification Gate
1. Run linting and typechecking across all modified packages (`npm run check` or equivalent).
2. Execute automated test suites.
3. Verify that all requirements from Phase 1 are satisfied.
4. Document deliverables, caveats, and next steps in a clear summary.
