---
name: ship-review-prep
description: Use when preparing for a ship review, launch review, or "is X ready to ship?", "prep ship review for X".
---

Validate a project's readiness for ship review and compile a status summary.

**Before starting:** Read `gotchas.md` and `runs.log` in this skill folder.

## Instructions

Given a project name or path:

1. Read the project folder. Check completeness against expected artifacts:
   - README.md, CONTEXT.md, product-brief.md, designs.md
   - rfc-frontend.md, rfc-backend.md, decisions.md, truths.md
   - Test plan, launch-checklist.md, analytics-spec.md
2. Flag missing artifacts.
3. Grep the project folder for: "TBD", "open question", "pending", "awaiting", "unclear".
4. Read CONTEXT.md for blockers or stale status.
5. Check `projects/INDEX.md` for cross-project dependencies — are dependent projects on track?
6. Check recent git activity: `git log --since="14 days ago" -- [project path]`.
7. Output:

```
## Ship Review: [Project Name]

### Status
[Phase, target launch, team]

### Artifact Completeness
- [x] README.md
- [ ] rfc-frontend.md — MISSING
...

### Open Questions ([count])
- [file]: [TBD item]

### Blockers
- [description]

### Cross-Project Risks
- [dependent project]: [risk]

### Recent Activity (last 2 weeks)
- [commit summary]
```

## Post-Run
Append to `runs.log`. If new failure patterns discovered, add to `gotchas.md`.
