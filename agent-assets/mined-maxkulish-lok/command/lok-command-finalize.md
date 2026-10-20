# /design-doc:finalize - Finalize Design Documents

**Purpose**: Mark a design document as finalized after user approval. Updates the document status, posts to Linear, and prepares for implementation.

**Usage**:
- `/design-doc:finalize CLO-XX` - Finalize specific design document
- `/design-doc:finalize` - Interactive mode

---

## When to Use

This command is typically invoked:
1. After `/design-doc:create` produces a draft
2. After user reviews and approves the design
3. Before `/plan:create` generates implementation plan

---

## Command Execution Instructions

### Step 1: Extract Task Number

1. **If user provided task number** (e.g., `/design-doc:finalize clo-9`):
   - Normalize to both formats (CLO-9 for Linear, clo-9 for files)
   - Proceed to Step 2

2. **If no task number provided**:
   - Ask: "Which design document do you want to finalize? (e.g., CLO-9)"
   - Wait for response

### Step 2: Locate Design Document

Search for design document:
```bash
ls docs/design-docs/clo-XX-*.md
```

**If NOT found**:
```
ERROR: Design document not found

Expected: docs/design-docs/clo-XX-*.md

Create one first: /design-doc:create CLO-XX
```
Exit command.

**If found**: Read the document

### Step 3: Check Current Status

Read the design document header:

```markdown
**Status**: Draft | Finalized
```

**If already finalized**:
```
Design document is already finalized.

File: docs/design-docs/clo-XX-[description].md
Finalized: [date]

No action needed.
```
Exit command.

### Step 4: Validate Design Document

Check that required sections are complete:

| Section | Required | Check |
|---------|----------|-------|
| Summary | Yes | Not empty |
| Background | Yes | Not empty |
| Architecture | Yes | Not empty |
| Detailed Design | Yes | Contains implementation approach |
| Implementation Plan | Yes | Has at least one phase |
| Acceptance Criteria | Yes | Has at least 3 criteria |
| Open Questions | No | Check if empty |

**If Open Questions section has items**:
```
WARNING: Open questions exist

The following questions are still unresolved:
- [Question 1]
- [Question 2]

Options:
1. [finalize] - Finalize anyway (questions will be addressed during implementation)
2. [resolve] - Address questions first
3. [cancel] - Cancel finalization

Your choice:
```

### Step 5: Update Design Document

Edit the design document to update status:

**Change**:
```markdown
**Status**: Draft
```

**To**:
```markdown
**Status**: Finalized
**Finalized**: [Current Date]
**Approved By**: [User or "Team"]
```

### Step 6: Post to Linear

Create a comment on the Linear task:

```
mcp__linear-server__create_comment(
  issueId="CLO-XX",
  body="## Design Document Finalized

The design document for this task has been reviewed and approved.

**Document**: `docs/design-docs/clo-XX-[description].md`
**Status**: Finalized
**Date**: [Current Date]

**Key Decisions**:
- [Summary of architectural decisions from the doc]

**Next Steps**:
1. Generate implementation plan: `/plan:create CLO-XX`
2. Begin implementation: `/plan:implement CLO-XX`

The design is now locked and ready for implementation."
)
```

### Step 7: Update Workflow State (if exists)

If `docs/status/clo-XX-workflow.yaml` exists, update it:

```yaml
phases:
  design:
    status: complete
    finalized: true

history:
  - timestamp: [ISO timestamp]
    action: design_finalized
    phase: design
    details: "Design document approved and finalized"
```

### Step 8: Git Commit

Commit the finalized design document and AI review (if exists):

```bash
# Add design document
git add docs/design-docs/clo-XX-[description].md

# Add AI review if it exists
if [ -f docs/reviews/clo-XX-design-review.md ]; then
  git add docs/reviews/clo-XX-design-review.md
fi

git commit -m "$(cat <<'EOF'
docs(CLO-XX): finalize design document

- Status updated from Draft to Finalized
- AI review included (if generated)
- Ready for implementation planning

Related: docs/design-docs/clo-XX-[description].md
EOF
)"
```

### Step 9: Confirm to User

```
SUCCESS: Design document finalized!

File: docs/design-docs/clo-XX-[description].md
Status: Finalized
Linear: Comment posted

The design is now approved and locked.

Next steps:
1. Generate plan: /plan:create CLO-XX
2. Implement: /plan:implement CLO-XX

Or continue with orchestrator: /task:orchestrate CLO-XX
```

---

## Special Cases

### Case 1: Design document has errors

If validation finds issues:

```
VALIDATION FAILED: Design document incomplete

Missing or empty sections:
- [ ] Detailed Design (no implementation approach)
- [ ] Acceptance Criteria (less than 3 items)

Please complete these sections before finalizing.

Options:
1. [edit] - Open document for editing (exit command)
2. [force] - Force finalization (NOT recommended)
3. [cancel] - Cancel

Your choice:
```

### Case 2: Not on feature branch

```
WARNING: Not on feature branch

Current branch: main
Expected: feat/clo-XX-*

Commits to finalized docs should be on a feature branch.

Options:
1. [create] - Create feature branch
2. [continue] - Continue on main (NOT recommended)
3. [cancel] - Cancel

Your choice:
```

---

## Validation Checklist

Before finalizing, verify:

- [ ] Summary clearly describes the task objective
- [ ] Background provides context from Linear and architecture
- [ ] Architecture section includes component overview
- [ ] Detailed Design has implementation approach
- [ ] Implementation Plan has clear phases
- [ ] Acceptance Criteria are specific and testable
- [ ] Security Considerations addressed
- [ ] No critical Open Questions remain

---

## Document Status Lifecycle

```
Draft (created by /design-doc:create)
  │
  ▼
[User Review]
  │
  ▼
Finalized (by /design-doc:finalize)
  │
  ▼
[Implementation begins]
```

Once finalized:
- Document is considered "locked"
- Major changes require creating a new version
- Minor clarifications can be added inline

---

## Integration Notes

**Called by**: `/task:orchestrate` after design checkpoint approval

**Calls**: None (terminal action for design phase)

**Updates**:
- Design document (`docs/design-docs/clo-XX-*.md`)
- Workflow state file (if exists)
- Linear task (comment)
- Git repository (commit includes design doc and AI review if exists)
