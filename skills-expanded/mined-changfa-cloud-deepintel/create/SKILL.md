---
name: create-skill
description: Create or update a standard reusable Skill. Use when the user asks to create, save, record, or update a Skill or procedural memory, or when a completed workflow should be preserved for future reuse.
---

# Create a Skill

Create a concise `SKILL.md` that another Agent can use without the original conversation.

## Workflow

1. Identify the reusable goal, trigger phrases, required inputs, ordered steps, and expected result.
2. Choose a short name under 64 characters using lowercase letters, digits, and hyphens. Prefer an action-oriented name.
3. Write a description that states both what the Skill does and when it should trigger. Put trigger guidance in the description because it is always visible to the Agent.
4. Write only instructions that are useful and non-obvious. Assume the Agent already understands general reasoning and common tools.
5. Match detail to risk: allow flexibility for judgment-heavy work and use exact steps for fragile operations.
6. Call `create_user_skill` with the name, description, and complete Markdown instructions.
7. Report the saved `/user-skills/<name>/SKILL.md` path.

## Required Shape

The `create_user_skill` tool creates the frontmatter. Supply a body with clear imperative steps, important constraints, and a short example only when it materially clarifies the workflow.

Keep the Skill self-contained and concise. Do not create README, changelog, installation guide, or other auxiliary documentation. Do not copy transient conversation details, secrets, or one-off task state into the Skill.

If the requested process is not yet clear enough to reuse, ask only for the missing information that changes the workflow. If the user explicitly provides a complete process, create the Skill directly.
