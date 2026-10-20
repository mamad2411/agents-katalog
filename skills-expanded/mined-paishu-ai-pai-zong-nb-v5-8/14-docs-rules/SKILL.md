---
name: docs-rules
description: Create and maintain README files, API docs, usage docs, comments, AGENTS.md, .ai_project.md, prompt rules, skill files, and project conventions. Use for documentation, workflow rules, prompt engineering, knowledge distillation into skills, and Codex behavior refinement.
---

# Docs And Rules

## Workflow

1. Identify the reader: user, developer, operator, reviewer, or future Codex agent.
2. Identify the document job: onboarding, reference, decision, procedure, troubleshooting, or skill.
3. Keep docs task-oriented and short.
4. Include prerequisites, commands, expected output, and common failure points when useful.
5. Separate MUST, SHOULD, and MAY when priority matters.
6. Validate examples against actual files and commands when possible.

## Knowledge Distillation

When converting knowledge into docs or skills:
- Extract reusable procedures, not background prose.
- Capture triggers, inputs, workflow, checks, avoid rules, and output contract.
- Move long examples or references out of the core prompt/skill when they are not always needed.
- Do not paste large external text verbatim.
- Preserve source and license awareness.

## Comments

- Explain why complex code exists, not what each line does.
- Document public interfaces, non-obvious constraints, and operational hazards.
- Avoid stale comments by keeping them close to the code they explain.

## Prompt And Skill Rules

- Prefer concise, testable instructions.
- Make triggers explicit in `description`.
- Keep main prompts focused on priorities and routing.
- Move domain details into skills.
- Merge or prune skills that overlap too much.

## Output

State what changed, where, why it matters, and how it should be used.
