---
name: forge-diagnose
description: >-
  Four-phase root cause analysis when tests fail, CI breaks, or behavior is
  wrong. Use instead of random fixes.
---
# Forge Diagnose

**Activates:** on failure during execute, prove, or land.

## Phases

1. **Reproduce** â€” exact command, env flags, error output (copy verbatim)
2. **Isolate** â€” narrow to file/test; git bisect if regression unknown
3. **Hypothesize** â€” max 3 causes ranked; pick one to test first
4. **Fix & prove** â€” minimal change; re-run failing + related tests

## Techniques

- Read stack trace bottom-up to first project frame
- Compare with last green commit (`git diff`)
- Check env flags (`.env`, `vi.stubEnv` in tests)
- For flakes: run test 3Ã— before declaring fixed

## Defense

- Add regression test in `forge-prove` before closing diagnose
- If root cause is missing guard, fix at boundary not call site only

## Exit

Document in handoff: root cause one sentence + test that prevents recurrence.

Prompt cross-ref: `docs-ai/cross-cutting/agent-forge/workflow/prompts/operations/production-debug.md`
