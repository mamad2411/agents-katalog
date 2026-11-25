---
name: test-driven-development
description: "Compatibility reminder for RED-GREEN-REFACTOR. Implementation workflows enforce TDD directly."
---

# TDD Compatibility Entry

For every behavior change or bug fix, follow the assigned implementation workflow:

1. **RED:** prove the gap with a focused failing test or reproducible check.
2. **GREEN:** make the smallest scoped change that passes.
3. **REFACTOR:** clean only what the passing evidence justifies.

Use the repository's existing test stack. If RED is genuinely impractical, record why, provide the closest reproducible check, and let the reviewer judge the exception. Report RED and GREEN evidence plus residual gaps.

Minimum test selection: cover the changed normal path, relevant boundary, and relevant error path. Reuse existing fixtures and avoid brittle timing, live-network, or environment assumptions. For skill/workflow behavior changes, use 2-3 realistic trigger/eval prompts with expected outcomes as the RED checks.
