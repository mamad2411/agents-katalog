---
name: prompt-improvement
description: Improve vague, incomplete, ambiguous, risky, or poorly structured prompts into clear executable prompts for AI agents, coding assistants, automations, reports, research, or model-specific workflows. Use when the user asks to rewrite, clarify, optimize, score, translate, structure, or improve a prompt.
---

# Prompt Improvement

Turn rough intent into a clear prompt without changing what the user asked for.

## Core Principle

Preserve explicit intent. Add assumptions only when labeled.

## Workflow

1. Classify the problem
   - Identify whether the prompt is vague, ambiguous, overbroad, missing inputs, missing output format, missing audience, risky, or already good enough.

2. Extract intent
   - Separate explicit requirements, inferred goals, missing information, assumptions, constraints, and risks.
   - Do not invent requirements.

3. Decide whether to ask or rewrite
   - Ask 1 to 3 concise questions only when missing information changes the correct outcome.
   - Proceed with assumptions for low-risk drafting, brainstorming, research, reports, templates, and clear-enough tasks.

4. Rewrite
   - Make the task executable.
   - Add context, requirements, process, output format, quality rules, and language guidance only when useful.
   - Keep identifiers, file paths, commands, schema keys, model IDs, and API names unchanged.

5. Check fidelity
   - Confirm the rewrite preserves the user's request.
   - Remove hidden goals.
   - Mark assumptions and open questions clearly.

## Default Output

```markdown
## Improved Prompt

```text
[Prompt ready to use]
```

## What Changed

## Assumptions

## Questions
```

## Reusable Prompt Skeleton

```text
Role:

Task:

Context:

Requirements:

Process:

Output Format:

Quality Rules:

Language And Tone:
```

## Rules

- Respond in the user's language.
- Keep reusable model-facing prompt text in English when it improves portability.
- Do not make prompts longer unless the added structure improves execution.
- Do not remove explicit constraints.
- Do not convert uncertainty into fact.
