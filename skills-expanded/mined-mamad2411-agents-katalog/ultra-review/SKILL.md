---
name: ultra-review
description: >-
  Deep Ultra Review pass for DisasterTraining changes. Use after implementing a
  feature, before claiming done, when the user asks for review, or before a PR.
---

# Ultra Review

Thorough self-review inspired by Claude Code ultra-review practices.

## When to run

- After a multi-file change
- Before “tapos na” / “ready na”
- When user says review, check, or audit

## Review checklist

### A. Intent

- [ ] Change matches the latest user request (not an older interpretation)
- [ ] No scope creep

### B. Product flow

- [ ] Exercise plan → Use Template → readiness → publish → monitoring still works
- [ ] Template events do not force the old Edit Simulation Event page
- [ ] Timeline / schedule / resources remain coherent

### C. Backend

- [ ] Validation matches UI fields
- [ ] No array-to-string or type mismatches on `simulation_events`
- [ ] Authorization still admin/trainer where required
- [ ] Side effects (auto-register, redirects, status updates) are intentional

### D. Frontend

- [ ] Empty, loading, and error states handled for touched screens
- [ ] Links/tabs use `simulationEventHref` / lifecycle tabs where appropriate
- [ ] No leftover debug UI

### E. Safety

- [ ] No secrets committed
- [ ] No destructive git commands
- [ ] Migrations/seeders only if explicitly needed

## Report format

```markdown
## Ultra Review
**Verdict:** Pass | Pass with notes | Needs fixes

### Findings
- [critical] ...
- [major] ...
- [minor] ...

### Suggested fixes
1. ...
```

Fix **critical** and **major** before finishing. Mention minors only if useful.
