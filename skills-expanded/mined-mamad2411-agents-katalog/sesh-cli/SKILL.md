---
name: sesh-cli
description: Use the `sesh` CLI/TUI to list, find, enter, resume, create, tag, archive, rename, delete, send-to, or inspect coding-agent sessions across machines. Use when the user asks about sesh command usage, the session TUI, entering/resuming a sesh, cross-machine session state, the sesh daemon, or peers.
---

# sesh CLI skill

Use this skill when the user wants to **use** `sesh` (manage their
coding-agent sessions), not develop sesh itself.

`sesh` is multi-machine coding-agent session management that feels like one
machine. A per-machine **daemon** (`sesh-daemon`) owns a local SQLite store
and runs a tmux **walker** (which pane each session is in) + agent
transcript watchers. Daemons peer-to-peer over gRPC so **every machine sees
every machine's sessions** (a full mesh). The `sesh` CLI/TUI talks only to
the local daemon over a unix socket.

## Short UUIDs

Every command that takes a `<uuid>` also accepts a **short prefix** — the
first 8 characters (or any unambiguous prefix). For example, if a session's
UUID is `a808a699-…`, you can use `a808a699` or even `a808` if that prefix is
unique:

```bash
sesh info a808a699          # same as sesh info a808a699-xxxx-xxxx-xxxx-xxxx
sesh send a808a699 "hello"
sesh pane-capture a808      # only if a808 uniquely identifies one session
```

If a prefix matches multiple sessions, **non-archived sessions win**. If the
tie is still ambiguous (multiple non-archived, or multiple archived with no
active match), the command errors and lists all matching UUIDs.

Use `sesh find <prefix>` to explore matches before acting:

```bash
sesh find a808              # list every session whose UUID starts with a808
```

## Before running commands

- **Read-only — safe to run anytime:** `list`, `find`, `info`, `state`, `pane`,
  `pane-resolve`, `tags`, `tail`, `transcript`, `doctor`, `daemon status`, `peer` (listing),
  `pick`/`tui` (interactive; they emit a selection, they don't mutate).
- **Mutating / side-effecting — confirm intent first:** `new` (spawns an
  agent), `register`, `rename`, `tag`/`untag`/`retag`, `archive`/`unarchive`,
  `delete`, `send` (messages the agent), `abort`, `compact`, `autoname`,
  `autoname-toggle`, `resume` (switches/launches tmux), `copy`,
  `backup`/`restore`/`import`, `daemon start/stop/restart`, `peer add/remove`.
- Be especially careful with:
  - `delete <uuid>` — removes the record (a tombstone propagates across the
    mesh). `--force` tombstones a sesh this machine doesn't own (orphan
    cleanup); only use it when the owning machine is gone. Once deleted, the
    session is gone everywhere: it is no longer resolvable (by full UUID or
    short prefix) and all reads/mutations on it report "not found" (exit 1).
  - `send <uuid> <message>` — actually drives the agent.
  - `import` — one-shot migration of v1 `~/.sesh/sessions.json`.

## Core concepts

- **UUID & short id.** Each session has a UUID. The "short id" is the part
  up to the first `-` (e.g. `a42f8a74`); the TUI shows it and most users
  refer to sessions by it. Commands accept the full UUID.
- **Machine = origin.** Every record carries the machine that owns it
  (`$SESH_MACHINE`). The owning machine is the single writer for it. Reads
  work from anywhere (the mesh synced the record locally). **Everything else
  routes cross-machine through one owner-routing seam** — run it from any
  machine that peers with the owner and it's forwarded to the owner's daemon,
  which applies it and (for a mutation) propagates the updated record back.
  This covers **record mutations (`rename`/`tag`/`untag`/`retag`/`archive`/
  `unarchive`/`delete`/`autoname-toggle`)**, **agent actions (`send`/`abort`/
  `compact`)**, and **transcript reads (`tail`/`transcript`/`autoname`)**.
  You no longer have to ssh to the owner to mutate or read a remote session.
  (A termux-owned session still can't be reached from a server that termux
  doesn't dial back — that errors clearly. `delete --force` for an orphan
  whose owner is gone stays local, since there's no owner to forward to.)
- **Live vs detached.** "Live" = the session currently has a tmux pane (the
  walker found it); "detached" = no pane. The glyphs: `●` live+idle,
  `◐` live+busy, `○` detached.
- **Archived is orthogonal** to live/busy — an archived session can still be
  live. Views: active (default), archived, all.
- **Agents:** `claude`, `pi`, `codex`. Some verbs are agent-specific
  (`abort`/`compact` are pi-only).

## The TUI — `sesh tui` (the primary interface)

Full-screen manager over **every** machine's sessions, with live updates.
Columns: id · name · cwd · agent · machine · socket · tags · created
(rows sort by creation time, earliest→latest). The name (blue) and cwd
(green) columns are color-accented so they stand out; archived rows are
dimmed gray and the cursor row is reverse-highlighted.

Keys: `↑↓`/`jk`/`Ctrl-j`/`Ctrl-k` move · `/` fuzzy-filter · `Tab` cycle
active/archived/all · `i` toggle the id column · `y` show full UUID popup ·
`a` archive · `u` unarchive · `r` rename · `t` add-tag · `x` remove-tag ·
`d` delete · `Enter` select · `q`/`Esc` quit.

`sesh tui` **emits** the selected session on `Enter` (it doesn't drive tmux
itself — "emit, don't drive"); a wrapper navigates. `sesh tui --enter`
opts into driving locally instead (switch to a live pane / resume a detached
one / ssh into a remote owner).

## Entering / resuming a session

```bash
sesh resume <uuid>                       # live → switch to its pane; detached → resume the agent
sesh resume <uuid> --target socket:sess  # create that tmux session (if absent) + open a window
sesh resume                              # no uuid → interactive picker
sesh pick                                # pick a session; print the selection (json/nul/kv) on stdout
sesh pick --select <uuid> --enter        # non-interactive enter of a specific sesh
```

`resume`/`pick`/`tui` use vanilla `tmux switch-client`/`attach` — no
master-tmux assumptions. The myrig shell layer (`sesh-tui`, `sesh-enter`)
wraps these to route through master-tmux.

## Listing & inspecting

```bash
sesh list                                # active sessions, all machines
sesh list --machine <name>               # one machine
sesh list --archived                     # include archived (alias: --include-archived)
sesh list --agent claude --tag work      # filters
sesh list --columns uuid,name,agent,machine,status,cwd,tags,archived,tmux-socket,tmux-session,tmux-window,tmux-pane,live   # TSV for fzf/awk (unknown column name errors)
sesh find <partial-uuid>                 # list all sessions (including archived) matching a UUID prefix
sesh info <uuid> [--json]                # full record
sesh state <uuid>                        # turnStatus + per-agent extras
sesh tags                                # all tags in use across the mesh (every machine)
sesh tail <uuid> [-n N]                  # last N transcript lines (any machine; forwards to the owner)
sesh transcript <uuid>                   # full transcript (any machine; forwards to the owner)
sesh pane [--pane %ID] [--socket-path P] # which REGISTERED sesh owns a tmux pane (store-backed; status bars)
sesh pane-resolve --pane %ID --socket-path P  # uuid of the agent LIVE in a pane, registered or not (walker-backed)
sesh pane-capture <uuid> [-n N]          # capture current pane text (local; for inspecting stuck TUI state)
sesh pane-keys <uuid> <key>...           # send raw tmux key names to a pane (local; for navigating TUI prompts)
```

`pane` vs `pane-resolve`: `pane` reads the **store** (only knows registered
records); `pane-resolve` runs the **walker** to identify the *live* agent in a
pane even if it was never registered — the primitive for *adopting* an agent
(`uuid=$(sesh pane-resolve …) && sesh register "$uuid" …`). Works for all three
agents (claude via argv/`agents --json`, pi via its rpc socket, codex via the
rollout it holds open). **Local-only** (pane ids are per-tmux-server, like
`pane`). `--json` emits `{uuid, agent, cwd, machine, tmux}`. Exit codes: `0`
resolved · `3` no agent in the pane · `4` agent found but unresolvable (e.g. a
codex that hasn't taken its first turn yet — it has no session on disk until
then).

All `--json` output uses **camelCase** keys. `info --json` and each element of
`list --json` / `find --json` are the full session record:
`{uuid, name, agent, machine, cwd, turnStatus, archived, autoRename, summary,
lastAutoNameTurnCount, contextPct, filePath, tmux:{socket, session, window,
pane}, createdAt, updatedAt, originSeq, tags, deleted}`. To check a tombstone:
`sesh info <uuid> --json | grep '"deleted": true'`.

`pane-capture` returns the visible text of the pane (last N lines, default 50).
`pane-keys` sends raw tmux key names (Enter, Escape, Up, Down, q, 1, 2, …) —
use it for TUI prompts that appear before the agent accepts conversation
messages. Both are **local-only** and **refuse a remote-owned uuid** with a
clear "owned by <machine>; run on <machine>" error — they drive the local tmux,
so feeding a remote record's per-machine pane/socket would error cryptically or
hit the wrong local pane. Run them on the owning machine.

### Startup prompts that can block a freshly-spawned claude session

When spawning a claude session in a directory whose `CLAUDE.md` imports files
outside the cwd (e.g. `@~/.config/AGENTS.md`), claude may open to an
interactive confirmation:

```
Allow external CLAUDE.md file imports?
  > 1. Yes, allow external imports
    2. No, disable external imports
Enter to confirm · Esc to cancel
```

`sesh send` will not work while this prompt is visible — the agent hasn't
initialised yet. The recovery pattern:

```bash
sesh pane-capture <uuid>              # confirm the prompt is showing
sesh pane-keys <uuid> Enter           # confirm option 1 (already selected)
# wait a moment, then:
sesh send <uuid> "your first message"
```

If you spawn frequently in the same directory and keep hitting this prompt,
configure the acceptance globally:
- Accept it once interactively in a manually-opened claude session; claude
  remembers the answer per-project in `~/.claude/projects/<dir>/settings.json`.
- Or set `allowExternalImports: true` in your `~/.claude/settings.json`.

## Lifecycle (run from anywhere — mutations forward to the owner)

```bash
sesh new --agent claude --name foo --tag work [-- agent-args...]  # spawn + register from birth; cwd defaults to $PWD
sesh new --agent claude --model opus     # launch with a specific model (see "Model selection")
sesh new --agent claude --target socket:sess --msg "greet me" --name foo  # spawn window + send initial message, print reply
sesh new --agent pi --dry-run            # print the plan, register nothing (add --json for a JSON plan)
sesh new --agent claude --no-launch      # register only
sesh new --agent claude --session-id <uuid> --no-launch  # pre-assign the UUID (must be a well-formed UUID)
sesh new --agent claude --cwd ./sub      # --cwd is absolutized to a realpath (relative is resolved against $PWD)
sesh new --headless --agent claude --msg "do X" --name child  # persistent headless child (no tmux window)
sesh register <session-id> --agent pi --name foo   # record an already-running agent; --cwd defaults to $PWD
sesh rename <uuid> <name>                # sets autoRename=false (unless --keep-auto)
sesh tag <uuid> <tag>...    /  sesh untag <uuid> <tag>...  /  sesh retag <uuid> old=new   # empty/whitespace tag names are rejected (e.g. tag '' or retag old=)
sesh archive <uuid>  /  sesh unarchive <uuid>            # orthogonal to live/busy
sesh delete <uuid> [--force]             # tombstone (propagates); --force for an orphan
```

Note: `codex` can't pre-assign a session id, so interactive `new --agent
codex` is unsupported — start it and `sesh register`. (`new --headless
--agent codex` and `delegate --agent codex` DO work — they recover the id
from codex's own output.)

### Spawning child agents — `new --headless` and `delegate`

Two ways for one agent to spawn another (e.g. a parent agent farming out
work). Both run the agent non-interactively — no tmux window:

```bash
# PERSISTENT child you keep talking to. Runs the first turn (--msg), creates
# the session on disk, registers it, prints the reply. Later `sesh send
# <uuid>` resumes it headlessly. claude/codex only.
sesh new --headless --agent claude --msg "You are my test runner. Reply READY." --name runner
sesh send <uuid> "run the suite and summarise failures"   # talk to it over time

# EPHEMERAL one-shot: spawn a worker, give it ONE task, print the reply, then
# DELETE the session. ⚠️ The session DISAPPEARS once it returns — it is gone
# afterward (use --keep to retain it). pi, claude, and codex.
sesh delegate --agent codex "What is 2+2? Reply with just the number."
sesh delegate --agent claude --keep --name audit "audit auth.go for bugs"   # keep the session
```

- **`new --headless`** is for a child you'll converse with repeatedly;
  **`delegate`** is for "do this one thing and tell me the answer." Reach for
  delegate unless you need to follow up.
- `--headless` requires `--msg` (the first turn is what creates the on-disk
  session). **pi can't run headless** (it needs a live terminal to serve its
  rpc socket) — `new --headless --agent pi` errors; use `delegate --agent pi`
  (one-shot) or interactive `new --agent pi` instead. pi works fine with
  `delegate` because that's a single `pi -p` turn.
- **`--msg` also works for non-headless (tmux) spawns** — requires `--target`
  or a running `$TMUX` session. Waits for the agent to appear live in its pane,
  then delivers the message and prints the reply. Incompatible with `--no-launch`.
- delegate's worker runs read-only-ish (codex `--sandbox read-only`); it's
  meant to answer, not mutate your workspace unattended.

### Model selection — `--model` (set at launch)

`sesh new` and `sesh delegate` take `--model` to launch the agent with a
specific model. It maps to each agent's own flag (`claude/codex/pi --model`;
codex's `-m`), so use that agent's model names:

```bash
sesh new --agent claude --model opus              # alias or full id (sonnet, opus, claude-opus-4-8)
sesh new --agent pi --model sonnet:high           # pi patterns: provider/id, alias, :<thinking>
sesh delegate --agent codex --model gpt-5.4 "…"   # codex model id
```

**Defaults via `~/.sesh/config.toml`** — set a default model per agent (with
an optional global fallback) so you don't pass `--model` every time:

```toml
[models]
default = "opus"          # fallback for any agent when it has no specific default
claude  = "opus"
codex   = "gpt-5.5"
pi      = "anthropic/claude-opus-4-7"
```

Precedence: **`--model` flag > `[models].<agent>` > `[models].default` >** the
agent's own built-in default (no flag passed). `--list-models` (pi) /
`claude --help` / codex docs enumerate valid names.

Scope notes:
- This sets the model **at the start** of a session only. There is no command
  to change a running/existing session's model; switch it inside the agent
  (claude `/model`, codex/pi `/model` picker).
- `new --agent codex` is unsupported regardless (no pre-assignable id), but
  `delegate --agent codex --model …` works.

**Agent binary location via `[agents]`** — override where sesh looks for each
agent's CLI binary. By default sesh resolves `claude`/`codex`/`pi` against the
daemon's PATH augmented with common version-manager shim dirs (mise/asdf,
`~/.local/bin`, `~/.cargo/bin`, …). If your binary lives somewhere exotic — or
the daemon's PATH lacks the shims dir holding it (the spawn-works /
resume-fails asymmetry) — declare the path explicitly:

```toml
[agents]
claude = "/opt/tools/claude"
codex  = "/home/me/.local/share/mise/shims/codex"
pi     = "/home/me/bin/pi"
```

Precedence: **`[agents].<agent>` config path (if set and an executable file) >
PATH/shim-dir heuristic >** loud not-found error. A configured path that is NOT
an executable file is a loud error naming the path (no silent fallback) — fix
or remove the override.

## Driving the agent

```bash
sesh send <uuid> <message>           # send a message and return the agent's reply (two-way; see below)
sesh send <uuid> <message> --no-wait # deliver only; don't await or print a reply
# An empty/whitespace-only <message> is rejected up-front with "message is empty".
sesh await <uuid> [--timeout D]      # block until the turn completes (busy → idle), print the status (D=0 means no limit; a negative D is rejected)
sesh abort <uuid>                    # abort current operation (pi-only)
sesh compact <uuid>                  # trigger context compaction (pi-only)
sesh autoname <uuid>                 # auto-generate a name via `pi -p`
sesh autoname --all                  # auto-name every nameable session in the mesh; un-nameable ones (no transcript yet) are skipped, the rest still named
sesh autoname-toggle <uuid> [--on|--off]
```

`send`/`abort`/`compact` (and the mutations and transcript reads above) route
to the owning machine through the one owner-routing seam, so they work on a
session anywhere in the mesh (not just local).

**`send` is two-way for all three agents** — by default it blocks until the
agent finishes its turn and prints the reply. How the reply is obtained
depends on the agent and whether the session is live in a tmux pane:

- **pi** — delivered over its socket; returns the streamed reply (works even
  when detached/headless).
- **claude / codex, live in a pane (attached)** — the message is typed into
  the live pane (so a human watching sees it, and the conversation isn't
  forked), then `send` waits for the turn to finish and returns the last
  assistant message.
- **claude / codex, detached (no live pane)** — the session is resumed
  **headlessly** (`claude -p --resume` / `codex exec resume`) and the reply
  is returned. (codex runs read-only with no approval prompts; claude resume
  is cwd-scoped, so the session's recorded `cwd` must still exist.)

> Caveat (exp14): never headless-resume a claude/codex session that is also
> live in a pane — it forks the in-memory conversation. `sesh` avoids this
> automatically by typing into the pane whenever one is live; the headless
> path is taken only for detached sessions.

**`--no-wait`** makes `send` fire-and-forget: it delivers the message and
returns immediately without awaiting the turn or printing a reply (it still
errors if *delivery* fails). For a detached claude/codex this launches the
headless turn in the background, so turn-time errors are logged by the
daemon, not surfaced to the caller. Use it when you just want to nudge an
agent and not block.

**`await`** is a pure read on the mesh-synced `turnStatus`, so it works for a
session on any machine with no forwarding; an already-idle session returns
immediately. It's mostly useful for observing a turn you didn't start (a
human-driven session, or one nudged with `send --no-wait`) — a plain `send`
already waits. Caveat: if a human is also driving the session, `await`
returns on whichever turn finishes first. `--timeout 0` (the default) waits
forever; a *negative* `--timeout` is rejected with a clear error rather than
silently behaving like "no limit".

**`autoname --all`** auto-names every nameable non-archived session across the
mesh (renames forward to each owner). A session that can't be named yet — most
commonly a freshly-registered one with no transcript on disk — is *skipped*
(reported on stderr) and the rest are still named; the batch does not abort on
the first such session. Naming a single explicit `<uuid>` still surfaces its
error.

## Daemon & peers

```bash
sesh daemon status [--json]    # machine, uptime, sessions, peers, schema version
sesh daemon start | stop | restart      # restart = the reliable way to pick up a redeployed binary
sesh daemon ensure             # idempotent start (supervisor entrypoint)
sesh peer ...                  # manage peer-daemon connections (~/.sesh/peers.json)
sesh doctor                    # diagnose agents/tmux/daemon/config
```

The daemon is normally supervised (supervisord/launchd on servers; a
nohup leaf on termux). If supervised, restart via the supervisor, not
`sesh daemon restart`, so they don't race. `sesh daemon start` (and the
`start` half of `restart`) refuses with an error if a daemon is already
running, rather than spawning a duplicate — so a stray manual start can't
clobber the supervised instance (the guard is an exclusive flock on the
pidfile, so even concurrent starts can't both win). If a background start
FAILS, the client surfaces the daemon's real error (e.g. missing
`SESH_MACHINE`) and captures its stderr to `~/.sesh/daemon.log`.

## Maintenance

```bash
sesh backup        # import transcripts into a single SQLite file (idempotent)
sesh restore       # reconstruct transcripts from a backup
sesh import        # one-shot import of v1 ~/.sesh/sessions.json
sesh copy <uuid> <dest>   # copy a session's transcript elsewhere (same-agent)
```

`restore` notes:
- `--from <file>` must point at an EXISTING backup; a missing/typo'd path
  errors `no such backup file` (it will not silently create an empty DB).
- `restore [uuid]` accepts a full UUID or a **short prefix** (like `copy`),
  resolved against the backup's stored transcripts; an unknown or ambiguous
  prefix is a loud error, not a silent no-op.
- Default target is `--to native` (reconstruct at the agent's real path).
  Only **claude** has a deterministic native path; pi/codex filenames embed a
  timestamp, so a native restore **skips** them and reports them as
  "unsupported" (restore those with `--to <dir>`). A mixed-agent backup still
  restores its claude entries — it does not abort partway.

`copy` notes:
- Cross-machine `copy <uuid> --to <machine>` restores `--to native` on the
  peer, so it only works for **claude** sessions; copying a pi/codex session
  cross-machine errors loudly up front (use `--to-dir <dir>` locally instead).
  A failed remote restore now propagates a nonzero exit (it no longer reports
  a false "copied" success).

`sesh import` writes SQLite directly (the daemon normally owns writes), so it
refuses with an error if a daemon is live on the socket — running it then would
corrupt the daemon's in-memory origin-seq counter. Stop the daemon first
(`sesh daemon stop`, or via your supervisor) and re-run. Pass `--force` only if
you will restart the daemon immediately after (a restart re-seeds the counter
from the new DB max).

## Common flags & environment

- Global flags: `--machine <name>` (target a machine; default all/local),
  `--json` (machine-readable), `--socket <path>` (daemon socket, default
  `~/.sesh/daemon.sock`).
- `new`/`delegate` flags: `--model <name>` (launch model; see "Model
  selection") among the per-command flags above.
- Config: `~/.sesh/config.toml` `[models]` sets default launch models and
  `[agents]` overrides each agent binary's path (both under "Model selection").
  The mesh/peers live in `~/.sesh/peers.json`, not here.
- Env: `SESH_HOME` (state dir, default `~/.sesh`), `SESH_MACHINE` (origin
  identity — **required**; the daemon refuses to start without it, no
  hostname fallback), `SESH_TMUX_SOCKETS` (override walker socket discovery),
  `SESH_CWD_FORMATTER` (a command to relabel the TUI cwd column).
- Exit codes for the picker (`pick`/`tui`): `0` selected, `130` cancelled,
  `3` nothing to select.

## Picker emit contract

`pick`/`tui` (without `--enter`) print the selection on stdout as
`--format json` (default), `nul`, or `kv`. JSON fields: `action`
(goto|resume), `uuid`, `machine`, `agent`, `cwd`, `name`, and `tmux`
(`socket`/`session`/`window`/`pane`). A wrapper reads this and navigates.

`action` is auto-derived from the row's liveness — `goto` for a live
session (has a tmux pane), `resume` for a detached one — consistently for
both `pick` and `tui`. Pass `--action <verb>` to override it (e.g.
`send`). `--cursor <uuid>` on `tui` pre-positions the highlight on a row
(full UUID or a short prefix, like every other `<uuid>` arg); an
unresolvable prefix is a loud error, not a silent no-op.
