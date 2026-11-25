---
name: guide
description: What Clouding Bar can do and how to set it up, in Cowork or in Claude Code. Use when the user asks about the Clouding Bar plugin — "I have the Clouding Bar plugin. Please walk me through what it can do.", how to install or set it up, or why Clouding Bar doesn't show a chat or a Cowork task.
---

# Walking someone through Clouding Bar

**First see where you are — never ask the user.** Run `uname -s; echo "$CLAUDE_CODE_ENTRYPOINT"`:

- `Linux` — Cowork, in its sandbox (`remote_cowork`: Cowork in the cloud, where the Mac is
  reached only through device tools such as `device_bash`). Follow **In Cowork**.
- `Darwin` — Claude Code on a Mac (the terminal, VS Code or Claude Desktop's Code tab). Follow
  **In Claude Code**.

Give only the steps for where you are: never the other place's, never "tell me where you are".
Then, in the user's language: two or three lines on what Clouding Bar does (not the whole list
below), and in the same reply get them set up — in Cowork, the download link and what to click,
right away. Don't run anything else or change other files.

## What it is

Clouding Bar is a Mac menu bar app (macOS 12 or later). This plugin is only its link to Claude:
it reports what each Claude Code chat is doing, and the app shows it — on the Touch Bar, in a floating pill
or in the notch — and lets you answer from there.

- Every chat with its own colour, its own Cloud and a short name: working, waiting for you, done.
- The 5-hour limit, the context window, the model, the subagents at work.
- Claude's permission requests and questions, answered from the bar or the pill without going
  back to the chat.
- A screenshot of an area of the screen, or a file dropped on the pill, goes straight into the
  chat; dictation too.
- A heads-up when another chat finishes; stats of how much you used.

## In Cowork

The Mac app does the work here; this plugin does nothing in Cowork. What's left happens on the Mac.

**Getting the app.** Unless they said it's on their Mac already (you can't see its Applications
from here), give them the link and what to click — in the same reply, without being asked.
Download nothing yourself and ask for no folder: Cowork's network doesn't reach GitHub (HTTP 403,
in the cloud and on the Mac alike), and the app can't be installed from Cowork (no macOS here).
Don't send them to GitHub's pages or to Claude Code, and don't mention `/reload-plugins` or
`/clouding-bar:install` — those are Claude Code's.

1. **The link**: <https://github.com/nikolanaidenko-eng/clouding-bar/releases/latest/download/Clouding-Bar.dmg>
   — a click on it downloads **Clouding-Bar.dmg** into Downloads.
2. **Tell them exactly what to click**, numbered, in their language — they may never have installed
   a Mac app:
   1. Finder → Downloads → double-click **Clouding-Bar.dmg**.
   2. In the window that opens, drag **Clouding Bar** onto **Applications**.
   3. Open Clouding Bar from Applications (or ⌘ Space, type "Clouding Bar", Return).
   4. It asks to connect to Claude Code: **Connect**. macOS then asks for Accessibility:
      **Open System Settings** and switch Clouding Bar on.
   Stop there. Seeing Cowork tasks takes the claude.ai sign-in, which is a risk: say so first
   (**Before the claude.ai sign-in**, below) and don't list it as a step to take.

**Before the claude.ai sign-in.** The app's claude.ai sign-in is optional and goes against
Anthropic's terms. Tell the user this, plainly and in their language, *before* you mention how to
sign in — in the same reply as the install steps, if Cowork tasks come up, and whenever they ask why a
Cowork task or a claude.ai chat isn't shown:

- Anthropic's terms don't allow third-party apps to collect or store claude.ai session keys, or to
  reach claude.ai automatically. Signing in could put their account at risk, including suspension.
  Anthropic hasn't approved Clouding Bar. It's their own risk.
- Without it everything else keeps working. What goes away: Cowork tasks, claude.ai chats, the
  account-wide limit, and sending to a Claude Desktop or Terminal chat through Remote Control without
  switching windows.

Don't recommend it, don't present it as a normal step and never sign in for them. Only if they say they
want Cowork tasks anyway: in the app, **Settings → General → Claude → claude.ai → Sign In…** — it
shows the same warning and waits for **I Understand**, then claude.ai's sign-in page; the window closes
by itself. Cowork tasks (and claude.ai and Claude Desktop chats) then show up in the chats list, with
the account-wide 5-hour limit. No plugin, no folder, nothing for you to write.

A question Cowork asks in Claude Desktop shows up on the Touch Bar and in the pill, and can be
answered there (Claude Desktop's window has to be on the current desktop) — this is read from the
window and needs no sign-in.

## In Claude Code

1. `/reload-plugins`, so the chat that's open reports too, then `/clouding-bar:install` — it gets
   the newest release from GitHub, checks it (Clouding Bar's Developer ID, notarized by Apple)
   and puts it in Applications.
2. When the app opens: **Connect** (it adds its status line — the 5-hour limit and the context —
   to `~/.claude/settings.json`, and in VS Code a small wrapper), then allow Accessibility.
3. Chats that were already open show up after `/reload-plugins` in them, or in a new chat.

## Good to know (only if they ask)

- No account, no analytics, no server of its own. The plugin itself uses no network, except
  `/clouding-bar:install` downloading the app from GitHub.
- The app checks GitHub for updates once a day (menu bar icon → Check for Updates).
- Everything else: <https://github.com/nikolanaidenko-eng/clouding-bar>.
