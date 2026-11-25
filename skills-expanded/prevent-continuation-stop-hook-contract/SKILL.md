---
name: prevent-continuation-stop-hook-contract
description: "Return a narrow stop-hook result that can halt the query loop without throwing, while still surfacing blocking errors separately."
metadata:
  author: ychampion
---

# SKILL: Prevent Continuation Stop-Hook Contract
**Domain:** tool-orchestration  
**Trigger:** Apply when post-response hooks may decide that the query loop must stop, but the caller still needs a structured non-exception contract.
**Source Pattern:** Distilled from reviewed tool-loop and result-shaping patterns.

## Core Method
Represent stop-hook outcomes with a compact return contract instead of control-flow exceptions. Separate hard blocking errors from the boolean that says continuation should stop, and let the loop interpret that result after hooks, teammate callbacks, and summary messages have all been emitted. This keeps hook orchestration observable and composable while still allowing hooks to end the turn decisively.

## Key Rules
- Return a small structured result such as `{ blockingErrors, preventContinuation }` rather than throwing for normal stop decisions.
- Preserve the distinction between “there were blocking error messages” and “hooks intentionally stopped continuation.”
- Let hook attachments and summary messages be emitted before returning the stop decision so the stop remains visible in transcripts.
- Reuse the same contract across related hook families so teammate and task-completed hooks can short-circuit the loop in the same shape.

## Example Application
If a stop hook determines that a teammate should pause after reaching idle state, emit the relevant hook summary and return `preventContinuation: true`. The query loop can then stop cleanly without mistaking that decision for a crash.

## Anti-Patterns (What NOT to do)
- Do not throw exceptions for ordinary hook-driven stop decisions; callers lose the chance to emit hook summaries and structured attachments.
- Do not collapse blocking errors and stop signals into one field; the loop needs to know whether to surface errors or just stop.
