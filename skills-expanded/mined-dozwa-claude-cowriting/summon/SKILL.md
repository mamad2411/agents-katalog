---
name: summon
description: Ask one persona of the review party for a review.
argument-hint: "<persona> [file or section]"
disable-model-invocation: true
---

The first word of `$ARGUMENTS` names a persona of the paper's review party as the author typed it: its id, with or without the `cowrite:` prefix (the plugin has checked that it exists; `/cowrite:party` lists them). The rest names the file or section to review; empty, it is the section the author is working on (ask which, if unclear).

Use the `cowrite:<persona>` agent to review it. Relay its hints and questions as given, without rewritten text.
