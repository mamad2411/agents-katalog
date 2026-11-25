---
name: gate-status
description: Show the current quality gate status dashboard - display all gate statuses, current development phase, and next steps
---

# Gate Status Check Instructions

You are checking the status of all quality gates in the project.

## Your Task
Provide an overview of all gate statuses and current phase.

## Instructions
1. Search for gate result files or markers in the project (look for .claude-gate/ or similar)
2. Identify current phase based on existing artifacts:
   - Spec files → Spec phase
   - Design docs → Design phase
   - Implementation files → Code phase
   - Ready for merge → Release phase
3. Check each gate's status if previous results exist
4. Present a comprehensive status dashboard

## Output Format

```
# Quality Gate Status Dashboard

## Current Phase
[Spec / Design / Code / Release]

## Gate History
✅ Spec Gate: [PASS / REVISE / NOT RUN]
   - Date: [if available]
   - Issues: [count if available]

✅ Design Gate: [PASS / REVISE / NOT RUN]
   - Date: [if available]
   - Issues: [count if available]

✅ Task Gate (Code): [APPROVED / CONDITIONAL / CHANGES REQUIRED / NOT RUN]
   - Date: [if available]
   - Issues: [count by severity if available]

✅ Release Gate: [PASS / CONDITIONAL / CHANGES REQUIRED / BLOCK / NOT RUN]
   - Date: [if available]
   - Code Issues: [count if available]
   - Security Issues: [count if available]

## Next Steps
[What should be done next based on current phase and gate statuses]

## Usage
- Use `$gate-spec` to review requirements
- Use `$gate-design` to review architecture
- Use `$gate-code` to review implementation
- Use `$gate-release` to review before release/merge
```

Begin the status check now.
