---
name: antonify-instruction-architect
description: Create, rewrite, or audit system instructions and reusable agent skills using the Antonify method. Use when the user asks for system prompts, agent instructions, SKILL.md files, JSON-output agents, prompt architecture, image/video prompt agents, variation agents, or validation checklists.
---

# Antonify Instruction Architect

Use this skill to turn rough intent into a precise operating brief for an AI agent.

Default to a simple user experience: the user may give only a rough idea. Infer the first useful input schema and output shape for them, then show two test outputs so they can react.

## Inputs To Identify

- The agent's one-sentence job
- The input the agent receives
- The output the agent must produce
- Whether the output needs a strict schema or only a response pattern
- The facts, claims, structure, or tone it must preserve
- The transformations it may perform
- What it should not add without support
- The quality bar for a good result
- The checks it should run silently before answering

If details are missing and the task is still safe to complete, make conservative assumptions and label them.

## Workflow

1. Choose the target form: system instruction, JSON-output agent, SKILL.md, image prompt agent, video prompt agent, variation agent, or validation checklist.
2. Define the job in one sentence.
3. Draft the input schema or input fields. If the user did not provide them, infer the smallest useful set and label it as a draft.
4. Draft the output shape.
   - Use a strict output schema for JSON, tables, forms, automation payloads, or parsed output.
   - Use a response pattern for master prompts, system instructions, conversational agents, and open-ended work.
5. Add preservation rules for facts, user intent, formatting, tone, claims, brand details, or source constraints.
6. Add transformation rules that say what the agent may change, improve, restructure, classify, generate, or remove.
7. Add anti-invention rules. Make claims, proof, examples, metrics, citations, and constraints explicit.
8. Add role-specific quality criteria that are visible and testable.
9. Add a silent validation checklist.
10. Return the finished instruction.
11. Run an automatic two-example test:
    - Example A: normal realistic input and output
    - Example B: vague, missing-field, or edge-case input and output
12. End by asking what should change: input fields, output shape, tone, strictness, or examples.

For schema-based agents, the two examples must match the schema. For master prompts or open-ended agents, the examples should show the proposed response pattern.

## For SKILL.md Outputs

- Use a lowercase hyphenated `name` that matches the skill folder.
- Put the most important trigger words at the start of `description`.
- Keep `SKILL.md` focused on the core workflow.
- Move deeper guidance into `references/` and mention when to read it.
- Avoid platform-specific frontmatter unless the user names a target platform.
- Prefer instructions first. Add scripts only when deterministic behavior is needed.

## Validation Checklist

Before returning, confirm:

- The agent no longer has to guess its job, input, or output.
- The input schema or fields are clear enough for a user to provide.
- The output schema or response pattern is specific enough to test.
- Preservation rules and allowed transformations do not conflict.
- Anti-invention rules cover unsupported facts, proof, metrics, and citations.
- The instruction says what "good" means in observable terms.
- The result includes two test examples or explains why examples are not possible.
- The result is not bloated with duplicate rules.

## Response Shape

Return:

1. The finished instruction
2. Draft input schema or input fields
3. Draft output schema or response pattern
4. Two example outputs for user review
5. A short question asking what the user wants changed

## Reference

Use `references/antonify-method.md` for the compact Antonify method. If the full Antonify repo is available, deeper guides live in `docs/`, `templates/`, `checklists/`, and `examples/`.
