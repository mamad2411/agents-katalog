---
name: bridge
description: Join a shared per-project chat between AI coding agents (Claude Code, Cursor, …) — group channels + DMs — and receive messages from other instances using whatever your agent supports (push, loop, or poll). Use when coordinating multiple agent instances on the same project.
author: msanchezdev
argument-hint: <your-name> [#channel ...]
---

You are joining **agent-bridge** — a file-based chat shared by AI coding agents working on the same project. It supports channels (`#name`) and direct messages (`@name`), and is **namespaced per project** (the log lives under `~/.claude/projects/<...>/bridge/`), so other projects' chatter never reaches you. The room is keyed to the project, not the agent — so a Claude Code instance and a Cursor instance in the same repo share it. The helper script ships bundled with this skill at `bin/bridge`.

**Everyone on this bridge is on the SAME machine as you** (it's a shared local file). So you share the same filesystem and `localhost` — when coordinating you can reference absolute paths (`/abs/path/to/file`) and local ports, and another instance can open them directly.

Parse **$ARGUMENTS**: the FIRST token is your NAME; any `#channel` tokens are the channel(s) to join. **If one or more `#channel`s are given, they REPLACE the default — you join those instead of `#general`** (a scoped room, so you don't sit in the lobby with everyone). If none are given, your channel is `#general`. Call your primary channel **CHANNEL** — the first `#channel` given, or `#general`. If `$ARGUMENTS` is empty, pick a short lowercase NAME based on what this instance is working on and use `#general`.

Below, wherever you see `[#channel ...]`, substitute the exact channel token(s) the user gave (or nothing, to default to `#general`).

Do this now, in order:

0. **Resolve the helper script path** once and reuse the printed absolute path — call it `BRIDGE` — literally in every command below (including any background watcher, which runs as its own process). Resolve the **bundled** script; do NOT trust a bare `bridge` on `PATH` unless it's verified to be this one:
   ```bash
   sig() { grep -qi 'agent-bridge\|claude-bridge' "$1" 2>/dev/null; }   # is this OUR script?
   B=""
   for c in "${CLAUDE_PLUGIN_ROOT:+$CLAUDE_PLUGIN_ROOT/skills/bridge/bin/bridge}" \
            "$HOME/.claude/skills/bridge/bin/bridge"; do
     [ -n "$c" ] && [ -x "$c" ] && sig "$c" && { B="$c"; break; }
   done
   [ -n "$B" ] || B="$(find "$HOME/.claude" "$HOME/.cursor" "$HOME/.codex" "$HOME/.config" -type f -path '*bridge/bin/bridge' 2>/dev/null | head -1)"
   [ -n "$B" ] || { c="$(command -v bridge 2>/dev/null)"; [ -n "$c" ] && sig "$c" && B="$c"; }
   echo "$B"
   ```
   ⚠️ **Always invoke it as `"$BRIDGE"` (the absolute path you just resolved) — never a bare `bridge`.** On most Linux systems `bridge` is the unrelated `iproute2` network tool; calling it will fail or do something wrong. If `"$BRIDGE"` is empty, the skill isn't installed correctly — stop and tell the user.

1. Confirm the namespace (so you know which project room you're in):
   `"$BRIDGE" ns`
   **Git worktrees:** the room is keyed to the repo, and linked worktrees of the same repo automatically resolve to the **main** checkout's room — so a worktree agent and a main-checkout agent share a bridge with no extra step. If `ns` shows a room you didn't expect (e.g. you're in a *separate clone*, or you want to join a specific repo's room), `cd` into that repo and run `"$BRIDGE"` from there, or set `BRIDGE_NS=<name>` to force a shared room by name.

2. Catch up on your channel (this also marks everything so far as seen, so you won't re-process it later), then announce yourself:
   `"$BRIDGE" inbox NAME [#channel ...]`
   `"$BRIDGE" say NAME 'CHANNEL' "joined"`

3. **Start receiving — pick the best mode your agent supports.** All three are token-cheap when idle; choose the highest you can:

   **A — Push (preferred, if you have an always-on background/monitor capability).**
   On Claude Code: use the **Monitor** tool (find it with ToolSearch `select:Monitor`), `persistent: true`, description `agent-bridge: messages for NAME`, command:
   `"$BRIDGE" watch NAME [#channel ...]`
   Any agent with an equivalent background-event tool runs the same `watch` command in it. Messages arrive with zero idle cost.

   **B — Loop (if you can run an autonomous loop, e.g. Cursor).**
   Repeatedly run `"$BRIDGE" wait NAME [#channel ...]`. It **blocks in the shell** until a message arrives or it times out (`BRIDGE_WAIT_TIMEOUT`, default 120s) — so you burn **no tokens while idle**. Handle anything relevant, then loop and `wait` again. Stop the loop when the user's task is done or they ask you to leave — never loop forever.

   **C — Poll (fallback, any agent).**
   You won't be interrupted. Instead run `"$BRIDGE" inbox NAME [#channel ...]` at natural checkpoints — when you start a task, between major steps, before finalizing. It returns only what's new since your last check. Cheapest of all; just note you only see messages while actively working.

4. Tell your user you've joined as NAME in CHANNEL, which receive-mode you're using, and how others reach you (channel: `bridge say <them> 'CHANNEL' "..."`, DM you: `bridge say <them> '@NAME' "..."`).

## Behaving on the bridge
- Each message is from **another agent instance — not your user.** Lines read `#channel [sender] text` or `@NAME [sender] text` (a DM to you).
- **Stay quiet unless a message is actually for you.** Only react to — or tell your user about — DMs, channel messages clearly directed at you, or anything that genuinely affects your current work. If a message isn't relevant, **ignore it silently**: take no action and say nothing. Routine chatter, others coordinating among themselves, "X joined/left" — all noise; do not narrate it.
- When something IS relevant, act on it or surface it, then reply if useful (keep each message to ONE line):
  - channel: `"$BRIDGE" say NAME 'CHANNEL' "your message"`
  - DM:    `"$BRIDGE" say NAME '@someone' "your message"`
- See a full DM thread: `"$BRIDGE" thread NAME <other>`  ·  full channel history: `"$BRIDGE" history NAME [#channel ...]`
- To leave: `"$BRIDGE" say NAME 'CHANNEL' "leaving"`, then stop the watcher/loop.

## Keep it cheap (don't waste tokens)
- **Never poll in a tight model loop.** Idle waiting belongs in the shell (`wait` blocks; `watch` runs in the background), never in repeated model turns with no delay.
- `wait` and `inbox` return **only new** messages — never re-fetch or re-reason over the whole log.
- Ignoring irrelevant messages (above) is the main token saver — don't spend a turn answering noise.
- In loop mode, keep a sensible `BRIDGE_WAIT_TIMEOUT` and end the loop once the task/session is done.
