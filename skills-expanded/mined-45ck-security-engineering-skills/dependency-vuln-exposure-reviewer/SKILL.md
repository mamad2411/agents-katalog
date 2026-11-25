---
name: "dependency-vuln-exposure-reviewer"
pack: "security-engineering-pack"
purpose: "Review dependency choices and deployment exposure to identify vulnerable packages, frameworks, runtimes, and inherited attack paths."
inputs: ["dependency manifest", "runtime versions", "framework list", "public exposure", "update policy"]
outputs: ["dependency exposure findings", "risky components list", "upgrade/remediation options", "inherited-risk notes", "priority actions"]
handoffs: ["security-requirements-writer", "threat-surface-mapper", "security-misconfiguration-checker"]
---
# dependency-vuln-exposure-reviewer

## Purpose
Review dependency choices and deployment exposure to identify vulnerable packages, frameworks, runtimes, and inherited attack paths.

## Trigger this skill when
- The current artifact has security implications that need structured review or hardening.
- You need to turn vague security concerns into concrete findings, controls, or requirements.
- You want the next security-focused action to be explicit rather than ad hoc.

## Expected inputs
- dependency manifest
- runtime versions
- framework list
- public exposure
- update policy

## Deliverables
- dependency exposure findings
- risky components list
- upgrade/remediation options
- inherited-risk notes
- priority actions

## Operating procedure
1. Read the artifact from a security perspective and identify the concrete trust and exposure model.
2. Separate facts from assumptions and call out missing information that affects confidence.
3. Map the highest-risk paths first rather than trying to describe every possible issue equally.
4. Translate findings into concrete control or requirement language that a builder can act on.
5. Prefer explicit attack paths, assets, boundaries, and failure conditions over generic advice.
6. Finish with the most sensible handoff skill based on the dominant risk area you found.

## Quality gates
- Findings are specific to the artifact and threat context, not generic security boilerplate.
- Output separates facts, assumptions, risks, controls, and recommended next action.
- Prioritization reflects impact and exposure, not just the number of issues found.
- Recommendations are implementable and framed in a way that can be tested or reviewed later.

## Handoff targets
- security-requirements-writer
- threat-surface-mapper
- security-misconfiguration-checker

## Output style
- Be explicit about uncertainty.
- Prefer concrete attack paths and control implications over generic slogans.
- Separate facts, risks, recommendations, and next steps.
- Make the output usable by engineers, reviewers, and test designers.

## Failure modes to avoid
- Do not confuse compliance language with real security risk reduction.
- Do not bury critical exposure behind long, unprioritized issue lists.
- Do not recommend controls without explaining the attack or failure they address.
- Do not hide uncertainty when architecture or deployment details are missing.

## Minimum output skeleton
```md
## Summary
## Findings
## Structured outputs
## Risks
## Recommendations
## Recommended next skill
```
