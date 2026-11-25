---
name: spin-tags
description: Add optional wording variants to static copy using the actual sender's supported syntax while preserving meaning, merge variables and experiment control.
---

# Vary static wording carefully

Read the reviewed message, voice context and frozen test plan. Use this skill only when wording variation is requested and the actual sender supports it. No deliverability improvement is promised.

Inspect current sender documentation and render behavior. Do not assume OXYGEN uses another platform's dialect. If support cannot be verified, return plain-text alternatives instead of untested tags.

Vary whole grammatical phrases with the same meaning. Keep the offer, proof, numbers, identity and personal evidence unchanged. Never spin merge variables or the dimension currently under A/B test. Incidental variation is not an experiment.

Keep the option count small enough to inspect all combinations. Preview each resulting message in the actual sender to check substitution, punctuation, grammar and factual consistency. If there are too many combinations to review, simplify.

Deliver the verified syntax, rendered examples and any unsupported case. Do not alter suppression, cadence or sending controls. Use `outbound-copywriter` for substantive copy changes and `split-test-designer` for a meaningful variant test.
