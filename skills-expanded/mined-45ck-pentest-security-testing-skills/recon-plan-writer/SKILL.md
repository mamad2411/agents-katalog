---
name: "recon-plan-writer"
pack: "pentest-security-testing-pack"
purpose: "Plan safe, scoped reconnaissance for an authorized security assessment so discovery work stays useful and non-destructive."
inputs: ["authorized scope", "target inventory", "known technologies", "time constraints", "assessment goals"]
outputs: ["recon plan", "enumeration checklist", "evidence targets", "priority discovery paths", "tool/use cautions"]
handoffs: ["cloud-asset-discovery-planner", "api-attack-surface-mapper", "manual-web-test-sequencer"]
---
# recon-plan-writer

## Purpose
Plan safe, scoped reconnaissance for an authorized security assessment so discovery work stays useful and non-destructive.

## Trigger this skill when
- The current artifact or engagement needs a structured security-testing step rather than ad hoc probing.
- You need evidence-backed outputs that can hand off cleanly to reporting or remediation.
- You are working only within owned or explicitly authorized scope.

## Expected inputs
- authorized scope
- target inventory
- known technologies
- time constraints
- assessment goals

## Deliverables
- recon plan
- enumeration checklist
- evidence targets
- priority discovery paths
- tool/use cautions

## Operating procedure
1. Confirm the authorization, scope, red lines, and stop conditions before doing anything else.
2. Read the artifact or engagement context from an assessor perspective and identify the highest-value review path first.
3. Prefer safe proof, minimal-impact testing, and evidence capture over deeper exploitation.
4. Separate facts, hypotheses, validated observations, and unresolved questions.
5. Record what was tested, what was not tested, and why.
6. Finish with the most sensible handoff skill based on whether the next need is more testing, reporting, or remediation.

## Quality gates
- Output remains specific to the authorized target and current evidence.
- Unsafe, out-of-scope, or ambiguous actions are explicitly rejected or escalated.
- Findings or test plans are concrete enough for another engineer or reviewer to follow.
- Recommendations are actionable and proportional to the demonstrated issue.

## Handoff targets
- cloud-asset-discovery-planner
- api-attack-surface-mapper
- manual-web-test-sequencer

## Output style
- Be explicit about authorization assumptions and testing boundaries.
- Prefer concrete evidence paths, affected scope, and next actions over generic advice.
- Separate facts, hypotheses, validated findings, and recommendations.
- Make the output usable by defenders, builders, and reviewers.

## Failure modes to avoid
- Do not proceed as though all targets are authorized when the scope is unclear.
- Do not recommend disruptive or destructive actions when lower-impact proof is sufficient.
- Do not blur speculation and validated evidence.
- Do not produce vague findings that owners cannot reproduce or fix.

## Minimum output skeleton
```md
## Summary
## Facts and scope
## Structured outputs
## Risks or findings
## Recommendations
## Recommended next skill
```
