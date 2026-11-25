---
name: verification-contracts
description: "Generate verification contracts before delegating tasks to sub-agents, defining how success will be measured. Triggers on: verification contract, delegation contract, task verification, contract-first delegation."
---

# Verification Contracts Skill

> 🎯 **Contract-first decomposition:** Only delegate a task if you can verify its completion.
>
> Before delegating ANY task to a specialist, generate a verification contract that defines how success will be measured.

## When to Load This Skill

Load this skill when:
- About to delegate a task to a sub-agent
- Completing a delegated task and need to verify
- Developer/overlord receiving work and need to understand contract structure

## Contract Generation

**Before every delegation**, generate a `verificationContract`:

```
Task: "Add dark mode toggle to settings page"
       │
       ▼
┌─────────────────────────────────────────────────────────────────────┐
│ PATTERN MATCHING                                                    │
│                                                                     │
│ 1. Check for advisory patterns (no automated verification):        │
│    - "investigate", "research", "explore", "discuss", "plan",      │
│      "design", "audit", "review", "analyze"                        │
│                                                                     │
│ 2. Check for skip patterns (minimal verification):                 │
│    - "document", "readme", "docs", "comment", "typo", "spelling"   │
│                                                                     │
│ 3. Otherwise, generate verifiable contract from task + files       │
└─────────────────────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────────────────────┐
│ CONTRACT OUTPUT                                                     │
│                                                                     │
│ {                                                                   │
│   "type": "verifiable",                                             │
│   "criteria": [                                                     │
│     { "activity": "typecheck", "description": "No type errors" },  │
│     { "activity": "lint", "description": "No lint errors" },       │
│     { "activity": "unit-test", "pattern": "DarkModeToggle" },      │
│     { "activity": "e2e", "timing": "immediate" }                   │
│   ],                                                                │
│   "generatedFrom": "auto",                                          │
│   "generatedAt": "<timestamp>"                                      │
│ }                                                                   │
└─────────────────────────────────────────────────────────────────────┘
```

## Contract Types

| Type | Meaning | Verification | Examples |
|------|---------|--------------|----------|
| `verifiable` | Task has clear, automatable success criteria | Full test-flow runs | Add component, fix bug, implement feature |
| `advisory` | Task is exploratory with no clear success test | User reviews output | Investigate, research, explore, plan |
| `skip` | Task is trivial and doesn't need verification | Lint/typecheck only | Update docs, fix typo, add comments |

## Contract Generation Algorithm

```
function generateContract(taskDescription, expectedFiles):
  lowerDesc = taskDescription.toLowerCase()
  
  # Check for advisory patterns (proceed automatically, log for review)
  advisoryPatterns = ["investigate", "research", "explore", "discuss", 
                      "plan", "design", "audit", "review", "analyze"]
  for pattern in advisoryPatterns:
    if pattern in lowerDesc:
      log("ℹ️ Advisory task detected: no automated verification")
      return { type: "advisory", criteria: [] }
  
  # Check for skip patterns (minimal verification)
  skipPatterns = ["document", "readme", "docs", "comment", "typo", "spelling"]
  for pattern in skipPatterns:
    if pattern in lowerDesc:
      return { 
        type: "skip", 
        criteria: [
          { activity: "typecheck", description: "No type errors" },
          { activity: "lint", description: "No lint errors" }
        ]
      }
  
  # Generate verifiable contract
  criteria = [
    { activity: "typecheck", description: "No type errors" },
    { activity: "lint", description: "No lint errors" }
  ]
  
  # Add criteria based on expected file patterns
  for file in expectedFiles:
    if file matches "*.tsx" or "*.jsx":
      criteria.push({ activity: "unit-test", pattern: componentName(file) })
    if file matches "app/*" or "pages/*":
      criteria.push({ activity: "e2e", timing: "immediate" })
    if file matches "*.ts" and not test file:
      criteria.push({ activity: "unit-test", pattern: moduleName(file) })
  
  return {
    type: "verifiable",
    criteria: deduplicate(criteria),
    generatedFrom: "auto",
    generatedAt: now()
  }
```

## Store Contract in State

Write the contract to the current `chunk.json` → `verification.contract` before delegation:

```json
{
  "verification": {
    "contract": {
      "type": "verifiable",
      "criteria": [...],
      "generatedFrom": "auto",
      "generatedAt": "2026-02-28T10:00:00Z"
    }
  }
}
```

## Advisory Task Handling

When an advisory task is detected, **proceed automatically** with logging:

```
ℹ️ Advisory task detected: "Investigate why checkout API is slow"
   No automated verification — output will be logged for your review.
   Proceeding...
```

After completion, log the output to `chunk.json` → `advisory`:

```json
{
  "advisory": {
    "taskId": "adhoc-003",
    "description": "Investigate why checkout API is slow",
    "output": "Found N+1 query in OrderService.getItems()",
    "completedAt": "2026-02-28T10:30:00Z"
  }
}
```

**When to still prompt the user:**
- Task description is ambiguous (could be advisory OR verifiable)
- User has `"promptForAdvisory": true` in project.json
- Task is part of a PRD (advisory tasks in PRDs may indicate unclear requirements)

## Verification on Completion

After specialist reports done, verify against the contract:

1. **Run each criterion** in the contract using existing test-flow
2. **Record results** in `chunk.json` → `verification.results`:
   ```json
   {
     "verification": {
       "status": "pass",
       "results": [
         { "activity": "typecheck", "status": "pass" },
         { "activity": "lint", "status": "pass" },
         { "activity": "unit-test", "status": "pass", "attempts": 1 },
         { "activity": "e2e", "status": "pass", "attempts": 1 }
       ],
       "completedAt": "2026-02-28T10:15:00Z"
     }
   }
   ```
3. **All criteria must pass** for task success
4. **On failure:** Trigger fix loop (existing test-flow behavior)
5. **Store failure details** for potential reassignment:
   ```json
   {
     "activity": "unit-test",
     "status": "fail",
     "error": "Expected DarkModeToggle to handle click, but onClick was not called",
     "attempts": 3
   }
   ```
