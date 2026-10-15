---
name: cross-check
description: Verify Investo implementation against requirements and generate compliance reports.
---

# Cross-Check Skill

Verify implementation against requirements and generate compliance report.

## Arguments

- `$ARGUMENTS` - One of the following:
  - (empty) - Check all requirements
  - `phase:<N>` - Check specific phase (e.g., `phase:1`)
  - `fr:<ID>` - Check specific functional requirement (e.g., `fr:FR-001`)
  - `nfr:<ID>` - Check specific non-functional requirement
  - `component:<name>` - Check specific component

## Objective

Systematically verify that implementations align with documented requirements, identify gaps, and generate actionable reports. Ensures nothing falls through the cracks between planning and implementation.

---

## Execution Steps

### Step 1: Locate Requirements

1. **Search for requirements documents**:
   - `docs/requirements.md` (primary — single source of truth)
   - `aidlc-docs/inception/requirements/requirements.md` (reference with intent analysis)

2. **Search for AIDLC design artifacts** (for traceability):
   - `aidlc-docs/inception/user-stories/stories.md` (if exists — verify story coverage)
   - `aidlc-docs/inception/application-design/components.md` (if exists — verify component coverage)
   - `aidlc-docs/inception/plans/execution-plan.md` (verify planned stages were completed)

3. **Search for development plan**:
   - `aidlc-docs/aidlc-state.md`

4. **If not found**, report error and suggest running `/init-project`

### Step 2: Parse Requirements

1. **Extract Functional Requirements (FR-XXX)**:
   - ID, Description, Acceptance Criteria
   - Priority, Status

2. **Extract Non-Functional Requirements (NFR-XXX)**:
   - ID, Description, Metrics
   - Priority

3. **Build requirements checklist**

### Step 3: Apply Scope Filter

| Argument | Scope |
|----------|-------|
| (empty) | All requirements |
| `phase:N` | Requirements mapped to phase N |
| `fr:FR-XXX` | Single functional requirement |
| `nfr:NFR-XXX` | Single non-functional requirement |
| `component:name` | Requirements for component |

### Step 4: Analyze Implementation

For each requirement in scope:

1. **Search codebase** for implementation:
   - Look for requirement ID in comments
   - Search for related function/class names
   - Check test files for coverage

2. **Cross-reference AIDLC artifacts** (if available):
   - Check user stories coverage (are all stories implemented?)
   - Check component design coverage (are all components built?)
   - Check execution plan stages (were all planned construction stages completed?)
   - Verify AIDLC state tracking in `aidlc-docs/aidlc-state.md`

3. **Evaluate completeness**:
   - Core functionality implemented?
   - Edge cases handled?
   - Error scenarios covered?
   - Tests exist and pass?

4. **Check acceptance criteria**:
   - Each criterion individually verified
   - Evidence documented

### Step 5: Determine Status

| Status | Criteria |
|--------|----------|
| ✅ Complete | Fully implemented, tested, acceptance criteria met |
| ⚠️ Partial | Implemented but missing tests/edge cases/criteria |
| ❌ Gap | Not implemented or significantly incomplete |
| 🔄 Deferred | Explicitly postponed with documented reason |
| ⏳ In Progress | Currently being worked on |

### Step 6: Generate Compliance Matrix

```markdown
## Compliance Matrix

**Scope**: {scope description}
**Date**: YYYY-MM-DD
**Checked by**: Claude

---

### Summary

| Status | Count | Percentage |
|--------|-------|------------|
| ✅ Complete | N | X% |
| ⚠️ Partial | N | X% |
| ❌ Gap | N | X% |
| 🔄 Deferred | N | X% |
| ⏳ In Progress | N | X% |
| **Total** | **N** | **100%** |

---

### Functional Requirements

| ID | Description | Status | Evidence | Notes |
|----|-------------|--------|----------|-------|
| FR-001 | User authentication | ✅ | `src/auth.py`, tests pass | All criteria met |
| FR-002 | Data export | ⚠️ | `src/export.py` | Missing CSV format |
| FR-003 | Search feature | ❌ | - | Not implemented |

---

### Non-Functional Requirements

| ID | Description | Status | Evidence | Notes |
|----|-------------|--------|----------|-------|
| NFR-001 | Response < 200ms | ✅ | Benchmark results | P95 = 150ms |
| NFR-002 | 99.9% uptime | ⏳ | - | Monitoring not set up |

---

### Acceptance Criteria Detail

#### FR-001: User authentication

| Criterion | Status | Evidence |
|-----------|--------|----------|
| Users can register with email | ✅ | `test_auth.py:test_register` |
| Users can login with password | ✅ | `test_auth.py:test_login` |
| Invalid credentials rejected | ✅ | `test_auth.py:test_invalid_login` |
| Password reset via email | ⚠️ | Implemented, no email sending |

[Repeat for requirements with issues]
```

### Step 7: Identify Gaps and Actions

For each Gap (❌) or Partial (⚠️):

```markdown
## Gaps Analysis

### GAP-001: FR-003 - Search feature not implemented

**Requirement**: FR-003 - Search by title and author
**Status**: ❌ Gap
**Impact**: Core functionality missing, blocks user stories

**Proposed Action**:
- Add to development plan as new task
- Priority: High
- Estimated effort: 2-3 hours

---

### GAP-002: FR-002 - Missing CSV export format

**Requirement**: FR-002 - Data export (partial)
**Status**: ⚠️ Partial - JSON works, CSV missing
**Impact**: Medium - some users need CSV

**Proposed Action**:
- Add CSV format support
- Add to current phase or TECH-DEBT
```

### Step 8: Propose Updates

```markdown
## Proposed Actions

### Add to Development Plan

| Gap | Requirement | Proposed Task | Priority |
|-----|-------------|---------------|----------|
| GAP-001 | FR-003 | Implement search feature | High |

### Add to TECH-DEBT

| Gap | Requirement | Issue | Priority |
|-----|-------------|-------|----------|
| GAP-002 | FR-002 | Add CSV export format | Medium |

---

Apply these updates? (yes/no/selective)
```

### Step 9: Update Documents (on approval)

1. **If adding to development plan**:
   - Create new task in appropriate phase
   - Reference requirement ID

2. **If adding to TECH-DEBT**:
   - Create DEBT-NNN entry
   - Link to requirement

3. **Create cross-check report**:
   - Save to `docs/cross-checks/YYYY-MM-DD-{scope}.md`

### Step 10: Summary Report

```
## Cross-Check Complete

**Scope**: {scope}
**Date**: YYYY-MM-DD

### Compliance Summary

| Status | Count | Percentage |
|--------|-------|------------|
| ✅ Complete | N | X% |
| ⚠️ Partial | N | X% |
| ❌ Gap | N | X% |

**Overall Compliance**: X%

### Actions Taken

- Development Plan: {N} tasks added
- TECH-DEBT: {N} items added
- Cross-check report: `docs/cross-checks/{filename}`

### Critical Gaps

[List any high-priority gaps requiring immediate attention]

### Recommendations

1. [Priority recommendation]
2. [Secondary recommendation]
```

---

## Requirement Status Criteria

### Complete (✅)
- Code implements the requirement
- All acceptance criteria met
- Unit tests exist and pass
- Edge cases handled
- Documented appropriately

### Partial (⚠️)
Core functionality works BUT:
- Missing some acceptance criteria
- Tests incomplete
- Edge cases not handled
- Documentation missing

### Gap (❌)
- Requirement not addressed in code
- Significantly incomplete
- Core functionality missing

### Deferred (🔄)
- Explicitly marked as deferred
- Has documented reason
- Planned for future phase

### In Progress (⏳)
- Currently being implemented
- Tracked in development plan
- Expected completion known

---

## Integration with Other Skills

### Triggers Cross-Check
- `/dev-{project}` automatically after phase completion
- Manual invocation for verification

### Cross-Check Outputs To
- **Development Plan**: New tasks from gaps
- **TECH-DEBT**: Partial implementations
- **Session Logs**: Referenced for traceability

---

## Guidelines

### Scope Control
- Check one phase or component at a time for manageable reports
- Full check periodically (weekly/milestone)

### Gap Prioritization

| Gap Type | Priority | Action |
|----------|----------|--------|
| Core functionality | Critical | Block phase completion |
| Acceptance criteria | High | Add to current phase |
| Edge cases | Medium | TECH-DEBT or next phase |
| Documentation | Low | TECH-DEBT |

### Evidence Requirements

Good evidence:
- Specific file and line numbers
- Test names that verify behavior
- Benchmark results for NFRs

Weak evidence:
- "Code exists" without specifics
- "Should work" without tests
- No measurable metrics for NFRs

---

## Example Invocations

Check all requirements:
```
/cross-check
```

Check specific phase:
```
/cross-check phase:1
```

Check single requirement:
```
/cross-check fr:FR-003
```

Check component:
```
/cross-check component:authentication
```
