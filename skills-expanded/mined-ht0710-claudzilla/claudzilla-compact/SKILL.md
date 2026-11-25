---
name: claudzilla-compact
description: Draft a /compact line (or /clear) from this session and put it in the user's prompt box.
disable-model-invocation: true
---

# Draft a compact

Draft what a `/compact` must keep from this session, then hand it to the `compact_draft` tool. It is deferred: load it with ToolSearch `select:mcp__primer__compact_draft` first.

- **Keep:** only what exists nowhere but this conversation: decisions and why, preferences stated, open items, branch or uncommitted state, exact errors under debug; anything in a file → its path.
- Keep at most about 1500 characters. Settled decisions that don't fit go in the notes file the conversation already names, appended; if none is named, create `decisions.md` in the scratchpad. Keep only its path.
- **Drop:** finished detail, lists of scratch files, line references.
- Skip CLAUDE.md, rules and memory: they reload after compact.
- Facts from this session, not guesses.
- Next step needs nothing from this session → `clear: true` instead (free; `/compact` re-reads the whole conversation).

Call `compact_draft` once, with `{keep, drop}` or `{clear: true}`. Plain text, no markdown. Then reply in one line: the draft is in the prompt box; check it, then press Enter.
