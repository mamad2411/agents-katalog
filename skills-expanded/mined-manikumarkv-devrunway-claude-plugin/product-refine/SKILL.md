---
name: product-refine
description: PM and developer handoff for a specific GitHub issue. Reads the full story context, facilitates scope and AC alignment, records all decisions, then updates the GitHub issue and writes docs/product-tasks/<ticket>-refined.md. Usage — /product-refine <issue-number>
argument-hint: "<issue-number>"
arguments:
  - name: issue
    description: "GitHub issue number"
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Bash(find *)
  - Bash(ls *)
  - Bash(gh *)
---

# Product Refine

Parse `$ARGUMENTS[0]` as the GitHub issue number.

---

## Step 1 — Load full context

```bash
# Fetch the issue
gh issue view <issue-number> --json title,body,milestone,labels,assignees,comments

# Find the source plan doc
find docs/product-plans/ -name "*.md" | xargs grep -l "Story.*<issue-number>" 2>/dev/null | head -1
```

Read both the issue and the plan doc section that produced it.

Summarise to the user:

> **Issue #<number>: <title>**
> Milestone: <milestone>
> Size: <size>
>
> **Story:**
> As a <persona>, I want <action>, so that <benefit>.
>
> **Acceptance Criteria:**
> - [ ] …
>
> I'm ready to refine this story. What would you like to discuss or clarify?

---

## Step 2 — Guided discussion

This is a conversation. The goal is to surface and resolve any ambiguity between PM intent and developer understanding before code is written.

Guide the discussion through these areas, but only raise a topic if it has unresolved ambiguity — do not interrogate unnecessarily:

**Scope & boundaries**
- Is there anything in the AC that is actually out of scope for this story?
- Are there any edge cases the AC doesn't cover?

**Technical questions from the developer**
- Is there anything technically unclear that would block implementation?
- Any dependency on another issue or external system?

**UX / behaviour questions**
- What happens in error states?
- Are there loading states, empty states, or disabled states to handle?

**Definition of done**
- Are unit tests required? E2E? Both?
- Is this feature-flagged? Behind a permission?

Record every question asked and every answer given.

---

## Step 3 — Summarise decisions

Before writing anything, list all changes agreed during the discussion:

> Here are the decisions from our refinement:
>
> 1. **AC updated:** Added "handles empty list state" to criteria
> 2. **Scope clarified:** Pagination is out of scope for this story
> 3. **Edge case added:** API timeout shows inline error, not toast
>
> Confirm these are correct before I update the issue and write the doc?

Wait for confirmation.

---

## Step 4 — Update GitHub issue

Add a comment to the issue with the refinement summary:

```bash
gh issue comment <issue-number> --body "$(cat <<'EOF'
## Refinement Notes — <date>

### Updated Acceptance Criteria
- [ ] …  _(updated)_
- [ ] …  _(added)_

### Decisions Made
1. …
2. …

### Out of Scope (confirmed)
- …

### Technical Notes
- …

_Refined via `/product-refine`. Full Q&A: docs/product-tasks/<issue-number>-refined.md_
EOF
)"
```

---

## Step 5 — Write the refined doc

Write to `docs/product-tasks/<issue-number>-refined.md`:

```markdown
# Refinement: #<number> <title>
_Date: <today>_
_Participants: PM, Dev_

## Original Story
As a <persona>, I want <action>, so that <benefit>.

## Refinement Q&A

**Q:** <question asked>
**A:** <answer given>

**Q:** …
**A:** …

## Final Acceptance Criteria
- [ ] …  _(original)_
- [ ] …  _(updated)_
- [ ] …  _(added)_

## Decision Log
| Decision | Reason | Who |
|---|---|---|
| <what changed> | <why> | PM / Dev |

## Out of Scope (confirmed)
- …

## Technical Notes for Developer
- …

## Status
Ready for development → `/dev-brainstorm <issue-number>`
```

---

## Step 6 — Hand off

> Refinement complete.
>
> - GitHub issue #<number> updated with a comment
> - Doc saved to `docs/product-tasks/<issue-number>-refined.md`
>
> Developer next step:
> ```
> /dev-brainstorm <issue-number>
> ```
