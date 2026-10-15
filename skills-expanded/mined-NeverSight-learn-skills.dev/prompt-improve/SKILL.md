---
name: prompt-improve

description: Rewrite a prompt to make it clearer, more precise, and more effective without changing the user's intended goal. Use when a prompt feels vague, ambiguous, overly broad, or could produce better results with sharper instructions.

metadata:

  disable-model-invocation: true

---

# Prompt Improve

Make the prompt sharper.

This skill rewrites a prompt so its intent, requirements, constraints, and expected result are easier for an agent or model to understand and execute correctly.

It improves the prompt **without changing what the user is trying to accomplish**.

It is not a prompt generator. It is a prompt refinement tool.

## Preserve the intent

Before rewriting, identify:

- The actual objective
- The desired output or outcome
- Important constraints
- Relevant context
- Required format or behavior
- Any explicit preferences or exclusions

Treat these as part of the user's intent.

Do not add requirements that the user did not imply.

Do not remove meaningful constraints.

Do not change the desired outcome merely because another approach seems better.

## Improve the prompt

When rewriting, optimize for:

- **Clarity** — remove ambiguity and unclear references.
- **Specificity** — make important requirements explicit.
- **Structure** — organize complex instructions into logical sections.
- **Actionability** — make it clear what the agent should actually do.
- **Constraints** — surface important limits, exclusions, or conditions.
- **Output definition** — make the expected result unambiguous.
- **Efficiency** — remove unnecessary wording, repetition, and filler.

Prefer the smallest change that produces a meaningful improvement.

A short prompt should remain short when the task is simple.

Do not turn every prompt into a long system-style specification.

## Handle ambiguity

If the prompt contains ambiguity that can be resolved from the available context, resolve it in the rewrite.

If the ambiguity materially changes the intended task and cannot be resolved safely, do not invent an answer.

Instead, preserve the ambiguity explicitly and identify what needs clarification.

## Preserve user voice

Unless the user asks for a specific style, preserve the natural tone and level of directness of the original prompt.

Do not unnecessarily make casual prompts formal.

Do not add corporate, academic, or technical language merely to make the prompt sound sophisticated.

## Output

Format every reply as:

### Improved prompt

```text
<rewritten prompt>
````

### Changes

Briefly explain the most important improvements.

Keep the explanation concise.

## When the prompt is already good

If the prompt is already clear and sufficiently precise, do not rewrite it unnecessarily.

Return the original prompt and state:

> The prompt is already clear. No meaningful rewrite is needed.

## Important boundaries

* Do not execute the prompt.
* Do not answer the prompt.
* Do not invent missing requirements.
* Do not change the user's goal.
* Do not optimize for verbosity.
* Do not add hidden assumptions.
* Do not rewrite a prompt merely for stylistic preference.

## Maintenance

This skill should remain focused on improving existing prompts while preserving their original intent.

Only update this file when its refinement criteria or output format need to change.