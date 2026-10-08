---
invoked_by: scripts/generate_artifacts.py — generate_skill_definition() via load_prompt("artifacts/generate_skill", ...)
variables:
  project: Project name
  skill_name: Skill name slug (e.g. "myproject-test")
  skill_purpose: One-line skill purpose from strategy
  skill_implementation: Implementation description from strategy
  skill_args: Argument specification string
  arch_summary: Architecture summary text (pre-truncated to 2000 chars)
  tech_summary: Tech stack summary text (pre-truncated to 2000 chars)
  patterns_summary: Patterns summary text (pre-truncated to 2000 chars)
  generation_timestamp: ISO-format timestamp of generation
  codebase_hash: Hash of the analyzed codebase
notes: >
  Placeholder-style text shown to the AI (e.g. {{Skill Display Name}}) uses {{ }} so
  that str.format() passes them through as literal { } for the AI to see and fill in.
---

# Skill Definition Generation

You are creating a skill definition for the **{project}** project.

## Skill to Create

**Name:** {skill_name}
**Purpose:** {skill_purpose}
**Implementation:** {skill_implementation}
**Args:** {skill_args}

## Project Context

**Architecture Summary:**
```markdown
{arch_summary}
```

**Tech Stack Summary:**
```markdown
{tech_summary}
```

**Patterns & Conventions:**
```markdown
{patterns_summary}
```

## Your Mission

Create a complete skill definition markdown file with YAML frontmatter.

**Output Path:** `.claude/skills/{skill_name}/SKILL.md`

Use this structure:

```markdown
---
name: {skill_name}
description: {skill_purpose}
user_invocable: true
args: {skill_args}
generated: true
generation_timestamp: {generation_timestamp}
generation_version: "2.0"
source_project: {project}
source_codebase_hash: {codebase_hash}
---

# {{Skill Display Name}}

Quick-reference skill for **{project}**.

## Usage

```bash
/{skill_name} {{args}}
```

## Purpose

{{Detailed purpose - BE SPECIFIC with project context}}

## Implementation

{{Actual commands/operations to perform - USE ACTUAL PROJECT FILES AND COMMANDS}}

For example:
- If this is a test skill, use the actual test framework command from TechStackSummary
- If this is an architecture skill, reference actual directories from ArchitectureSummary
- If this is a patterns skill, cite actual files from PatternsSummary

## Examples

{{Concrete usage examples with actual project context}}

---

*This skill was automatically generated.*
```

**CRITICAL: Output requirements**

Your entire text response MUST be ONLY the raw file content — starting with `---` (the YAML frontmatter opener), with no preamble, no explanation, and no summary before or after. The system saves your text output directly as the file if the Write tool call is not detected, so any conversational text will corrupt the artifact.

1. Use the Write tool to write the skill definition to `.claude/skills/{skill_name}/SKILL.md`
2. Also output the raw file content as your complete text response (no wrapping prose)
3. Use actual commands from the project (from TechStackSummary — test framework, build tools, etc.)
4. Reference actual files and directories from ArchitectureSummary
5. Do not use generic placeholders — be specific to THIS project
