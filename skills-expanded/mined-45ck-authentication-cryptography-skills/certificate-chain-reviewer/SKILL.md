---
name: "certificate-chain-reviewer"
pack: "authentication-cryptography-pack"
purpose: "Review certificate chains, issuer trust, validation behavior, pinning assumptions, and deployment mistakes that weaken transport trust."
inputs: ["system overview", "auth or trust flow description", "architecture diagrams", "protocol or implementation notes", "deployment assumptions"]
outputs: ["review findings", "risk notes", "design recommendations", "test or verification suggestions", "recommended next skill"]
handoffs: ["ca-ra-role-explainer", "certificate-revocation-reviewer", "trust-store-reviewer"]
---
# certificate-chain-reviewer

## Purpose
Review certificate chains, issuer trust, validation behavior, pinning assumptions, and deployment mistakes that weaken transport trust.

## Trigger this skill when
- The current artifact contains authentication, certificate, transport-trust, token, or PKI behavior that needs structured review.
- You need to turn vague trust or crypto concerns into concrete findings, controls, or requirements.
- You want the next auth- or trust-focused action to be explicit rather than ad hoc.

## Expected inputs
- system overview
- auth or trust flow description
- architecture diagrams
- protocol or implementation notes
- deployment assumptions

## Deliverables
- review findings
- risk notes
- design recommendations
- test or verification suggestions
- recommended next skill

## Operating procedure
1. Read the artifact from an identity, trust, transport, and verification perspective rather than only from the happy path.
2. Separate facts from assumptions and call out missing details that reduce confidence.
3. Focus on the highest-risk failure modes first: interception, impersonation, replay, downgrade, leakage, unsafe recovery, or broken trust assumptions.
4. Translate findings into explicit design, implementation, or verification actions.
5. Prefer concrete flow-level reasoning over generic cryptography advice.
6. Finish with the most sensible handoff skill based on the dominant weakness you found.

## Quality gates
- Findings are specific to the artifact and its trust model, not generic crypto boilerplate.
- Output separates facts, assumptions, risks, controls, and recommended next action.
- Prioritization reflects exposure and exploitability, not just theoretical correctness.
- Recommendations are implementable and framed in a way that can be tested or reviewed later.

## Handoff targets
- ca-ra-role-explainer
- certificate-revocation-reviewer
- trust-store-reviewer

## Output style
- Be explicit about uncertainty.
- Prefer concrete flow, trust, and failure-path reasoning over slogans.
- Separate facts, risks, recommendations, and next steps.
- Make the output usable by engineers, reviewers, and test designers.

## Failure modes to avoid
- Do not claim security merely because encryption or certificates exist somewhere in the design.
- Do not blur identification, authentication, authorization, session handling, and trust-anchor management into one vague discussion.
- Do not recommend controls without naming the attack or failure they address.
- Do not hide uncertainty when protocol or deployment details are missing.

## Minimum output skeleton
```md
## Summary
## Findings
## Structured outputs
## Risks
## Recommendations
## Recommended next skill
```
