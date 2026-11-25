---
name: "memory-poisoning-risk-reviewer"
pack: "llm-agent-security-pack"
purpose: "Review whether long-term memory, vector stores, notes, or cached context can be poisoned and later influence the agent unsafely."
inputs: ["memory design", "write paths", "retrieval logic", "trust signals", "example stored records"]
outputs: ["memory poisoning findings", "poisoning scenarios", "trust and write-control recommendations", "containment actions", "recommended next skill"]
handoffs: ["retrieval-trustworthiness-reviewer", "prompt-injection-reviewer", "guardrail-policy-writer"]
---
# memory-poisoning-risk-reviewer

## Purpose
Review whether long-term memory, vector stores, notes, or cached context can be poisoned and later influence the agent unsafely.

## Trigger this skill when
- The current artifact has LLM, prompt, retrieval, memory, or agent-tooling behavior that needs structured review or hardening.
- You need to turn vague AI safety or agent security concerns into concrete findings, controls, or requirements.
- You want the next agent-security-focused action to be explicit rather than ad hoc.

## Expected inputs
- memory design
- write paths
- retrieval logic
- trust signals
- example stored records


## Deliverables
- memory poisoning findings
- poisoning scenarios
- trust and write-control recommendations
- containment actions
- recommended next skill


## Operating procedure
1. Read the artifact from an agent-security perspective and identify the concrete trust, autonomy, and side-effect model.
2. Separate facts from assumptions and call out missing details that materially affect risk or confidence.
3. Start with the highest-impact abuse paths rather than trying to describe every possible issue equally.
4. Translate findings into explicit controls, approvals, isolation boundaries, or policy language that builders can act on.
5. Prefer concrete exploit paths, sinks, boundaries, and failure conditions over generic AI-safety slogans.
6. Finish with the most sensible handoff skill based on the dominant risk pattern you found.

## Quality gates
- Findings are specific to the actual prompt, retrieval, memory, tool, or runtime design rather than generic AI risk boilerplate.
- Output separates facts, assumptions, risks, controls, and recommended next action.
- Prioritization reflects impact, privilege, and automation potential rather than just issue count.
- Recommendations are implementable and framed in a way that can be tested or reviewed later.

## Handoff targets
- retrieval-trustworthiness-reviewer
- prompt-injection-reviewer
- guardrail-policy-writer


## Output style
- Be explicit about uncertainty.
- Prefer concrete abuse paths and control implications over generic safety slogans.
- Separate facts, risks, recommendations, and next steps.
- Make the output usable by engineers, reviewers, security testers, and policy owners.

## Failure modes to avoid
- Do not treat "the model should know better" as a security control.
- Do not bury high-impact autonomous action risk behind long, unprioritized issue lists.
- Do not recommend guardrails without explaining the exploit or failure they address.
- Do not hide uncertainty when prompt assembly, retrieval, memory, or runtime details are missing.

## Minimum output skeleton
```md
## Summary
## Findings
## Structured outputs
## Risks
## Recommendations
## Recommended next skill
```
