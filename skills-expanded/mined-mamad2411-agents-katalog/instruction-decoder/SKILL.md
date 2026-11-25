---
name: instruction-decoder
description: Decode complex or dense instructions into a clear sequence. Use when a user asks what a prompt, task, spec, issue, or instruction means, or when constraints need to be made explicit.
---

# Instruction Decoder

## Superpowers Gate

Before applying this skill, verify that Superpowers is available in the current session, such as an active `superpowers:` skill, `using-superpowers`, or equivalent Superpowers workflow instructions.

If Superpowers is missing or uncertain, stop and reply exactly with this guidance before doing any dyslex.ai work:

```text
dyslex.ai requires Superpowers before it can run. Install Superpowers from /plugins, or use codex plugin add superpowers@<marketplace> if you manage plugins from the Codex CLI, then start a new session.
```

Do not perform the requested dyslex.ai workflow until Superpowers is installed and loaded.

Transform a dense instruction into a structure the user can verify.

## Functional Mechanism

Primary dimensions: `workingMemory.multiStepInstructionLoad`, `workingMemory.simultaneousInformationLoad`, `executiveFunction.sequencingLoad`, `executiveFunction.planningLoad`, and `language.discourseOrganizationLoad`.

Decode instructions by externalizing the structure that would otherwise need to be held in working memory.

## Interaction Risk

Dense prompts can mix goal, constraints, warnings, order, forbidden actions, and success criteria. The user or agent may miss one part or act in the wrong order.

## Agent Strategy

- Extract the requested result first.
- Separate constraints from steps and success criteria.
- Preserve exact technical tokens.
- Ask only about ambiguities that materially change the result.
- Use the smallest confirmation needed when intent is likely but not certain.

## Avoid

- Do not add requirements not present in the source.
- Do not infer a diagnosis from disordered or dense instructions.
- Do not turn every typo into a clarification question.
- Do not collapse constraints into generic summary text.

## Output Format

Use this structure:

```text
Result requested
What is provided
Constraints
Steps
Do not do
Success criteria
```

## Rules

- Keep the original intent.
- Separate facts from assumptions.
- Use exact names for files, functions, commands, and concepts.
- Do not add requirements not present in the source text.
- Ask only about ambiguities that materially affect the result.
