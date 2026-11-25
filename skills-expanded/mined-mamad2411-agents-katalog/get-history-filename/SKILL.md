---
name: get-history-filename
description: Find the on-disk conversation transcript (JSONL) for an agent session by tracing its tmux pane → process → working directory → project dir. Use when an agent needs to locate where its own — or a peer's — chat history is stored on disk, e.g. "where is my history file", "find this session's transcript", "what jsonl is pane %N writing to".
---

# Get History Filename

Locate the JSONL transcript file backing a running agent session, starting from nothing but its **tmux pane**. The trick is that the pane runs the agent process, the process knows its working directory, and the harness derives the transcript path deterministically from that directory.

This skill currently covers **Claude Code** and **Codex**. Other agent harnesses use different on-disk layouts and will be added as their own sections below.

---

## Claude Code

### Shortcut: by agent identity

If the target has a claimed identity (stamped as `agentName`/`customTitle` in its
transcript), the quickest resolve is:

```bash
agent-message lookup <identity>        # prints the transcript UUID
```

It reads the in-transcript stamp rather than tracing a live pane, so it resolves
even **after** the agent's process has been killed. The pane → file chain below is
the general method — it works for any session, identity-stamped or not.

### How the path is derived

Claude Code stores each session's transcript at:

```
~/.claude/projects/<sanitized-cwd>/<session-uuid>.jsonl
```

- **`<sanitized-cwd>`** — the agent's current working directory with every `/` replaced by `-`. So `/home/slomp` → `-home-slomp`, and `/Users/tcdent/Work/uptime` → `-Users-tcdent-Work-uptime`. (The mapping is lossy: two different sessions launched from the same cwd land in the *same* dir, and unusual characters may be sanitized too — so confirm by mtime/content, see Caveats.)
- **`<session-uuid>.jsonl`** — one file per session. Claude **reopens-and-appends** on each write rather than holding the fd open, so the file will *not* show up in `/proc/<pid>/fd` — you identify the live one by recent mtime.

### The chain, pane → file

1. **Pane → agent process.** List panes and find the one running `claude`; grab its `pane_pid` / tty.
2. **Process → cwd.** `readlink /proc/<claude_pid>/cwd`.
3. **cwd → project dir.** Replace `/` with `-`, prefix with `~/.claude/projects/`.
4. **Project dir → live transcript.** Pick the `*.jsonl` with a current mtime (the one being written this minute).
5. **Confirm.** `grep -c` the file for a string unique to the current conversation.

### Script

Run with no arguments to resolve the **current** session (walks this process's own ancestry). Pass a tmux pane id (e.g. `%11`) to resolve a **peer** pane instead.

```bash
#!/usr/bin/env bash
# get-history-filename — locate a Claude Code session transcript from a tmux pane
set -uo pipefail

pane="${1:-}"

# 1. Resolve the claude PID
if [ -n "$pane" ]; then
  pane_pid=$(tmux list-panes -a -F '#{pane_id} #{pane_pid}' 2>/dev/null \
             | awk -v p="$pane" '$1==p{print $2}')
  # the pane_pid is the pane's shell; descend to its claude child (exact name match)
  child=$(pgrep -P "$pane_pid" -x claude 2>/dev/null | head -1)
  claude_pid=${child:-$pane_pid}
else
  # walk our own ancestry up to the claude process
  pid=$$ ; claude_pid=""
  while [ "${pid:-0}" -gt 1 ] 2>/dev/null; do
    # match the process *name*, not a cmdline substring — a wrapper shell that
    # sources ~/.claude/shell-snapshots/* would otherwise false-match on ".claude".
    [ "$(cat "/proc/$pid/comm" 2>/dev/null)" = claude ] && { claude_pid=$pid; break; }
    # ppid is field 2 *after* the comm field; comm is in parens and may contain
    # spaces/parens, so strip through the last ") " before splitting.
    stat=$(cat "/proc/$pid/stat" 2>/dev/null) || break
    rest=${stat##*) }
    pid=$(set -- $rest; echo "$2")
  done
fi
[ -z "${claude_pid:-}" ] && { echo "no claude process found" >&2; exit 1; }

# 2. cwd  ->  3. project dir
cwd=$(readlink "/proc/$claude_pid/cwd")
proj="$HOME/.claude/projects/$(printf '%s' "$cwd" | sed 's#/#-#g')"
[ -d "$proj" ] || proj=$(dirname "$(find "$HOME/.claude/projects" -name '*.jsonl' -printf '%p\n' | head -1)")

# 4. live transcript (most recently modified)
transcript=$(ls -t "$proj"/*.jsonl 2>/dev/null | head -1)

echo "claude_pid : $claude_pid"
echo "cwd        : $cwd"
echo "project    : $proj"
echo "transcript : $transcript"
```

### Confirming you have the right file

mtime narrows it; content makes it certain. Grep for something said only in this conversation:

```bash
grep -c 'SOME_UNIQUE_PHRASE_FROM_THIS_CHAT' "$transcript"
```

A non-zero count confirms it. To list candidates when several sessions share a cwd, sort by recency:

```bash
find ~/.claude/projects/-home-slomp/ -name '*.jsonl' -mmin -5 -printf '%t  %p\n'
```

### Caveats

- **fd won't reveal it.** Claude doesn't keep the transcript open; don't bother with `lsof`/`/proc/<pid>/fd` for the path — use mtime.
- **Lossy cwd mapping.** Multiple sessions from the same directory collapse into one project dir. Disambiguate by mtime, then by grepping unique content.
- **Compaction / resume.** A long session may roll into a new transcript UUID after context summarization; the *active* file is always the freshest mtime.
- **`pane_pid` is the shell, not the agent.** A tmux pane's `pane_pid` is the login shell; `claude` is its child — descend one level (the script does this with `pgrep -P`).

---

## Codex

### How the path is derived

Codex stores each current-format session transcript at:

```
~/.codex/sessions/YYYY/MM/DD/rollout-<timestamp>-<thread-id>.jsonl
```

- **`<thread-id>`** — exported in the running Codex process environment as `CODEX_THREAD_ID`.
- **`YYYY/MM/DD` and `<timestamp>`** — encoded in the rollout filename. Do not reconstruct these from the clock; find the file by `CODEX_THREAD_ID`.
- Older or imported sessions may exist as root-level `~/.codex/sessions/rollout-*.json` files. Those are real Codex transcripts, but this Codex build's resumable files are the dated JSONL rollouts.

### The chain, pane → file

1. **Pane → Codex process.** Read tmux `pane_pid`; in current Codex npm installs this may be the `node` wrapper process.
2. **Process → thread id.** Read `CODEX_THREAD_ID` from `/proc/<pid>/environ`. If `pane_pid` is a shell wrapper, scan its descendants for a process with that environment variable.
3. **Thread id → rollout file.** Search `~/.codex/sessions` for `*${CODEX_THREAD_ID}*.jsonl`.
4. **Confirm.** `grep -c` the file for a string unique to the current conversation.

### Script

Run with no arguments to resolve the **current** session. Pass a tmux pane id (e.g. `%7`) to resolve a **peer** Codex pane.

```bash
#!/usr/bin/env bash
# get-codex-history-filename — locate a Codex session transcript from a tmux pane
set -uo pipefail

pane="${1:-}"

env_value() {
  # $1=pid, $2=var name. /proc environ is NUL-delimited.
  tr '\0' '\n' <"/proc/$1/environ" 2>/dev/null \
    | awk -F= -v key="$2" '$1==key { sub(/^[^=]*=/, ""); print; exit }'
}

descendants() {
  # Print a shallow process tree rooted at $1. This is enough for pane shell -> node/codex.
  root="$1"
  echo "$root"
  kids=$(pgrep -P "$root" 2>/dev/null || true)
  for kid in $kids; do
    descendants "$kid"
  done
}

# 1. Resolve the candidate Codex process root.
if [ -n "$pane" ]; then
  pane_pid=$(tmux list-panes -a -F '#{pane_id} #{pane_pid}' 2>/dev/null \
             | awk -v p="$pane" '$1==p{print $2}')
  [ -n "${pane_pid:-}" ] || { echo "no pane found for $pane" >&2; exit 1; }
else
  pane_pid=$$
fi

# 2. Find CODEX_THREAD_ID on the pane process or one of its descendants.
codex_pid=""
thread_id=""
for pid in $(descendants "$pane_pid"); do
  value=$(env_value "$pid" CODEX_THREAD_ID)
  if [ -n "$value" ]; then
    codex_pid="$pid"
    thread_id="$value"
    break
  fi
done

[ -n "$thread_id" ] || { echo "no CODEX_THREAD_ID found under pid $pane_pid" >&2; exit 1; }

# 3. Resolve thread id to rollout file.
transcript=$(find "$HOME/.codex/sessions" -type f -name "*${thread_id}*.jsonl" -print | head -1)
[ -n "$transcript" ] || { echo "no Codex rollout JSONL found for thread $thread_id" >&2; exit 1; }

cwd=$(readlink "/proc/$codex_pid/cwd" 2>/dev/null || true)

echo "codex_pid  : $codex_pid"
echo "thread_id  : $thread_id"
echo "cwd        : $cwd"
echo "transcript : $transcript"
```

### One-liner for your own Codex session

When already inside Codex, the environment normally has `CODEX_THREAD_ID`, so this is enough:

```bash
find ~/.codex/sessions -type f -name "*${CODEX_THREAD_ID}*.jsonl" -print
```

### Confirming you have the right file

```bash
grep -c 'SOME_UNIQUE_PHRASE_FROM_THIS_CHAT' "$transcript"
```

A non-zero count confirms it. To inspect recent Codex rollout candidates:

```bash
find ~/.codex/sessions -type f -name '*.jsonl' -mmin -10 -printf '%t  %p\n'
```

### Caveats

- **Use `CODEX_THREAD_ID`, not mtime, when possible.** Multiple Codex sessions can share the same cwd and recent mtimes.
- **The pane command may be `node`.** npm-installed Codex runs through a Node wrapper; the process environment still carries `CODEX_THREAD_ID`.
- **Copied JSONL files may not be indexed yet.** `codex resume --all` can see dated rollout files even if `codex doctor` says state DB rows are missing.
- **Legacy root-level `.json` files are different.** They are transcript data, but not the current resumable rollout JSONL format.
- **macOS differs.** This script uses Linux `/proc`. On macOS, prefer resolving the thread id from the Codex process environment if available through your process tools, then use the same `~/.codex/sessions` filename search.

---

## Other harnesses

_To be added._ (Each harness gets its own subsection here with its storage layout and a pane → file recipe — e.g. Aider or a custom in-house harness.)
