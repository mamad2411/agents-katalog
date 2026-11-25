---
name: delivery-handoff
description: Use when finishing a branch, completing a task, packaging an artifact, or giving the final engineering handoff.
---

# Delivery Handoff

Lead with outcome, then evidence, then risk.

## Finish Checklist

- Scope matches the user's latest request.
- Related user changes were not reverted.
- Commands/checks are summarized with pass/fail/not-run.
- UI/artifacts were rendered when applicable.
- Not-run checks explain why.
- Remaining risk is specific.
- Resume point is clear for non-trivial work.

## Implementation Handoff

```md
Implemented:

Changed files:
- path - summary

Verification:
- command/check: pass/fail/not run - evidence

Not verified:
- item - reason

Remaining risk:
- specific issue
```

## Debugging Handoff

```md
Root cause:
Fix:
Verification:
Blast radius:
Remaining uncertainty:
```

## Artifact Handoff

- Link final deliverables.
- State render/open verification.
- If visual verification was impossible, label it clearly.

