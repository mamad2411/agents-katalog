---
description: Holistic refactoring workflow with mandatory validation checkpoints
alwaysApply: false
---

# Holistic Refactoring Workflow

**When to use:** Large-scale refactoring tasks (renaming, restructuring, major changes)

**Key Principle:** ONE systematic pass with comprehensive validation, not reactive fixes.

---

## Multi-Persona Workflow

### Phase -2: Validation Planning (MANDATORY)

**Personas:** Solution Architect + QA Engineer + TRAC Analyst

**Outputs:**
- File type inventory (all file extensions in project)
- Validation checklist (refactoring mapped to each file type)
- Search patterns for final validation
- Risk assessment for high-risk areas
- Test plan for validation

**Acceptance Criteria:**
- Complete file type inventory documented
- Validation checklist covers ALL file types
- Search patterns defined (case-sensitive and case-insensitive)

---

### Phase -1: Requirements & Decisions

**Personas:** Solution Architect + All relevant domain personas

**Outputs:**
- Q&A document with critical decisions
- Refactoring scope and boundaries
- Architectural Decision Records (ADRs) if needed

**Acceptance Criteria:**
- All critical questions answered
- Scope clearly defined
- Breaking changes identified

---

### Phase 0-N: Implementation

**Personas:** Developer + Domain personas

**Outputs:**
- Code changes
- Progressive validation after EACH phase
- Commits per logical category

**Acceptance Criteria:**
- Each phase validated before proceeding to next
- No "complete" claims without validation
- Logical commit structure

---

### Phase N+1: Final Validation (MANDATORY)

**Personas:** QA Engineer (PRIMARY) + Data Flow Analyst

**Outputs:**
- Validation report with search results
- Zero-defect confirmation OR list of legitimate exceptions
- Sign-off from QA Engineer

**Validation Steps:**
1. Run ALL search patterns from Phase -2
2. Case-sensitive search: `grep "OldTerm"`
3. Case-insensitive search: `grep -i "oldterm"`
4. Namespace search: `grep "OldNamespace"`
5. Verify zero results (or only legitimate exceptions)
6. Check build succeeds
7. Run linter
8. Document results

**Acceptance Criteria:**
- Zero occurrences of old terminology (or only documented exceptions)
- Build succeeds
- No linter errors introduced
- QA Engineer sign-off

**QA Engineer has VETO power:** Can block "complete" claim if validation fails.

---

### Phase N+2: User Acceptance

**Personas:** None (User validates)

**Outputs:**
- User sign-off OR additional issues found

**If user finds issues:**
- STOP and analyze WHY validation missed them
- Update validation checklist for future
- Document failure in learnings

---

## Critical Rules

### ALWAYS

✅ Create validation checklist in Phase -2  
✅ Use grep/search tools to verify completion  
✅ Consider ENTIRE project ecosystem (all languages, all file types)  
✅ Validate BEFORE claiming "complete"  
✅ Get QA Engineer sign-off  
✅ ONE systematic pass, not reactive fixes

### NEVER

❌ Claim "complete" without running validation searches  
❌ Skip file types (scripts, tests, docs, config, Dockerfiles)  
❌ Rely on memory or assumptions  
❌ Do reactive fixes after user catches issues  
❌ Ignore validation failures

---

## Success Criteria

A refactoring is considered **SUCCESSFUL** when:

1. ✅ Validation checklist created in Phase -2
2. ✅ All personas invoked appropriately
3. ✅ QA Engineer signs off on final validation
4. ✅ Zero issues found by user
5. ✅ <10 commits for entire refactoring
6. ✅ User says "good job" instead of expressing frustration

---

## Time Estimation

**With proper workflow:**
- Planning (Phase -2, -1): 2 hours
- Implementation (Phase 0-N): 4 hours
- Final validation (Phase N+1): 1 hour
- **Total: 7-8 hours**

**Without proper workflow (reactive approach):**
- Implementation: 6 hours
- Reactive fixes: 6+ hours (multiple rounds)
- User frustration: priceless
- **Total: 12-15+ hours**

**Time saved: 40-50% with proper workflow**

---

## Escalation

**If validation fails:**
1. QA Engineer documents failures
2. Solution Architect updates validation checklist
3. Developer fixes systematically (not reactively)
4. Re-validate before proceeding

**If user finds issues:**
1. CRITICAL FAILURE - Validation process failed
2. Document in learnings
3. Update validation checklist for future
4. Analyze why validation missed the issue

---

**Last Updated:** 2025-11-16  
**Version:** 1.0.0  
**Based On:** v3.0.0 Refactoring Failure Analysis  
**Priority:** CRITICAL - Prevents future systematic failures
