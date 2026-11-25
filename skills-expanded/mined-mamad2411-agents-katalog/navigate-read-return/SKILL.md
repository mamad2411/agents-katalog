# Navigate Read Return

## When To Use

Use this skill when the task requires visiting a different page to extract information and then returning to the original page to continue the workflow.

Use it for:

- looking up details on a linked page (job listing, product detail, profile)
- gathering a fact from a secondary page before acting on the primary page
- round-trip navigation where both the outbound read and the return leg matter

Do not use it for:

- one-way navigation where the user just wants to go somewhere
- tasks that stay on a single page
- multi-tab comparison tasks (use cross-tab-compare instead)

## Procedure

1. Record the current page URL and any relevant context before navigating away.
2. Navigate to the target page using the most direct path available.
3. Read the target page and extract the specific information needed.
4. Store the extracted fact in notes before navigating back.
5. Navigate back to the original page using go_back or direct navigation.
6. Verify the return landed on the expected origin page.
7. Continue the workflow using the extracted fact.

## Required Evidence

- The origin page URL recorded before navigation
- The target page reached and the specific fact extracted
- Evidence that the fact was stored before returning
- The origin page verified after return

## Common Failures

- Navigating back without capturing the needed fact first
- Forgetting to verify the return page matches the expected origin
- Over-decomposing the round trip into too many intermediate steps
- Using go_back when the history stack is unreliable, instead of direct navigation

## Verification

- Confirm the extracted fact is present in notes or the final response.
- Confirm the agent returned to the origin page before continuing.
- If the return page differs from the expected origin, re-navigate rather than proceeding on the wrong page.

## Relevance

This skill covers a common real-world browser pattern: drill into a detail page, extract what you need, come back. It is distinct from cross-tab-compare (which keeps multiple tabs open) and from one-way navigation.

Current E2E targets:

- `tests/e2e/job-board.test.ts`
- `tests/e2e/go-back-chain.test.ts`
