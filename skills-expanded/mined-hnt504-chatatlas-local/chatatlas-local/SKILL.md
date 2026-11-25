---
name: chatatlas-local
description: Search and read the user's saved ChatGPT, Claude and other AI chats, kept on their own computer by ChatAtlas Local. Use when the user mentions an earlier conversation ("what did ChatGPT tell me about…", "that chat where I planned…", "find where I decided…"), wants to compare what different AIs said, or wants to pick up past work from another assistant.
---

# Your saved chats (ChatAtlas Local)

The user keeps their AI conversations in a local archive, imported from ChatGPT's and Claude's data
exports. Read it with the `chatatlas-local` command. Everything stays on their computer.

If the `chatatlas` MCP tools are connected (search_chats, read_chat…), use those instead; they do the
same thing.

## Find, then read

1. Search for the words the user would have used. Every word must be in the chat; each word also
   finds longer words it starts ("plan" finds "planning"), and accents don't matter.

   ```sh
   chatatlas-local search sourdough starter --limit 10
   chatatlas-local search budget --platform claude --since 2026-01
   ```

   Each result shows the chat's id (like `chatgpt:6720ab…` or `claude:3f1b…`) and the message where
   the words appear. If nothing comes back, try fewer or different words before saying it isn't there.

2. Read the chat that matters before answering from it:

   ```sh
   chatatlas-local show chatgpt:6720ab --md
   ```

   The start of an id is enough. `--from 40` starts at message 40 in a long chat.

Other ways in:

```sh
chatatlas-local list --platform chatgpt --since 2026-08 --limit 30   # newest first
chatatlas-local list --title "garden"                                 # words in the title
chatatlas-local topics --days 60                                      # what they talked about lately
chatatlas-local stats                                                 # what the archive holds
```

Add `--json` to `search`, `list`, `show` and `stats` for data you can read without the formatting.

## When you answer

- Say which platform and date the information came from ("in a ChatGPT chat from March 2026…").
- Quote the user's own words when it's a decision they made, rather than paraphrasing it.
- The archive only knows what was in the exports they imported, so the newest chats may be missing.
  If something should be there and isn't, suggest a fresh export:
  `chatatlas-local import ~/Downloads/<new export>.zip` (re-importing only adds and updates).

## Don't

- Don't run `forget`, or `tag`, unless the user asks you to. Reading is always fine.
- Don't paste whole conversations back at the user; summarize and quote the parts that matter.
