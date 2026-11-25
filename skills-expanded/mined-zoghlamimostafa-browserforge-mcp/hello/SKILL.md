---
name: hello-skill
description: Example skill: greet people and keep a note, using the hello plugin.
requires-plugins: hello
---
# Hello skill

When the user asks you to greet someone and remember it:

1. Call `hello_greet` with the person's name.
2. Call `hello_note_add` with a one-line note such as "Greeted <name>".
3. Tell the user what you did.

You can also run the ready-made workflow `greet-and-note` with `skill_run_workflow`.
