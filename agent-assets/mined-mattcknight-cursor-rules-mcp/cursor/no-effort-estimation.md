# No Effort Estimation - MANDATORY

**Priority:** 🔴 CRITICAL  
**Applies To:** ALL analysis, documentation, recommendations, technical writing  
**Status:** MANDATORY - No exceptions

---

## Core Rule

> **NEVER provide effort estimates (hours, days, story points, complexity ratings) unless EXPLICITLY instructed by the user.**

Effort estimation is the responsibility of the engineering team and product management, not the AI assistant.

---

## What NOT to Do

### ❌ FORBIDDEN: Unsolicited Effort Estimates

**NEVER include these without explicit instruction:**

- ❌ "Estimated effort: 2-4 hours"
- ❌ "Effort: 5-8 hours"
- ❌ "Complexity: HIGH/MEDIUM/LOW"
- ❌ "Story points: 3-5"
- ❌ "Development time: 1-2 days"
- ❌ "Testing effort: 2 hours"
- ❌ "Estimated LOC: 100-150"
- ❌ "Implementation time: 3 hours"
- ❌ "Quick win: 30 minutes"
- ❌ "Total effort: X hours"

**These are ESTIMATIONS and must be avoided.**

---

## What TO Do Instead

### ✅ PROVIDE: Factual Information Only

**Focus on FACTS, not ESTIMATES:**

- ✅ "Files requiring modification: 3"
- ✅ "Modifications required: 14 changes across components"
- ✅ "Complexity factors: 1000+ lines, complex logic, multiple dependencies"
- ✅ "Dependencies: Unit tests, integration tests, documentation updates"
- ✅ "Scope: 2 methods in 1 file"
- ✅ "Impact: Changes affect 5 related components"
- ✅ "Changes: Add validation logic to existing method"

**Let the team estimate based on these facts.**

---

## Exception: User Explicitly Requests Estimation

**ONLY provide estimates when user says:**

- "Estimate the effort for..."
- "How long will this take?"
- "What's the complexity?"
- "Provide effort estimates"
- "Give me hours for..."

**Example User Request:**
> "Can you estimate how long this feature will take?"

**Acceptable Response:**
> "Based on the complexity factors (1000+ lines, complex logic, multiple dependencies), estimated effort: 2-3 hours. This is a rough estimate and should be refined by the team based on their velocity and experience."

---

## Rationale

### Why Avoid Effort Estimates?

1. **AI Lacks Context:**
   - Team velocity unknown
   - Developer experience level unknown
   - Existing technical debt unknown
   - Testing infrastructure unknown
   - Code review overhead unknown

2. **Creates False Expectations:**
   - Stakeholders may take AI estimates as commitments
   - Actual effort often differs from AI guesses
   - Team may feel pressured to meet AI-generated numbers

3. **Not AI's Responsibility:**
   - Engineering teams own their estimates
   - Product managers define priorities
   - Scrum masters facilitate planning
   - AI provides facts, teams provide estimates

4. **Better Alternatives Exist:**
   - Provide factual complexity indicators
   - List dependencies and scope
   - Reference similar past work
   - Let team use planning poker, t-shirt sizing, etc.

---

## Complexity Indicators (Acceptable)

Instead of "Effort: HIGH", provide factual complexity indicators:

### ✅ GOOD: Factual Complexity Factors

**Example 1:**
```markdown
**Complexity Factors:**
- 1000+ lines of code
- Complex business logic with multiple edge cases
- Integration with 3 external systems
- Different behavior based on configuration
- Requires testing across multiple scenarios
```

**Example 2:**
```markdown
**Scope:**
- Files: 3
- Modifications: 14 changes across components
- Testing: Unit tests (2 files), Integration tests (5 scenarios)
- Dependencies: Database schema changes, API updates
```

### ❌ BAD: Effort Estimates

```markdown
**Effort:** 2-3 hours
**Complexity:** HIGH
**Story Points:** 5
```

---

## Document Templates

### Before (With Effort Estimates) ❌

```markdown
## Files Requiring Modification

| File | Changes | Effort | Complexity |
|------|---------|--------|------------|
| `ServiceA.ts` | 5 methods | 2-3 hours | HIGH |
| `ComponentB.tsx` | 1 component | 0.5-1 hour | LOW |

**Total Effort:** 3-4 hours
```

### After (Without Effort Estimates) ✅

```markdown
## Files Requiring Modification

| File | Changes | Scope | Complexity Factors |
|------|---------|-------|-------------------|
| `ServiceA.ts` | 5 methods | 500 lines, complex logic, multiple dependencies | Requires extensive testing |
| `ComponentB.tsx` | 1 component | 50 lines, simple UI update | Straightforward modification |

**Scope Summary:** 2 files, 6 modifications total
```

---

## Analysis Document Updates

### Section Headers to Avoid

❌ **AVOID:**
- "Effort Estimate"
- "Estimated Hours"
- "Development Time"
- "Story Points"
- "Complexity Rating"

✅ **USE INSTEAD:**
- "Scope"
- "Modifications Required"
- "Complexity Factors"
- "Dependencies"
- "Impact"

---

## Examples: Before & After

### Example 1: File Analysis

**❌ BEFORE (With Estimates):**
```markdown
**File:** `UserService.ts`

**Modifications Required:** 2 methods

**Effort:** 2-4 hours

**Complexity:** MEDIUM
```

**✅ AFTER (Facts Only):**
```markdown
**File:** `UserService.ts`

**Modifications Required:** 2 methods

**Scope:** Add validation logic to `createUser()` and `updateUser()` methods

**Dependencies:** Unit tests, integration tests with test data

**Complexity Factors:** Validation logic, database updates, testing with multiple user types
```

---

### Example 2: Implementation Summary

**❌ BEFORE (With Estimates):**
```markdown
## Implementation Summary

- Files: 2
- Modifications: 14
- **Effort: 3-4 hours**
- **Complexity: HIGH**
```

**✅ AFTER (Facts Only):**
```markdown
## Implementation Summary

- Files: 2
- Modifications: 14
- Scope: Service layer (5 methods), UI components (3 components)
- Complexity Factors: Complex validation logic, multiple dependencies
- Testing Requirements: 10+ unit tests, 5 integration test scenarios
```

---

### Example 3: Recommendation

**❌ BEFORE (With Estimates):**
```markdown
**Recommendation:** Implement in 3 phases

1. Phase 1: Core validation (5-8 hours)
2. Phase 2: UI components (3-4 hours)
3. Phase 3: Integration (5-8 hours)

**Total: 13-20 hours**
```

**✅ AFTER (Facts Only):**
```markdown
**Recommendation:** Implement in 3 phases

1. Phase 1: Core validation
   - Files: 4 (service layer)
   - Scope: Add validation checks, error handling
   - Dependencies: Unit tests, validation rules

2. Phase 2: UI components
   - Files: 3 (UI layer)
   - Scope: Form components, error display
   - Dependencies: Component tests, UI mocks

3. Phase 3: Integration
   - Files: 2 (integration layer)
   - Scope: Connect services to UI
   - Dependencies: Integration tests, E2E tests

**Team to estimate effort based on velocity and experience.**
```

---

## Enforcement Checklist

Before completing ANY analysis or documentation, verify:

- [ ] Did I avoid stating "Effort: X hours"?
- [ ] Did I avoid stating "Complexity: HIGH/MEDIUM/LOW"?
- [ ] Did I avoid stating "Story Points: X"?
- [ ] Did I avoid stating "Development time: X"?
- [ ] Did I provide factual complexity indicators instead?
- [ ] Did I list scope, files, and modifications?
- [ ] Did I note dependencies and testing requirements?
- [ ] Did I let the team own the estimation?

**If any answer is NO, revise the document.**

---

## Summary

**The Rule:**
> Provide FACTS (files, scope, complexity factors), not ESTIMATES (hours, complexity ratings).

**The Reason:**
> Engineering teams own estimation. AI provides information for informed estimation.

**The Exception:**
> Only estimate when explicitly instructed by the user.

**The Enforcement:**
> Every document must pass the "No Estimates" checklist before completion.

---

**Rule Status:** ✅ ACTIVE  
**Scope:** ALL analysis, documentation, recommendations, technical writing  
**Purpose:** Prevent AI from providing unsolicited effort estimates; let engineering teams own estimation
