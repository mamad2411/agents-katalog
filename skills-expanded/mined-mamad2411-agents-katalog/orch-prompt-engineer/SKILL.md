---
name: orch-prompt-engineer
description: Prompt engineering specialist for agents and orchestration systems. Owns system prompts, role structure, few-shot selection, output formatting contracts, and guardrail prompting. Auto-invoked for prompt authoring, refinement, or regression investigation.
---

# Agent Prompt Engineering

Prompts are the production config of an LLM system: an unversioned, untested
prompt edit can change answers, costs, and safety behavior in one deploy. The
levers are structure, explicit contracts, and examples — not adjectives.

## When to reach for this

- Writing or refactoring a system prompt for an agent or pipeline stage
- An output parser keeps breaking, or the model drifts from the required format
- Choosing few-shot examples, or a prompt has grown into contradictory rules
- Investigating a behavior regression after a prompt or model change

## Principles

1. **Contract before content.** State the output format up front and enforce it
   with a parser (or the provider's structured-output / JSON mode). A format the
   code doesn't validate is a suggestion, not a contract.
2. **Order instructions by precedence.** Role and goal, then hard constraints,
   then rules, then tool guidance, then examples, then output format. When rules
   conflict, say which wins — the model otherwise picks inconsistently.
3. **Few-shot the hard cases.** Examples teach the decision boundary; 2–5
   examples of the ambiguous and adversarial inputs beat ten of the obvious ones.
4. **Pair every "never X" with an example.** Negative instructions alone are
   weak; "never do X — e.g. given input I, do Y instead" sticks.
5. **Write guardrails as behaviors, not vibes.** Specify when to refuse, when to
   ask a clarifying question, and when to escalate — each with a trigger
   condition and a canned shape for the response.
6. **Version and eval every prompt change.** Prompts live in the repo, change
   via PR, and run the regression suite — a one-word edit is still a release.

## System-prompt skeleton

```markdown
# Role and goal
You handle <task> for <system>. Success means <measurable outcome>.

# Hard constraints (override everything below)
- Never <action>. If asked, respond with <shape>.
- Output MUST validate against the schema in "Output format".

# Rules
1. <rule>           # numbered: referable in evals and incident review
2. If <ambiguous condition>, ask one clarifying question instead of guessing.

# Tools
Prefer <tool-a> for <case>; <tool-b> only when <condition>.

# Examples
<input> → <ideal output>          # hard/ambiguous cases, not happy path

# Output format
Respond with JSON matching: { "...": ... }   # enforced by parser
```

## Pitfalls

- Format instructions buried mid-prompt and contradicted by a later example
- Few-shot examples whose style leaks (the model copies their length, tone, or
  even their literal field values)
- Piling on rules to patch failures instead of fixing retrieval, tools, or evals —
  long rule lists dilute each other
- "Be concise"-style adjectives where a measurable bound ("≤ 3 sentences") works
- Prompt edits shipped without a before/after eval run, so the regression is
  found by users
- Untrusted content (user input, retrieved docs) interpolated into the
  instruction section instead of clearly delimited data sections

---
*Related: `orch-tool-design` (tool schemas the prompt references), `orch-eval`
(regression gate for prompt changes), `orch-sandbox-safety` (injection defense for
untrusted input), `ai-prompt-engineer` (ai-pack sibling) · domain agent:
`orch-architect` · output/ADR format: `playbook-conventions`*
