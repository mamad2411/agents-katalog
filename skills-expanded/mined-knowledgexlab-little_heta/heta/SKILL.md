---
name: heta
description: Search and recall the user's own documents, files, and saved memory — and save new things worth remembering — using Little Heta, a local CLI knowledge base. Use whenever a task needs external knowledge from the user's own materials or earlier context, or when the user states a fact, decision, or preference worth keeping, instead of guessing or grepping files.
---

# Little Heta

`heta` is a local command-line knowledge base. It indexes the user's
documents — PDF, Office, images, audio, code, Markdown — answers questions
from them and from saved memory, and can store new memories.

Reach for `heta` whenever a task needs **external knowledge** from the user's
own documents, or needs to **recall or save memory** — instead of guessing or
grepping. Run commands with the Bash tool.

## 1. Check Heta is set up

Run `heta status` once at the start.

- Shows a model provider and KB files → Heta is ready, continue.
- Shows config missing / "not configured" → tell the user to run `heta init`
  themselves. It is an interactive API-key setup, so do **not** run it yourself.

## 2. Four core commands

These four cover retrieval and memory. **Default to `heta ask`.**

| Command | When to use it |
|---------|----------------|
| `heta ask "<question>"`   | **Default.** Answers from saved memory and indexed documents together. |
| `heta query "<question>"` | When the answer must come strictly from indexed documents. |
| `heta recall "<query>"`   | When you want the user's personal memory (past chats, facts), not documents. |
| `heta remember "<text>"`  | When the user states a fact, decision, or preference worth keeping for later. |

Examples:

```bash
heta ask "How does our auth flow refresh tokens?"
heta query "What does the design doc say about rate limits?"
heta recall "what did I decide about the database"
heta remember "We decided to use Postgres for the main store."
```

Show the user Heta's output, then add a short summary.

## 3. Other commands

Heta can also index files (`heta insert`), clean up, and toggle settings.

- For a quick list: run `heta --help`.
- For full usage of any command: read `COMMANDS.md` in this skill's directory
  (next to this file). Only read it when the user actually needs one of those
  commands — do not load it ahead of time.
