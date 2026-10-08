# Claude Code Instructions

## Workflow Selection (MANDATORY - READ FIRST)

**BEFORE starting any work, you MUST determine which workflow to use.**

### Decision Tree (Use This Every Time)

```
IF new feature OR significant change OR API change OR database change
  THEN → Read /workflows/feature-development.md
  THEN → Create spec in /dev/features/yyyy-MM-dd_feature-name/

ELSE IF critical production bug OR security vulnerability OR service outage
  THEN → Read /workflows/hot-fix.md
  THEN → Create incident docs in /dev/hotfixes/yyyy-MM-dd_issue-name/

ELSE IF code improvement WITHOUT behavior change AND tests exist (≥80% coverage)
  THEN → Read /workflows/refactoring.md
  THEN → Create analysis in /dev/refactorings/yyyy-MM-dd_refactoring-name/

ELSE IF code improvement WITHOUT tests OR low test coverage
  THEN → Read /workflows/feature-development.md
  THEN → Write tests first, then refactor

ELSE (unclear which workflow applies)
  THEN → Default to /workflows/feature-development.md
```

**After selecting workflow:**
1. **READ** the complete workflow file from start to finish
2. **UNDERSTAND** all phases, rules, and transition logic
3. **FOLLOW** the workflow strictly - no shortcuts, no skipped phases

---

## Repository Structure

### Workflows (Centrally Managed - Git Submodule)
**Location**: `/workflows/`

Team-wide process definitions managed centrally:
- `/workflows/feature-development.md` - For new features and changes (6 phases)
- `/workflows/hot-fix.md` - For critical production issues (6 phases)
- `/workflows/refactoring.md` - For code improvements (4 phases)

**IMPORTANT**: 
- These files are managed centrally by the team
- DO NOT modify these files in your project
- They are updated via Git Submodule

### Development Documentation (Project-Specific)
**Location**: `/dev/`

Project-specific documentation and artifacts:
- `/dev/features/` - Feature specifications
  - Format: `yyyy-MM-dd_feature-name/`
  - Contains: `spec.md`, `implementation.md`
  
- `/dev/hotfixes/` - Hotfix documentation
  - Format: `yyyy-MM-dd_issue-name/`
  - Contains: `incident.md`, `fix.md`
  
- `/dev/refactorings/` - Refactoring documentation
  - Format: `yyyy-MM-dd_refactoring-name/`
  - Contains: `analysis.md`, `plan.md`

**These directories belong to THIS project only.**

---

## Critical Rules (Apply to ALL Workflows)

### Rule 1: Status Markers (MANDATORY - NO EXCEPTIONS)
**EVERY response MUST start with a status marker from the active workflow.**

**Format**: `[STATUS_MARKER] Description of current action`

**Examples**:
- `[SPEC] Creating specification for user authentication feature...`
- `[INCIDENT] Documenting critical database connection failure...`
- `[ANALYSIS] Analyzing PaymentService for refactoring opportunities...`

**If you forget the status marker, the response is invalid.**

### Rule 2: Read Complete Workflow First
**BEFORE starting any work:**
1. ✅ Select the appropriate workflow using the decision tree above
2. ✅ Read the COMPLETE selected workflow file (feature-development.md, hot-fix.md, or refactoring.md)
3. ✅ Understand all phases, rules, and transition logic
4. ✅ Start with the first phase of the selected workflow

**DO NOT**:
- ❌ Start work before reading the workflow
- ❌ Assume you know what to do
- ❌ Skip reading the workflow "because you've seen it before"

### Rule 3: Follow Workflow Strictly
**Once a workflow is selected:**
- ✅ Follow ALL phases in order
- ✅ Complete each phase fully before moving to next
- ✅ Use transition rules to determine when to proceed
- ✅ Use status markers from the workflow

**DO NOT**:
- ❌ Skip phases
- ❌ Take shortcuts
- ❌ Ignore transition rules
- ❌ Mix workflows (finish one workflow before starting another)

### Rule 4: Use IF-THEN Logic for Decisions
**Every workflow has transition rules at the end of each phase.**

**Example format**:
```
IF all conditions met
  THEN → Move to next phase
  THEN → Update status

ELSE IF blocking condition
  THEN → Set status to BLOCKED
  THEN → Wait for resolution
```

**ALWAYS check transition rules before moving to next phase.**

---

## Quick Reference: When to Use Which Workflow

### Feature Development (`/workflows/feature-development.md`)
**Use for**: 90% of development work
- Adding new features
- Modifying existing features
- Bug fixes (non-critical)
- API changes
- Database changes
- Writing tests

**Phases**: SPEC → REVIEW → IMPLEMENTATION-PLAN → IMPL → VERIFY → DONE

### Hot-Fix (`/workflows/hot-fix.md`)
**Use for**: Emergencies only
- Production is down
- Critical bugs affecting users
- Security vulnerabilities
- Data corruption

**Phases**: INCIDENT → ASSESS → FIX → VERIFY → DEPLOY → LEARNING

### Refactoring (`/workflows/refactoring.md`)
**Use for**: Code improvements (with tests)
- Improving code structure
- Reducing complexity
- Removing duplication
- Performance optimization

**Prerequisites**: ≥80% test coverage required
**Phases**: ANALYSIS → PLAN → REFACTOR → VERIFY

---

## Workflow Selection Examples

### Example 1: "Add user registration"
```
Analysis: New feature, adds functionality
Decision: Feature Development
Action: Read /workflows/feature-development.md
Create: /dev/features/2025-11-12_user-registration/
```

### Example 2: "Users can't login - production down"
```
Analysis: Critical production bug, service outage
Decision: Hot-Fix
Action: Read /workflows/hot-fix.md
Create: /dev/hotfixes/2025-11-12_login-failure/
```

### Example 3: "Clean up messy validation code"
```
Analysis: Code improvement, no behavior change
Check: Do tests exist? Coverage ≥80%?
  IF yes → Refactoring workflow
  IF no → Feature Development (write tests first)
```

### Example 4: "Optimize database queries"
```
Analysis: Depends on approach
IF only code structure changes (no new features)
  AND tests exist
  THEN → Refactoring workflow
ELSE IF algorithm changes or new features
  THEN → Feature Development workflow
```

---

## Project-Specific Notes

### Technology Stack
[Add your project's key technologies here]
- Language: 
- Framework: 
- Database: 
- Testing Framework: 

### Code Conventions
[Reference to style guide if it exists]
- Code style: 
- Naming conventions: 
- Documentation requirements: 

### Testing Requirements
[Your project's testing standards]
- Minimum test coverage: 
- Required test types: 
- Test framework: 

### Development Environment
[Any project-specific setup notes]
- Setup instructions: 
- Environment variables: 
- Database setup: 

---

## Getting Help

### If unsure which workflow to use:
1. Use the decision tree at the top of this file
2. Ask the team for clarification
3. **When in doubt**: Default to Feature Development workflow

### If workflow instructions are unclear:
1. Read the workflow file completely again
2. Check the examples in the workflow
3. Review the transition rules for the current phase
4. Ask for clarification from the team

### If you encounter issues:
1. Use status marker `[BLOCKED]` to indicate you're stuck
2. Clearly describe the blocking issue
3. Suggest possible solutions or ask specific questions
4. Wait for guidance before proceeding

---

## Common Mistakes to Avoid

❌ **Starting work without selecting a workflow**
✅ **Always select workflow first using decision tree**

❌ **Skipping phases to save time**
✅ **Complete all phases - they ensure quality**

❌ **Forgetting status markers**
✅ **Every response starts with [STATUS_MARKER]**

❌ **Mixing different workflows**
✅ **Finish one workflow completely before starting another**

❌ **Ignoring test coverage requirements for refactoring**
✅ **Check coverage first, write tests if needed**

❌ **Using hot-fix workflow for non-critical bugs**
✅ **Hot-fix is for emergencies only**

---

## Success Checklist

Before considering any work complete, verify:
- [ ] Correct workflow was selected and followed
- [ ] All phases completed in order
- [ ] All transition rules satisfied
- [ ] Status markers used in every response
- [ ] Documentation created in correct /dev/ subdirectory
- [ ] All acceptance criteria met (Feature Development)
- [ ] All tests passing (all workflows)
- [ ] Clean Code principles followed (Refactoring)
- [ ] Learning session scheduled (Hot-Fix)

---

## Remember

**The workflows exist to ensure:**
- ✅ Quality and consistency
- ✅ Clear communication
- ✅ Complete documentation
- ✅ Proper testing
- ✅ Team alignment

**Following workflows is not optional - it's mandatory for all development work.**

When in doubt, read the workflow again. When still in doubt, ask the team.