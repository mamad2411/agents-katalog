---
name: implement-prd
description: Workflow for implementing an OpenSDR milestone from its PRD in .internal/prd/. Use when asked to build, implement, or continue a PRD/milestone (e.g. "implement PRD 03", "start M2", "build the enrichment tools").
---

# Implement a PRD

Follow these steps in order. Do not skip the reading steps. The PRDs depend on contracts that only exist in `.internal/plan.md`.

## 1. Load context
1. Read `AGENTS.md` (invariants + commands).
2. Read `.internal/plan.md` §3–§12 (architecture, contracts, safety, storage, providers, testing).
3. Read the target PRD in full, plus every PRD listed under **Depends on**.
4. Check `.internal/prd/README.md`. If a dependency is not `Done`, check whether the PRD names an interface stub to code against (e.g. `SuppressionChecker`). If none exists, stop and tell the user which dependency blocks you.

## 2. Plan
- List every FR and acceptance criterion (AC) in the PRD.
- For each AC, name the test file and test case that will prove it. Write this list as the first comment in your PR description or task notes.
- Identify provider endpoints you will touch. For each one, run the `verify-provider-api` skill **before** writing the client.

## 3. Build (test-first where practical)
- Write failing tests for the ACs first, then implement.
- New provider client → follow the `add-provider` skill.
- New or changed MCP tool → follow the `add-mcp-tool` skill.
- Keep the layering rules from plan §3.1. If you feel you need to break one, stop and ask.
- Extend the demo provider for every new capability or tool. Demo mode must work for every tool you ship.

## 4. Verify
```bash
npm run lint && npm run typecheck && npm test && npm run build
```
All must pass. Then run the e2e smoke test and, if the PRD touches tools, list tools through the MCP Inspector (`npm run inspect`) or the e2e harness.

## 5. Close out
- Tick the AC checkboxes in the PRD that are now covered by passing tests. Leave unchecked any you could not prove, and say why.
- Update the PRD header status and the table in `.internal/prd/README.md`.
- If you discovered that `.internal/plan.md` is wrong or incomplete, update `.internal/plan.md` **and** every affected PRD in the same change. Never let them diverge.
- Summarize what you built, which ACs are proven, and any open questions.

## Hard rules
- Never write to stdout outside the MCP transport.
- Never commit API keys or unscrubbed fixtures.
- Never weaken a safety gate (plan §6) to make a test pass.
- Never call real provider APIs in default tests. Live tests are opt-in only (`OPENSDR_LIVE_TESTS=1`).
