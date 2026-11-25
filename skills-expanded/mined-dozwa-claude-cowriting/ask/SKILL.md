---
name: ask
description: Ask one persona a question directly.
argument-hint: "<persona> <question>"
disable-model-invocation: true
---

The first word of `$ARGUMENTS` names a persona of the paper's review party as the author typed it: its id, with or without the `cowrite:` prefix (the plugin has checked that it exists). The rest is the author's question.

Use the `cowrite:<persona>` agent to answer it. It may read the author's text, notes and `party.md`. Relay its answer as given, without rewritten text.
