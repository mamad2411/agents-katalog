---
name: perfect-prompt
description: Stress-test and refine user prompts until they are specific, unambiguous, and execution-ready. Use when the user asks to improve, validate, critique, rewrite, or make a perfect prompt, or when they mention prompt quality, ambiguity, missing context, unclear requirements, or prompt engineering.
---

# Perfect Prompt

## Goal

Turn a rough prompt into an execution-ready prompt by finding vague wording, missing context, hidden assumptions, weak success criteria, and unnecessary scope.

Do not rewrite immediately if the prompt is underspecified. Interrogate it first.

## Workflow

1. Classify the prompt and choose the next action:
   - **Simple**: enough context and a clear expected output.
   - **Rough**: direction exists, but important details are missing.
   - **Ambiguous**: multiple interpretations could produce different work.
   - **Unclear**: goal, audience, or output cannot be inferred safely.
2. Act on the classification:
   - **Simple**: tighten the wording and return the improved prompt.
   - **Rough**: ask for the missing detail that changes the result most.
   - **Ambiguous**: name the competing interpretations, recommend one, then ask.
   - **Unclear**: ask for the goal before rewriting.
3. Audit the prompt across these axes:
   - **Objective**: what outcome should the agent produce?
   - **Context**: what background, files, audience, constraints, or examples matter?
   - **Scope**: what is included, excluded, and deferred?
   - **Output**: format, length, tone, language, artifacts, and acceptance criteria.
   - **Process**: whether the agent should ask first, research, plan, implement, verify, or stop.
   - **Risk**: irreversible actions, sensitive data, external calls, cost, credentials, or ambiguity.
4. Separate blockers from improvements:
   - **Blocker**: missing information that would change the task, output, or safety boundary.
   - **Improvement**: detail that would polish the result but is not required to proceed.
5. Ask one question at a time until blockers are resolved.
6. For each question, provide a recommended answer the user can accept or edit.
7. If the answer can be discovered from the codebase, files, conversation, or provided references, inspect those instead of asking.
8. Rewrite the prompt after blockers are resolved, preserving the user's intent.
9. Provide the final prompt plus a short change note explaining what was clarified.

## Question Rules

- Ask the highest-impact unresolved question first.
- Do not ask about preferences that do not change the final prompt.
- Do not bundle unrelated questions together.
- If the user asks for speed, make reasonable assumptions and label them clearly in the final prompt.
- If the prompt is already good, say so and offer only targeted improvements.

## Output Rules

- Do not return a long critique when the user needs a usable prompt.
- Keep the final prompt copy-pasteable.
- Preserve requested language, tone, and domain vocabulary unless they weaken clarity.
- Include assumptions only when they materially affect execution.
- If the prompt controls an agent, include when the agent should ask before acting.

## Final Prompt Shape

Use this structure when it fits the task:

```md
Role: [who the agent should act as]
Goal: [specific outcome]
Context: [relevant background and inputs]
Task: [ordered work to perform]
Constraints: [must / must not rules]
Output: [format, tone, language, length, files]
Verification: [how completion should be checked]
Ask first if: [conditions that require clarification]
```

For short prompts, collapse this into one concise paragraph.

## Quality Bar

A perfect prompt is:

- Clear enough that two capable agents would produce similar results.
- Specific about output and success criteria.
- Explicit about constraints and non-goals.
- Honest about uncertainty and missing information.
- Short enough to use, but complete enough to prevent avoidable rework.
