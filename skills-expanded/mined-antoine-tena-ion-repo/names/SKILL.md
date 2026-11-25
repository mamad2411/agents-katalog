---
name: names
description: Choose the names above the chat's messages - the person's, their Claude's, a task's or another session's - by default their git name, Claude and each one's own. Use when the user wants another name for themselves, Claude or a gray message in the chat, or from `/repo:look`.
argument-hint: "[the person's name] [Claude's name]"
---

Talk to the user in their language; nothing outside `~/.claude/` is touched.

The mod `chat.tsx` writes the person's name above their messages and Claude's above its replies.
It reads them from `~/.claude/chat-names.json` (`{"person": "...", "claude": "...", "others":
{"task-notification": "..."}}`, each key optional); a missing or empty key falls back to the real
name: `git config user.name` for the person, `Claude` for Claude, and for a message that came from
elsewhere (gray bar) the name it shows by itself (`task-notification`, a session's name…), the key
of `others`.

1. Read `~/.claude/chat-names.json` (absent: `{}`) and `git config user.name`.
2. With `$ARGUMENTS`, the first word is the person's name, the rest Claude's: go to 3. Otherwise
   ask both with the AskUserQuestion tool, in one call, two questions:
   - how the person wants to be called: their real name first, as `<git name> (Recommended)`,
     then the first name it holds when it differs (`antoine-tena` gives `Antoine`), then the
     current choice if it is another one. "Other" takes any name typed.
   - how their Claude should be called: `Claude (Recommended)` first, then the current choice if
     it is another one. "Other" takes any name typed.
   Only when the user asks for it, or names a gray message: ask, per name it shows by itself, the
   name it takes, its own name first as `<name> (Recommended)`. Without `$ARGUMENTS` in that case,
   ask that alone.
3. Write `~/.claude/chat-names.json` (`python3 -I` with `json`, indent 2, `ensure_ascii=False`): a
   real name chosen is left out of the file, so a later change of `git config user.name` follows;
   a gray message given back its own name leaves `others`, empty `others` removed.
   No key left: remove the file. When `chezmoi source-path ~/.claude/chat-names.json` answers,
   `chezmoi re-add` it and say chezmoi's repo has it to commit.
4. The mod reads the names again within ten seconds: the next message shows them. Ask whether
   they suit; if not, back to 2.
