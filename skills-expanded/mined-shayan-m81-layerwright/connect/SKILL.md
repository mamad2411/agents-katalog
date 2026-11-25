---
name: connect
description: Connect this session to Figma and keep it listening for requests from the Layerwright window, so the user can send work from Figma and this session starts on it by itself. Use for /layer:connect, or when the user asks to connect, link or pair this session with Figma.
---

# Connect to Figma

1. `figma_status({ title, listen: true })`: the title is the task in 2–4 words ("Figma connection" if there is none yet).
2. It returns `doFirst`: call that tool with exactly those arguments (step 4 tells the user this session now listens), unless a Monitor with the description "Requests from the Layerwright window in Figma" already runs in this session (a second one exits at once anyway). When it expires, start it again. When it stops by itself (this session left Layerwright alone for 30 minutes and left Figma), leave it stopped: the next Figma call returns `doFirst` again. No `doFirst` (not Claude Code) → requests arrive with the next Figma step, or with `/layer:inbox`.
3. Not connected: say so in one line and how to open it: Figma desktop → Plugins → Development → Layerwright (never imported: run `npx layerwright plugin`, which prints the manifest's full path and the steps for this computer). The watcher keeps running, so the session still wakes up when the window opens and the user sends something. Still nothing after that → `/layer:doctor`.
4. Connected: one or two lines, in the user's language (`language` from figma_status, if it returns one): the file and page, what is selected, how many sessions share Figma, and that this session now listens. In the Layerwright window they select layers, pick this session ("<the title>") and send a request or their own words; it starts here by itself, and the answer appears in the window.
5. When a request arrives (the Monitor reports it), do it as `/layer:inbox` says: `figma_inbox`, `figma_reply` working, do it, `figma_reply` done with one line.
