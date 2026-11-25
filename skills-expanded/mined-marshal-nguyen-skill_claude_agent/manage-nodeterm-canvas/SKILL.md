---
name: manage-nodeterm-canvas
description: Create, organize and control nodes on the nodeterm canvas — open Claude Code / Codex / Gemini / terminal nodes, spawn a team of agents that divide up a task, create git worktrees as bound groups, wrap nodes in labeled groups, arrange/align/rename them, link nodes so you can read back what they produced, show an image/video/web page, write to or close a terminal. Use whenever the user says "Build with Nodeterm orchestration", asks to create or open nodes/sessions/terminals, split or parallelize work across subagents/agents/sessions/worktrees, delegate parts of a task to other agents, work on several things at once, build something using multiple Claude (or other agent) sessions, collect or synthesize the results of agents you opened, organize the canvas into groups by topic, or visualize code/output you produced. Only works inside a nodeterm Claude session.
---

# Manage the nodeterm canvas

You are running inside a node on the nodeterm canvas. You can create and control nodes by
running the local CLI shim below. Every node you open is connected to your node by an edge.

Run the shim (absolute path):

```sh
sh "/home/giang-nguyen/.config/node-terminal/canvas-control/nodeterm.sh" <verb> [args]
```

Verbs:
- `list` — list current nodes (id, kind, title). Start here when you need a node id.
- `open-terminal [--count N] [--cwd P] [--cmd C] [--group <id>] [--after <id,id>]` — open N plain terminals (default 1).
- `open-claude [--count N] [--cwd P] [--prompt T] [--group <id>] [--after <id,id>]` — open N Claude sessions (default 1).
- `open-agent --agent claude|codex|gemini|opencode|<custom-id> [--count N] [--cwd P] [--prompt T] [--group <id>] [--after <id,id>]` — open N sessions of any agent CLI.
  `--group` parents the node(s) into an existing group frame; a worktree-bound group also
  hands its worktree path down as the cwd.
  `--after <id,id>` opens the node **armed**: it does NOT start yet, and launches itself once
  every listed station has gone idle — that is how you express "B needs what A produces" without
  sitting in a poll loop. The armed node is also context-linked to each station it waits on, so
  it can read their work the moment it wakes. Only agent nodes that report status
  (claude/codex/gemini) can be waited on — waiting on a plain terminal is refused, because a
  plain terminal never reports finishing and the node would hang forever. Note the semantics:
  "idle" is the end of a station's TURN, not proof its whole job is done — right for a station
  given one self-contained prompt, wrong if you expect a long conversation first.
- `show-image <path>` — open an image file as a node.
- `show-video <path>` — open a video file as a player node.
- `show-web (--url U | --file P.html | --html "<...>")` — open a web viewer (live URL or local HTML you wrote).
- `open-browser --url U` — open a navigable browser (back/forward/address bar) at a URL.
  In an SSH project, nodes you open run on the HOST (same machine as you). The media viewers are
  the exception: they read the DESKTOP's disk, so `show-image` works (it reads back over the
  connection) but `show-video` and `show-web --file/--html` are refused for a host path —
  use `--url`, or copy the file to the desktop first.
- `group --nodes <id,id> [--label "Frontend Team"]` — wrap nodes in a labeled group frame.
- `arrange --nodes <id,id> [--layout grid|row|column] [--cols N]` — tidy layout, no overlap.
- `align --nodes <id,id> --edge left|right|top|bottom|hcenter|vcenter` — align edges/centers.
- `link --to <id,id> [--from <id>]` — context-link nodes, so each can READ the other's
  transcript on demand with the get-linked-context skill. `--from` defaults to you. Nothing is
  pushed into the linked sessions — reading is on demand, so linking never interrupts anyone.
  Agent sessions you open (`open-claude`/`open-agent`/`spawn-team`) are linked to you
  automatically; use `link` for nodes you did not open, or to link two OTHER nodes together.
- `verify --node <id> [--lenses correctness,security,tests] [--focus "..."] [--agent <id>] [--synthesis off] [--label L]` —
  open a review PANEL over that node's work: one reviewer per lens, each armed behind the target
  (they start when it goes idle) and linked to it so they can read what it actually did, plus a
  judge armed behind the whole panel that merges their findings into one verdict
  (`--synthesis off` skips the judge). Default lenses are correctness, security, tests; any word
  works as a lens, known ones just get a sharper brief. Reviewers are told NOT to change files —
  they share one checkout, and finding is a separate job from fixing. Use this instead of asking
  one agent "are you sure?": several INDEPENDENT looks from different angles catch what one pass,
  or several identical passes, cannot.
- `spawn-team --label "Frontend Team" --team '[{"title":"UI","prompt":"...","agent":"claude"}]'` —
  open one agent per role (each prompt starts that member working), arrange them in a grid,
  wrap them in a labeled group, and connect + context-link each to you. Max 8 roles per call.
- `open-worktree --branch <name> [--base <ref>] [--path P] [--group <id>]` — create a git
  worktree (new branch off base, default: the repo's default branch) and wrap it in a bound
  group frame (or bind it to an existing empty group). Terminals created inside the group
  run in the worktree. Local projects only.
- `close-worktree --group <id> [--mode unbind|remove]` — unbind (default) drops the binding
  and keeps the directory; remove asks the user to confirm deleting the worktree.
- `branch --node <id>` — branch a Claude node's conversation: the node stays on the new
  branch and a new node opens resuming the original. Target must be a Claude agent node.
- `rename --node <id> --title "New Name"` — rename any node (terminals, groups, stickies…).
- `write --node <id> --text "..."` — type text into a terminal node. (Asks the user to confirm.)
- `close --node <id>` — close a node. (Asks the user to confirm.)

Notes:
- `write` and `close` require the user to approve a confirmation dialog; they may be denied.
- If the CLI says canvas control is unavailable, you are not in a controllable nodeterm session — do not retry.

To orchestrate a team: decide the roles + a concrete starting prompt for each, then one
`spawn-team` call (or `open-claude` per role followed by `group` + `arrange`).

Typical requests this skill covers:
- "Create Claude Code nodes for X and organize them into groups by subject" → decide the
  workstreams, then either one `spawn-team` per subject (each team is already a labeled
  group), or `open-claude`/`open-agent` per node followed by `group --nodes ... --label`
  per subject and `arrange` inside each.
- "Open a codex/gemini session" → `open-agent --agent codex|gemini`.
- "Tidy up / group my terminals" → `list`, then `group` + `arrange` + `align`.
- "Rename this node/group" → `rename`.

## Nodeterm orchestration ("Build with Nodeterm orchestration")

When the user says "Build with Nodeterm orchestration" (or asks you to orchestrate a build
across Nodeterm sessions), be the orchestration chef — plan the kitchen, then run it:

0. First decide what is actually independent. For every "and then" in your plan, ask: does
   the next step READ the previous step's output? If it does not, there is no dependency and
   the wait is wasted — those steps are separate stations, open them all at once. If it does,
   the dependency is real: open the downstream station with `--after <upstream-id>` and it
   will start itself when the upstream goes idle. Do not fake this by polling in your own
   session; that is what `--after` exists to replace.
1. Break the task into 2–5 independent workstreams (by subsystem, not by file).
2. Per workstream, give it its own branch + kitchen station:
   `open-worktree --branch <slug>` → note the returned `groupId`, then
   `open-agent --agent claude --group <groupId> --prompt "<concrete, self-contained task>"`.
   Each stream now works on its own branch in its own worktree group — no tree conflicts.
3. Keep the kitchen tidy: members opened with `--group` land in neat grid slots inside the
   frame automatically (the frame grows to fit), and successive `open-worktree` frames fan
   out side by side — after opening all stations, align the frames with
   `arrange --nodes <groupId,groupId,…> --layout row` (arrange/align work on top-level
   nodes, so pass the GROUP ids, not the children). `rename` each group by subject.
4. Track progress (their status badges show working/waiting) and coordinate.
5. Collect the results yourself — this is the half most orchestrators skip. Every station you
   opened is context-linked to you, so when one goes idle, read what it actually did with the
   **get-linked-context** skill (summary or transcript for that node id) instead of asking the
   user to relay it. Then do the work only you can do: reconcile the streams against each
   other, name the conflicts and the leftovers, and report ONE synthesis. A station you never
   read is a station whose work you cannot vouch for — say so rather than assuming it went
   fine. Stations you did not open are not linked; `link --to <id>` them first.
6. Verify before you report. When a station's work matters — anything touching money, auth, data
   migration or a public API — run `verify --node <stationId>` instead of re-reading it yourself.
   You cannot independently check work you were part of planning; a panel of reviewers who each
   look through ONE lens, and who did not watch it being written, can. Fold their verdict into
   your synthesis, and say which findings you accepted and which you dismissed and why.
7. Hand back: the user merges from the group's chip (never merge for them); release a finished
   station with `close-worktree --group <id>` (unbind keeps the directory).
