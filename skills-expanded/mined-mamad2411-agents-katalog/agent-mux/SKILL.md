---
name: agent-mux
description: |
  Cross-engine dispatch layer for AI coding agents. Use when you need to:
  launch a worker on Codex/Claude/Gemini/agy/Grok, recover a timed-out dispatch, steer
  a running agent, or fan out parallel work. Profiles live in ~/.agent-mux/prompts/.
---

# agent-mux

## QUICKSTART (95% of use cases)

**1. Discover workers:**
```bash
agent-mux config prompts        # live roster with effort defaults
agent-mux config prompts --json # structured
agent-mux config engines --json # engine capabilities + model allowlists
```
Selection: scout for reads, lifter for writes, architect for plans, grunt for bulk edits.

**2. Profile dispatch (the 80% case):**
```bash
agent-mux -P=lifter --cwd /repo "Fix retry logic in src/client.go" 2>/dev/null
```
Blocks until done. Result is stdout JSON with `status`, `response`, `activity.files_changed`.

**3. Prompt-file dispatch (for heredoc quoting issues):**
```bash
cat > /tmp/prompt.md << 'EOF'
Fix the `parseConfig()` function. Handle edge cases:
- Empty input returns `{}`
- Nested backticks in strings
EOF
agent-mux -P=lifter -C=/repo --prompt-file=/tmp/prompt.md
```
Or use `--stdin` JSON mode for full quoting control.
`--stdin` implies `--yes`, so machine JSON dispatches do not stop for
interactive confirmation by default.

**4. Effort note:**
Don't override `-e` unless upgrading. Check `config prompts` for profile defaults -- passing `-e=high` to an xhigh profile (scout, auditor, grunt, architect) is a DOWNGRADE.

For opt-in GPT-5.6 depth, inspect `config engines --json` first. Sol and Terra may expose `max`/`ultra`; Luna stops at `max`; GPT-5.5/5.4-family models stop at `xhigh` on Codex 0.144.1. Max/Ultra require an explicit model and verified live/bundled catalog support:

```bash
agent-mux -E=codex -m=gpt-5.6-sol -e=max --cwd /repo "hard bounded task"
```

Ultra may trigger native Codex collaboration, but delegation is not guaranteed. `--reasoning` is a deprecated one-release alias; use `--effort`, and never pass differing explicit values.

**Key flags:** `-P` profile, `-E` engine, `-m` model, `-e` effort, `--cwd` / `-C` cwd, `--async`, `--timeout`. Prefer spelling `--cwd` in plans for clarity. Note: `-E` (engine) and `-e` (effort) are different — case matters.

**5. Sync wait + result:**
```bash
agent-mux -P=lifter --cwd /repo "task"  # blocks until done
# stdout is JSON: {"status":"completed","response":"...","activity":{"files_changed":2},...}
```

**Async-first:** Prefer `--async` for dispatches over 2 minutes — lets you monitor, steer, or bail early. Sync is fine for quick probes.

**6. Async pattern:**
```bash
agent-mux -P=scout --async --cwd /repo "probe" > /tmp/dispatch.json 2>/dev/null &
# ... do other work ...
wait  # shell wait: waits for the async launcher process to finish writing the ack
ID=$(jq -r .dispatch_id < /tmp/dispatch.json)
agent-mux wait --poll 30s "$ID" 2>/dev/null
RESULT=$(agent-mux result "$ID" --json 2>/dev/null)
printf '%s\n' "$RESULT" | jq -e '.status == "completed"' >/dev/null
```
Note: `--async` does NOT daemonize -- the CLI writes an ack and keeps a host process alive. Shell `&` is required for true parallel startup. `wait --poll <duration> <id>` is the lifecycle wait primitive; `result <id> --json` is the structured collection primitive.

---

## DETAILS (remaining 5%)

**1. Engine override:**
```bash
agent-mux -P=researcher -E=gemini -m gemini-3.1-pro-preview --cwd /repo "Analyze auth module"
```
- **Codex**: implementation, debugging, precise edits. Model discovery uses the PATH-resolved CLI once per process: live catalog, bundled fallback, then conservative legacy fallback. `DispatchSpec.Effort` is forwarded on initial and resume invocations.
- **Claude**: planning, synthesis, review
- **Gemini**: analysis, second opinion (models: `gemini-3-flash-preview`, `gemini-3.1-pro-preview`)
- **agy**: experimental CLI-first model access. Plain stdout; agent-mux internally invokes the local agy CLI with its fixed `--sandbox`, discovers Antigravity conversation IDs from `agy.log`, and uses inbox + `--conversation` for nudge/redirect resume. Operator-supplied sandbox/permission/reasoning/max-turn/full-access options are rejected. This does not imply plugins, MCP, browser automation, Google services, or provider service actions.
- **Grok**: Grok Build CLI support. Default dispatch is headless `prompt-file` plus streaming JSON with exact UUID resume, adapter-owned prompt/session/debug files, model `grok-4.5` by default, omitted native sandbox flags by default, and public artifact scanning with private Grok sidecars excluded. Opt-in v1.5 structured reports use private prompt-file transport plus `grok-worker-report-schema=agent-mux.worker-report.v1`; this is text/code-only, fake-covered, and live-smoke-proven on Grok CLI 0.2.93 for bounded worker reports. `worker_report.json` is the sanitized public report sidecar; `grok_prompt.md` sidecars are private. Web/X search, image input/output, structured activity, token/cost usage, custom sandbox aliases, native allow/deny, max-turns, plugins/MCP/hooks/memory/subagents, and GAAL-native indexing are not claimed. Use `agent-mux config engines --json` for the active Grok model allowlist; refresh explicitly with `agent-mux config engines --refresh-models --engine grok --json`.

Gemini ignores `-e` -- use model selection for depth control.

**2. Steering:**
```bash
agent-mux status <dispatch_id> --json 2>/dev/null
agent-mux steer <dispatch_id> redirect "Narrow scope to src/parser only; skip the broad audit." 2>/dev/null
agent-mux wait --poll 30s <dispatch_id> 2>/dev/null
agent-mux steer <dispatch_id> abort 2>/dev/null
```
- `status <id> --json` is the one-off live check. Do not poll status in a loop.
- `steer <id> redirect "new direction"` narrows or redirects a running worker; then wait and collect result.
- `steer <id> nudge "message"` asks for a wrap-up/status nudge.
- `steer <id> abort` SIGTERMs async host when live; otherwise writes `control.json` for the watchdog.

**3. Data model (3 paths):**
- `~/.agent-mux/dispatches/<ULID>/` -- durable (meta.json, result.json)
- `$XDG_RUNTIME_DIR/agent-mux/<ULID>/` or `/tmp/agent-mux-$UID/<ULID>/` -- runtime (events.jsonl, inbox.md)
- `~/.agent-mux/prompts/` -- profiles; `<cwd>/.agent-mux/` -- skills/, hooks/

**4. Gaal tracing:** (session_id available after session start; absent for startup failures; Grok session IDs are exact UUIDs for agent-mux resume and are not GAAL-native trace IDs)
```bash
jq -r .session_id ~/.agent-mux/dispatches/<id>/meta.json
gaal inspect <session_id>
```

**5. Bash timeout:**
Claude Code defaults to 120s. Long dispatches need explicit `timeout: 300000` or `run_in_background: true` on the Bash tool call.

**6. Recovery:**
- `timed_out` + `activity.files_changed` non-empty -> `--recover=<id>` with a continuation prompt
- `timed_out` + empty `activity.files_changed` -> reframe into a narrower fresh dispatch
- `failed` -> check cause, retry once or escalate

```bash
agent-mux -P=lifter --recover=<id> --cwd /repo "Continue from the existing edits. Finish remaining parser tests."
```

**7. Landmines:**
- `--async` does NOT daemonize -- use shell `&`
- `status: completed` does not mean task success -- check `response`
- `-e` is effort, `-E` is engine (case matters)
- Codex Max/Ultra require `-m`; legacy discovery cannot prove them. Luna rejects Ultra and GPT-5.5/5.4-family models reject Max/Ultra on the Codex 0.144.1 matrix
- `--reasoning` is deprecated; it aliases `--effort`, and a differing explicit pair fails preflight
- agy rejects explicit portable sandbox, permission, reasoning, max-turn, and full-access options; use model/add-dir/prompt only
- Grok rejects explicit add-dir, permission, reasoning, full-access, max-turns, raw `prompt-json`/`json-schema`, web/X, image, native allow/deny, plugin/MCP/hook, trace/export/debug, subagent, and memory controls; use model, optional supported Grok sandbox (`off`, `workspace`, `read-only`, `strict`, `devbox`), prompt, timeout, and the AgentMUX-owned v1.5 report schema only
- `--recover` resumes with NEW prompt, does not fetch result (use `result <id>`)
- `-e=high` on xhigh profiles is a downgrade, not a floor
- `wait` has no `--timeout` — only `--poll` for cadence (e.g., `wait --poll 30s <id>`)
- There is no `agent-mux config pipelines` command in the current CLI. Use `agent-mux config prompts` and compose multi-step flows with profiles unless a named pipeline profile appears in the prompt roster.

**8. References:** Deep dives in `references/`:
- first-run.md -- first-launch/onboarding contract for cold machines
- pitfalls.md -- audit-grounded landmines with session evidence
- async-and-steering.md -- lifecycle, fan-out, steering mechanics
- recovery-guide.md -- timeout/failure handling
- gemini-specifics.md -- Gemini approval mode, resume quirks
