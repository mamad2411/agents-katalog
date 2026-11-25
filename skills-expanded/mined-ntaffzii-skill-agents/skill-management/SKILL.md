---
name: skill-management
description: "Manage a skill repository: create, classify, improve, deprecate, or reorganize agent skills with clean buckets, clear SKILL.md metadata, progressive disclosure, and installable structure. Use when the user asks to make skills, organize skills, compare skill quality, or maintain a skills repo."
---

# Skill Management

Use this skill to keep a skills repository clean and usable.

## Repository Model

- `skills/` contains individual capabilities.
- `workflows/` contains ordered playbooks that combine skills.
- `mcp-tools/` contains executable actions exposed through MCP.
- `data/workflows.json` indexes workflows for browsing and automation.
- `data/tools.json` indexes tool groups and their skill/workflow relationships.

## Bucket Model

- `engineering/` - daily code work
- `productivity/` - non-code workflows
- `obsidian/` - Obsidian-specific work
- `misc/` - useful but infrequent
- `personal/` - tied to one user's setup
- `in-progress/` - drafts
- `deprecated/` - retired skills

## Workflow Creation

Create a workflow when a job needs multiple skills in a repeatable order.

Each workflow should include:

- Goal
- When to use
- Skills
- Steps
- Verification
- Output

Also add or update the matching entry in `data/workflows.json` with:

- `id`
- `title`
- `description`
- `path`
- `recommendedSkills`
- `steps`

## Skill Creation Workflow

1. Define the job
   - What task does this skill make repeatable?
   - What trigger should load it?
   - What should the agent do differently after loading it?

2. Write metadata
   - `name` must be lowercase and hyphenated.
   - `description` must include task, trigger, and use cases.

3. Write the body
   - Keep it procedural.
   - Prefer workflow steps and rules.
   - Add output format only when consistency matters.

4. Add references only when needed
   - Put long syntax tables, examples, or domain docs in `references/`.
   - Keep references one level deep from `SKILL.md`.

5. Classify status
   - Shippable skills go into a domain bucket.
   - Drafts go into `in-progress/`.
   - Old skills go into `deprecated/` with a short reason in the file.

## Bucket Status Skills

The status buckets also contain their own operating skills:

- `in-progress` - prototype and promote draft skills.
- `personal` - keep user-specific instructions private and scoped.
- `deprecated` - retire stale skills with replacement guidance.

## Rules

- Keep stable skills in domain buckets, not status buckets.
- Do not promote draft skills until trigger behavior and workflow are clear.
- Do not mix personal setup details into public skills.
- Update workflow and tool registries when skill relationships change.

## Quality Checklist

- The skill has exactly one main job.
- The description makes triggering obvious.
- The workflow has a verification step.
- The instructions are not generic advice.
- The skill is small enough to read quickly.
- Related files are discoverable from `SKILL.md`.

## Output Format

End with:

- Skills created or changed
- Bucket classification
- Workflow or registry updates
- Validation result
- Remaining cleanup
