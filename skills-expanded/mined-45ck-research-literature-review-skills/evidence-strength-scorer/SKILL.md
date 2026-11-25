---
name: "evidence-strength-scorer"
pack: "research-literature-review-pack"
purpose: "Assess the weight and credibility of evidence behind claims in the literature."
inputs: ['selected papers', 'claim set or themes', 'quality criteria', 'context of use']
outputs: ['evidence strength ratings', 'confidence notes', 'high-risk claim list']
handoffs: ['critical-analysis-writer', 'related-work-synthesizer', 'future-work-generator']
---
# evidence-strength-scorer

## Purpose
Assess the weight and credibility of evidence behind claims in the literature.

## Trigger this skill when
- You are doing literature review, related work, comparative research, or evidence-driven design.
- The user needs structured research outputs instead of scattered notes or ad hoc summaries.
- You need traceable justification for claims, gaps, methods, or future directions.

## Expected inputs
- selected papers
- claim set or themes
- quality criteria
- context of use

## Deliverables
- evidence strength ratings
- confidence notes
- high-risk claim list

## Operating procedure
1. Clarify the research objective, boundary, and decision the output is meant to support.
2. Distinguish source evidence from inference, synthesis, or speculation.
3. Produce the skill-specific artifact in a structured, reusable form.
4. Preserve source-to-theme, theme-to-gap, or claim-to-evidence traceability where relevant.
5. Recommend the next best handoff instead of collapsing the whole literature workflow into one output.

## Quality gates
- The output is scoped to the actual research question rather than generic background.
- Contradictions, uncertainties, and evidence limitations are surfaced explicitly.
- The structure is reusable in a report, review, appendix, or research memo.
- The synthesis adds value beyond a paper-by-paper summary.

## Handoff targets
- critical-analysis-writer
- related-work-synthesizer
- future-work-generator

## Output style
- Prefer matrices, theme groupings, claim-evidence structures, and explicit comparison criteria.
- Keep facts, synthesis, and speculation distinct.
- Preserve traceability from conclusions back to sources or evidence buckets.
- Surface missing evidence and unresolved questions instead of smoothing them over.

## Failure modes to avoid
- Do not confuse summary volume with analytical depth.
- Do not treat all sources as equally credible or equally relevant.
- Do not fabricate consensus where the literature is mixed or thin.
- Do not hide exclusion reasons, scope limits, or methodological weaknesses.
