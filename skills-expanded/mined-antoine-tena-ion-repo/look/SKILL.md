---
name: look
description: Change the look of the chat and the status line in one form - the person's color, their name, their Claude's, the status line's colors - each kept by default. Use when the user wants to customize the chat or the status line, or says yes to the look question at session start.
---

Talk to the user in their language; nothing outside `~/.claude/` and ion-repo's machine settings
is touched.

Each part has its own skill, which holds how it is done: `/repo:color` (the bar beside their
messages), `/repo:names` (the names above the messages), `/repo:statusline` (the status line's
style and palette). This one asks all of them at once.

1. Read the current state as those skills do: the theme and its `professionalBlue`
   (`/repo:color` step 1), `~/.claude/chat-names.json` and `git config user.name`
   (`/repo:names` step 1), `cd ~ && ion repo set` (`/repo:statusline` step 1).
2. One AskUserQuestion call, four questions, each with "Keep <current>" first:
   - their color: keep, then three colors of `/repo:color`'s palette that stand apart;
   - their name: keep, then their git name if it is not the current one, then the first name
     it holds (`antoine-tena` gives `Antoine`);
   - Claude's name: keep, then `Claude` if it is not the current one;
   - the status line's colors: keep, then `chat` (their color and Claude's, following any
     change of their color) if it is not the current one, then a one-hue palette of
     `/repo:statusline` (`blue`, `pink`…). Its style is changed through "Other" or
     `/repo:statusline`.
   Any name, color or palette typed in "Other" is taken.
3. Apply only what changed, each by its skill's own steps (`/repo:color` step 3,
   `/repo:names` step 3, `/repo:statusline` step 4). An answer that asks for more choices ("other
   colors", "show me the styles") runs that skill with what is known so far.
4. `python3 "${CLAUDE_PLUGIN_ROOT}/hooks/reminders.py" yes look`: the start question comes back
   only when this skill offers something new.
5. Say in one line what changed and where it shows: the bar at once, the names and the status
   line within ten seconds.
