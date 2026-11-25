---
name: quality-change-review
description: 'Independently review or accept a candidate change and verify defect claims with evidence, separating findings, gaps and hypotheses. Use for review or acceptance decisions, not implementation. RU: ревью, проверка приёмки, проверка находки, мутационное тестирование.'
---

# Independent review and verified findings

Use for an independent review or acceptance decision, not implementation. Establish the request, review authority, required independence, exact candidate and relevant boundaries before inspecting. Record the current revision, staged/unstaged and relevant untracked work where authorized. When the tree may move, check candidate identity before relying on earlier evidence; a snapshot is not proof of runtime behavior.

Trace the actual behavior from producer and inputs through consumers, state transitions and observable effects. For cross-layer changes inspect shared wiring and the complete integrated range, not only each child verdict. For a prior finding, verify the current candidate and relevant regression; previous reviewer or implementer summaries are leads, not fresh results.

Classify observed defects, evidence gaps and hypotheses separately. State the trigger, affected boundary, impact and precise source or evidence. An unavailable required gate can block acceptance without being a proven product defect. Do not infer authorization to edit, stage, move a board card or publish from review alone. Run only permitted checks with side effects understood; preserve partial, failed and unrun results.

## Verifying a claim or finding

- State precisely what was observed and the boundary of the claim. Code inspection, static analysis, live execution and tests establish different facts; never imply an unexercised path or an unavailable test was verified. For a negative claim, define the searched or tested scope and confirm the observation instrument works.
- Reproduce a reported failure when practical before relying on its predicted cause. Verify a fix against the relevant behavior and the final artifact: reproducing a defect is not evidence that the fix works. If execution is unsafe, unavailable or unauthorized, use the best permitted evidence and state the limit.
- Use mutation only when it materially tests the claimed guard and is authorized and safe. Check that the intended test was selected, the code ran, the fixture could express the defect and a failing result failed for the intended reason. Restore only the exact owned change, verify the final bytes and any rebuilt artifact, and preserve unrelated work. Do not mutate in a read-only review.
- If a test failure may disclose sensitive values and checking is authorized, exercise the failing assertion with a synthetic canary and inspect the retained output without revealing the canary; assertion frameworks can print subexpression values.
- Counts, searches and output must cover the actual question: truncation, deselection, collection failure and zero records can look cleaner than reality. Report command, scope, outcome and limits; never report a partial or still-running check as passed. Worked examples: [instances](instances.md).

For requested negative guarantees consult [negative contract review](references/negative-contracts.md); for backend reviews [backend boundaries](references/backend-boundaries.md); for cross-runtime configuration and session changes [integration boundaries](references/integration-boundaries.md). For exact final validation results use `quality-change-verify`, and for noisy command evidence `agent-command-run`. Give the requested verdict with actionable findings, evidence and limitations, without overstating untested behavior.
