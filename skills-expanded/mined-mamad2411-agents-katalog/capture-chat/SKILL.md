---
name: capture-chat
description: Export and capture chat sessions (Claude Code, Codex, Cowork) as portable markdown for archiving or ingest. Use when the user says "export this conversation", "capture this chat", "save this session", "export with artifacts", "save the conversation to my vault", "capture conversation", "export conversation", or any request to preserve a session as a file. Two modes — capture (conversation markdown only) and export (conversation + artifacts). Default destination is the cross-harness .aai session archive; redirectable to a vault inbox or any path.
---

Read `instructions.md` in this skill's directory and follow it.

Path note: this skill also ships inside the `ambient` library plugin, so its
instructions may reference files as `${CLAUDE_PLUGIN_ROOT}/library/capture-chat/<file>`.
When installed standalone, resolve those to `<file>` in this directory.
