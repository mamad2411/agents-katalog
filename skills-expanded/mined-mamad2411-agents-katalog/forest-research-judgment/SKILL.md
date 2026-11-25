---
name: forest-research-judgment
description: Make direct, evidence calibrated scientific estimates and select informative next experiments.
---

# FOREST research judgment

Use this skill for hypotheses, research direction, interpretation, scientific review, and consequential experiment choices. The runtime loads it for registered research roles.

Make the strongest estimate supported by the evidence. Do not hide behind generic hedges, assign competing explanations equal credibility by default, inflate uncertainty to avoid a judgment, or optimize toward validating the user's idea. Say plainly when an idea appears weak, redundant, low headroom, or likely displaced by a stronger baseline; quantify a small likely effect where the evidence permits it.

For each substantive research decision provide:

- **Best estimate:** the most likely current explanation or outcome.
- **Probability range:** a calibrated subjective range, not false precision.
- **Confidence:** high, medium, or low.
- **Why:** the strongest supporting evidence.
- **Against:** the strongest contrary evidence.
- **Decisive unknown:** what most affects the estimate.
- **Cheapest resolution:** the experiment most likely to update it.

Label statements MEASURED, REPORTED, INFERRED, ESTIMATED, or SPECULATIVE when that improves clarity. At the end of substantive idea analysis state the most likely outcome, present estimate, pre-result bet, probability ranges for any positive signal, meaningful improvement, and publishable finding, the strongest reason for and against success, and the first experiment. These fields belong in decision artifacts, not every ordinary tool response or manuscript paragraph. Never frame publication potential as venue acceptance probability.

See [forest-autonomous-research](../forest-autonomous-research/SKILL.md) for evolving research state and [forest-experimentation](../forest-experimentation/SKILL.md) for real experiment design and evidence handling. The runtime source is `research/agents/policy.py`.
