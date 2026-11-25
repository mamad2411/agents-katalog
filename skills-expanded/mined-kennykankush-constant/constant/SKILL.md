---
name: constant
description: "Carry or consult a conversation between agent CLIs (Codex, Claude Code, and OpenCode; Gemini as a source) with Constant. Use when the user asks to move, hand off, fork, or continue this thread (or another one) in a different agent CLI, ask another runtime about it, find or read back an earlier carried conversation, or mentions Constant by name. Do not use for general session search unrelated to carrying."
allowed-tools: Bash(constant --version), Bash(constant --help), Bash(constant doctor:*), Bash(constant sessions:*), Bash(constant ps:*), Bash(constant route:*), Bash(constant recall:*), Bash(constant ask:*)
---

# Constant

Constant carries one conversation between agent CLIs. It reads a runtime's
local session, strips it to the conversation, redacts secrets, records a
snapshot, and writes a session the target runtime can resume natively. The
target then continues the thread with the history in its own context.

Supported targets: `codex`, `claude`, `opencode`. Gemini sessions can be
carried from, not into.

## Learn the installed CLI

The installed binary is the authority for syntax. Check it first:

```bash
constant --version
constant doctor --json      # installed runtimes, versions, and whether each is validated
```

`constant --help` prints the full command reference. `constant integration`
shows which runtimes have this guide installed as a skill.

Use `--json` (or `--plain`) on every read command. Several commands open an
interactive picker or explorer when they run in a terminal with no arguments
(`constant resume`, `constant sessions`, `constant trail`). Never run
`constant host` or `constant resume` from an agent: they take over the
terminal with a live runtime.

## Carry this conversation to another runtime

Name your own session explicitly instead of relying on "newest in this
folder":

| You are running in | Your session id |
| --- | --- |
| Claude Code | `$CLAUDE_CODE_SESSION_ID` |
| Codex | `$CODEX_THREAD_ID` |
| other | `constant sessions --from <runtime> --json`, newest `id` for this `cwd` |

Preview, then carry:

```bash
constant carry --session "$CLAUDE_CODE_SESSION_ID" --to codex --dry-run --json
constant carry --session "$CLAUDE_CODE_SESSION_ID" --to codex --json
```

The JSON result includes:

- `id`: the target runtime's session id
- `resume`: the exact command that resumes it (for example `codex resume <id>`)
- `handle`: the conversation's stable name, such as `cobalt-37`
- `receipt`: what was kept, dropped, and redacted (`turns`, `tools`,
  `dropped_tools`, `dropped_scaffold`, `dropped_reasoning`, `redactions`)

Give the user the `resume` command and the receipt. Carrying does not move
the user's terminal; the user, or a terminal multiplexer they asked you to
drive, runs the `resume` command.

Your current turn is still being written while you run the carry, so the
carried copy ends at the last completed turn. Say so if it matters.

Options:

- `--with-tools`: also carry tool calls and their results (redacted and size
  capped). Without it, only the conversation text carries.
- `--new`: fork a separate continuation instead of refreshing the existing
  target session for this conversation.
- `--render paged`: for very long threads, carry a compact layout (summary
  card, index, recent turns verbatim). Older turns stay readable with
  `constant recall`.

Carrying again to the same target refreshes that target session in place.
The source session is never modified.

## Ask another runtime

When the user wants a second runtime's judgment without taking over the
terminal, ask it headlessly:

| You are running in | Your session id |
| --- | --- |
| Claude Code | `$CLAUDE_CODE_SESSION_ID` |
| Codex | `$CODEX_THREAD_ID` |

```bash
constant ask --to claude --session "$CODEX_THREAD_ID" \
  --question "Review the current plan for hidden failure modes." --json
constant ask --to codex --session "$CLAUDE_CODE_SESSION_ID" \
  --question - < question.txt --json
```

`ask` forks the conversation into a new target projection, runs that runtime
non-interactively, and returns its answer. It does not take over the terminal,
does not modify the source conversation, and never refreshes an existing target
projection. The JSON result includes `answer`, `session`, `resume`, `handle`,
and the carry `receipt`.

The question is sent over stdin, not exposed in the provider's argv. Use
`--with-tools` to include redacted tool history, and `--timeout SECS` to bound
the call. Only `codex` and `claude` are verified `ask` targets today. Treat an
ask as billable provider work: use it only when the user asks or authorizes it.
The target keeps its own permissions and sandbox settings and may inspect or
modify the workspace accordingly.

## Find conversations

```bash
constant sessions --json               # carryable sessions for this folder, newest first
constant sessions --all --json         # every runtime store
constant sessions auth --json          # filter by name or id
constant ps --json                     # agent sessions running right now, with resume commands
constant route --json                  # carry lineage (which session came from which)
```

## Read history back

```bash
constant recall cobalt-37              # a carried conversation's filed turns, by handle
constant recall cobalt-37 ch04 12      # one turn, verbatim
constant recall cobalt-37 ch04 3-9     # a range
constant export --session <id> --out thread.json   # distilled, redacted conversation as JSON
```

`recall` and `export` are read-only.

## Rules

- Carry only when the user asks for it. A carry writes a new session into
  the target runtime's store (`~/.codex`, `~/.claude`, or OpenCode through
  its own import command).
- Ask only when the user asks or authorizes it. An ask carries the thread and
  invokes the target runtime, which may consume paid provider usage.
- Do not delete sessions, snapshots, or `~/.constant`. Constant never
  overwrites an original session; keep it that way.
- Never run the `gemini` binary to inspect sessions. Carry gemini sessions
  with `constant carry --session <path> --to <target>` instead.
- Redaction covers common secrets (API keys, tokens, private keys, auth
  headers, email addresses), not everything. Do not carry a thread into a
  runtime the user would not want reading it.
- If `doctor` shows a runtime version that is not validated, tell the user
  before carrying into it.
