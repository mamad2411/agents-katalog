---
name: peerctl
description: Spawn, message, steer, interrupt, list, stop, attach to, and recover Claude Code peers, including long-lived process peers owned by a daemon.
---

# peerctl

Peer lifecycle and messaging for Claude Code. Two engines:

- `process` (default) — a daemon-owned CLI process: `claude --print
  --input-format stream-json`, `codex app-server`, `opencode serve`,
  `pi --mode rpc`, or `agy --input-format stream-json`. It accepts
  messages: `send` starts a turn when idle and steers it when busy;
  `interrupt` ends the turn and keeps the process; `wait` returns the
  turn result; `inbox` collects turn results, exits, and denied
  permissions.
- `bg` — a `claude --bg` session owned by Claude's daemon. Lifecycle
  only; use `attach` to write one message to it.

Backends for a process peer: `claude` (default), `codex` (`codex
app-server`), `opencode` (`opencode serve`), `pi` (`pi --mode rpc`), and
`agy` (`agy --input-format stream-json`). `agy` cannot steer: a busy
send and `steer` are refused, and `interrupt` works only during a tool
step. See the peers guide for their differences.

Use this skill to dispatch a worker or reviewer and then talk to it:
send a follow-up task, steer a running turn, interrupt, collect results,
or rebuild a peer after its daemon stopped.

## Commands

```bash
python3 tools/peerctl.py spawn NAME --cwd DIR [--prompt TEXT] \
    [--engine process|bg] [--backend claude|codex|opencode|pi|agy] [--model M] \
    [--permission-mode MODE] [--agent-json JSON] [--settings JSON] \
    [--system-prompt TEXT] [--add-dir DIR] [--env K=V] \
    [--command 'ARGV'] [--workspace LABEL] [--max N]
python3 tools/peerctl.py send NAME TEXT [--json]
python3 tools/peerctl.py steer NAME TEXT [--interrupt] [--json]
python3 tools/peerctl.py interrupt NAME
python3 tools/peerctl.py wait NAME [--timeout S] [--json]
python3 tools/peerctl.py inbox [NAME] [--clear] [--json]
python3 tools/peerctl.py status NAME [--json]
python3 tools/peerctl.py attach NAME TEXT [--from-name N] [--from-mode bypass|default]
python3 tools/peerctl.py recover NAME [--backend B] [--permission-mode MODE] \
    [--settings JSON] [--env K=V] [--command 'ARGV']
python3 tools/peerctl.py ls [--workspace LABEL] [--cwd DIR] [--json] [--all]
python3 tools/peerctl.py stop NAME|ID [--rm]
python3 tools/peerctl.py daemon start|stop|status
python3 tools/peerctl.py export PATH
python3 tools/peerctl.py import PATH [--adopt]
```

Defaults:

- `--engine process`; `--backend claude`; `--permission-mode bypassPermissions`
- `--disallow AskUserQuestion` (bg only)
- per-workspace pool cap 8 managed live sessions (`--max` overrides)
- process state at `$AGENTABI_PEER_STATE`, default
  `~/.local/state/agentabi/peers`; bg manifest at `$PEERCTL_STATE`,
  default `~/.local/state/peerctl/pool.json`
- the first command starts the peer daemon; it stays up until
  `daemon stop`

`ls` shows process peers plus sessions created by peerctl; `ls --all`
adds every live Claude session on the machine. The `ENGINE` column says
which commands apply.

## Messaging rules

- `send` idle → new turn. `send` busy → steer, read by the model when the
  current tool call finishes. `SendResult.mode` says which happened.
- A steer is confirmed only by the write to the child process stdin.
  Claude sends no acknowledgement; `wait` is the authority.
- `wait` returns `status` (`success`, `error`, `cancelled`), `text`,
  `usage`, `num_turns`, and `stop_reason`. A timeout raises.
- `attach` writes to `cc-socks/<pid>.sock` of a bg or interactive
  session. It is one-way and unacknowledged; the command reports the
  message id, not delivery. It refuses process peers.
- `recover` starts a new process with `--resume <session_id>` from
  `peers.json`. The in-flight turn is not replayed; settings and env are
  never saved.

## State model

- The daemon is authoritative for process peers;
  `claude agents --json` is authoritative for bg sessions.
- `peers.json` keeps name, session id, cwd, model, and replayable spawn
  options, never keys. `pool.json` is a cache for workspace labels and
  handover.
- `sessionId` is the stable identity; the short id and the name are
  mutable.
- `stop` routes by engine: the daemon for process peers, `claude stop
  <short-id>` for bg sessions.

## Handover across tool versions (bg pool)

1. Before switching: `python3 tools/peerctl.py export /tmp/pool-<time>.json`
2. After switching: `python3 tools/peerctl.py import /tmp/pool-<time>.json --adopt`
3. Matching order: `sessionId` first, then `(cwd, name)`, else orphan.
4. Import never stops anything. Orphans are reported for a human
   decision; they are not killed or silently dropped.

## Safety

- Stopping the daemon stops its peers. Recover from `peers.json` when
  that was not intended.
- Keep the pool cap in place; each Claude session costs roughly
  250–300 MiB plus MCP children.
- Do not let peers spawn peers without a depth or budget limit.
- `--disallowedTools` must use the `=` form; the flag is variadic and
  otherwise swallows the positional prompt.
