---
name: cmux-event-bus-messaging
description: |
  Use this cmux-only skill only when cmux is already active or the user explicitly requests
  cmux integration. It covers cmux pub/sub for worker-to-worker and worker-to-orchestrator
  push messaging, completion signaling inside cmux workspaces, `cmux log` publishing,
  `cmux events` replay/resume/cursors, the claim-check pattern for payloads over 16 KiB,
  and idle-bus or lost-wakeup races. Do not trigger it for native host orchestration or
  completion signaling outside cmux; native collaboration requires no cmux setup.
author: Claude Code
version: 1.0.0
date: 2026-07-02
---

# cmux Event Bus Messaging

This is an optional cmux-only add-on. Load it only when `cmux` is available and a cmux
workspace is already active, or when the user explicitly requests cmux integration. If
cmux is absent, do not install or start it unless the user explicitly requested that
environment change; otherwise use the host's native collaboration messaging.

## Problem
When orchestrating multiple agent workers (`claude`/`codex`) in cmux workspaces, the
obvious-but-wrong approach is to scrape each worker's terminal with `cmux read-screen` in
a poll loop, or conclude "cmux is a terminal multiplexer, not a message bus, so there's no
push channel." **Both are wrong.** cmux exposes a genuine pub/sub event bus with replay and
resume. Workers can push structured completion messages onto it; an orchestrator (or another
worker) subscribes and receives them event-driven.

## Context / Trigger Conditions
- Fanning out `claude -p '…'` / `codex exec '…'` workers across `cmux new-workspace --command`
  and needing their results back. Wherever `claude` appears, substitute your own Claude Code
  launch command: `ccodex launch --` for the gateway route, which keeps your own Claude login and
  serves native Anthropic AND gateway models in one session (ADR-0014), or a personal alias.
- Wanting worker→worker reactions, not just fan-in to one orchestrator.
- Your orchestrator script hangs at startup on `cmux events --limit 1` (idle bus).
- A worker finishes and signals before the subscriber is ready → completion lost.

## Solution

### The bus exists
- `cmux events` — newline-delimited JSON stream: monotonic `seq`, retained replay
  (`--after <seq>`, 4096 events in memory), durable cursor (`--cursor-file`), name/category
  filters, `--reconnect` resume. Frame cap 16 KiB; slow subscribers dropped at 1024 pending.
- Every event is also appended to `~/.cmuxterm/events.jsonl` (16 MiB rotation) — durable tail.
- `cmux rpc <method>` exposes ~248 methods (`cmux capabilities` lists them).

### Publishing (no free-form emit RPC — ride `cmux log`)
There is NO "emit arbitrary JSON" method. `feed.push` needs a `session_id` (agent hook-feed
items only). But **every `cmux log` call emits a `sidebar.log.appended` event.** So:
- **publish:** `cmux log --level info --source "msg:<topic>" "MSGB64:$(printf '%s' "$msg" | base64 | tr -d '\n')"`
- **subscribe:** `cmux events --category sidebar --name sidebar.log.appended` → for each frame,
  read `payload.args`, extract the `MSGB64:<b64>` token, base64-decode, and route by the
  `--source msg:<topic>` tag.
- Base64 is required: it keeps spaces/quotes/newlines intact through the event's shell-quoted
  `args` field (raw text gets mangled).

### Claim-check for large payloads
The 16 KiB frame cap means you must NOT put a full agent result on the bus. Worker writes its
output to a FILE and publishes only `id=<n> status=<ok|err> file=<path>`; the subscriber reads
the file for the real payload.

### Gotcha 1 — idle-bus hang (this WILL bite you)
`cmux events --limit N` waits for N real **event** frames; the initial `ack` frame does NOT
count. On an idle bus it blocks forever. To read the current sequence number, grab the ack
line instead:
```sh
START_SEQ="$(timeout 3 cmux events --no-heartbeat 2>/dev/null | head -1 \
  | python3 -c 'import json,sys;print(json.load(sys.stdin).get("resume",{}).get("latest_seq",0))')"
```
`head -1` closes the pipe after the ack — no waiting for a real event.

### Gotcha 2 — lost wakeup
Capture `latest_seq` BEFORE spawning workers, then subscribe with `--after <seq>`. A completion
published before the subscriber is up gets **replayed**, not lost. Dedupe by worker id, because
replay can re-deliver a frame.

## Verification
Live roundtrip (from inside cmux):
```sh
( cmux events --category sidebar --name sidebar.log.appended --no-ack --no-heartbeat --limit 1 \
  | python3 -c 'import json,sys,base64,re;e=json.load(sys.stdin);a=e["payload"]["args"];print(base64.b64decode(re.search(r"MSGB64:([A-Za-z0-9+/=]+)",a).group(1)).decode())' ) &
sleep 1
cmux log --level info --source "msg:demo" "MSGB64:$(printf 'hello "world" & spaces' | base64 | tr -d '\n')"
wait   # subscriber prints:  hello "world" & spaces
```
Confirms the message published by one process is received + decoded by another, intact.

## Example
Orchestrator fan-in: capture `START_SEQ`; spawn N workers whose command ends with
`… > result.out 2>&1; cmux log --source "msg:$TOPIC" "MSGB64:$(printf 'id=%s status=ok file=%s' "$i" "$result" | base64 | tr -d '\n')"`;
then one subscriber `cmux events --name sidebar.log.appended --after "$START_SEQ" --reconnect`,
decode, dedupe by id, read each `file` for the payload. Working implementation:
`scripts/cmux-bus.sh` in the agentic-sdlc bundle (pub/sub/seq helper).

## Notes
- Spawn workers with `cmux new-workspace --command "<text>"` — it types into the workspace's
  INTERACTIVE zsh, so the operator's OWN shell aliases expand — this bundle defines none, so an
  alias like `ccode` works only if that operator already defined it; no alias/config edit needed.
- Teardown a workspace with `cmux close-workspace --workspace <ref>` — `workspace-action` has
  NO `close` verb (only close-others/above/below).
- Delegation-plane ranking: **Claude subagents** (results in-conversation) > **cmux event bus**
  (visible workspaces, payloads, many-to-many, replay) > **wait-for+file** (wakeup only) >
  **read-screen** (polling, last resort).
- codex workers: run in a dir listed `trusted` in `~/.codex/config.toml` and append `< /dev/null`
  so `codex exec` doesn't block on stdin.

## References
- cmux CLI contract: https://raw.githubusercontent.com/manaflow-ai/cmux/main/docs/cli-contract.md
- `cmux docs api`, `cmux capabilities`, `cmux events --help`
- See also: cmux-terminal skill (general cmux CLI), poll-wait-orchestrator-blocked-not-completion-terminal
