---
name: research-verification
description: Independently assess research claims against supplied evidence before they are relied upon.
license: MIT
---
# Research Verification

## Overview
Before reporting a finding, ask an independent verifier to classify each claim against the actual evidence as supported, contradicted, unsupported, or overstated. This is a lightweight claim gate, not a replacement for multi-source reconciliation on high-stakes research.

## Procedure
1. Preserve the exact claim, its producer, and the primary evidence available.
2. Select a verifier different from the producer and suitable for the subject.
3. Supply the task, rubric and primary evidence, especially for numbers, dates, quotations and precise technical assertions; retain an initial evidence-based judgment before showing the producer's evaluative summary, then assess that summary separately as attributed information rather than ground truth.
4. Require a verdict and reasoning for each claim. Hold unsupported claims; correct or flag contradicted and overstated claims.
5. Escalate contested or reliability-critical research to independent source reconciliation.

## Rules
- Independence is essential: a model's self-review is not the same as independent verification.
- Plausibility-only checks are weak for precise facts; evidence context is the preferred mode.
- Choose a verifier with appropriate safety and subject-matter limitations for sensitive topics.
- Keep the initial evidence judgment separate from summary-assisted review; the [research-team protocol](../../specs/research-team-protocol.md#independence-and-artifacts) cites both the adversarial-report harm and the honest-report improvement, so this rule is not a claim that all summaries degrade accuracy.

## Pitfalls
- Calling an unsupported number verified because it sounds plausible.
- Using the producing worker as the only verifier.
- Treating a local claim check as a complete evidence review.

## Verification checklist
- [ ] Producer and verifier differ.
- [ ] Primary evidence was provided where available.
- [ ] Unsupported and overstated claims were withheld or clearly labeled.
