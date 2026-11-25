---
name: help
description: What Layerwright can do with Figma from here, the /layer commands, and whether Figma is connected right now. Use when the user asks what Layerwright or this plugin can do, how to start with it, or which /layer commands exist.
---

# Layerwright: what it does

0. If `figma_status` (below) returns `doFirst`, call that tool with exactly those arguments before anything else, and say in one line that you're watching the Layerwright window in Figma for their requests: it lets requests from the Figma window start this session by themselves.
1. Call `figma_status` with a `title` for this session (the task, in 2–4 words; "Layerwright tour" if there is none yet).
2. The language. If figma_status returns `language`, explain everything below in it. If it doesn't, ask the user which language they want Layerwright to explain things in (AskUserQuestion when you have it: the language they wrote in first, then English, Persian, and Other), save the answer with `layerwright_memory({ action: "language", language })`, and say in one line that every session will use it from now on (they can change it by asking). Keep commands, file names and layer names as they are.
3. Say in one line: connected or not, which file and page, what is selected, how many sessions share Figma.
   - Not connected: Figma desktop → Plugins → Development → Layerwright. Never imported? Run `npx layerwright init` once (or `npx layerwright plugin`): it prints the manifest's full path and how to import it in Figma on this computer.
4. Show the commands as a short table, descriptions in that language:

| Command | What it does |
|---|---|
| `/layer:connect` | Connect this session to Figma and keep it listening for requests from the Figma window |
| `/layer:import <file or folder>` | HTML or a Claude Design export → editable Figma layers (Auto Layout, your components) |
| `/layer:design <what>` | A new screen or flow in Figma, built with the file's Design System |
| `/layer:edit <change>` | Change an existing design: the selection, or a frame by name |
| `/layer:code [where]` | The selected Figma frame → code in this project, checked against the design |
| `/layer:check [frame]` | Compare code with Figma, or audit a design (spacing, contrast, tokens) |
| `/layer:components` | Turn the selection into a component, or a set with variants |
| `/layer:prototype` | Wire screens into a clickable prototype with transitions |
| `/layer:shot` | A picture of the selection, saved and shown to you |
| `/layer:skills` | The design, UX, UI and design-to-code skills sessions read before a job; add your own from a link, or write one (`/layer:skills new …`) |
| `/layer:inbox` | Do the requests sent from the Figma window (only needed when they don't start by themselves) |
| `/layer:update` | Update Layerwright when a newer version is out (the Figma plugin, these commands, the server) |
| `/layer:doctor` | Find out why Figma isn't connecting |
| `/layer:report` | Draft a GitHub issue about a Layerwright problem |

5. One line about the Figma window: in the Layerwright plugin they can select layers, pick this session and send a request ("Build this in code", "Polish this design", or their own words). Claude Code with this plugin starts on it by itself (this session is listening now); Codex gets it with its next Figma step, or with `/layer:inbox`. The window also has a compact mode (the button next to Star) that keeps just the selection, the actions and the chat box.
6. End with one suggestion that fits what is selected right now (a frame is selected → `/layer:code` or `/layer:check`; nothing → `/layer:design` or `/layer:import`).
