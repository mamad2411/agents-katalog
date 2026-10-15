---
name: subagent-prompt-foundry
description: >-
  Generate deterministic, reusable system prompts for custom subagents across code, research, design, security, planning, validation, and workflow tasks. Use when the user asks for a system prompt for an agent, wants to make a prompt reusable, needs a production-grade subagent prompt with structure or constraints, or wants a parent agent to delegate work to an isolated subagent. Triggers: "create a custom subagent", "system prompt for an agent", "make this prompt reusable", "design a subagent prompt", "production-grade prompt for a reviewer". Do not use for generic prompt advice, direct task execution, meta-agent prompt creation, or requests that only want the final answer.
license: MIT
compatibility: Platform-agnostic. Requires Python 3 for bundled scripts and network access for mandatory web research. Subagents run outside the parent agent's primary context window.
metadata:
  tags:
    - prompt-engineering
    - subagents
    - multi-agent
    - deterministic-prompts
allowed-tools: "Bash(python:*) WebFetch"
---

# Subagent Prompt Foundry

Generate a **system prompt for a custom subagent**.

Return **only the final system prompt** unless the user explicitly asks for the skill package itself.

## Progressive disclosure and file navigation

This skill uses staged loading. Go to the smallest file that solves the current need.

| Situation | Go here | Do not go here |
|---|---|---|
| You need the main workflow, routing, or final output rule | `SKILL.md` | Do not start in `references/` unless the case is ambiguous |
| Routing is ambiguous or overlaps with neighboring skills | `references/ROUTING_MATRIX.md` and `assets/routing-checklist.md` | Do not jump to `references/OUTPUT_STRUCTURES.md` first |
| The request is underspecified and you need to decide between asking questions vs researching first | `references/RESEARCH_AND_CLARIFICATION.md` | Do not use `references/FAILURE_MODES.md` as your first source for this |
| You need the parent↔subagent handoff format or isolated-execution rules | `references/SUBAGENT_PROTOCOL.md` and `assets/parent-subagent-message-template.json` | Do not invent a custom handoff structure if these files are sufficient |
| The user supplied no exact output format | `references/OUTPUT_STRUCTURES.md` | Do not override a user-provided exact format |
| You need to check common prompt-quality mistakes before finalizing | `references/FAILURE_MODES.md` | Do not use it as a substitute for the main workflow |
| You need a starting skeleton for the generated prompt | `assets/subagent-template.md` | Do not use it unchanged when the request needs domain-specific structure |
| You need to validate that the generated prompt includes the required sections | `scripts/validate_prompt_shape.py` | Do not skip validation |
| You need to compare a revised prompt to a prior version | `scripts/diff_prompt_versions.py` | Do not diff manually if a prior version exists |
| You need to score determinism before returning the prompt | `scripts/score_determinism.py` | Do not estimate determinism informally |
| You need to verify routing quality or overlap behavior | `evals/evals.json` | Do not rely on intuition alone |

## Activation criteria

### Use this skill when the user asks for:
- a system prompt for an agent or subagent
- a reusable or production-grade agent prompt
- a prompt that should be generalized from an example
- a parent agent that delegates work to a subagent
- a structured prompt with explicit methodology, constraints, or output rules

### Trigger phrases
- "create a custom subagent"
- "system prompt for an agent"
- "make this prompt reusable"
- "design a subagent prompt"
- "turn this into a production-grade prompt"
- "create a reviewer / auditor / planner / researcher prompt"

### Do not use this skill when:
- the user wants direct task execution
- the user wants generic advice on prompting
- the user wants a meta-agent that writes prompts for other agents
- the user wants only the final answer, not a reusable prompt artifact

### Anti-trigger phrases
- "just do the task"
- "just answer the question"
- "give me prompt tips"
- "I only need the result"
- "create a meta-agent that writes prompts"

## Overlap resolution

This skill must coexist cleanly with:
- direct task-execution skills
- generic prompt-advice skills
- narrower single-agent prompt skills
- meta-agent prompt skills

Prefer this skill only when the user wants a reusable system prompt for a custom subagent.

Prefer another skill when the user clearly wants:
- the task completed directly
- advice rather than a prompt artifact
- a meta-agent that generates prompts for other agents
- a narrower one-off prompt where reuse is not part of the request

If overlap is unclear, load:
- `references/ROUTING_MATRIX.md`
- `assets/routing-checklist.md`

## Core objective

Produce a system prompt that makes the subagent:

1. understand its role precisely
2. know exactly which inputs, artifacts, and sources to use
3. know exactly what deliverable it must produce
4. follow an explicit, verifiable methodology
5. ask clarifying questions when missing details materially affect the result
6. perform web research before finalizing the prompt
7. prefer first-party and official sources, using strong third-party sources when they improve correctness or context
8. operate in an isolated context outside the parent agent's primary context window
9. communicate with the parent agent through a defined protocol
10. remain deterministic in structure while adapting to the requested domain

## Required tools and files

The following scripts are required for this skill's workflow. Invoke them relative to the skill directory root:

```
python scripts/validate_prompt_shape.py prompt.md
python scripts/score_determinism.py metrics.json
python scripts/diff_prompt_versions.py prompt_v1.md prompt_v2.md
```

- `scripts/validate_prompt_shape.py`
- `scripts/diff_prompt_versions.py`
- `scripts/score_determinism.py`

The following files are required reference points:
- `references/ROUTING_MATRIX.md`
- `references/RESEARCH_AND_CLARIFICATION.md`
- `references/SUBAGENT_PROTOCOL.md`
- `references/FAILURE_MODES.md`
- `references/OUTPUT_STRUCTURES.md`
- `assets/subagent-template.md`
- `assets/parent-subagent-message-template.json`
- `assets/routing-checklist.md`
- `evals/evals.json`

Do not skip the scripts. Use them as part of the workflow, not as optional extras.

### How to use score_determinism.py

The determinism scorer takes a JSON file with four dimensions, each rated 0.0 to 1.0:

```json
{
  "structure_stability": 0.0,
  "constraint_preservation": 0.0,
  "research_completeness": 0.0,
  "protocol_clarity": 0.0
}
```

| Dimension | What it measures | 1.0 means | 0.0 means |
|---|---|---|---|
| structure_stability | Would the same request class produce the same section layout? | Identical skeleton every time | Layout varies unpredictably |
| constraint_preservation | Are all user-provided constraints present in the final prompt? | Every constraint preserved | Constraints dropped or diluted |
| research_completeness | Did research inform the terminology, sources, and constraints? | All domain terms verified | No research performed |
| protocol_clarity | Is the parent↔subagent handoff schema unambiguous? | Full message contract defined | No handoff structure |

Rate each dimension yourself after drafting the prompt. Write the JSON to a temporary file and pass it to the script. A composite score below 0.7 means the prompt needs structural work, not wording tweaks.

## Mandatory workflow

Follow this order exactly:

1. Route correctly
2. Check whether the request is sufficiently specified
3. Perform web research
4. Ask clarifying questions if research does not resolve material ambiguity
5. Define role and scope
6. Bind inputs, artifacts, and sources
7. Define task and deliverable
8. Define domain-specific dimensions
9. Define methodology
10. Define evidence standards
11. Define parent↔subagent protocol
12. Define output format
13. Apply constraints
14. Draft the prompt
15. Validate prompt shape with `scripts/validate_prompt_shape.py`
16. Critique using `references/FAILURE_MODES.md`
17. Diff against any prior draft with `scripts/diff_prompt_versions.py`. Skip this step if no prior draft exists.
18. Rate determinism dimensions, write metrics JSON, score with `scripts/score_determinism.py`
19. Return only the final system prompt

Do not reorder this workflow.

## Web research policy

Web research is mandatory.

### Always do this
- search for first-party or official documentation relevant to the requested subagent domain
- use web findings to sharpen terminology, constraints, deliverables, and clarifying questions
- include strong third-party sources only when they materially improve correctness, context, or practical coverage

### Source priority
1. first-party sources
2. official documentation
3. standards and specs
4. strong third-party sources

### Do not do this
- do not browse aimlessly
- do not substitute third-party summaries for official sources when official sources exist
- do not skip research just because the request seems familiar

For research and clarification rules, load:
- `references/RESEARCH_AND_CLARIFICATION.md`

## Clarification policy

If the prompt is still underspecified after research, ask only short, decision-relevant questions that affect:
- role
- inputs
- deliverable
- format
- constraints
- source policy
- tools
- evaluation criteria
- parent↔subagent handoff

Do not ask broad, lazy questions like "Can you give more context?"

## Parent↔subagent execution model

The subagent runs outside the parent agent's primary context window.

The subagent must not assume access to:
- hidden context
- the full conversation
- the parent's scratchpad
- omitted constraints

### Parent sends
- task_summary
- goal
- constraints
- artifacts
- allowed_tools
- required_output
- success_criteria
- exclusions

### Subagent returns
- task_understanding
- assumptions
- blocking_questions
- output
- evidence
- uncertainty
- confidence
- next_step

For details, load:
- `references/SUBAGENT_PROTOCOL.md`
- `assets/parent-subagent-message-template.json`

## Required subagent behavior

The generated prompt must enforce:

### Role
Use a direct role opener such as:
- You are auditing...
- You are reviewing...
- You are validating...
- You are researching...
- You are planning...
- You are generating...

Never use:
- You are a helpful assistant

### Inputs
Bind the subagent to explicit artifacts and sources only.

### Methodology
Use explicit actions such as:
- inspect
- compare
- verify
- classify
- synthesize
- cite

### Evidence
Require grounded conclusions and explicit references where appropriate.

### Domain adaptation
Do not flatten different domains into generic logic.

## Output format

If the user provides an exact format, preserve it exactly.

If not, load:
- `references/OUTPUT_STRUCTURES.md`

Do not go to `references/OUTPUT_STRUCTURES.md` when the user has already provided a strict structure.

## Constraints

The generated prompt must forbid the subagent from:
- acting like a generic assistant
- relying on vague wording like "think carefully"
- assuming features exist because they are named
- trusting documentation blindly
- treating tests as proof unless they actually verify the property
- treating scaffolding as implementation
- omitting uncertainty when evidence is incomplete

## Self-check loop

1. Draft once
2. Review the draft against `references/FAILURE_MODES.md`
3. Rewrite once
4. Validate shape with `scripts/validate_prompt_shape.py`
5. Score determinism with `scripts/score_determinism.py`

If a prior draft exists, also run:
- `scripts/diff_prompt_versions.py`

## Routing validation

Use `evals/evals.json` to test:
- trigger cases
- anti-trigger cases
- overlap with neighboring skills
- routing precision against similar use cases

Do not claim routing quality without checking `evals/evals.json`.

## Quality gate

Before returning the final system prompt, verify that it:
- defines one concrete subagent role
- includes scope boundaries
- binds explicit inputs and sources
- includes mandatory research and targeted clarification behavior
- defines the parent↔subagent protocol
- preserves exact user format when provided
- has passed script-based validation
- has a determinism score
- contains no filler or redundant instructions

## Performance Notes

Take your time with each step. Do not skip validation steps.

- The research step (step 3) is mandatory even when the domain seems familiar. Skipping it produces generic prompts that fail the failure-modes critic pass.
- The validation scripts (steps 15 and 18) are not optional extras. They exist because informal quality checks miss structural problems that the scripts detect reliably.
- The self-check loop (draft → critique → rewrite → validate) typically catches 2–3 significant issues per prompt. Skipping it produces lower-quality output.
- When a prior draft exists, always run `scripts/diff_prompt_versions.py`. Regression from one version to the next is a common and silent failure mode.
- Determinism scoring below 0.7 is a signal to restructure the prompt, not to tweak wording.

## Examples

### Example 1: Code review subagent

**User:** I need a system prompt for a code review subagent that my CI pipeline can call.

**Agent workflow:**
1. Routes to this skill (user wants a reusable system prompt for a custom subagent)
2. Researches code review standards (e.g., Google Engineering Practices, OWASP)
3. No material ambiguity after research — skips clarifying questions
4. Drafts a prompt binding the subagent to: diff as input, PR description as context, findings as output with severity ratings
5. Validates shape: confirms Role, Scope, Inputs, Task, Methodology, Output sections present
6. Critiques against failure modes: checks for generic-assistant drift, domain flattening
7. Scores determinism: 0.85 — acceptable
8. Returns the finished system prompt

---

### Example 2: Generalizing a one-off prompt

**User:** Make this prompt reusable across projects: "Review this API and flag any security issues."

**Agent workflow:**
1. Routes to this skill (user wants a reusable prompt artifact)
2. Researches API security standards (OWASP API Security Top 10)
3. Asks one targeted question: "Should the subagent produce a structured JSON report or a markdown summary?"
4. Drafts prompt binding the subagent to: API spec file as input, OWASP Top 10 as source, structured findings as output
5. Validates shape and scores determinism
6. Returns the finished system prompt

---

### Example 3: Security audit subagent for parent agent delegation

**User:** Design a subagent my parent agent can delegate security audits to.

**Agent workflow:**
1. Routes to this skill (parent↔subagent delegation is a primary trigger)
2. Researches security audit frameworks and common subagent handoff patterns
3. Loads `references/SUBAGENT_PROTOCOL.md` and `assets/parent-subagent-message-template.json`
4. Drafts prompt defining the parent→subagent message schema (artifacts, constraints, success criteria) and the subagent→parent return schema (findings, confidence, blocking questions)
5. Validates, critiques, scores
6. Returns the finished system prompt

## Troubleshooting

### Script not found
If `scripts/validate_prompt_shape.py` cannot be found, verify that you are running the script relative to the skill directory root, not from the repository root. Correct invocation:
```
cd path/to/skill-dir
python scripts/validate_prompt_shape.py assets/subagent-template.md
```

### Determinism score is low (below 0.7)
A low score means the prompt structure is under-specified. Common causes:
- Role opener is vague ("You are an assistant that helps with...")
- Methodology section uses filler verbs ("think carefully", "consider")
- Output section does not specify a concrete format or schema

Fix by tightening the role opener, replacing filler verbs with explicit actions (inspect, verify, classify, synthesize), and adding a concrete output schema.

### Validation fails with missing sections
The validator checks for: Role, Scope, Inputs, Task, Methodology, Output. If any are missing, add them explicitly as labeled sections in the generated prompt. Do not merge multiple required sections into one.

### Research step returns no useful results
If web research returns nothing relevant for an obscure domain, fall back to:
1. First-party documentation for adjacent domains
2. Standards bodies (ISO, NIST, OWASP, RFC) that cover the space
3. Note the gap explicitly in the prompt's evidence standards section

### Routing confusion with neighboring skills
If this skill and a direct-task skill both seem applicable, check `references/ROUTING_MATRIX.md` and `assets/routing-checklist.md`. The deciding question: does the user want a reusable prompt artifact, or just the task done? If the latter, defer to the direct-task skill.

## Output rule

Return only the finished system prompt.
