---
name: skill-creator
description: Create, validate, store, update, or convert instructions and documentation into Mocu Agent Skills. Use when the user requests a new or modified skill or a complete SKILL.md file.
---

# Mocu Skill Creator

Create focused, executable Agent Skills that follow the Agent Skills open format.

## Storage

Store every skill only at:

```text
<BaseDirectory.AppData>/com.mocu.app/skills/<skill-name>/SKILL.md
```

Resolve `<BaseDirectory.AppData>` from Mocu's runtime context. If the resolved path already ends with `com.mocu.app`, do not append it again.

Never store skills in project-local or custom locations, including `.mocu/skills`. Never replace `com.mocu.app` with `Mocu` or another name. If the user requests another location, explain that Mocu skills are global and use the global path.

Keep all supporting files inside the same skill directory.

## Required Format

Every `SKILL.md` must start on its first line with:

```md
---
name: skill-name
description: Explain what the skill does and when it should activate.
---

# Skill Instructions

Write concise, ordered, and actionable instructions.
```

The skill name must:

- Use only lowercase English letters, numbers, and hyphens.
- Be short and descriptive.
- Contain no spaces, underscores, path separators, or `..`.
- Match its directory name exactly.

The description must clearly state the capability and activation conditions.

## Workflow

1. Identify the requested task, activation conditions, required inputs, expected output, tools, and important limitations.
2. Ask only for essential missing information.
3. Choose or preserve a valid skill name.
4. Write concise instructions in execution order.
5. Include validation, error handling, commands, or supporting files only when needed.
6. Never invent tools, APIs, commands, files, or capabilities unless the user explicitly requested.
7. Resolve and validate the global destination.
8. Check existing files before writing. Ask for confirmation before overwriting a skill unless the user explicitly requested its update.
9. Save `SKILL.md` and any required resources inside the skill directory.
10. Verify written files before reporting success.

For updates, read the existing global skill first, preserve useful content, and modify only what the request requires. Do not modify or delete copies found outside the global directory.

## Validation

Before returning or saving a skill, confirm that:

- The destination is under `com.mocu.app/skills`.
- `com.mocu.app` is not duplicated.
- The skill cannot escape the global skills directory.
- The directory name matches the frontmatter `name`.
- The file is named exactly `SKILL.md`.
- Frontmatter contains valid `name` and `description` fields.
- Instructions are complete, actionable, safe, and concise.
- Every referenced supporting file exists inside the skill directory.
- No secrets, unsupported functionality, or unrelated content are included.

## Output

If asked only for `SKILL.md`, return the complete file beginning directly with `---`, without commentary or a surrounding code fence.

If asked for a complete skill package, return the global target path, directory tree, and complete contents of every file.

If asked to save the skill, write it globally and report success only after verifying the files. If writing fails, report the path and error without claiming success.