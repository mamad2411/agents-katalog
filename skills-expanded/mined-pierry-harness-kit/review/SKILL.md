---
name: review
description: Adversarial design review of a System Design Doc. Interrogates the staff questions, finds the cost-explosion and failure risks, returns a verdict. Sensors and evals gate.
user_invocable: true
---

Review a System Design Doc the way a staff engineer runs a design review. Follow guides/pipeline.md.

Ask once if missing: path to the design doc (default latest under
`.claude/runtime/outputs/architect/design/`). Reviews own or external designs.

Read:
- the target design doc
- guides/design-method.md  (judge against the canon and the three pillars)
- guides/writing-style.md
- guides/templates/design-review.md
- guides/pipeline.md

Interrogate, do not summarize. For each of the 10 staff questions, give the design's answer and the
gap. Order findings by severity (blocker / high / medium / low). Name trade-offs the design left
implicit. Be specific: cite the section, name the failure, propose the fix. Default to skeptical.

Verdict: ship | revise | block.

Save to .claude/runtime/outputs/architect/review/{feature_id}.md (reuse the design's feature_id).

Sensors: sensors/design-structure.md (review variant: all 10 questions answered, verdict present).
Evals: evals/design-review-depth.md.

After save reply: Review saved at {path}. Verdict: {ship|revise|block}. Score: {N}/10.
