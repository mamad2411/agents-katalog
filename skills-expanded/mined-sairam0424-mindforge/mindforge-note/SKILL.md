---
name: "mindforge-note"
description: "Zero-friction idea capture. Append, list, or promote notes to todos."
---

<objective>
Zero-friction idea capture — one Write call, one confirmation line.

Three subcommands:
- **append** (default): Save a timestamped note file. No questions, no formatting.
- **list**: Show all notes from project and global scopes.
- **promote**: Convert a note into a structured todo.

Runs inline — no Task, no AskUserQuestion, no Bash.
</objective>

<execution_context>
@.agent/workflows/mindforge-note.md
@docs/References/ui-brand.md
</execution_context>

<context>
$ARGUMENTS
</context>

<process>
Execute the note workflow from @.agent/workflows/mindforge-note.md end-to-end.
Capture the note, list notes, or promote to todo — depending on arguments.
</process>
