---
name: automation-design
description: Design Codex automations, scheduled research jobs, recurring reports, reminders, monitors, thread follow-ups, and workspace jobs. Use when the user asks to set up, improve, schedule, template, audit, or design an automation, monitor, reminder, or recurring Markdown report.
---

# Automation Design

Design reliable automation prompts and schedules.

## Workflow

1. Identify automation type
   - Choose reminder, thread follow-up, daily or weekly report, monitoring task, research digest, or workspace job.

2. Capture requirements
   - Clarify task, schedule, timezone, output destination, source rules, language, failure behavior, and whether duplicates should be suppressed.
   - Ask only when missing details would change the created automation.

3. Write a self-contained prompt
   - Include goal, scope, sources or file boundaries, output format, quality rules, and missing-information behavior.
   - Keep schedule settings separate from task instructions.

4. Recommend schedule
   - Use human-readable schedule language unless a tool requires structured syntax.
   - State the timezone explicitly.

5. Confirm or create
   - When an automation tool is available and the user asked to create it, use the tool.
   - If schedule or destination is missing, ask before creation.

## Prompt Template

```text
Task:
[What Codex should do]

Scope:
[Topics, files, repos, sources, or boundaries]

Quality rules:
- Use reliable sources or concrete local files.
- Include links or file paths.
- State uncertainty clearly.
- Avoid duplicate or low-value items.

Output:
[Markdown report, thread reply, file path, etc.]

Language and tone:
[Thai/English, concise/detailed]
```

## Rules

- Prefer updating an existing automation over creating a duplicate.
- Use current-source tools for news, prices, laws, schedules, product releases, and other changing facts.
- Do not expose raw schedule syntax unless useful.
- Report what will happen, when it will happen, and where the result will appear.
