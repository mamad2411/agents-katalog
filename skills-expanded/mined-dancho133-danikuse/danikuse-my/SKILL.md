---
name: danikuse-my
description: Work in the user's own Brave browser. Use when the user invokes /danikuse-my or asks to do something in "my browser", "my Brave", where they are already logged in, or to fill something in for them personally. This surface is always visible and never headless.
---

# /danikuse-my — the user's Brave

CLI: `danikuse my <verb>`. Bridge verbs first (Danikuse Bridge extension in the user's Brave, no CDP, no restart): `tabs` (list his tabs), `open <url>` (opens an inactive tab, no focus steal), `eval` (returns page title, URL, and text of the active page), `windows` (titles only, works without the extension). CDP verbs (`snapshot`, `fill`, `click`, `screenshot`, `close`) only when the bridge is unavailable and the task truly needs them. Every result is one JSON object; act on `status` and `next`, never claim success without `ok`.

1. Never create a new tab when a suitable tab is already open: claim it and navigate it (`danikuse my goto <url> [match]`). Creating tabs without asking is forbidden. `open` (new inactive tab) is only for when no suitable tab exists.
2. Personal Brave steals screen focus: navigation jumps the user's screen. If the task needs no user login, stop and offer the agent browser instead — do not touch Personal Brave. Only proceed here when the task truly needs the user's session. Then announce "using your Brave" before the first action.
2. If the JSON says `personal-brave-cdp-unavailable`, follow its `next` exactly: Brave gets a localhost CDP port for this task only. Never leave the port open after the task.
3. Fill drafts freely; submit, pay, publish, delete, password or access changes always wait for the user's word, in every mode. No `--hide` on this surface: the user's browser is always visible.
4. Done when the final JSON is `ok` and the run folder holds the evidence asked for.
