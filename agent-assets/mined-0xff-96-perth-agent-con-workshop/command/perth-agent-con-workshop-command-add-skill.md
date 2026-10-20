---
description: Scaffold a new Claude Code slash command (skill) in .claude/commands/
argument-hint: <skill-name> <what it should do>
allowed-tools: Read, Write
---
Arguments: `$ARGUMENTS`
Treat the **first token** as the skill name and **the rest** as what it should do.
If no arguments were given, ask me for them.

Create a new slash command, following the existing commands' shape.

Steps:
1. Read `.claude/commands/verify.md` and `.claude/commands/run.md` to match the
   frontmatter (`description`, optional `allowed-tools`) and body style.
2. Create `.claude/commands/<skill-name>.md` with a clear `description` and a body
   that tells the agent exactly what to do, in numbered steps.
3. Tell me to start a new Claude Code session (or that it's available now) and that
   the command will appear in the `/` menu as `/<skill-name>`.

Keep it focused. Do not commit unless I ask.
