# Content Intelligence Package Instructions

This package converts normalized source observations into retrieval signals. Keep observation, inference, and recommendation data separate.

## Invariants

- Never treat raw engagement as truth, quality, or universal performance.
- Preserve source timestamps and observed metrics.
- Explicitly mark anti-pattern and ineligible candidates.
- Do not copy source wording into recommendations.
- All recommendations must cite selected observation IDs.
- Deterministic bootstrap scoring must remain inspectable and tested.
