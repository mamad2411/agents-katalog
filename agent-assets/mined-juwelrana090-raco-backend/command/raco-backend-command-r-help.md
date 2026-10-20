> ⚠️ PROJECT SCOPED: Read from .claude/commands/ only.

Read .claude/commands/system/ and .claude/commands/custom/ and display all commands.

## System Commands (12)

| Command              | Description                                                      |
| -------------------- | ---------------------------------------------------------------- |
| /r-start             | Load session — skills cache first, then full memory              |
| /r-end               | End session — EOD summary + save                                 |
| /r-task [desc]       | Execute a task with full cache-first context                     |
| /r-plan [feature]    | Plan a feature before writing any code                           |
| /r-fix [desc]        | Diagnose and fix — cache-first gotcha check                      |
| /r-todo              | List tasks / /r-todo add [desc] to add / pick from list to start |
| /r-done              | Mark task done + auto quality review                             |
| /r-find [thing]      | Location + blast radius in one pass                              |
| /r-log [type] [desc] | Log a decision / gotcha / pattern                                |
| /r-memory [scan      | update                                                           | status]                 | Memory maintenance |
| /r-cache [warm       | status]                                                          | Skill cache maintenance |
| /r-tokens            | Token usage meter                                                |

## Custom Commands

[list any found in .claude/commands/custom/]
[if empty: No custom commands yet — see .claude/commands/custom/README.md]
