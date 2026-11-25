---
name: review-desk
description: Optional. Open the Reel Studio desk (a local review app) and work from its review notes - notes pinned to frames, renders, approvals. Use only when the person asks for the desk or already uses it - "open the desk", "apply my desk notes", "fix what I marked", "what's on this frame" - or a production has a review.json. Never required: reviewing and approving in chat works the same.
---

# Review desk (optional)

The kit works the same without it: storyboards are approved in chat, and QA is the `make-video` steps. Start the
desk when the person asks, or they already use it (a `review.json` in the production). `make-video` offers it once,
when a storyboard is ready; don't push it beyond that.

The desk (`desk/`) is a local page for the person: it plays a production's composition frame-exact through the
renderer's own clock (`__seek`), and lets them pin notes to frames, render stills, preview videos and QA, read the
storyboard, approve, and send notes to a coding agent. It only reads and writes files in the project, so everything it does
reaches you as files (and, if it is registered, through the `reel-desk` MCP server).

## Open it

Open it for the person; don't hand them a command to run (many are not technical).

- **Claude desktop app** (a `preview_start` tool is available): `preview_start` with name `desk`. It starts the
  server from `.claude/launch.json` and shows the desk in the app's browser pane, next to the chat. `setup` writes
  that entry; if it is missing, add it: `{"name": "desk", "runtimeExecutable": "node", "runtimeArgs":
  ["desk/server.mjs", "--port", "4100"], "port": 4100}` under `configurations`.
- **Elsewhere** (terminal, Codex, Copilot): run `node desk/server.mjs` in the background and give the person
  <http://127.0.0.1:4100>. `npx reel-studio desk` does the same. Port: `--port <n>`.

Then open the production they are working on, and say in one line what they can do there: play it, pin notes to a
frame, approve the storyboard.

The `reel-desk` MCP tools below are not registered by default. If they aren't available and the person wants them:
Claude Code: `claude mcp add reel-desk --scope project -- node desk/mcp.mjs`; Codex:
`codex mcp add reel-desk -- node desk/mcp.mjs`; Copilot: add it to `.vscode/mcp.json` or the Copilot CLI's
`/mcp add` (then restart the session). Without them, read and
write `review.json` directly.

## Where things are

| | |
|---|---|
| Notes and approvals | `productions/<brand>/<ID>/review.json` (tracked in git: it is the review record) |
| What the person has open | `desk/.state.json`, or the `desk_state` tool |
| Desk renders | `productions/<brand>/<ID>/qa/desk/` (stills, `preview.mp4`, `qa/`); never the delivered export |

## Working from notes

1. `desk_state` tells you which production and time "this frame" means. `list_notes` gives the open notes
   (`id`, `t` in seconds, `text`). Without the MCP server, read `review.json`.
2. For each note: change the composition, check it with `render_frame` at the note's `t` (or
   `node core/render.mjs still … --t <t>`) and **look at the image**.
3. `resolve_note` with a one-line reply saying what changed. If a note needs a fact, an asset or a decision you
   don't have, keep it `open` and put the question in the reply. Only the person closes notes (after checking).
4. Your own QA findings can go on the timeline too: `add_note` (they show as by `claude`, the desk's name for any agent).

The desk's **Send to agent** button runs exactly this loop headlessly with the person's own login: Claude Code
(`claude -p`, `ANTHROPIC_API_KEY` removed, tools limited to read/edit/render/QA and `reel-desk`) or Codex
(`codex exec`, workspace-write sandbox, `OPENAI_API_KEY` removed), picked with `REEL_AGENT`. One session per
production (`review.json` → `claude.session` / `codex.session`).

## Approvals are the person's

The desk's **Approve storyboard** ticks `- [x] Storyboard approved` in the production README and fills
*Approved by / date*; **Approve final cut** adds a final-cut line. Both are logged in `review.json` → `approvals`.
**Never write an approval yourself**, in the README or in `review.json`, and never treat a fixed note as approval.
When a storyboard is ready, say "it's in the desk for approval" and stop (golden rule 2).
