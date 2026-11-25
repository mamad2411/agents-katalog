---
name: testing
description: Match requirement criteria to existing checks and behavioral evidence without confusing verification levels.
---

# Verify the required behavior

- Map each criterion to requirement ID, trigger/input, expected observable result, registered check ID and evidence level. Include meaningful error, empty, repeated-operation and async-order cases according to risk. Tests copying implementation logic or merely asserting mock calls do not establish real boundary behavior.
- Executor runs registered checks. Use exact action/check IDs; AI cannot add commands/checks during a run. Existing mandatory checks remain required even when new tests are forbidden. New tests depend on risk and project rules; never impose a universal coverage percentage.
- Evidence belongs to the verified input fingerprint. Check success proves the exercised level, not all requirements. Quote the scenario connecting check to criterion. Source-review proves directly inspectable source properties; unit/mock, integration, browser and human evidence have distinct limits. Missing, failed, uncertain or stale is not pass.

## Browser scenarios, when applicable

For observable web interaction/visual requirements, establish whether an authorized registered browser verifier exists. Otherwise report the gap or use the contract's human acceptance; do not start servers, install dependencies or use browser tools from a read-only AI action.

Propose a scenario that inspects rendered state, uses stable accessible selectors, performs the real action and asserts its result/error state. Wait for the relevant condition with a bounded timeout. With Playwright, prefer locator web-first assertions; unconditional networkidle and arbitrary sleeps are not application readiness. Preserve the existing language/toolchain instead of requiring Python or upstream scripts.

Identify tested URL/state, input, viewport and result in evidence. Screenshots support visual assessment and console output aids diagnosis; neither alone proves API behavior, persistence or subjective acceptance. A passing test cannot manufacture internal runtime values.

After repair, repeat the original suitable check and relevant regression on the new fingerprint. Report remaining uncovered requirements instead of closing them with a prior receipt.

Modified adaptation of anthropics/skills webapp-testing: inspection before action retained; Python, black-box helpers, server lifecycle and unconditional networkidle removed. Copyright 2026 Anthropic, PBC. [Apache-2.0](../licenses/anthropics-webapp-testing-Apache-2.0.txt). Official Playwright documentation and pinned sources: [PROVENANCE](../PROVENANCE.json).
