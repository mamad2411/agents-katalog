---
name: investigate
description: "Alias for debug+. Invoke when encountering any bug, test failure, or unexpected behavior. Redirects to debug+ which wraps superpowers:systematic-debugging with scout agent context."
argument-hint: "[bug description or failure output]"
user-invocable: true
---

<!-- rig-generated -->

# investigate — Alias for debug+

Redirects to `/debug+` which wraps `superpowers:systematic-debugging` with scout
agent context harvesting. This alias exists for backward compatibility.

## Procedure

Use `/debug+` instead. It follows the same systematic debugging process:

1. Reproduce the issue and capture output
2. Use the scout agent when code exploration is needed
3. Delegate to `superpowers:systematic-debugging`
4. Report findings with evidence

- [ ] Issue reproduced and symptom documented
- [ ] Root cause identified with evidence
- [ ] Fix applied and tests pass

## Skill Chain

Invoke `/debug+` directly for the full skill. After resolving, return to your
current phase.

## Completion

Report one of these states:

- **DONE** — Root cause identified and fix applied with passing tests.
- **DONE_WITH_CONCERNS** — Root cause identified but fix has side effects or needs review.
- **BLOCKED** — Cannot reproduce the issue or insufficient context to diagnose.
- **NEEDS_CONTEXT** — Need user input to reproduce the issue or understand expected behavior.
