---
name: tmux-agent-tools
description: Use when running or supervising Claude Code or Codex CLI as managed tmux workers via claude-tmux, codex-tmux, or tmux-agent-sessions. Covers start/resume, send, wait, capture, status/doctor/self-test, list, stop/cleanup, human approval gates, and multi-agent pair-review, critic, debate, dialogue, or fanout. Trigger on tmux as the execution layer for managed AI agent sessions; not for general tmux config, theming, shell wrappers, non-tmux headless claude/codex, or human team debate.
---

# Tmux Agent Tools

## Overview

Use `claude-tmux` and `codex-tmux` as the canonical interface for any long-running Claude Code or Codex CLI session in tmux. Prefer these wrappers over hand-written `tmux send-keys` flows because they provide consistent session naming, capture, wait, status, secret injection, and cleanup.

Use `tmux-agent-dialogue` (and its `pair-review` / `critic` / `debate` presets) when the task is a bounded two-party exchange with a JSONL transcript. Use `tmux-agent-fanout` for parallel one-to-many work. Use `tmux-agent-sessions` for read-only inventory across all wrappers.

Local and SSH sessions keep the pane open after the agent CLI exits, showing the exit code so failures can still be captured.

The wrapper scripts are bundled at:

- `scripts/claude-tmux`
- `scripts/codex-tmux`
- `scripts/tmux-agent-dialogue`
- `scripts/tmux-agent-sessions`
- `scripts/tmux-agent-fanout`

If the commands are not on `PATH`, resolve them from the skill directory and run the script path directly.

## When Not To Use

- One-off non-interactive shell commands — run them directly.
- A simple file read, search, test, or build command — don't spawn a tmux agent for it.
- Externally visible, destructive, or privacy-sensitive work unless the user has already authorized it.

## Command Choice

- `claude-tmux` when the worker should run Claude Code; `codex-tmux` when it should run Codex CLI.
- `start` for a local working directory; `start-ssh` when tmux stays local but the CLI runs over SSH.
- `resume` (claude or codex) when an existing session ID should continue inside a managed tmux session.
- The subcommands `send`, `capture`, `wait*`, `status`, `attach`, `stop`, and `result` all take the **agent name** you chose, not the full tmux session name.
- If you don't know which wrapper owns a session, `tmux-agent-sessions list --name <n>` resolves it.

## Core Workflow

1. **Start** with a short stable name:

```bash
codex-tmux start --exact worker ~/github/project 'Read the repo and report the failing test. Write $TMUX_AGENT_RESULT when done.'
claude-tmux resume --exact worker ~/github/project ee5aca88-a1af-48d3-af21-54f60d618f22
```

2. **Send** follow-up work without attaching:

```bash
codex-tmux send worker 'Now implement the smallest fix and run the targeted test.'
codex-tmux send-wait-literal worker 'End with the split marker described here.' '[CODEX-01]' 180
```

Use `send-wait-literal` for marker-driven orchestration when stale pane content may already contain an older marker. Keep the literal out of the sent prompt (or split it in the prompt instructions) so the prompt echo cannot satisfy the wait.

3. **Wait** for pane stability or a marker before reading output:

```bash
codex-tmux wait worker 180                                # idle stability
codex-tmux wait-literal worker '[CODEX-01]' 180           # literal marker
codex-tmux wait-text --literal worker '[CODEX-01]' 180    # same, explicit
codex-tmux wait-and-capture --literal --marker '[DONE]' --tail 80 --strip-ansi --json worker 180
```

`wait-literal` (or `wait-text --literal`) is required when the marker contains regex metacharacters like `[`, `]`, `(`, `)`, `.`, `*`, `?`. Use plain `wait-text` only when you intentionally want regex matching.

For **alternation markers** (e.g. wait for `[DONE]` OR `Need approval`), use `wait-and-capture` with an escaped regex; do NOT race two `wait-literal` calls. See `references/cheatsheets.md` for the worked example.

4. **Inspect or clean up**:

```bash
codex-tmux status worker
codex-tmux status --json worker
codex-tmux env-doctor worker
codex-tmux doctor
codex-tmux self-test
codex-tmux stop worker
```

`status --json` is the stable automation contract. Treat `running:false` as authoritative even if the tmux session still exists for capture.

Use `env-doctor [name]` before deeper debugging when an agent CLI uses the wrong provider, model, base URL, token, timeout, login state, or behaves differently inside tmux than outside tmux. It compares the caller environment, tmux global environment, and the running agent child process environment, redacting token/key values. This catches tmux-side provider pollution before chasing shell startup files, app switchers, or CLI login state.

5. **Read the agent's structured result** instead of scraping the pane:

```bash
codex-tmux result --field '.status' --wait 30 --json worker
```

Agents should write `$TMUX_AGENT_RESULT` (a JSON file at `$TMUX_AGENT_DIR/<name>/result.json`) with `schema_version: 1`, `status`, `summary`, `artifacts`, `errors`. Parent branches on `.present` → `.valid` → `.body` in that order. See `references/contracts.md`.

## Approval gates

To pause a worker until a human writes a decision file:

```bash
marker=/tmp/agent-7/approve.txt
codex-tmux wait-and-capture --literal --marker '[NEEDS-APPROVAL]' \
  --pause-until-file "$marker" --pause-timeout 1800 worker
# Operator (another shell): echo approve > "$marker"  → exit 0
#                           echo reject  > "$marker"  → exit 7
# Timeout fires             →                            exit 8
```

While blocked, `$TMUX_AGENT_DIR/<name>/approval-status.json` reports `state: "awaiting_approval"`. Use this gate for any destructive/irreversible action a worker is about to take.

## Orchestrator playbook (multi-agent collaboration)

These tools are for **long-running supervised work**, not for unbounded agent sprawl. Before spawning more than one worker — including any `dialogue` / `pair-review` / `critic` / `debate` / `fanout` — apply all four rules:

1. **Ask the user up front: tool (claude or codex), model tier, and effort/reasoning level per worker.** Never assume defaults.
2. **Declare an explicit worker upper bound** (e.g., "I will run at most 3 workers; if that is insufficient I will stop and report, not spawn helpers").
3. **Forbid cascade spawning** by writing a literal ban into each worker's prompt body: "Do not call `claude-tmux`, `codex-tmux`, `tmux-agent-fanout`, or `tmux-agent-dialogue`. Do not start background jobs. Do not SSH out. Reason only from provided context and write `$TMUX_AGENT_RESULT` when done." The wrappers have no kernel-level sandbox; this prompt-level barrier is the only stopgap.
4. **Bound dialogue length.** `critic` and `debate` require positive even `--turns`. Pick a small number (2–6).

For credential-free smoke tests of any preset, use `--agent-a fake --agent-b fake`. Real `codex` / `claude` participants only after explicit user authorization.

Cross-review pattern (workers produce → dialogue reviews): see `references/multi-agent.md`. Fanout details, dialogue presets, SSH participants, participant profiles, and `github-comment` (which never posts without `--post-github-comment`): same file.

Always run `tmux-agent-dialogue validate-transcript --transcript <path>` before summarizing, sharing, or posting a transcript.

## Safety

- Both wrappers run their CLIs with permissive flags (`--dangerously-skip-permissions` for Claude, `--yolo` for Codex). Do not use them for destructive, privacy-sensitive, externally visible, payment, or irreversible operations without explicit user authorization.
- `claude-tmux status <name>` reports a `diagnostic` when the pane looks like it is waiting for a first-run or permission confirmation. It does NOT auto-accept that prompt.
- Prefer `doctor` and `self-test` before debugging agent behavior; they verify wrapper dependencies and tmux capture/wait without starting a real agent.
- For secret injection (`--secret KEY=URI`) and audit log enablement (`TMUX_AGENT_TOOLS_AUDIT_LOG`): see `references/security.md`. Missing secrets fail closed before the session is created.

## Session naming

- Without `--exact`, `start` appends a random suffix to avoid collisions.
- With `--exact`, the session uses the requested name exactly under the tool prefix.
- **Single caller per agent name.** Two `start --exact same-name` kills the first. Wrapper state under `$TMUX_AGENT_DIR/<name>/` is NOT lock-protected.

## Remote sessions

`start-ssh` when the target repo is on another host:

```bash
claude-tmux start-ssh --exact review example-host ~/github/project 'Review the diff and return findings only.'
```

Requirements: local `tmux`; remote shell can resolve `claude` or `codex` on `PATH`; SSH target preconfigured.

## References

Load these only when you hit the relevant scenario — they are not needed for routine use:

- `references/cheatsheets.md` — scenario → command, token-efficient patterns, completion-signaling matrix, marker pitfalls (including the alternation case), failure-mode triage.
- `references/multi-agent.md` — dialogue / pair-review / critic / debate / fanout details, worker→dialogue bridge pattern, SSH participants, participant profiles, github-comment (no posting by default).
- `references/contracts.md` — `status --json` stable fields, `result.json` schema with worked example, approval-gate state/exit codes, concurrency model, cost accounting, inventory/cleanup.
- `references/security.md` — secret injection backends, audit log operator surface, full environment-override table, pre-flight checks.
