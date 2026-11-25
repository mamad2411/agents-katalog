---
name: tedflow-finalize-plan
description: Finalize and archive a completed coding plan by adding completion status, condensing verbose instructions, preserving decisions, and writing an implementation summary. Use when validation has passed or the user asks to finalize a plan, archive a completed plan, mark a plan complete, clean up a plan after implementation, or turn an implementation plan into a historical record.
---

# Workflow Finalize Plan

Use this skill to turn a completed implementation plan into a concise historical record.

## Inputs

Treat the user's current request as the input. If it does not include a plan path, ask for one.

Before finalizing, make sure the implementation is complete and automated verification has passed. If that is uncertain, use `tedflow-validate-plan` first or ask the user whether to validate.

## Process

1. Read the plan completely.
2. Identify completed phases, implemented files, key decisions, gotchas, and testing evidence.
3. Add a status block at the top of the plan, after YAML frontmatter if present:

```markdown
> **Status:** Completed
> **Completed:** YYYY-MM-DD
> **Summary:** [One sentence describing what was accomplished]
```

Use the current date for `Completed`.

4. Condense verbose implementation instructions into summaries.
5. Remove code examples and step-by-step "what to write" guidance now that the code exists.
6. Preserve:
   - Phase names and concise descriptions.
   - File paths that were created or modified.
   - Key architectural decisions and why they were made.
   - Important gotchas or future maintenance notes.
   - Success criteria, marked complete where appropriate.
   - Manual verification items only when the user explicitly confirmed them.
7. Add an implementation summary at the end:

```markdown
---

## Implementation Summary

### What Was Built

- [Component/feature]: [brief description]

### Key Files

- `path/to/file.ext` - [purpose]

### Design Decisions

- [Decision]: [brief rationale]

### Testing

- [Tests/checks that passed]
```

## Cleanup Guidance

Before:

```markdown
Create the endpoint with the following code:
[large code example]
```

After:

```markdown
Added the endpoint for [behavior].

**Files:** `path/to/endpoint.ts`
**Notes:** Follows the existing router pattern.
```

## Completion

After updating the plan, report:

```markdown
Plan finalized: [plan path]

Changes made:
- Added completion status with today's date.
- Condensed detailed implementation instructions.
- Removed code examples that are now represented in the codebase.
- Added implementation summary.
```
