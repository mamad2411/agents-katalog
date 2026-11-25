---
name: pi-agent
description: "Delegate coding/tasks to pi CLI over RPC with persistent, resumable sessions."
version: 1.0.0
author: Dustin Chadwick (@ShaggyD)
license: MIT
metadata:
  hermes:
    tags: [Coding-Agent, RPC, Session-Continuity, Automation, JSONL]
    related_skills: [opencode, codex, hermes-agent]
---

# Pi Agent -- RPC Session Orchestrator

Use `pi --mode rpc` for a long-lived, bidirectional coding agent process with durable session continuity and machine-readable events.

## Problem

Remote coding agents lose state when sessions break or auth expires. Running pi in RPC mode means managing JSON event streams, remembering session file paths, and wiring up stdin/stdout yourself. When something fails, the whole session is gone.

## Built

Complete coverage of the pi RPC protocol: session lifecycle (start, resume, fork), JSON command structure, event stream parsing, response extraction, and failure recovery patterns. Includes the native Hermes `pi_agent` tool plugin for full lifecycle management without manual process wrangling.

## Outcome

Your coding agent survives terminal restarts, auth reconnects, and network blips without losing context. Sessions are resumable, events are structured, and the failure modes you'd hit on day one are already handled.

## When to use

- You need multi-turn control of pi from another orchestrator
- You need resumable session continuity across restarts
- You want structured event streaming (`message_update`, `tool_execution_*`, `turn_end`)
- You need session branching (`fork`) and session switching (`switch_session`)

## Prerequisites

- `pi` CLI installed and on PATH
- RPC mode available: `pi --mode rpc --help`
- For persistence, do NOT use `--no-session`

## Core continuity model

1. Start pi in RPC mode.
2. Send JSON commands over stdin (one JSON object per line).
3. Read JSON lines from stdout (events + command responses).
4. Persist `sessionFile` from `get_state`.
5. Resume later with `pi --mode rpc --session <sessionFile>`.

Fallback: `pi --mode rpc -c` resumes the latest session.

## Start / resume patterns

```bash
# new session in current directory
pi --mode rpc

# new session in a specific project directory
cd ~/code/my-project && pi --mode rpc

# resume exact session
pi --mode rpc --session /path/to/session.jsonl

# resume last session
pi --mode rpc -c
```

## Minimal command flow

```json
{"type":"prompt","message":"Summarize failing tests and suggest fixes."}
{"type":"get_state"}
{"type":"get_session_stats"}
{"type":"get_fork_messages"}
{"type":"fork","entryId":"abc123"}
```

> Important: the prompt payload key is `message` (not `prompt`). Using `prompt` can fail with runtime errors in current pi builds.

## Event model you should expect

- `agent_start` / `agent_end`
- `turn_start` / `turn_end`
- `message_update` (streaming text/tool deltas)
- `tool_execution_start` / `tool_execution_update` / `tool_execution_end`
- `compaction_start` / `compaction_end`

Use `turn_end` or `agent_end` as completion boundaries for a prompt cycle.

## Hermes integration patterns

### A) Native Hermes `pi_agent` tool (preferred)

Use the built-in stateful tool when available:

- `action: start` — launch `pi --mode rpc` in a specific `workdir` (optional `pi_session_path`, `provider`, `model`)
- `action: send` — send `message` or raw `command` JSON; auto-assigns/accepts `request_id`
- `action: poll` — incremental event retrieval with cursor/offset semantics
- `action: wait` — block until completion boundary (default `until_event="turn_end"`) with timeout
- `action: list` — inspect active + detached sessions
- `action: resume` — revive a detached session by starting a new live process (uses saved `sessionFile` when available; otherwise starts fresh in the same workdir and returns a warning)
- `action: prune` — remove stale detached metadata entries older than `max_age_days` (default 7)
- `action: stop` — terminate a live session

#### Quick usage (copy/paste)

```json
{"action":"start","workdir":"/home/dchadwick/dev/thoughtspace"}
```

```json
{"action":"send","session_id":"<SESSION_ID>","message":"Summarize the failing tests and propose the smallest fix.","request_id":"req-1"}
```

```json
{"action":"wait","session_id":"<SESSION_ID>","request_id":"req-1","until_event":"turn_end","timeout_seconds":90}
```

```json
{"action":"poll","session_id":"<SESSION_ID>","limit":200}
```

```json
{"action":"list"}
```

```json
{"action":"resume","session_id":"<DETACHED_SESSION_ID>"}
```

```json
{"action":"prune","max_age_days":7}
```

```json
{"action":"stop","session_id":"<SESSION_ID>"}
```

#### Typical loop (5 lines → 6 for complex prompts)

```text
1) {"action":"start","workdir":"/path/to/repo"}
2) {"action":"send","session_id":"<SESSION_ID>","message":"...","request_id":"req-1"}
3) {"action":"wait","session_id":"<SESSION_ID>","request_id":"req-1","until_event":"turn_end","timeout_seconds":180}
4) {"action":"poll","session_id":"<SESSION_ID>","limit":200}
5) {"action":"stop","session_id":"<SESSION_ID>"}
```

**For complex prompts** (multi-turn research, file reading, test running): `wait()` returns massive streaming delta data (400K–800K+ chars) that gets truncated. The clean text response is in the session JSONL file — see `references/response-extraction.md` for how to extract it. Add a 6th step: extract from session file after `turn_end`.

```text
1) start → 2) send → 3) wait (until turn_end) → 4) extract text from session file → 5) poll (to sync) → 6) stop
```

Simple prompts (one-shot code gen) resolve in 15–30s and the text is available directly in `wait()` output.

### B) Process-tool fallback

If native `pi_agent` is unavailable, run pi in a Hermes background process and interact with `process`:

1. Start: `terminal(..., background=true, pty=false)`
2. Send JSON: `process(action="submit", data='{"type":"prompt",...}')`
3. Poll/log: `process(action="poll"|"log")`
4. Stop: `process(action="kill")`

## `pi_agent` tool runtime behavior (important)

- Session metadata persists at `~/.hermes/state/pi_agent_sessions.json`.
- After Hermes process restart, previously known sessions are restored as **detached** metadata entries.
- Detached sessions are listable for continuity context, but **not writable** (`send` will fail) because stdio handles cannot be reattached safely.
- Use `action: resume` on a detached session to spawn a new live RPC process:
  - preferred path: reuses saved `sessionFile` (`--session <file>`) for continuity
  - fallback path: if `sessionFile` is missing, starts a fresh RPC process in the same workdir and returns a warning
- Use `action: prune` periodically to remove stale detached metadata (`max_age_days`, default 7).

## Project-directory startup (important)

RPC sessions inherit the current working directory unless explicitly set. For project-specific work, start pi in the target repo directory.

Examples:

```bash
cd ~/dev/thoughtspace && pi --mode rpc
# or from wrappers/scripts: subprocess.Popen(..., cwd="~/dev/thoughtspace")
```

Without this, repository checks (branch status, diffs, tests) may run in the wrong location.

## Authentication and key resolution (important)

For `opencode-go`, credentials should be available to the spawned pi process via one of these:

1. `~/.pi/agent/auth.json` provider entries (preferred):

```json
{
  "opencode-go": { "type": "api_key", "key": "..." },
  "opencode": { "type": "api_key", "key": "..." }
}
```

2. Environment variable `OPENCODE_API_KEY` in the process environment.

If using a Python wrapper, do not assume shell startup files are loaded — explicitly pass `env=...` to `subprocess.Popen(...)` and/or load `.env` yourself.

## RPC prompt payload shape

Use `message` for `type: "prompt"` payloads:

```json
{"type": "prompt", "message": "Hello"}
```

Using `{"prompt": ...}` can fail with provider/runtime errors.

## Pitfalls

1. **Delegate git operations to pi — don't run them yourself via terminal**
   - When you need to stage, commit, or push changes, hand the work to pi agent with a structured prompt. Give it the exact file lists, commit messages, and order of operations in one message. This session proved pi handles multi-commit workflows reliably.
   - Example pattern: `"Stage these files, commit with message X. Then stage these, commit with message Y. Do them in order."` — pi executes them sequentially, each as its own turn.
   - **Always run `npm test` (or equivalent) after any code change** before committing. Dusty explicitly emphasizes this. If pi agent made the changes, ask it to run tests as the final step of the commit workflow.
   - **Don't** run `git add` / `git commit` yourself via the terminal tool when pi is available for the repo. The user expects the agent to do the git work.

2. **Distinguish poll noise from genuine model slowness**
   - When you `poll()` while a turn is in progress, you'll see character-level `thinking_delta` events and tool stdout streaming — this is **intermediate streaming events**, not the agent typing slowly. Some agents finish fast; you're just reading raw event fragments.
   - **Correct assessment approach**: `send()` the prompt, then `wait(until_event='turn_end')` to block for completion, then `poll()` for the final result. The time between `send` and `turn_end` is the true wall-clock time — not what the character deltas suggest.
   - **`poll()` during an active turn** shows every `message_update` (thinking fragment by fragment), `tool_execution_update` (stdout line by line). These make the agent look glacially slow when it's actually running at normal speed.
   - If you need a progress check during a long-running turn, just check `total_seen` increasing — don't read the individual delta events.
   - **However, some models ARE genuinely slow at multi-turn code analysis.** Deepseek-v4-flash has been observed spending 10+ turns and generating 10–20k tokens per turn just exploring file structures (reading, ls, searching) without writing any code. In this case it's NOT poll noise — the model is genuinely spending time churning through exploration.
   - **How to tell the difference:**
     - Poll noise: model finishes its turn quickly (<30s per turn for simple reads), but streaming fragments make it look slow
     - Genuine slowness: each turn takes 60s+, the model reads 3–5 files per turn, and needs 8+ turns of pure exploration before writing any output
   - **What to do when a model is genuinely slow:**
     - Follow the escalation path (see `references/model-escalation.md`): switch to a stronger model, re-send the prompt, switch back after breakthrough
     - If the escalation model is unavailable (no credentials), fall back to direct work with terminal/file tools and report to the user
     - Do NOT wait for the slow model to eventually finish — it's not a performance issue, it's a capability gap

3. **Follow user-specified escalation paths — don't kill the agent**
   - If the user says "start with model X, escalate to model Y at barriers, then downgrade back" — **follow it exactly**. Do not kill the pi agent and take over directly via terminal or other tools. The user expects the agent to self-escalate.
   - When stuck (prolonged silence >3 minutes with no tool calls), send a `set_model` command to switch to the escalation model, re-send the prompt, then `set_model` back after breakthrough.
   - See `references/model-escalation.md` for exact commands and lifecycle.

4. **Mixing logs and JSON on stdout**
   - Ensure your wrapper only parses valid JSON lines.

5. **Forgetting to persist `sessionFile`**
   - Without it, exact continuity is harder (you only have `-c`).

6. **Assuming one response line per command**
   - RPC emits asynchronous events; match on command `id`/`command` response.

7. **Using `--no-session` accidentally**
   - This disables persistence and breaks restart continuity.

8. **Launching in the wrong repository**
   - RPC inherits current working directory. Start pi from the target project root (or set `cwd` in your wrapper), otherwise branch/diff analysis is against the wrong repo.

9. **`wait()` returns massive output for multi-turn prompts**
   - When pi runs 5–12 tool-calling turns (reading files, running tests, git analysis), the `wait()` response bundles all streaming deltas — think fragments, partial tool calls, text — into one 400K–800K+ char blob. This gets truncated in tool output.
   - **Fix:** Increase `timeout_seconds` to 180+ for research prompts. Extract the clean final text from the session JSONL file instead of parsing `wait()` output (see `references/response-extraction.md`).

10. **Auth looks like transport failure**
   - If prompt calls fail with `No API key found for unknown`, RPC is healthy but provider auth is missing. Fix auth first (`OPENCODE_API_KEY` or `pi /login`) before debugging your wrapper.

11. **Stale sessions accumulate and consume resources**
   - Each `start` spawns a live pi process that sits in the background until killed. Over a long session you can accumulate 5–10 orphaned pi processes consuming RAM and file handles.
   - **Prevention:** Always `stop` sessions when done with them. Use `action: stop` with `session_id`.
   - **Cleanup:** Run `action: list` to see all sessions, then `action: stop` on each stale one. Or kill by PID: `ps aux | grep 'pi.*rpc' | grep -v grep` then `kill <PID>`.
   - **Auto-cleanup:** The `action: prune` command only removes detached metadata entries (session file references), **not** live processes. Use `action: stop` for live sessions.


See `references/rpc-pitfalls.md` for concrete error transcripts and fast triage checks.

## References

- `references/auth-and-extension-troubleshooting.md` — common auth and extension startup failures, plus deterministic fixes.
- `references/response-extraction.md` — extracting pi's final text response from the session JSONL file when `wait()` returns truncated streaming delta data.
- `references/hermes-stateful-tool-integration.md` — native Hermes `pi_agent` tool wiring (`start/send/poll/wait/stop/list`), registry verification, persistence file, and restart gotchas (detached sessions).
- `references/rpc-pitfalls.md` — concrete error transcripts and fast triage checks for RPC issues.
- `references/model-escalation.md` — switching mid-session between models (cheap → strong → back) when the user specifies an escalation path.
- `references/model-capability-discovery.md` — testing which models support vision, transcription, or other capabilities; cost comparison before choosing a model.
## Verification checklist

- [ ] `pi --mode rpc --help` works
- [ ] `get_state` returns a `sessionFile`
- [ ] restart with `--session <that file>` succeeds
- [ ] prompt cycle reaches `turn_end` or `agent_end`
- [ ] `fork` and `switch_session` tested if workflow needs branching
