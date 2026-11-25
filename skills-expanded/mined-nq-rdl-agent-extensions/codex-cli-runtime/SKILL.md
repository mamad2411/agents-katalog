---
name: codex-cli-runtime
license: Apache-2.0
description: Internal helper contract for calling the codex-companion runtime from Claude Code
user-invocable: false
metadata:
  repo: https://github.com/nq-rdl/agent-extensions
---

<!--
SPDX-License-Identifier: Apache-2.0
Derived from openai/codex-plugin-cc v1.0.6 (db52e28), Apache-2.0. Modified for rdl-agent-extensions.
-->

# Codex Runtime

Use this skill when executing `codex:rescue`, directly or in a delegated worker.

Primary helper:
- `node "${CLAUDE_PLUGIN_ROOT}/scripts/codex-companion.mjs" task "<raw arguments>"`

Execution rules:
- The rescue executor is a forwarder, not an orchestrator. Its only job is to invoke `task` once and return that stdout unchanged.
- Prefer the helper over hand-rolled `git`, direct Codex CLI strings, or any other Bash activity.
- Do not call `setup`, `review`, `adversarial-review`, `status`, `result`, or `cancel` from `codex:rescue`.
- Use `task` for every rescue request, including diagnosis, planning, research, and explicit fix requests.
- You may use the `codex:prompting` skill (GPT-5.6 prompting) to rewrite the user's request into a tighter Codex prompt before the single `task` call.
- That prompt drafting is the only Claude-side work allowed. Do not inspect the repo, solve the task yourself, or add independent analysis outside the forwarded prompt text.
- Leave `--effort` unset unless the user explicitly requests a specific effort.
- Leave model unset by default. Add `--model` only when the user explicitly asks for one. `codex:rescue` maps spoken model names; `codex:model-guide` owns the alias table.
- Add `--write` only when the request asks Codex to fix, implement, or otherwise change files. Omit it for investigation, diagnosis, review, research, or an explicit read-only request; the runtime then runs read-only. Continuing a thread does not authorize edits by itself.

Command selection:
- Use exactly one `task` invocation per rescue handoff.
- If the forwarded request includes `--background` or `--wait`, treat that as Claude-side execution control only. Strip it before calling `task`: `task` does not parse `--wait`, so a forwarded `--wait` becomes prompt text.
- If the forwarded request includes `--model`, pass it through to `task`; the companion resolves every alias in the `codex:model-guide` table.
- If the forwarded request includes `--effort`, pass it through to `task`.
- If the forwarded request includes `--resume`, strip that token from the task text and add `--resume-last`.
- If the forwarded request includes `--fresh`, strip that token from the task text and do not add `--resume-last`.
- `--resume`: always use `task --resume-last`, even if the request text is ambiguous.
- `--fresh`: always use a fresh `task` run, even if the request sounds like a follow-up.
- Phrasing alone ("keep going", "dig deeper") never adds `--resume-last`. `codex:rescue` asks the user when a resumable thread exists; without one, `--resume-last` fails with "No previous Codex task thread was found for this repository."
- `--effort`: accepted values are `low`, `medium`, `high`, `xhigh`, `max`, `ultra` (`ultra` is not available on either Luna). Unknown values warn and pass through; codex enforces per-model gating.

Runtime support:
- The companion needs `codex` on `PATH` with the app-server runtime: it checks `codex --version` and `codex app-server --help`, then drives `codex app-server` with approval policy `never` and a read-only or workspace-write sandbox. Do not call the `codex` CLI directly; `codex proto` no longer exists.
- Tested with `codex-cli 0.158.0` on 2026-09-29. A tested version is not a minimum; if the installed CLI rejects the runtime, report the error and point to `/codex:setup`.

Safety rules:
- Preserve the user's task text as-is apart from stripping routing flags.
- Do not inspect the repository, read files, grep, monitor progress, poll status, fetch results, cancel jobs, summarize output, or do any follow-up work of your own.
- Return the stdout of the `task` command exactly as-is.
- If the Bash call fails or Codex cannot be invoked, do not write a substitute answer. Report the failure with its most actionable stderr lines (a delegated worker returns them to its caller), and point to `/codex:setup` for install or authentication errors.
