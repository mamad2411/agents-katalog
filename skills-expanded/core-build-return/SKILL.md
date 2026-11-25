---
name: core-build-return
description: "Work process. What happens to you and to the element agents when the core is built — a node update, the «Deploy core» button, npm run serve:rebuild: the build stops every agent, and after its end — good, failed or cut off — the ones that were running come back by themselves, in the same conversations. Load it before you start a core build or a node update, when you wake with the line «Node: the core build has finished», and when the person asks why an agent went off during a build or whether it comes back."
---

# The core build, and the agents that come back (node steps 675, 707)

**Process: work.** Nothing here is built by you: it is how the node behaves; you plan around it and say it to the person.

## What happens

Every agent's `claude` is a child of the core, so a core build with the closed lid stops all of them — you too. Before it stops the
core, the build writes who was running and its own process (`data/node/agent-return.json`); after its end it brings each of them back in
the same conversation (`claude --continue`) with a line from the node: the element agents first, then you, with the list of who came
back, who did not (memory) and which work sessions were stopped. The end is any of three (step 707, the owner 2026-11-09: «с неудачным
исходом автоматически поднимать себя так же как и удачным»): a GOOD build — the new build runs; a FAILED build — the previous build is up
again and the line names the cause; a build CUT OFF (its process died, the lid stayed shut) — the core's next start sees the dead builder
and returns everyone with «the build was cut off». An agent that was asleep stays asleep.

An element that says «done» while the build runs does not wake you — the closed lid would kill that session, and it is not on the
return list. Its words wait in `data/node/held-for-main.json` and come to you after the build, good or failed, together with the
work sessions it cut — even if you were asleep before it (step 696): the node wakes you with them; do what each line asks, then
`npm run done -- --close`. An element cut mid-turn comes back and finishes; its own «done» then wakes you as usual.

The terminal page of every agent shows the build instead of «Start the agent» while it runs, and at the end «Close and start the agent»
and «Close» (only «Close» after a failure).

## What you do

- **Before a node update:** the node's fork must carry Fractera's last commit — syncing it is your work (CLAUDE.md §4, the owner
  2026-11-08: «if exist claude for crome , or git token , you must to do sync alwayes»): the Chrome extension or a write token; check
  with `gh api repos/Fractera/web4-node-starter-kit/compare/main...<owner>:web4-node-starter-kit:main` (identical). Never ask
  «will you click it or shall I?» — you do it (the owner 2026-11-08: «why you ASK ME ? IT NOT GOOD … NOT ASK IF IT IS POSSIBLE»). The
  only block is a missing sign-in of the fork's owner in their Chrome with no write token: open github.com/login in that Chrome, say in
  one line that the update waits for their sign-in, and on their next word check and sync yourself — no question, no choice.
- **Until the node has a GitHub token** (the page `build/github` shows none), every answer about a fork sync — blocked or done through
  Chrome — ends with one line in the person's language: what the token would have saved («без токена GitHub я не смог синхронизировать
  форк сам — …» or «синхронизировал через Chrome; с токеном это шло бы без браузера и без входа»), the one-time path (a fine-grained
  token of the fork's owner, the fork only, Contents read and write) and the full link `http://localhost:<core port>/<lang>/architect/
  build/github`. Never a refusal, never a reproach; you never create or type the token yourself. The owner 2026-11-08: «подталкивать
  пользователей к тому чтобы он однажды прошел этот путь предоставил токен».
- **Before a build:** write your state — `current-steps.md` and the work record — as if you would not come back; tell the person in one
  line: «I go off with the build and come back by myself in a few minutes». Start the update or the build detached, never as your own
  child (`node scripts/spawn-free.mjs scripts/node-update-run.mjs`).
- **When you come back** with the node's line: `npm run serve:status`, then go on from where you stopped and tell the person the result.
  The line is a continuation of their conversation, not a task from the node — do not close yourself.
- **Who did not come back** (the line names them, memory was short): wake them when the person needs them — `npm run wake -- <id>`.
- **A work session** (`<id>--work`) is not continued: one folder has one «last conversation». Its job, if unfinished, goes again —
  `npm run task -- <id> --work`.
- **You come back after a failure** with «the core build FAILED» or «WITHOUT success»: the previous build runs; read the cause
  (`logs/node-update.log` or the terminal page), tell the person in one line, fix it or start again — detached.
- **You come back after a cut-off** («CUT OFF»): `npm run serve:status`; stopped services — `npm run serve:start`; then the build again,
  detached. ✗ 2026-11-09: the main agent started `npm run node:update` as its own background child — the lid killed the core, the agent
  and the update mid-build; `node-update.mjs` now refuses a start from an agent's session (707-3).
- **You did not come back** (the computer was off, memory was short): the person wakes you on the terminal page or in Telegram.

## The price

Each returned agent is a live session (about 300 MB) and one turn of its conversation; the node checks free memory before each and
refuses the rest — say who and why. Where it lives: `lib/deploy/agent-return.cjs`, `scripts/agent-return.mjs`, the log
`logs/agent-return.log`.
