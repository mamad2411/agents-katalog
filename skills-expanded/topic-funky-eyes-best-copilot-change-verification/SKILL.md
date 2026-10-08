---
name: change-verification
description: "Use after code or configuration changes to prove the changed behavior with minimal sufficient commands, HTTP/browser checks, or static evidence. DO NOT USE FOR: purely speculative review without a concrete change."
---

# Change Verification

## Choose Evidence

- Unit or integration tests for behavior changes.
- Build/typecheck/lint for compile-time or static confidence.
- HTTP or CLI commands for API/tool behavior.
- Browser evidence for visible UI behavior.
- Schema/frontmatter/residual scans for documentation, agent, skill, or plugin changes.

## Minimum Report

```markdown
## Verification
- command:
- result:
- evidence:
- coverage:
- gaps:
```

## Rules

- Do not claim “passed” without a command or concrete static check.
- If a command cannot run, explain why and provide the strongest alternative evidence.
- For public contract, auth, data, dependency, CI, or runtime config changes, include blast radius summary.
