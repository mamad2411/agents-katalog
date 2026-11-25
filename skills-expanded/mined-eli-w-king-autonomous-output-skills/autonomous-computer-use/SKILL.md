---
name: autonomous-computer-use
description: "Computer Use (AI-First edition): safe, app-targeted desktop automation on a Mac or Windows laptop, in the background, without taking over your mouse or keyboard. The first test is a short joke in a new note in Notes (Mac) or in Notepad (Windows). It never sends or buys anything. Use for 'open Notes', 'write it in Notepad', 'use Computer Use', 'do it in the app'."
---

# Computer Use (AI-First edition)

Use desktop apps for the person without taking over their laptop: they keep working while it runs.

## Before the first use

- The setting `"chat.agentHost.computerUse.enabled": true` is on (the workshop settings have it), and VS Code
  Insiders was restarted after.
- If the Computer Use tools aren't in this chat, look them up once with tool search. If they're still missing,
  ask the person to type `/computer on` in the chat.
- **Mac, once:** System Settings > Privacy & Security > **Accessibility**, and > **Screen & System Audio
  Recording**: turn on Copilot Computer Use. If it still reports a missing permission, turn on Visual Studio Code -
  Insiders in both too. Then quit and reopen VS Code Insiders. Nothing else: never ask for Full Disk Access, Input
  Monitoring, Contacts, the camera or the microphone.
- **Windows:** nothing to grant.

## The first test

- **Mac:** "Use Computer Use to write a short joke in a new note in Notes." Open Notes in the background, make a
  new note, type the joke, and read it back from the note.
- **Windows:** "Use Computer Use to write a short joke in a new note in Notepad." Open Notepad, open a new tab, type
  the joke, and read it back. Don't save unless asked.
- Say what you wrote and where. Keep it short and kind.

## How to act

1. **Least intrusive route first.** Files, folders and links: use files, the shell or the browser, not Computer
   Use. Websites: the integrated browser. Native apps: Computer Use.
2. **App-targeted only.** Every read, click and keystroke names the app (and the window). Never bring an app to
   the front, move the real pointer, type into whatever has focus, or use AppleScript or system-wide shortcuts.
3. **Read before you act.** Get the window's state, confirm it's the right window and document, act on the latest
   element ids, and read again after anything changes.
4. **Use the text action the field offers** (set the value, patch rich text, or type into a focused field). If it
   refuses, read again once, then stop and say what's blocked.
5. **Check the result in the app's state,** not from the click.
6. **Unsure if it happened? Never repeat it.** Read the app first; it may already be done.
7. **Share the machine.** If the person's typing interrupts an action, read again and retry once, then move on
   and come back to it.

## Never send or buy

Never send a message, email or post, submit a form, sign up, accept terms, or pay for anything. Draft it, leave it
unsent, and tell the person exactly what's there and which button they'd press. Never type passwords or codes.
