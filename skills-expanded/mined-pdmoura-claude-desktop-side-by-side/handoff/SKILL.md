---
name: handoff
description: Hand the current Claude Code conversation to another Claude account, from the desktop app or any claude-<name> CLI, so it shows on that account's desktop sidebar and in its CLI /resume list with its full history, and back again; or, with "refresh", sync the current account's desktop and CLI copies; or, with "orgs", show the account's chats in the sidebar of all its organizations (same email, personal plan and team plan). Use for "/handoff Fullpond", "/handoff refresh", "/handoff orgs", "/handoff orgs this", "/handoff ssh", "move this conversation to my Cascade account", "hand this back to Pando", "continue this in the other account", "sync this with my CLI", "my chats don't show in my team account", "show this conversation in my team organization".
---

# Hand this conversation to another account

The user runs several Claude accounts side by side: desktop windows (the main "Claude" window and
claude-profile.ps1 windows such as "Claude (FullPond)") and CLI commands (`claude-fullpond`,
`claude-pando`, ...). Desktop windows read conversations from `%USERPROFILE%\.claude`; each CLI
account reads its own `%USERPROFILE%\.claude-<name>`. `claude-handoff.ps1` finds the most complete
copy of this conversation, copies it where the target account will look, and adds it to that
account's desktop sidebar. It works in every direction.

1. **Target.** Use the argument: a window name (`FullPond`, `Cascade`), an account folder name
   (`Fullpond`, `Pando`), `Desktop` for the main window's account, or an email. `refresh` (or `sync`)
   means the account this session is signed in to: it brings that account's desktop windows and CLI to
   the same copy, so the user can switch between them. If no argument was given, run the script with
   `-List`, show the user the names, and ask which one. Every handoff also refreshes the account it runs
   in, so both sides end up with the same copy.

2. **Run it** from the session's working directory. It finds this conversation by itself (from
   `CLAUDE_CODE_SESSION_ID`), so don't pass `-Session` unless the user names another conversation.
   - PowerShell tool:
     `powershell -NoProfile -ExecutionPolicy Bypass -File "$env:LOCALAPPDATA\ClaudeProfiles\claude-handoff.ps1" -To <target> -Path "<working directory>"`
   - Bash tool (Git Bash):
     `powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$LOCALAPPDATA/ClaudeProfiles/claude-handoff.ps1" -To <target> -Path "$PWD"`

3. **Tell the user the result**: where it was copied, which sidebars got it, and the "Next" (or, for a
   refresh, "In sync") steps the script printed. After a refresh the user may keep going here; messages
   sent afterwards are only here until the next refresh. The rules that keep a round trip safe:
   - send no more messages to this conversation here after the handoff;
   - restart the desktop window they are going to if it is already open (quit it from the system tray,
     reopen it), or in a terminal run the account's command (`claude-<name>`) and `/resume` there;
   - desktop and each CLI keep separate copies, so hand off again whenever they switch between them.

4. **If it reports that the conversation was continued in more than one place** (exit code 2), show the
   user which copies have messages the others lack and ask which one to keep. Then run the same command
   with `-Prefer <that copy>`; the other copies are saved as `.diverged` files first.

5. **`orgs` is a different job.** The desktop app keeps a separate sidebar list per organization. So when
   the same email has two organizations (a personal plan and a team plan, say), chats started in one
   don't show in the other. Nothing needs copying: a local chat is the same file whichever organization is
   signed in, and an SSH chat stays on the remote machine. Run the script in place of `-To <target>` (no
   `-Path` needed) with:
   - `-Orgs` for `/handoff orgs`: every chat of this account, local and SSH, into the lists of all its
     organizations;
   - `-Orgs -Session this` for `/handoff orgs this`: only this conversation;
   - `-Ssh` for `/handoff ssh`: only the SSH chats.

   It works in both directions and never changes or removes an entry. Tell the user what it added and
   its "Next" steps: switch organization in the app, and restart the app if the chats aren't in the
   sidebar. Also tell them: use a chat in one organization at a time; a chat continued in the team
   organization is processed under that organization; archive rather than delete, because deleting a chat
   in one organization can delete it for the others; and run it again after starting new chats. This is
   for the desktop app only.

6. **Don't improvise.** Don't delete, archive or rename anything, and don't copy conversation files or
   write sidebar entries by hand. If the script stops with an error (for example that the app's files look
   different after an update), report it to the user as it is.
