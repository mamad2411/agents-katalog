---
name: "trust-boundary-identifier"
pack: "security-engineering-pack"
purpose: "Identify trust boundaries between users, services, networks, data stores, third parties, and privileged components."
inputs: ["architecture diagrams", "data flow", "network topology", "user/service roles", "deployment context"]
outputs: ["trust boundary list", "boundary diagram notes", "implicit trust assumptions", "boundary risks", "recommended controls"]
handoffs: ["least-privilege-reviewer", "authn-authz-separator", "session-security-reviewer"]
---
# trust-boundary-identifier

## Purpose
Identify trust boundaries between users, services, networks, data stores, third parties, and privileged components.

## Trigger this skill when
- The current artifact has security implications that need structured review or hardening.
- You need to turn vague security concerns into concrete findings, controls, or requirements.
- You want the next security-focused action to be explicit rather than ad hoc.

## Expected inputs
- architecture diagrams
- data flow
- network topology
- user/service roles
- deployment context

## Deliverables
- trust boundary list
- boundary diagram notes
- implicit trust assumptions
- boundary risks
- recommended controls

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
- least-privilege-reviewer
- authn-authz-separator
- session-security-reviewer

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
