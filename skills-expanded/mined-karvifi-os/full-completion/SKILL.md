---
name: full-completion
description: Complete ANY incomplete, broken, or stalled project to 100% — no gaps left
triggers: [complete this, finish this, half done, incomplete, not working, broken, stuck, continue]
---

# SKILL: Full Completion

## Purpose
Take any project from its current state — however broken or incomplete — to a fully working, production-ready result. Nothing left half-done.

## The Iron Law
```
NO PARTIAL OUTPUTS.
NO "GOOD ENOUGH."
IF SOMETHING IS NOT COMPLETE, IT IS BROKEN.
```

## Process

### Step 1: State Assessment
Read everything that exists:
- Source code (all files)
- Any docs/ directory
- git log (understand history)
- Any README or notes
- Error messages or failure outputs

Produce an honest gap map:
```
WORKING ✅:
- [component]: [what works]

PARTIAL ⚠️:
- [component]: [what is done, what is missing]

BROKEN ❌:
- [component]: [what fails and why]

MISSING 🔲:
- [component]: [never existed, needs to be built]
```

### Step 2: Priority Matrix
Order gaps by: impact × effort (high impact + low effort first)
```
Priority 1 (BLOCKING): Things that prevent the app from running
Priority 2 (CORE): Things that are required for the primary use case
Priority 3 (QUALITY): Things that make it production-ready
Priority 4 (POLISH): Things that make it excellent
```

### Step 3: Completion Plan
For each gap, produce an exact task:
```
Gap: [component] is missing
Task: Create [exact file path]
      Implement [exact functions/endpoints]
      Test with: [specific verification]
      Done when: [measurable completion criteria]
```

### Step 4: Execution Loop
For each task in priority order:
1. Implement (TDD: test first)
2. Verify (tests pass, types check, lint clean)
3. Commit: "fix/feat(scope): close gap — [description]"
4. Update CONTEXT_STATE.md
5. Move to next

### Step 5: Integration Verification
After all gaps closed:
- All tests pass
- App starts cleanly
- Primary user journey works end-to-end
- No broken imports or missing dependencies
- All environment variables documented in .env.example

### Step 6: Documentation Completion
Complete what is missing:
- README with setup instructions
- .env.example with all variables
- API docs (if API exists)
- Architecture overview
- Deployment guide

## What "Complete" Means
```
□ Application starts without errors
□ All tests pass (≥80% coverage)
□ Type check passes (mypy/tsc --noEmit)
□ Lint passes
□ Security scan clean
□ All documented features work
□ Error states are handled (not just happy path)
□ Mobile responsive (if web)
□ .env.example is complete
□ README has working setup instructions
□ CI/CD pipeline exists
```

## Quality checks
- [ ] Gap map is honest (not optimistic)
- [ ] Priority matrix used (not random order)
- [ ] Every task has a verifiable completion criterion
- [ ] Integration verified (not just unit tests)
- [ ] Documentation complete
