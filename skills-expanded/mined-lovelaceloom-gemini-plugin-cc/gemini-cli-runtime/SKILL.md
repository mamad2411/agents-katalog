---
name: gemini-cli-runtime
description: Internal helper contract for calling the gemini-companion runtime (which wraps Google's Antigravity CLI, `agy`) from Claude Code
user-invocable: false
---

# `agy` Companion Runtime

Use this skill only inside the `gemini:gemini-rescue` subagent.

Primary helper:
- `GEMINI_RESCUE_MODE=1 node "${CLAUDE_PLUGIN_ROOT}/scripts/companion.mjs" task "<raw arguments>"`

The `GEMINI_RESCUE_MODE=1` env var asks the companion runtime to apply a finite default timeout (15 min) to the `task` call. This is belt-and-suspenders with the prompt-level "always pass `--timeout 15m`" rule below: if a rephrased forwarded request somehow loses the flag, the runtime still enforces a deadline. Direct `/gemini:task` callers do not set the env var, so unbounded behavior is preserved for them.

Execution rules:
- The rescue subagent is a forwarder, not an orchestrator. Its only job is to invoke `task` once and return that stdout unchanged.
- Prefer the helper over hand-rolled `git`, direct `agy` invocations, or any other Bash activity.
- Do not call `setup`, `review`, `adversarial-review`, `status`, `result`, or `cancel` from `gemini:gemini-rescue`.
- Use `task` for every rescue request, including diagnosis, planning, research, and explicit fix requests.
- You may use the `gemini-prompting` skill to rewrite the user's request into a tighter agy prompt before the single `task` call.
- That prompt drafting is the only Claude-side work allowed. Do not inspect the repo, solve the task yourself, or add independent analysis outside the forwarded prompt text.
- Default to read-only agy behavior. Add `--write` ONLY when the user explicitly asks for code changes.
- `--write` is gated by `GEMINI_PLUGIN_ALLOW_WRITE=1` in the environment. If the env var is missing the helper will refuse with exit 2 and a message explaining `--dangerously-skip-permissions`. Do not retry, do not try to set the env var yourself — surface the refusal to the user verbatim and let them decide.
- Leave `--model` unset by default. agy 1.0 binds its model internally and ignores `--model`, but the flag is still accepted on the companion's CLI for back-compat; passing it produces no behavioral change in agy. Only add `--model <name>` when the user explicitly requests one (purely informational).

Command selection:
- Use exactly one `task` invocation per rescue handoff.
- Run the `Bash` call in the foreground (do not set `run_in_background: true`). The rescue contract is synchronous: the parent agent expects agy's real answer, not a "running in background" stub from Claude Code's Bash tool. Issue #3 was caused by the previous "prefer background for long tasks" guidance, which made the wrapper forward a job-ID stub instead of agy's output. For genuinely long tasks, the user can call `/gemini:task --background "..."` directly from the main thread.
- If the forwarded request includes `--background` or `--wait`, treat that as Claude-side execution control only. Strip it before calling `task`, and do not treat it as part of the natural-language task text.
- If the forwarded request includes `--write` or `--read-only`, pass it through to `task`.
- **Timeout policy for rescue:** `task`'s built-in default is unbounded, which is unsafe for rescue because the parent agent blocks on a single foreground call. If the forwarded request includes `--timeout <duration>`, pass it through verbatim. If it does NOT include `--timeout`, you MUST add `--timeout 15m` to the `task` call. This bounds rescue against a hung agy process indefinitely stranding the parent agent. Forms accepted: `300s`, `5m`, `1h`, `500ms`, or `0` to disable. Users who want unbounded rescue must pass `--timeout 0` explicitly. On timeout the helper exits 124 — surface that to the user rather than retrying.
- Never call `purge` from this subagent. `/gemini:purge` is a destructive disk-cleanup operation the user invokes explicitly; rescue is forwarder-only.

Safety rules:
- Default to read-only agy work in `gemini:gemini-rescue` unless the user explicitly asks for code changes.
- Preserve the user's task text as-is apart from stripping routing flags.
- Do not inspect the repository, read files, grep, monitor progress, poll status, fetch results, cancel jobs, summarize output, or do any follow-up work of your own.
- Return the stdout of the `task` command exactly as-is.
- If the Bash call fails or agy cannot be invoked, return nothing.
